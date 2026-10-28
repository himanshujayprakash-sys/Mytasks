#!/bin/bash
# rebake_gt.sh <task dir> [...]: re-bake solution/gt_env.json for tasks whose world or oracle changed, before gate 1.
# Per task: one JUDGED oracle run (harbor 0.24.0, codex judge JUDGE_MODEL) on its harness_mcp_atlas build; only when it
# scores pytest 1.0 AND rubric 1.0 is gt_env.json written from that run (lib/rebake_gt_env.py, which also refuses a run
# made on another folder), then the task is rebuilt. A score below 1.0/1.0 is a defect in the task (rubric asks more
# than the reference does, or the oracle is wrong): nothing is written and the criteria that failed are printed.
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
source "$HERE/config.sh"; source "$HERE/lib/common.sh"
HMA_MAIN="${HMA_MAIN:-$DELIVERY/harness_mcp_atlas_main}"
J="$CACHE/jobs/rebake"; mkdir -p "$J" /tmp/qc/rebake
[ -s "$HOME/.codex/auth.json" ] || die "no codex login (~/.codex/auth.json): run 'codex login'"
scrub_env
for SRC in "$@"; do
  SRC="$(cd "$SRC" && pwd)"; U=$(basename "$SRC"); BLT="$HMA_MAIN/out/build/$U"; C="/tmp/qc/rebake/$U"
  [ -d "$BLT" ] || { log "$U: not built (run tools/hma_build.sh)"; continue; }
  rm -rf "$C" "${J:?}/$U-oracle"; cp -R "$BLT" "$C"
  log "$U: judged oracle run"
  ( export JUDGE_MODEL JUDGE_TRANSPORT
    export CODEX_AUTH_B64="$(base64 < "$HOME/.codex/auth.json" | tr -d '\n')"   # never printed
    harbor run -p "$C" -a oracle -e docker --force-build --cpus ignore --memory ignore -n 1 -o "$J" --job-name "$U-oracle" -y \
      > "$J/$U-oracle.log" 2>&1 )
  TR=$(ls -d "$J/$U-oracle"/*/ 2>/dev/null | head -1)
  [ -n "$TR" ] && [ -f "$TR/verifier/reward.json" ] || { log "$U: oracle run produced no reward.json ($J/$U-oracle.log)"; continue; }
  log "$U: oracle $(tr -d '\n ' < "$TR/verifier/reward.json")"
  if "$PY" "$PIPELINE/lib/rebake_gt_env.py" "$SRC" "$TR" "/tmp/qc/rebake/$U.gt_env.json" --ran-on "$C"; then
    cp "/tmp/qc/rebake/$U.gt_env.json" "$SRC/solution/gt_env.json"
    log "$U: solution/gt_env.json re-baked from the judged oracle"
    bash "$PIPELINE/tools/hma_build.sh" "$SRC"
  else
    "$PY" - "$TR" <<'PY'
import json, sys
d = json.load(open(sys.argv[1] + "/verifier/reward-details.json"))
for c in (d.get("rubric") or {}).get("criteria") or []:
    w, v = c.get("weight", 0), c.get("value", 0)
    if (w > 0 and v < 0.5) or (w < 0 and v >= 0.5):
        print("   rubric miss:", c.get("name"), "| judge:", (c.get("reasoning") or "")[:220].replace("\n", " "))
g = json.load(open(sys.argv[1] + "/verifier/grade_report.json"))
print("   pytest missed:", g.get("missed"), "guards:", g.get("guards_tripped"), "errors:", g.get("errors"))
PY
  fi
done

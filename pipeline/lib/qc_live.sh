#!/bin/bash
# qc_live.sh <batch> <uuid>: gate 1, part B. The skill's live runs (S5-10 judged oracle, S5-11 judged nop,
# S5-12 oracle with no judge), the same harbor command as the skill's tmux block but in the foreground, then the
# skill's own readers (live_check.py, gt_env_check.py). Needs Docker and the codex login (judge only; the
# oracle and nop agents use no model). Output: 1_qc/<uuid>/live/.
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
BATCH=$1; U=$2; BD=$(batch_dir "$BATCH"); Q="$BD/1_qc/$U"
B="/tmp/qc/$U"; [ -f "/tmp/qc/$U-report/env.sh" ] || die "$U: run the static checks first (they make the /tmp/qc copy)"
J="$CACHE/jobs/$BATCH"; mkdir -p "$J" "$Q/live"
scrub_env
[ -s "$HOME/.codex/auth.json" ] || die "no codex login (~/.codex/auth.json): run 'codex login'"

run() {   # $1 agent  $2 job suffix
  rm -rf "${J:?}/$U-$2"
  local s=$(date +%s)
  harbor run -p "$B" -a "$1" -e docker --force-build --cpus ignore --memory ignore \
    -n 1 -o "$J" --job-name "$U-$2" -y > "$Q/live/run_$2.log" 2>&1
  echo "$2 rc=$? secs=$(( $(date +%s) - s ))" >> "$Q/live/times.txt"
}
rm -f "$Q/live/times.txt"
(
  export JUDGE_MODEL JUDGE_TRANSPORT
  export CODEX_AUTH_B64="$(base64 < "$HOME/.codex/auth.json" | tr -d '\n')"   # never printed
  log "$U: S5-10 oracle + judge"; run oracle oracle
  log "$U: S5-11 nop + judge";    run nop nop
)
log "$U: S5-12 oracle, no judge"; run oracle oracle-nojudge

# The skill's reader block, pointed at this batch's jobs dir.
f=$("$PY" -c 'import json,sys;print(next(b["file"] for b in json.load(open(sys.argv[1]))["blocks"] if b["kind"]=="reader"))' "$Q/blocks/index.json")
sed -e "s/<uuid>/$U/g" -e "s|^J=.*|J=\"$J\"|" "$Q/blocks/$f" > "/tmp/qc/$U-report/readers.sh"
(cd /tmp/qc && bash "/tmp/qc/$U-report/readers.sh") > "$Q/live/readers.log" 2>&1
for a in oracle nop oracle-nojudge; do
  r=$(ls "$J/$U-$a"/*/verifier/reward.json 2>/dev/null | head -1)
  echo "$a: $( [ -n "$r" ] && tr -d '\n ' < "$r" || echo 'no reward.json')"
done > "$Q/live/rewards.txt"
log "$U: live done | $(tr '\n' ' ' < "$Q/live/rewards.txt")"
# Workflow step 3: is solution/gt_env.json stale? Judged against the oracle run above (fresh by construction).
"$PY" "$PIPELINE/lib/gt_stale_check.py" "$BD/tasks/$U" --jobs "$J" --ran-on "$B" --json "$Q/live/stale.json" > "$Q/live/stale.md" 2>&1
log "$U: gt_env.json $("$PY" -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d["verdict"], "-", d["evidence"])' "$Q/live/stale.json")"

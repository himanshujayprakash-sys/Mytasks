#!/bin/bash
# qc_static.sh <batch> <uuid>: gate 1, part A. Every scripted check of the workspace yuji-task-qc, taken
# straight from SKILL.md (lib/skill_blocks.py), run on a /tmp/qc copy as the skill's hard rules require.
# Output: 1_qc/<uuid>/static/<block>.log, one per command block. No Docker, no model.
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
BATCH=$1; U=$2; BD=$(batch_dir "$BATCH"); Q="$BD/1_qc/$U"
SRC="$BD/tasks/$U"; [ -f "$SRC/task.toml" ] || die "$U: not in batch $BATCH"
scrub_env
rm -rf "$Q/blocks" "$Q/static"; mkdir -p "$Q/blocks" "$Q/static"
# The exact files this QC judges: gate.py binds its verdict to this fingerprint.
"$PY" "$PIPELINE/lib/fingerprint.py" "$SRC" --files "$Q/qc_fingerprint.json" > /dev/null
"$PY" "$PIPELINE/lib/skill_blocks.py" "$TASK_QC_SKILL" "$Q/blocks" > "$Q/static/_blocks.txt" || die "cannot read $TASK_QC_SKILL"

# Stage 0 setup, as the skill writes it (the copy, env.sh); never in the source.
B="/tmp/qc/$U"; rm -rf "$B" "$B.re" "/tmp/qc/$U-report"; mkdir -p "/tmp/qc/$U-report"; cp -R "$SRC" "$B"
cat > "/tmp/qc/$U-report/env.sh" <<EOF
UUID="$U"
SRC="$SRC"
B="/tmp/qc/$U"
LS="/tmp/qc/$U/environment/light-servers"
REF="$REF"
T="/tmp/qc/$U/tests"
RK="/tmp/qc/$U/tests/reward"
O="/tmp/qc/$U-report/replay"
W="/tmp/qc/$U/tests/test_weights.json"
GT="/tmp/qc/$U/solution/gt_env.json"
export PYTHONDONTWRITEBYTECODE=1
EOF
# truth.txt / wrong.txt (Stage 2 leak scan) are hand-built; the review step or you put them in 1_qc/<uuid>/.
for f in truth.txt wrong.txt; do [ -s "$Q/$f" ] && cp "$Q/$f" "/tmp/qc/$U-report/$f"; done

cd /tmp/qc || exit 1
"$PY" - "$Q/blocks/index.json" <<'PY' > "$Q/static/_plan.txt"
import json, sys
for b in json.load(open(sys.argv[1]))["blocks"]:
    print(b["file"], b["kind"])
PY
while read -r f kind; do
  case "$kind" in
    static) ;;
    needs)  [ -s "/tmp/qc/$U-report/truth.txt" ] || { echo "not run: needs truth.txt/wrong.txt" > "$Q/static/${f%.sh}.log"; continue; } ;;
    *)      continue ;;
  esac
  sed "s/<uuid>/$U/g" "$Q/blocks/$f" > "/tmp/qc/$U-report/block.sh"
  bash "/tmp/qc/$U-report/block.sh" > "$Q/static/${f%.sh}.log" 2>&1
  echo "exit=$?" >> "$Q/static/${f%.sh}.log"
done < "$Q/static/_plan.txt"
log "$U: static checks done ($(ls "$Q"/static/*.log | wc -l | tr -d ' ') blocks, $(sed -n 1p "$Q/static/_blocks.txt" | cut -d' ' -f1-2))"

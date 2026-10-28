#!/bin/bash
# final_qc.sh <batch> <uuid>: gate 2. Three checks, all must pass:
#   1. the packaged task is byte for byte the files gate 1 passed (fingerprint)
#   2. every run, re-graded here with the task's own tests, gives the pytest score it recorded (lib/regrade.py):
#      proves the tests that ship produced the scores that ship, and that the grade does not depend on the machine
#   3. the workspace yuji-final-qc (every run, pass@k, reward reconstruction, reward hacking, hygiene)
#   4. clean_trajectories.py (dry run, apply, --check), then final QC again on the cleaned bundle
# PASS -> READY/<uuid> (a copy, ready to upload) + its entry in READY/LOCK.json. Waivers: the batch's waivers.txt
# IDs that apply to this task (MAJOR -> MINOR, as final_qc.py --waive does).
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
BATCH=$1; U=$2; BD=$(batch_dir "$BATCH"); P="$BD/3_packaged/$U"; OUT="$CACHE/runs/$BATCH"
[ -d "$P/trajectories" ] || die "$U: not packaged yet"
F="$BD/4_final_qc/$U"; rm -rf "$F" "$BD/READY/$U"; mkdir -p "$F"
# a task being re-checked is not READY until it passes again: drop its old lock entry
[ -f "$BD/READY/LOCK.json" ] && "$PY" -c 'import json,sys;p=sys.argv[1];l=json.load(open(p));l["tasks"].pop(sys.argv[2],None);open(p,"w").write(json.dumps(l,indent=1,sort_keys=True)+"\n")' "$BD/READY/LOCK.json" "$U"
H=$(gate_hash "$BATCH" "$U")
[ "$(gate_verdict "$BATCH" "$U")" = PASS ] || die "$U: gate 1 is $(gate_verdict "$BATCH" "$U"), not PASS"
[ "$(fingerprint "$P")" = "$H" ] || die "$U: 3_packaged/$U is not the files gate 1 passed: package again"

# 2. regrade every run
fail=0; echo "[" > "$F/regrade.json"; first=1
for run in "$OUT/$U"/trajectory/run_*; do
  line=$("$PY" "$PIPELINE/lib/regrade.py" "$P" "$run" "$F/regrade_$(basename "$run")") || fail=1
  [ $first = 1 ] || echo "," >> "$F/regrade.json"; first=0; echo "$line" >> "$F/regrade.json"
  log "$U: $(basename "$run") $(echo "$line" | "$PY" -c 'import json,sys;d=json.load(sys.stdin);print("recorded pytest %s, regraded %s: %s" % (d["recorded_pytest"], d["regraded_pytest"], "same" if d["match"] else "DIFFERENT"))')"
done
echo "]" >> "$F/regrade.json"
rm -rf "$F"/regrade_run_*/tests
[ $fail = 0 ] || { log "$U: final QC FAIL: a run does not regrade to its recorded score ($F/regrade.json)"; exit 1; }

# 3. workspace final QC
WAIVE=$("$PY" - "$BD/waivers.txt" "$U" <<'PY'
import re, sys
ids = []
for raw in open(sys.argv[1]).read().splitlines():
    line = raw.split("#", 1)[0].split()
    if not line: continue
    if re.fullmatch(r"[0-9a-f]{8}", line[0]):
        if line[0] == sys.argv[2][:8] and len(line) > 1: ids.append(line[1])
    else: ids.append(line[0])
print(",".join(dict.fromkeys(ids)))
PY
)
"$PY" -I "$FINAL_QC" "$P" --out "$F" --ref "$REF_FOLDER" --agent "$AGENT" --model "$MODEL" \
  ${WAIVE:+--waive "$WAIVE"} > "$F/stdout.txt" 2>&1
rc=$?
if [ $rc -ne 0 ]; then log "$U: final QC FAIL (exit $rc): $F/$U-final-qc.md"; exit $rc; fi
# 4. workflow step 4: clean the trajectories for the GitHub stage-1 repo (the lead's clean_trajectories.py), on the
#    READY copy only: preview, apply, then --check must report nothing left; final QC runs again on the cleaned
#    (trimmed) bundle, and only then is it locked. The regrade above already used the full run files it removes.
mkdir -p "$BD/READY"; cp -R "$P" "$BD/READY/$U"
M=$(ls "$BD/READY/$U/trajectories" | head -1)
"$PY" "$CLEAN_SCRIPT" --dry-run --model "$M" "$BD/READY/$U" > "$F/clean_dry_run.txt" 2>&1
"$PY" "$CLEAN_SCRIPT" --model "$M" "$BD/READY/$U" > "$F/clean_apply.txt" 2>&1 || { rm -rf "$BD/READY/$U"; die "$U: clean_trajectories.py failed ($F/clean_apply.txt)"; }
"$PY" "$CLEAN_SCRIPT" --check --model "$M" "$BD/READY/$U" > "$F/clean_check.txt" 2>&1 || { rm -rf "$BD/READY/$U"; die "$U: clean_trajectories.py --check still finds unclean files ($F/clean_check.txt)"; }
mkdir -p "$F/after_clean"
"$PY" -I "$FINAL_QC" "$BD/READY/$U" --out "$F/after_clean" --ref "$REF_FOLDER" --agent "$AGENT" --model "$MODEL" \
  ${WAIVE:+--waive "$WAIVE"} --no-llm-pack > "$F/after_clean/stdout.txt" 2>&1 \
  || { rm -rf "$BD/READY/$U"; die "$U: final QC fails on the cleaned bundle ($F/after_clean/$U-final-qc.md)"; }
"$PY" "$PIPELINE/lib/lock.py" "$BD" "$U" || { rm -rf "$BD/READY/$U"; die "$U: lock refused"; }
log "$U: final QC PASS, cleaned (--check clean), re-checked -> READY/$U (locked)"

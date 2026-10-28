#!/bin/bash
# run_models.sh <batch> <uuid>: model runs for ONE task that passed gate 1, through the harness's own resumable
# batch runner (scripts/run_batch.py: preflight, harbor, reshape, finance). RUNS_PER_TASK attempts of MODEL on
# AGENT (OpenHands, reasoning_effort high), judged by the codex judge. A rerun of the same command resumes; it never
# repeats an agent phase that already ran. Output: $CACHE/runs/<batch>/<uuid>/trajectory/run_N (2_runs/ links there).
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
BATCH=$1; U=$2; BD=$(batch_dir "$BATCH")
v=$(gate_verdict "$BATCH" "$U")
[ "$v" = PASS ] || die "$U: gate 1 is $v, not PASS: no model runs (see 1_qc/$U/GATE.md)"

# Runs happen on their own copy (the harness rewrites tests/test.sh in place), and that copy must be byte for byte
# the files gate 1 passed. Runs already made on other files are never mixed in: they would carry scores the
# shipped tests do not give (what went unnoticed after the hardening rounds).
RT="$CACHE/runtasks/$BATCH"; OUT="$CACHE/runs/$BATCH"; mkdir -p "$RT" "$OUT"
H=$(gate_hash "$BATCH" "$U")
if [ -f "$OUT/$U/.task_sha256" ] && [ "$(cat "$OUT/$U/.task_sha256")" != "$H" ]; then
  die "$U: the runs in 2_runs/$U were made on another version of the task ($(cut -c1-12 "$OUT/$U/.task_sha256") != gate $(echo "$H" | cut -c1-12)). Move 2_runs/$U away to run again."
fi
if [ ! -d "$RT/$U" ] || [ "$(fingerprint "$RT/$U")" != "$H" ]; then rm -rf "$RT/$U"; cp -R "$BD/tasks/$U" "$RT/$U"; fi
[ "$(fingerprint "$RT/$U")" = "$H" ] || die "$U: the run copy does not match the files gate 1 passed"
"$PY" "$PIPELINE/lib/toolchain.py" "$WORKSPACE" "$HARNESS" "$BD/2_runs/toolchain/$U.json" --for run || die "$U: toolchain refused"
mkdir -p "$BD/2_runs/logs" "$OUT/$U"; echo "$H" > "$OUT/$U/.task_sha256"
export MODEL JUDGE_TRANSPORT JUDGE_MODEL OPENHANDS_REASONING_EFFORT="$REASONING_EFFORT"
log "$U: $RUNS_PER_TASK x $MODEL ($AGENT, effort $REASONING_EFFORT, judge $JUDGE_TRANSPORT/$JUDGE_MODEL)"
(cd "$HARNESS" && python3 scripts/run_batch.py --task "$RT/$U" --model "$MODEL" --agent "$AGENT" \
   --n "$RUNS_PER_TASK" --concurrency 1 --output-dir "$OUT" --batch-id "$BATCH-${U:0:8}") \
   > "$BD/2_runs/logs/$U.log" 2>&1
rc=$?
# patch_test_sh must have found nothing to change (new did it already); anything else means the harness's verifier
# moved since gate 1, and these runs are not on the checked files.
[ "$(fingerprint "$RT/$U")" = "$H" ] || die "$U: the harness changed the task during the run (its verifier test.sh moved since gate 1): rerun 'new' and gate 1"
n=$(ls -d "$OUT/$U"/trajectory/run_* 2>/dev/null | wc -l | tr -d ' ')
log "$U: run_batch exit $rc, $n run folder(s) (log: 2_runs/logs/$U.log)"
exit $rc

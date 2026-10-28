#!/bin/bash
# check_task.sh <task dir>: gate 1 part A (every scripted check of the workspace yuji-task-qc) on one task folder,
# without a batch. Works on a throwaway copy; never writes in <task dir>. Prints GATE.md (findings, waivable or not).
# For authors fixing a task: run it after every change. A clean result here is necessary, not sufficient: the live
# oracle/nop, the staleness check and the review still run in the pipeline's gate 1.
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
source "$HERE/config.sh"; source "$HERE/lib/common.sh"
SRC="$(cd "${1:?task dir}" && pwd)"; U=$(basename "$SRC")
B="_chk_${U:0:8}_$$"; BD="$PIPELINE/batches/$B"
trap 'rm -rf "$BD"' EXIT
mkdir -p "$BD/tasks"; cp "$PIPELINE/waivers.default.txt" "$BD/waivers.txt"
rsync -a --exclude trajectories --exclude .DS_Store --exclude __pycache__ "$SRC/" "$BD/tasks/$U/"
# Checked exactly as given: a harness_mcp_atlas build (out/build/<uuid>) is what ships, so it is never rewritten here.
bash "$PIPELINE/lib/qc_static.sh" "$B" "$U" > /dev/null 2>&1
"$PY" "$PIPELINE/lib/gate.py" "$BD/1_qc/$U" "$BD/waivers.txt" off "$TASK_QC_SKILL" "$REF_FOLDER" > /dev/null
cat "$BD/1_qc/$U/GATE.md"
echo
echo "(PENDING after a clean run only means the live oracle/nop has not run: that happens in the pipeline.)"

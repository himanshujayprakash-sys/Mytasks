#!/bin/bash
# lead_qc.sh <playbook: structure|ruthless> <uuid>: run one static playbook of the lead's qc zip (pipeline/lead_qc =
# qc (2).zip) on a task's authoring layout (harness_mcp_atlas_main/input/<uuid>), exactly as written, in a headless
# Claude Code session. $TASK is a fresh /tmp/qc copy (the playbooks may write); the report goes to
# batches/<batch>/lead_qc/<uuid>/<playbook>.md with the playbook's own verdict on line 1.
set -uo pipefail
source "$(dirname "$0")/../config.sh"
PB=$1; U=$2; BATCH=${BATCH:-v2_20261028}
case "$PB" in structure) F="$LEAD_QC/static/10_structure.md";; ruthless) F="$LEAD_QC/static/20_ruthless.md";; *) exit 2;; esac
T="/tmp/qc/leadqc/$PB/$U"; rm -rf "$T"; mkdir -p "$(dirname "$T")"; cp -R "$HMA_MAIN/input/$U" "$T"
O="$PIPELINE/batches/$BATCH/lead_qc/$U"; mkdir -p "$O"; rm -f "$O/$PB.md"
P="export TASK=\"$T\" is already set for you: \$TASK=$T (a copy of one task in the authoring layout the harness builds from).
Follow the QC playbook at $F exactly as it is written: read it fully, run every script it gives as written against \$TASK,
quote the real output, apply its decision tables and severity rules. Do not edit anything outside /tmp/qc. Never print secrets.
Write your report, in the format the playbook prescribes, to $O/$PB.md. Its first line must be exactly
\"VERDICT: PASS\" or \"VERDICT: FAIL\" as the playbook decides, followed by the counts of critical/blocker, major and minor findings."
cd /tmp/qc && TASK="$T" claude -p "$P" --allowedTools "Read,Grep,Glob,Write,Bash" --add-dir "$T" --add-dir "$LEAD_QC" --add-dir "$O" \
  > "$O/$PB.session.txt" 2>&1
echo "$(date +%H:%M:%S) ${U:0:8} $PB: $(head -1 "$O/$PB.md" 2>/dev/null || echo 'no report written')"

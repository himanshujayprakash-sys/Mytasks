#!/bin/bash
# lead_qc_bundle.sh <bundle dir> <report dir>: run the lead's traj/10_bundle_playbook.md (qc (2).zip) on one packaged
# bundle with its trajectories, exactly as written, in a headless Claude Code session. $BUNDLE is a fresh /tmp/qc copy.
set -uo pipefail
source "$(dirname "$0")/../config.sh"
SRC="$(cd "${1:?bundle dir}" && pwd)"; mkdir -p "${2:?report dir}"; O="$(cd "$2" && pwd)"; U=$(basename "$SRC"); case "$U" in *-*-*-*-*) ;; *) U=$(basename "$(dirname "$SRC")");; esac   # the task uuid: the bundle folder itself, or its parent (gate2/<uuid>/bundle)
B="/tmp/qc/leadqc/bundle/$U"; rm -rf "${B:?}"; mkdir -p "$(dirname "$B")" "$O"; cp -R "$SRC" "$B"; rm -f "$O/bundle_playbook.md"
P="\$BUNDLE is already set for you: \$BUNDLE=$B (a copy of one packaged bundle with trajectories/<model>/run_N, trimmed layout).
Follow the QC playbook at $LEAD_QC/traj/10_bundle_playbook.md exactly as it is written: read it fully, run every script it
gives as written, quote the real output, apply its verdict mapping. Do not edit anything outside /tmp/qc. Never print secrets.
Write the report in the playbook's report format to $O/bundle_playbook.md. Its first line must be exactly \"VERDICT: PASS\"
or \"VERDICT: FAIL\" as the playbook's verdict mapping decides (SIGNED/REVIEW = PASS, BLOCKED = FAIL), followed by the counts."
cd /tmp/qc && BUNDLE="$B" claude -p "$P" --allowedTools "Read,Grep,Glob,Write,Bash" --add-dir "$B" --add-dir "$LEAD_QC" --add-dir "$O" \
  > "$O/bundle_playbook.session.txt" 2>&1
echo "$(date +%H:%M:%S) ${U:0:8} bundle playbook: $(head -1 "$O/bundle_playbook.md" 2>/dev/null || echo "no report: $(tail -2 "$O/bundle_playbook.session.txt")")"

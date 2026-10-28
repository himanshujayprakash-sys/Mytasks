#!/bin/bash
# qc_review.sh <batch> <uuid>: gate 1, part C. The checks of yuji-task-qc that need reading, not a script
# (Stage 2 leak scan from a hand-built truth.txt, Stage 2 / Stage 4 reading checks, the fact sheet), done by a
# headless Claude Code session that follows the workspace SKILL.md and writes the skill's qc_report.md.
# It reuses parts A and B (their logs are passed in), so it does not repeat the live runs.
# Output: 1_qc/<uuid>/review/qc_report.md (+ truth.txt / wrong.txt for the static leak-scan block).
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
BATCH=$1; U=$2; BD=$(batch_dir "$BATCH"); Q="$BD/1_qc/$U"
[ -f "/tmp/qc/$U-report/env.sh" ] || die "$U: run the static checks first"
mkdir -p "$Q/review"
scrub_env
PROMPT=$(cat <<EOF
You are the QC reviewer for one Yuji task bundle. Follow the skill at $TASK_QC_SKILL exactly (read it first),
for the bundle copy /tmp/qc/$U (env.sh at /tmp/qc/$U-report/env.sh; the read-only source is $BD/tasks/$U).

Already done by the pipeline, do NOT redo them:
- every scripted command block: outputs in $Q/static/*.log (block files in $Q/blocks/, index.json names each);
- the live runs S5-10/S5-11/S5-12 and their readers: $Q/live/readers.log, $Q/live/rewards.txt, $Q/live/run_*.log.
Read those outputs and judge them as the skill says.

Your job is the rest of the skill: the fact sheet, build truth.txt and wrong.txt as Stage 2 describes and save
them to $Q/truth.txt and $Q/wrong.txt (one value per line), run the Stage 2 leak-scan block with them, and do every
check the skill marks as reading (Stage 2 and Stage 4 reading checks, S4-31 candidates, S5-15 items).
Obey the skill's hard rules (never print secrets, never edit $BD/tasks/$U, never open trajectories/).
Waivers already granted for this batch (report them under Waivers, not as findings): $BD/waivers.txt.

Then apply the two static QC playbooks from the lead to the same task, exactly as they are written:
- $LEAD_QC/static/10_structure.md with \$TASK = $HMA_MAIN/input/$U (the authoring layout of this task in the harness)
- $LEAD_QC/static/20_ruthless.md with \$TASK = $HMA_MAIN/input/$U
Treat \$TASK as read-only (copy it under /tmp/qc first if a playbook script needs to write). Record the verdict of each playbook
and its findings in their own section of the report.

Write the report in the skill's report template to $Q/review/qc_report.md. Its first line must be exactly
"VERDICT: PASS", "VERDICT: FAIL" or "VERDICT: PARTIAL" (PASS only when the skill AND both playbooks pass), and every
BLOCKER or MAJOR finding (from the skill or a playbook; a playbook "critical" counts as BLOCKER, "major" as MAJOR)
must be a "### [<ID>] ..." heading with "- Severity: BLOCKER" or "- Severity: MAJOR" on the next line.
EOF
)
log "$U: review (headless Claude Code, skill $(sed -n 1p "$Q/static/_blocks.txt" | cut -d' ' -f1-2))"
(cd /tmp/qc && claude -p "$PROMPT" --allowedTools "Read,Grep,Glob,Write,Bash" \
   --add-dir "$BD" --add-dir "$WORKSPACE/skills" --add-dir "$REF" --add-dir "$HMA_MAIN/input/$U" --add-dir "$LEAD_QC" > "$Q/review/session.txt" 2>&1)
if [ -s "$Q/review/qc_report.md" ]; then
  log "$U: review $(head -1 "$Q/review/qc_report.md")"
else
  log "$U: review wrote no report (see $Q/review/session.txt)"
fi

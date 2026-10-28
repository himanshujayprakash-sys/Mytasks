# Pipeline settings. Every value can be overridden from the shell (VAR=... ./pipeline.sh ...).
# Sourced by pipeline.sh and every lib/ script; holds no secrets.

DELIVERY="${DELIVERY:-/Users/mac/Documents/Desktop items/Mcp_tooluse_delivery}"
PIPELINE="${PIPELINE:-$DELIVERY/pipeline}"

# The QC that gates everything: yuji-workspace (git@github.com:Animesh-Eth/yuji-workspace.git).
WORKSPACE="${WORKSPACE:-/Users/mac/Documents/Desktop items/yuji-workspace}"
TASK_QC_SKILL="${TASK_QC_SKILL:-$WORKSPACE/skills/yuji-task-qc/SKILL.md}"
FINAL_QC="${FINAL_QC:-$WORKSPACE/skills/yuji-final-qc/scripts/final_qc.py}"
# Reference sample 5b10675f and the other stage-1 bundles (final QC's S1-37 accepts a match with any of them).
REF_FOLDER="${REF_FOLDER:-$WORKSPACE/trajectories}"
REF="${REF:-$REF_FOLDER/5b10675f-e16b-5f22-ae7f-d8040f6324c4}"

# Model runs: yuji-harness-2 (scripts/run_batch.py), OpenHands on the Claude subscription (ccbridge).
HARNESS="${HARNESS:-$DELIVERY/yuji-harness-2-local}"
MODEL="${MODEL:-claude-opus-5}"
AGENT="${AGENT:-openhands}"
RUNS_PER_TASK="${RUNS_PER_TASK:-1}"          # trajectories/opus-5/run_1..run_N
REASONING_EFFORT="${REASONING_EFFORT:-high}"  # final QC F2 requires reasoning_effort = high

# Rubric judge for the judged QC runs and the model runs: codex login (~/.codex/auth.json).
JUDGE_TRANSPORT="${JUDGE_TRANSPORT:-codex}"
JUDGE_MODEL="${JUDGE_MODEL:-gpt-5.6-sol}"

# Gate 1 review: the reading checks of yuji-task-qc that no script covers (leak scan from truth.txt,
# Stage 2 / Stage 4 reading).
#   claude  a headless Claude Code session runs the full skill and writes qc_report.md (default)
#   manual  you (or Claude in a chat) do it and record it with: pipeline.sh review-ok <batch> <uuid> "<note>"
#   off     no review; the gate is the scripted checks + live runs only (the board says so)
QC_REVIEW="${QC_REVIEW:-claude}"

# Stage-1 workflow tools from the lead (2026-10-28): the trajectory cleanup for the GitHub stage-1 repo, and the
# harness that makes the trajectories (harness_mcp_atlas, github.com/148tabish/harness_mcp_atlas).
CLEAN_SCRIPT="${CLEAN_SCRIPT:-$DELIVERY/clean_trajectories.py}"
HMA="${HMA:-$DELIVERY/harness_mcp_atlas}"
# The separate checkout of harness_mcp_atlas origin/main that builds the tasks (tools/hma_build.sh), and the lead's QC
# playbooks from qc (1).zip (static/10_structure.md, static/20_ruthless.md, traj/10_bundle_playbook.md).
HMA_MAIN="${HMA_MAIN:-$DELIVERY/harness_mcp_atlas_main}"
LEAD_QC="${LEAD_QC:-$PIPELINE/lead_qc}"

# Docker can bind-mount these (no spaces, under $HOME); the batch folder links to them.
CACHE="${CACHE:-$HOME/.cache/yuji-pipeline}"

# Python 3.12 + pytest 9.1.1 (the verifier image's pins); the skill's commands call `python3`.
PY="${PY:-$PIPELINE/.venv/bin/python}"
export PATH="$PIPELINE/.venv/bin:$PATH"

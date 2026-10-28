#!/bin/bash
# pipeline.sh: created tasks -> workspace QC gate -> model runs (only for tasks that pass) -> client layout ->
# workspace final QC -> READY. Every stage is re-runnable; a stage whose output exists is skipped unless FORCE=1.
#
#   pipeline.sh new     <batch> <tasks folder> [uuid ...]   copy the tasks into batches/<batch>/tasks (source untouched)
#   pipeline.sh qc      <batch> [uuid ...]   gate 1: scripted checks -> live judged oracle/nop -> review -> gate.json
#   pipeline.sh run     <batch> [uuid ...]   model runs, gate-1 PASS tasks only (others are skipped and listed)
#   pipeline.sh package <batch> [uuid ...]   runs -> 3_packaged/<uuid>/trajectories/opus-5 (client layout)
#   pipeline.sh final   <batch> [uuid ...]   gate 2: yuji-final-qc; PASS -> READY/<uuid>
#   pipeline.sh all     <batch> [uuid ...]   qc, run, package, final in order (a task stops at the first failure)
#   pipeline.sh status  <batch>              BOARD.md + SKIPPED.md
#   CONTINUE_ON_FAIL=1 pipeline.sh qc ...    run every part of gate 1 even after a FAIL (complete findings; a waiver
#                                            added later then needs only `pipeline.sh regate`, no new runs)
#   pipeline.sh review-ok <batch> <uuid> "<note>"   record a manual review (QC_REVIEW=manual)
#   pipeline.sh verify  <READY folder | batch>   on any laptop: bundles still match READY/LOCK.json, same QC verdicts
#
# Settings: config.sh (model, runs per task, judge, review mode, paths). Waivers: batches/<batch>/waivers.txt.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/config.sh"; source "$HERE/lib/common.sh"
L="$PIPELINE/lib"
CMD="${1:-}"; shift || true

judge_preflight() {   # once per invocation, before any judged run (the skill's judge preflight)
  [ -n "${_JUDGE_OK:-}" ] && return 0
  local out; out=$(codex exec --skip-git-repo-check -m "$JUDGE_MODEL" "Reply with the single word ok." < /dev/null 2>&1 | tail -2)
  echo "$out" | grep -qiw ok || die "judge preflight: codex login does not serve $JUDGE_MODEL: $out"
  _JUDGE_OK=1; log "judge preflight: codex serves $JUDGE_MODEL"
}

gate() { "$PY" "$L/gate.py" "$1/1_qc/$2" "$1/waivers.txt" "$QC_REVIEW" "$TASK_QC_SKILL" "$REF_FOLDER"; }

toolchain() {   # <batch> <qc|run> <out.json>: same tools as every other laptop, or stop
  "$PY" "$L/toolchain.py" "$WORKSPACE" "$HARNESS" "$3" --for "$2" || die "toolchain refused (see above); nothing was run"
}

stage_qc() {   # <batch> <uuid>: A -> gate -> B -> gate -> C -> gate; stops at the first FAIL (the task is skipped)
  local b=$1 u=$2 bd v; bd=$(batch_dir "$1")
  v=$(gate_verdict "$b" "$u")
  if [ "$v" = CHANGED ]; then
    log "$u: the task changed after gate 1 checked it; every part of gate 1 runs again. Changed files:"
    changed_files "$b" "$u"
  elif [ "${FORCE:-0}" != 1 ] && [ "$v" != PENDING ]; then log "$u: gate 1 already $v (FORCE=1 to redo)"; return; fi
  if [ "${FORCE:-0}" = 1 ] || [ "$v" = CHANGED ]; then
    rm -rf "$bd/1_qc/$u/static" "$bd/1_qc/$u/live" "$bd/1_qc/$u/review" "$bd/1_qc/$u/gate.json" "$bd/1_qc/$u/truth.txt" "$bd/1_qc/$u/wrong.txt"
  fi
  toolchain "$b" qc "$bd/1_qc/$u/toolchain.json"
  [ -d "$bd/1_qc/$u/static" ] || bash "$L/qc_static.sh" "$b" "$u"
  gate "$bd" "$u" >/dev/null; [ "$(gate_verdict "$b" "$u")" = FAIL ] && [ "${CONTINUE_ON_FAIL:-0}" != 1 ] && { log "$u: gate 1 FAIL after the scripted checks: skipped"; return; }
  if [ ! -f "$bd/1_qc/$u/live/readers.log" ]; then judge_preflight; bash "$L/qc_live.sh" "$b" "$u"; fi
  gate "$bd" "$u" >/dev/null; [ "$(gate_verdict "$b" "$u")" = FAIL ] && [ "${CONTINUE_ON_FAIL:-0}" != 1 ] && { log "$u: gate 1 FAIL after the live runs: skipped"; return; }
  if [ "$QC_REVIEW" = claude ] && [ ! -s "$bd/1_qc/$u/review/qc_report.md" ]; then
    bash "$L/qc_review.sh" "$b" "$u"
    # the review saved truth.txt / wrong.txt: run the leak-scan block it unlocks, then judge again
    [ -s "$bd/1_qc/$u/truth.txt" ] && bash "$L/qc_static.sh" "$b" "$u" >/dev/null
  fi
  log "$(gate "$bd" "$u")"
}

case "$CMD" in
  new)
    b=${1:?batch name}; src=${2:?tasks folder}; shift 2
    bd="$PIPELINE/batches/$b"; mkdir -p "$bd/tasks" "$CACHE/runs/$b"
    [ -e "$bd/2_runs" ] || ln -s "$CACHE/runs/$b" "$bd/2_runs"
    [ -f "$bd/waivers.txt" ] || cp "$PIPELINE/waivers.default.txt" "$bd/waivers.txt"
    us=("$@"); [ ${#us[@]} -eq 0 ] && us=($(cd "$src" && ls -d *-*-*-*-*/ 2>/dev/null | tr -d /))
    for u in "${us[@]}"; do
      [ -f "$src/$u/task.toml" ] || { log "skip $u: no task.toml in $src/$u"; continue; }
      rm -rf "$bd/tasks/$u"; rsync -a --exclude trajectories --exclude .DS_Store --exclude __pycache__ "$src/$u/" "$bd/tasks/$u/"
      # Tasks come from a harness_mcp_atlas build (tools/hma_build.sh -> harness_mcp_atlas_main/out/build/<uuid>):
      # the files gate 1 checks are then byte for byte the files that run and ship. A source folder that is not a
      # build is refused, since its verifier files would be replaced at build time.
      grep -q "HARNESS-GENERATED" "$bd/tasks/$u/environment/state_capture.py" 2>/dev/null \
        || log "WARNING $u: not a harness_mcp_atlas build; run pipeline/tools/hma_build.sh first and add from its out/build"
      log "added $u ($(fingerprint "$bd/tasks/$u" | cut -c1-12))"
    done
    {
      echo "created=$(date -u +%FT%TZ)"; echo "source=$src"
      echo "workspace=$(git -C "$WORKSPACE" rev-parse --short HEAD 2>/dev/null) task_qc=$(grep -m1 -o 'yuji-task-qc [0-9.]*' "$TASK_QC_SKILL")"
      echo "build_harness=harness_mcp_atlas $(git -C "$DELIVERY/harness_mcp_atlas_main" rev-parse --short HEAD 2>/dev/null) model=$MODEL agent=$AGENT runs=$RUNS_PER_TASK judge=$JUDGE_TRANSPORT/$JUDGE_MODEL review=$QC_REVIEW"
    } >> "$bd/batch.log"
    "$PY" "$L/board.py" "$bd" >/dev/null; log "batch $b: $(ls "$bd/tasks" | wc -l | tr -d ' ') task(s) -> $bd" ;;
  qc)
    b=${1:?batch}; shift; batch_dir "$b" >/dev/null || exit 1; for u in $(batch_tasks "$b" "$@"); do stage_qc "$b" "$u"; done
    "$PY" "$L/board.py" "$PIPELINE/batches/$b" ;;
  run|package|final)
    b=${1:?batch}; shift; bd=$(batch_dir "$b") || exit 1
    for u in $(batch_tasks "$b" "$@"); do
      [ "$(gate_verdict "$b" "$u")" = PASS ] || { log "$u: gate 1 $(gate_verdict "$b" "$u"): skipped"; continue; }
      case "$CMD" in
        run)     bash "$L/run_models.sh" "$b" "$u" ;;
        package) bash "$L/package.sh" "$b" "$u" ;;
        final)   bash "$L/final_qc.sh" "$b" "$u" ;;
      esac
    done
    "$PY" "$L/board.py" "$bd" ;;
  all)
    b=${1:?batch}; shift; bd=$(batch_dir "$b") || exit 1
    for u in $(batch_tasks "$b" "$@"); do
      stage_qc "$b" "$u"
      [ "$(gate_verdict "$b" "$u")" = PASS ] || continue
      bash "$L/run_models.sh" "$b" "$u" && bash "$L/package.sh" "$b" "$u" && bash "$L/final_qc.sh" "$b" "$u"
      "$PY" "$L/board.py" "$bd" >/dev/null
    done
    "$PY" "$L/board.py" "$bd" ;;
  status)
    bd=$(batch_dir "${1:?batch}") || exit 1; "$PY" "$L/board.py" "$bd" ;;
  review-ok)
    b=${1:?batch}; u=${2:?uuid}; bd=$(batch_dir "$b") || exit 1; mkdir -p "$bd/1_qc/$u/review"
    echo "${3:-reviewed} ($(date -u +%FT%TZ))" > "$bd/1_qc/$u/review/REVIEW_OK"; log "$(gate "$bd" "$u")" ;;
  regate)
    # re-judge gate 1 from what is on disk (after a waiver or a review): no new runs
    b=${1:?batch}; shift; bd=$(batch_dir "$b") || exit 1
    for u in $(batch_tasks "$b" "$@"); do log "$(gate "$bd" "$u")"; done
    "$PY" "$L/board.py" "$bd" ;;
  verify)
    # On ANY laptop: re-check delivered bundles against READY/LOCK.json (files, runs, deterministic QC verdicts).
    bash "$L/verify.sh" "${1:?READY folder (or batch name)}" ;;
  *)
    sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
esac

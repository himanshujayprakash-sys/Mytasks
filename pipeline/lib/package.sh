#!/bin/bash
# package.sh <batch> <uuid>: the finished runs -> the client layout, 3_packaged/<uuid>/ =
# the task exactly as it ran + trajectories/opus-5/{pass_summary.json, run_N/...} (TASK-STRUCTURE.md section 6).
#   1. refuses a run the harness's internet audit failed, and a run without a rubric score (judge did not run)
#   2. the harness's own tools/delivery_utils/make_delivery.py builds trajectories/ (agent name openhands-sdk)
#   3. adds what the stage-1 bundles also ship and make_delivery leaves out: run_N/verifier/final_message.md and
#      run_N/artifacts/workspace/ (the agent's delivered files)
#   4. pass@N.json when RUNS_PER_TASK > 1 (final QC F9 reconciles it)
set -euo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
BATCH=$1; U=$2; BD=$(batch_dir "$BATCH")
OUT="$CACHE/runs/$BATCH"; RT="$CACHE/runtasks/$BATCH"
[ -d "$OUT/$U/trajectory" ] || die "$U: no finished runs in $OUT/$U/trajectory (run stage not done?)"
H=$(gate_hash "$BATCH" "$U")
[ "$(gate_verdict "$BATCH" "$U")" = PASS ] || die "$U: gate 1 is $(gate_verdict "$BATCH" "$U"), not PASS"
[ "$(cat "$OUT/$U/.task_sha256" 2>/dev/null)" = "$H" ] || die "$U: these runs were not made on the files gate 1 passed"
[ "$(fingerprint "$RT/$U")" = "$H" ] || die "$U: the run copy no longer matches the files gate 1 passed"
for a in "$OUT/$U"/trajectory/run_*/internet_audit.json; do
  [ -f "$a" ] || continue
  if "$PY" -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("severity")=="fail" else 1)' "$a"; then
    die "$U: $(basename "$(dirname "$a")") reached the open internet (internet_audit.json): not packaged"
  fi
done
if "$PY" -c 'import json,sys; s=json.load(open(sys.argv[1])); sys.exit(0 if s.get("runs_without_rubric") else 1)' "$OUT/$U/pass_summary.json"; then
  die "$U: a run has no rubric score (the judge did not run); re-score it before packaging"
fi
W=$(mktemp -d "$CACHE/pkg.XXXXXX"); trap 'rm -rf "$W"' EXIT
(cd "$HARNESS" && "$PY" tools/delivery_utils/make_delivery.py "$U" --output-dir "$OUT" --tasks-dir "$RT" \
   --delivery-dir "$W" > "$W/make_delivery.log" 2>&1) || { cat "$W/make_delivery.log" >&2; die "$U: make_delivery failed"; }
T="$W/$U/trajectories"; M=$(ls "$T" 2>/dev/null | head -1)
[ -n "$M" ] && [ -f "$T/$M/pass_summary.json" ] || die "$U: make_delivery produced no trajectories/<model>/pass_summary.json"
for run in "$T/$M"/run_*; do
  src="$OUT/$U/trajectory/$(basename "$run")"
  [ -f "$src/verifier/final_message.md" ] && cp "$src/verifier/final_message.md" "$run/verifier/final_message.md"
  if [ -d "$src/artifacts/workspace" ]; then mkdir -p "$run/artifacts/workspace"; cp -R "$src/artifacts/workspace/." "$run/artifacts/workspace/"; fi
done
"$PY" - "$T/$M" <<'PY'
# The harness writes result.json verifier_result.rewards.reward on its 0-100 scale; every stage-1 bundle (and final
# QC F3) has it 0-1, equal to report.json final_reward. Rescale only when it is exactly that score x100.
import json, pathlib, sys
for r in sorted(pathlib.Path(sys.argv[1]).glob("run_*")):
    res, rep = json.loads((r / "result.json").read_text()), json.loads((r / "report.json").read_text())
    rw = ((res.get("verifier_result") or {}).get("rewards") or {})
    fr = rep.get("final_reward")
    if isinstance(rw.get("reward"), (int, float)) and isinstance(fr, (int, float)) and rw["reward"] > 1 and abs(rw["reward"] / 100 - fr) < 1e-3:
        rw["reward"] = fr
        (r / "result.json").write_text(json.dumps(res, indent=2) + "\n")
        print("[package] %s: result.json reward rescaled to 0-1 (%s)" % (r.name, fr))
PY
"$PY" - "$T/$M" "$BD/tasks/$U/tests/test_weights.json" <<'PY'
# pass@N.json for a multi-run task, from the same numbers final QC reconciles (report.json final_reward).
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); s = json.loads((d / "pass_summary.json").read_text())
th = s.get("threshold", json.loads(pathlib.Path(sys.argv[2]).read_text()).get("threshold", 0.7))
runs = {}
for r in sorted(d.glob("run_*"), key=lambda p: int(p.name[4:])):
    rep = json.loads((r / "report.json").read_text())
    runs[int(r.name[4:])] = (rep.get("final_reward"), bool(rep.get("errored")), rep.get("failure_mode"))
if len(runs) > 1:
    ok = {n for n, (rw, err, _) in runs.items() if not err and rw is not None and rw >= th}
    hist = {}
    for n, (rw, err, fm) in runs.items():
        if n not in ok:
            k = fm or ("errored" if err else "below_threshold"); hist[k] = hist.get(k, 0) + 1
    vals = [rw for rw, _, _ in runs.values() if rw is not None]
    out = {"model": s.get("model"), "attempts_per_task": len(runs), "threshold": th, "passed": len(ok),
           "pass_rate": round(len(ok) / len(runs), 4), "mean_reward_per_trial": round(sum(vals) / len(vals), 4) if vals else None,
           "reward_per_run": {str(n): rw for n, (rw, _, _) in runs.items()}, "failure_mode_histogram": hist}
    (d / ("pass@%d.json" % len(runs))).write_text(json.dumps(out, indent=2) + "\n")
PY
find "$T" \( -name __pycache__ -o -name .DS_Store -o -name "*.pyc" \) -prune -exec rm -rf {} + 2>/dev/null || true
# The packaged task = the copy that ran (tests/test.sh as the harness patched it) + trajectories/.
P="$BD/3_packaged/$U"; rm -rf "$P"; mkdir -p "$BD/3_packaged"
cp -R "$RT/$U" "$P"; rm -rf "$P/trajectories"; cp -R "$T" "$P/trajectories"
find "$P" \( -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} + 2>/dev/null || true
[ "$(fingerprint "$P")" = "$H" ] || { rm -rf "$P"; die "$U: the packaged task differs from the files gate 1 passed"; }
"$PY" - "$P/trajectories/$M/pass_summary.json" "$U" <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
print("[package] %s: %s runs %s/%s | pytest %s rubric %s combined %s" % (sys.argv[2][:8], s.get("model"), s.get("runs_completed"),
      s.get("runs"), s.get("average_pytest_score"), s.get("average_rubric_score"), s.get("average_combined_score")))
PY

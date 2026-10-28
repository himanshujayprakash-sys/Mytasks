#!/bin/bash
# verify.sh <READY folder | batch name>: run on ANY laptop (with yuji-workspace, harbor 0.24.0 and this pipeline) to
# prove the delivered bundles are what passed, with the same verdicts. For every task in READY/LOCK.json:
#   1. files: the task and its trajectories hash to the locked values (a changed file is named)
#   2. gate 1 scripted checks, re-run here from this laptop's workspace skill: same blocking findings as locked
#   3. yuji-final-qc, re-run here: the same verdict line as locked
#   4. tools: this laptop's workspace commit / QC versions / harbor / pytest vs the locked ones
# Model runs cannot repeat bit for bit (the model samples); what must repeat is the grade of the recorded run, and
# final QC re-derives every recorded score from the run files (step 3). Writes VERIFY.md next to LOCK.json.
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/common.sh"
R="$1"; [ -d "$R" ] || R="$PIPELINE/batches/$1/READY"
R="$(cd "$R" 2>/dev/null && pwd)" || die "no READY folder at $1"
[ -f "$R/LOCK.json" ] || die "no LOCK.json in $R"
V="_verify_$(date +%Y%m%d_%H%M%S)"; VB="$PIPELINE/batches/$V"
mkdir -p "$VB/tasks" "$VB/out"; cp "$PIPELINE/waivers.default.txt" "$VB/waivers.txt"
trap 'rm -rf "$VB"' EXIT
TC="$VB/out/toolchain.json"; "$PY" "$PIPELINE/lib/toolchain.py" "$WORKSPACE" "$HARNESS" "$TC" --for qc >/dev/null 2>&1
for U in $("$PY" -c 'import json,sys;print(" ".join(sorted(json.load(open(sys.argv[1]))["tasks"])))' "$R/LOCK.json"); do
  [ -d "$R/$U" ] || { echo "$U missing" >> "$VB/out/missing.txt"; continue; }
  rsync -a --exclude trajectories "$R/$U/" "$VB/tasks/$U/"
  # waivers recorded for this task apply again, so a waived finding is not reported as a change
  "$PY" -c 'import json,sys;l=json.load(open(sys.argv[1]))["tasks"][sys.argv[2]];[print(sys.argv[2][:8],w,"locked waiver") for w in l["gate1"]["waived"]]' "$R/LOCK.json" "$U" >> "$VB/waivers.txt"
  log "$U: gate-1 scripted checks"
  bash "$PIPELINE/lib/qc_static.sh" "$V" "$U" > /dev/null 2>&1
  "$PY" "$PIPELINE/lib/gate.py" "$VB/1_qc/$U" "$VB/waivers.txt" off "$TASK_QC_SKILL" "$REF_FOLDER" > /dev/null
  log "$U: final QC"
  W=$("$PY" -c 'import json,sys;print(",".join(json.load(open(sys.argv[1]))["tasks"][sys.argv[2]]["gate1"]["waived"]))' "$R/LOCK.json" "$U")
  "$PY" -I "$FINAL_QC" "$R/$U" --out "$VB/out/fq_$U" --ref "$REF_FOLDER" --agent "$AGENT" --model "$MODEL" ${W:+--waive "$W"} --no-llm-pack > /dev/null 2>&1
done
"$PY" - "$R" "$VB" "$TC" <<'PY'
import json, pathlib, re, sys
R, VB, TC = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
sys.path.insert(0, str(VB.parent.parent / "lib"))
import fingerprint
lock = json.loads((R / "LOCK.json").read_text())["tasks"]
here = json.loads(TC.read_text()) if TC.exists() else {}
lines, bad = [], 0
for u, L in sorted(lock.items()):
    probs = []
    if not (R / u).is_dir():
        probs.append("folder missing")
    else:
        for part, only in (("task", None), ("trajectories", "trajectories")):
            now = fingerprint.files(R / u, only); old = L["files"][part]
            for k in sorted(set(now) | set(old)):
                if now.get(k) != old.get(k):
                    probs.append("%s file %s: %s" % (part, "added" if k not in old else "removed" if k not in now else "changed", k))
        g = VB / "1_qc" / u / "gate.json"
        if g.exists():
            gj = json.loads(g.read_text())
            blk = ["%s %s %s" % (f["sev"], f["id"], f["text"][:90]) for f in gj["findings"] if f["sev"] in ("BLOCKER", "MAJOR") and not f.get("waived")]
            probs += ["gate-1 check now finds: " + b for b in blk]
        else:
            probs.append("gate-1 checks did not run")
        fq = VB / "out" / ("fq_" + u) / ("%s-final-qc.md" % u)
        vl = (re.search(r"^- VERDICT: .*$", fq.read_text(), re.M) or [""])[0] if fq.exists() else "(final QC did not run)"
        if vl != L["final_qc"]["verdict_line"]:
            probs.append("final QC verdict differs: here %r, locked %r" % (vl, L["final_qc"]["verdict_line"]))
    bad += bool(probs)
    lines.append("## `%s`: %s" % (u, "SAME" if not probs else "DIFFERENT"))
    lines += ["- " + p for p in probs[:40]] + [""]
tool = []
lt = next(iter(lock.values()), {}).get("toolchain", {}).get("qc", {})
for k in ("workspace_commit", "task_qc", "final_qc", "harbor", "pytest"):
    if lt.get(k) and here.get(k) and lt[k] != here[k]:
        tool.append("- %s: here %s, locked %s" % (k, here[k], lt[k]))
head = ["# Verify %s" % R, "", "%d task(s): %d SAME, %d DIFFERENT" % (len(lock), len(lock) - bad, bad), ""]
if tool:
    head += ["Tools differ from the laptop that locked these (a DIFFERENT verdict may come from the newer QC, not the task):", *tool, ""]
(R / "VERIFY.md").write_text("\n".join(head + lines))
print("\n".join(head + lines))
sys.exit(1 if bad else 0)
PY

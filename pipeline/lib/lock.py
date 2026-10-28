#!/usr/bin/env python3
"""lock.py <batch dir> <uuid>: add or replace this task's entry in READY/LOCK.json, the record another laptop checks
against (pipeline.sh verify). It holds only content hashes, versions and verdicts, never a path or a credential:
  task_sha256          the files gate 1 passed = the files that ran = the files in READY/<uuid> (trajectories/ excluded)
  trajectories_sha256  READY/<uuid>/trajectories as delivered
  files                {relative path: sha256} of both, so a drift report names the file
  gate1, final_qc      verdicts, versions, waivers used, the deterministic final-QC verdict line
  runs                 per run: recorded pytest / rubric / combined, and the regraded pytest (equal, or no lock)
  toolchain            workspace + harness commits, harness local edits hash, harbor, python, pytest
"""
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fingerprint  # noqa: E402

BD, U = pathlib.Path(sys.argv[1]), sys.argv[2]
R = BD / "READY" / U
gate = json.loads((BD / "1_qc" / U / "gate.json").read_text())
task = fingerprint.files(R)
traj = fingerprint.files(R, "trajectories")
fq = (BD / "4_final_qc" / U / "after_clean" / ("%s-final-qc.md" % U)).read_text()
vline = (re.search(r"^- VERDICT: .*$", fq, re.M) or [""])[0]
regrade = json.loads((BD / "4_final_qc" / U / "regrade.json").read_text())
runs = {}
for ps in R.glob("trajectories/*/pass_summary.json"):
    for r in json.loads(ps.read_text()).get("per_run") or []:
        n = "run_%d" % r["run_index"]
        runs[n] = {k: r.get(k) for k in ("pytest_score", "rubric_score", "combined_score", "passed", "errored")}
        runs[n]["regraded_pytest"] = next((g["regraded_pytest"] for g in regrade if g["run"] == n), None)
tc = {}
for p in (BD / "1_qc" / U / "toolchain.json", BD / "2_runs" / "toolchain" / ("%s.json" % U)):
    if p.exists():
        t = json.loads(p.read_text())
        tc["qc" if "1_qc" in str(p) else "run"] = {k: t.get(k) for k in ("workspace_commit", "task_qc", "final_qc", "harness_commit",
                                                                          "harness_local_edits", "harness_local_edits_sha256", "harbor", "python", "pytest")}
waivers = sorted({f["id"] for f in gate.get("findings", []) if f.get("waived")})
entry = {
    "task_sha256": fingerprint.digest(task), "trajectories_sha256": fingerprint.digest(traj),
    "gate1": {"verdict": gate["verdict"], "task_sha256": gate.get("task_sha256"), "skill": " ".join(gate.get("skill") or []),
              "waived": waivers, "review": (gate.get("review") or {}).get("verdict")},
    "final_qc": {"verdict_line": vline, "waived": sorted(set(re.findall(r"\b(S\d-\d+|F\d+)\b", " ".join(waivers))))},
    "runs": runs, "toolchain": tc,
    "locked_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "files": {"task": task, "trajectories": traj},
}
if entry["task_sha256"] != gate.get("task_sha256"):
    sys.exit("lock refused: READY/%s differs from the files gate 1 passed" % U)
lp = BD / "READY" / "LOCK.json"
lock = json.loads(lp.read_text()) if lp.exists() else {"about": "pipeline.sh verify checks READY/<uuid> against this; "
                                                       "regenerate only through the pipeline", "tasks": {}}
lock["tasks"][U] = entry
lp.write_text(json.dumps(lock, indent=1, sort_keys=True) + "\n")
print("[lock] %s: task %s | trajectories %s | %d run(s)" % (U[:8], entry["task_sha256"][:12], entry["trajectories_sha256"][:12], len(runs)))

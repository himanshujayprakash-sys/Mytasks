#!/usr/bin/env python3
"""board.py <batch dir>: BOARD.md (one row per task, where it is in the pipeline) and SKIPPED.md (tasks that failed
gate 1 and get no model runs, with the reason). Reads only what the stages left on disk."""
import json
import pathlib
import re
import sys

BD = pathlib.Path(sys.argv[1])
runs_root = BD / "2_runs"
rows, skipped = [], []
for t in sorted(p for p in (BD / "tasks").iterdir() if (p / "task.toml").exists()):
    u = t.name
    g = BD / "1_qc" / u / "gate.json"
    gate = json.loads(g.read_text()) if g.exists() else {"verdict": "PENDING", "why": "not checked yet"}
    if gate["verdict"] == "FAIL":
        skipped.append((u, gate["why"], [f for f in gate.get("findings", []) if f["sev"] in ("BLOCKER", "MAJOR") and not f.get("waived")],
                        gate.get("review", {}).get("blocking", [])))
    nruns = len(list((runs_root / u / "trajectory").glob("run_*"))) if (runs_root / u / "trajectory").exists() else 0
    score = "-"
    ps = next((BD / "3_packaged" / u / "trajectories").glob("*/pass_summary.json"), None) if (BD / "3_packaged" / u / "trajectories").exists() else None
    if ps:
        s = json.loads(ps.read_text())
        score = "%s (pytest %s / rubric %s)" % (s.get("average_combined_score"), s.get("average_pytest_score"), s.get("average_rubric_score"))
    fq = BD / "4_final_qc" / u / ("%s-final-qc.md" % u)
    final = "-"
    if fq.exists():
        m = re.search(r"(?i)verdict[:*\s|]*\**\s*(PASS|FAIL|PARTIAL)", fq.read_text())
        final = m.group(1) if m else "see report"
    stage = ("READY" if (BD / "READY" / u).exists() else "final QC failed" if final in ("FAIL", "PARTIAL")
             else "packaged" if ps else "runs done" if nruns else "skipped (gate 1 FAIL)" if gate["verdict"] == "FAIL"
             else "waiting for runs" if gate["verdict"] == "PASS" else "in gate 1")
    rows.append("| `%s` | %s | %s | %d | %s | %s | **%s** |" % (u[:8], gate["verdict"], gate["why"].replace("|", "/")[:90], nruns, score, final, stage))

n_ready = sum(1 for r in rows if r.endswith("**READY** |"))
md = ["# %s" % BD.name, "", "%d tasks | %d ready | %d skipped at gate 1" % (len(rows), n_ready, len(skipped)), "",
      "| Task | Gate 1 | Why | Runs | Score (combined) | Final QC | Stage |", "|---|---|---|---:|---|---|---|", *rows, ""]
(BD / "BOARD.md").write_text("\n".join(md))
sk = ["# Skipped at gate 1 (no model runs)", "",
      "Fix the task in tasks/<uuid>/ (or its source and `pipeline.sh add`), then rerun `pipeline.sh qc`.", ""]
for u, why, fs, rv in skipped:
    sk += ["## `%s`" % u, "", why, ""] + ["- %s %s: %s (%s)" % (f["sev"], f["id"], f["text"], f["where"]) for f in fs] + ["- " + x for x in rv] + [""]
(BD / "SKIPPED.md").write_text("\n".join(sk if skipped else sk[:1] + ["", "None."]))
print("\n".join(md))

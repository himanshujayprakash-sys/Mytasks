#!/usr/bin/env python3
"""rebake_gt_env.py <task dir> <oracle trial dir> <out.json>: write solution/gt_env.json from an oracle run, in the
layout the tasks use: "_canary" (the task's harbor-canary line) first, then every app of the run's raw capture
(artifacts/logs/artifacts/atlas/end_env.json) as {status, output}.
Refuses unless the trial scored pytest 1.0 and rubric 1.0 (a judged oracle) and ran on the expected task copy
(--ran-on PATH, harbor's config.json task.path). Never writes in the task: compare <out.json>, then copy.
"""
import json
import os
import pathlib
import re
import sys

a = sys.argv[1:]
T, TR, OUT = (pathlib.Path(x).resolve() for x in a[:3])
ran_on = os.path.realpath(a[a.index("--ran-on") + 1]) if "--ran-on" in a else None
reward = json.loads((TR / "verifier" / "reward.json").read_text())
if not (reward.get("pytest") == 1.0 and reward.get("rubric") == 1.0):
    sys.exit("refused: the oracle run scored %s, not pytest 1.0 + rubric 1.0" % reward)
path = (json.loads((TR / "config.json").read_text()).get("task") or {}).get("path", "")
if ran_on and os.path.realpath(path) != ran_on:
    sys.exit("refused: the oracle ran on %s, not on %s" % (path, ran_on))
cap = TR / "artifacts" / "logs" / "artifacts" / "atlas" / "end_env.json"
env = json.loads(cap.read_text())
canary = re.search(r"harbor-canary GUID [0-9a-f-]{36}", (T / "task.toml").read_text()).group(0)
out = {"_canary": canary}
for k, v in sorted(env.items()):   # apps in alphabetical order, as the existing gt_env.json files have them
    if k.startswith("Light") and isinstance(v, dict):
        out[k] = {"status": v.get("status"), "output": v.get("output")}
OUT.write_text(json.dumps(out, indent=1) + "\n")
print("gt_env: %d apps from %s" % (len(out) - 1, TR.name))

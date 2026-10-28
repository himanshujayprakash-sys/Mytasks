#!/usr/bin/env python3
"""Pull the command blocks out of the workspace yuji-task-qc SKILL.md, so the pipeline always runs the version
that is checked in to yuji-workspace (no copy of the checks lives here).

usage: skill_blocks.py <SKILL.md> <out dir>

Writes <out dir>/NN_<stage>.sh for every ```bash block that works on one bundle (starts with
`source /tmp/qc/<uuid>-report/env.sh`), plus index.json naming each block's kind:
  static   runs unattended, no Docker, no model (Stages 0-5 probes)
  needs    needs a hand-built input (truth.txt / wrong.txt); runs only when that file exists
  live     the tmux live-run block; replaced by lib/qc_live.sh (same harbor command, run in the foreground)
  reader   reads the live trials (S5-10/11/12/15/16); run after the live stage
Blocks that do not start with the env.sh line (setup, Docker preflight with its prune commands, judge preflight)
are never extracted: the pipeline does those itself.
"""
import json
import pathlib
import re
import sys

skill, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("*.sh"):
    old.unlink()
text = skill.read_text()
version = (re.search(r"QC skill version: `([^`]+)`", text) or [None, "unknown"])[1]
stage = "0"
index = []
for m in re.finditer(r"^## (\d+)\. Stage (\d)|```bash\n(.*?)```", text, re.S | re.M):
    if m.group(2):
        stage = m.group(2)
        continue
    body = m.group(3)
    if not body.lstrip().startswith("source /tmp/qc/<uuid>-report/env.sh"):
        continue
    if "tmux new-session" in body:
        kind = "live"
    elif "live_check.py" in body or "gt_env_check.py" in body:
        kind = "reader"
    elif "truth.txt" in body or "wrong.txt" in body:
        kind = "needs"
    else:
        kind = "static"
    if re.search(r"docker [a-z]+ prune|\brm -rf /|git (push|commit)", body):
        kind = "skipped-unsafe"
    line = text[: m.start()].count("\n") + 1
    name = "%02d_stage%s_L%d.sh" % (len(index) + 1, stage, line)
    (out / name).write_text("#!/bin/bash\n# from %s line %d (%s)\n%s" % (skill.name, line, kind, body))
    index.append({"file": name, "stage": stage, "line": line, "kind": kind})
(out / "index.json").write_text(json.dumps({"skill": str(skill), "version": version, "blocks": index}, indent=1))
print(version, ", ".join("%s:%s" % (b["file"][:2], b["kind"]) for b in index))

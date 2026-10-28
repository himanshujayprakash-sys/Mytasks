#!/usr/bin/env python3
"""toolchain.py <workspace> <harness> <out.json> [--for qc|run]: record every tool version a verdict or a run depends
on, and refuse (exit 1) when this laptop's tools are not the shared ones, so the same task gives the same result on
another laptop:
  - yuji-workspace: commit; its skills/ must have no local edits (the QC must be the shared QC)
  - yuji-harness-2: commit; the files that decide grading and delivery must have no local edits
    (assets/verifier/test.sh, scripts/patch_test_sh.py, tools/delivery_utils/, tools/openhands_agent/);
    other local edits (this laptop's kiro / claude-code routing) are recorded, not refused
  - harbor 0.24.0, the pipeline's python / pytest (the verifier image's pytest 9.1.1)
A workspace behind origin/main is a warning (pull it so both laptops run the same QC), never a refusal.
"""
import json
import pathlib
import subprocess
import sys

ws, hz, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
purpose = sys.argv[sys.argv.index("--for") + 1] if "--for" in sys.argv else "qc"
GRADING = ("assets/verifier/", "scripts/patch_test_sh.py", "tools/delivery_utils/", "tools/openhands_agent/")


def sh(*cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception:
        return ""


def dirty(repo):
    return [l[3:] for l in sh("git", "status", "--porcelain", "--untracked-files=no", cwd=repo).splitlines()]


rec, refuse, warn = {}, [], []
rec["workspace_commit"] = sh("git", "rev-parse", "HEAD", cwd=ws)
ws_dirty = [f for f in dirty(ws) if f.startswith("skills/")]
rec["workspace_skills_edited"] = ws_dirty
if ws_dirty:
    refuse.append("yuji-workspace skills/ has local edits %s: the QC must be the shared one (git -C <workspace> diff)" % ws_dirty)
behind = sh("git", "rev-list", "--count", "HEAD..origin/main", cwd=ws)
if behind and behind != "0":
    warn.append("yuji-workspace is %s commit(s) behind origin/main: pull it so every laptop runs the same QC" % behind)
rec["task_qc"] = sh("grep", "-m1", "-o", "yuji-task-qc [0-9.]*", str(ws / "skills/yuji-task-qc/SKILL.md"))
rec["final_qc"] = sh("grep", "-m1", "-o", "yuji-final-qc [0-9.]*", str(ws / "skills/yuji-final-qc/SKILL.md"))
rec["harness_commit"] = sh("git", "rev-parse", "HEAD", cwd=hz)
hz_dirty = dirty(hz)
rec["harness_local_edits"] = hz_dirty
bad = [f for f in hz_dirty if f.startswith(GRADING)]
if bad and purpose == "run":
    refuse.append("yuji-harness-2 has local edits in files that decide grading or delivery %s" % bad)
rec["harness_local_edits_sha256"] = sh("bash", "-c", "git diff | shasum -a 256 | cut -c1-64", cwd=hz) if hz_dirty else None
hv = sh("harbor", "--version").splitlines()
rec["harbor"] = hv[-1] if hv else ""
if rec["harbor"] != "0.24.0":
    refuse.append("harbor on PATH is %r, the format needs 0.24.0" % rec["harbor"])
rec["python"] = sys.version.split()[0]
rec["pytest"] = sh(sys.executable, "-c", "import pytest;print(pytest.__version__)")
if rec["pytest"] != "9.1.1":
    refuse.append("pipeline pytest is %r, the verifier image pins 9.1.1" % rec["pytest"])
rec["refused"], rec["warnings"] = refuse, warn
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(rec, indent=1))
for w in warn:
    print("[toolchain] WARNING: " + w, file=sys.stderr)
for r in refuse:
    print("[toolchain] REFUSED: " + r, file=sys.stderr)
sys.exit(1 if refuse else 0)

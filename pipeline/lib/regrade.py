#!/usr/bin/env python3
"""regrade.py <task dir> <harness run dir trajectory/run_N> <out dir>: re-grade one finished run with the task's
own tests, outside Docker, exactly as tests/test.sh steps 1-3 and the ledger do, and compare with the score the
run recorded. A mismatch means the tests that ship are not the tests that produced the score (the task changed
after the run) or the grade depends on the machine. Prints one JSON line; exit 1 on a mismatch.

Inputs from the run: verifier/agent_trajectory.json (the trajectory the grader built; rebuilt from agent/ when
absent), verifier/end_env.json, verifier/server_tool_calls.log, artifacts/workspace, agent/ (ATLAS_AGENT_LOG_DIR).
Never writes inside the task or the run.
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

B, RUN, O = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
O.mkdir(parents=True, exist_ok=True)
T = O / "tests"
shutil.rmtree(T, ignore_errors=True)
shutil.copytree(B / "tests", T)
PY = sys.executable
blocks = re.findall(r"python3 - (?:[^\n]*)<<'PYEOF'\n(.*?)\nPYEOF", (B / "tests/test.sh").read_text(), re.S)
traj = O / "agent_trajectory.json"
if (RUN / "verifier/agent_trajectory.json").exists():
    shutil.copy(RUN / "verifier/agent_trajectory.json", traj)
else:   # test.sh step 1, pointed at the run's agent log
    code = blocks[0].replace('pathlib.Path("/logs/agent")', "pathlib.Path(%r)" % str(RUN / "agent")) \
                    .replace('pathlib.Path("/tmp/agent_trajectory.json")', "pathlib.Path(%r)" % str(traj))
    subprocess.run([PY, "-c", code], capture_output=True, text=True)
end = O / "end_env.json"
if (RUN / "verifier/end_env.json").exists():
    shutil.copy(RUN / "verifier/end_env.json", end)
    if len(blocks) > 1 and "end_env" in blocks[1]:   # test.sh step 2: both snapshot shapes
        subprocess.run([PY, "-c", blocks[1], str(end), str(traj)], capture_output=True, text=True)
logs = O / "verifier"
shutil.rmtree(logs, ignore_errors=True)
logs.mkdir()
slog = RUN / "verifier/server_tool_calls.log"
env = {k: v for k, v in os.environ.items() if not k.endswith(("_API_KEY", "_TOKEN", "_B64")) and k != "JUDGE_MODEL"}
env.update(PYTHONDONTWRITEBYTECODE="1", ATLAS_TESTS_DIR=str(T), ATLAS_VERIFIER_LOGS=str(logs), ATLAS_TRAJECTORY=str(traj),
           MCPATLAS_TRAJECTORY=str(traj), COMPLEXMCP_TRAJECTORY=str(traj), ATLAS_END_ENV=str(end),
           ATLAS_OLD_ENV=str(T / "old_env.json"), ATLAS_ORACLE=str(T / "oracle.json"),
           ATLAS_OUTPUT_ROOTS=str(RUN / "artifacts/workspace"),
           ATLAS_SERVER_LOG=str(slog if slog.exists() else O / "missing_server.log"),
           AUTH_CLAIMS_PATH=str(logs / "claims_coverage.json"), ATLAS_AGENT_LOG_DIR=str(RUN / "agent"))
subprocess.run([PY, "-c", "import sys;sys.path[:0]=[sys.argv[1],sys.argv[1]+'/reward/pytest'];import ledger;ledger.run_ledger()",
                str(T)], cwd=T, env=env, capture_output=True, text=True)


def load(p):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception:
        return {}


new = load(logs / "grade_report.json")
old = load(RUN / "verifier/grade_report.json")
rec = load(RUN / "verifier/reward.json").get("pytest")
got = new.get("reward")
want = old.get("reward", rec)
ok = got is not None and want is not None and abs(got - want) < (1e-9 if "reward" in old else 6e-5)
out = {"run": RUN.name, "recorded_pytest": want, "regraded_pytest": got, "match": ok,
       "recorded_missed": sorted(old.get("missed") or []), "regraded_missed": sorted(new.get("missed") or []),
       "regraded_guards": new.get("guards_tripped"), "errors": new.get("errors"),
       "server_log": slog.exists()}
if old and new and sorted(old.get("missed") or []) != sorted(new.get("missed") or []):
    out["match"] = False
print(json.dumps(out))
sys.exit(0 if out["match"] else 1)

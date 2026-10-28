#!/usr/bin/env python3
"""rebake_old_env.py <task dir> <out.json>: recapture tests/old_env.json, the untouched seed world, from the task's
OWN light-servers code and world_data at the seed its compose file sets (COMPLEXMCP_SEED). One entry per graded app
(task.toml [task.metadata] apps), each {"status": "ok", "output": <the app's session dict>}, the layout the existing
old_env.json files use. Runs the servers in-process (uv, Python 3.12, the task's own requirements.txt); no Docker, no
network beyond uv's package cache. Never writes in the task: compare <out.json> with tests/old_env.json, then copy.
Same method as the factory's old_env.py, without its hardcoded harness path and seed.
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import tomllib

T, OUT = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
LS = T / "environment" / "light-servers"
compose = (T / "environment" / "docker-compose.yaml").read_text()
seed = re.search(r'COMPLEXMCP_SEED:\s*"?(\d+)', compose).group(1)
# Keep the layout of the task's existing old_env.json: its app list, key order and "_canary" line (tasks differ:
# some snapshot only the graded apps, some every wired server). Without one, the graded apps.
prev_path = T / "tests" / "old_env.json"
prev = json.loads(prev_path.read_text()) if prev_path.exists() else {}
order = list(prev) or tomllib.loads((T / "task.toml").read_text())["task"]["metadata"]["apps"]
apps = [k for k in order if k.startswith("Light")]
code = r'''
import importlib, json, sys, pkgutil
out = {}
for app in json.loads(sys.argv[2]):
    pkg = importlib.import_module(f"software.{app}")
    for m in pkgutil.iter_modules(pkg.__path__):
        if m.name in ("app", "session"):
            continue
        mod = importlib.import_module(f"software.{app}.{m.name}")
        cls = next((getattr(mod, n) for n in dir(mod) if isinstance(getattr(mod, n), type)
                    and getattr(mod, n).__module__ == mod.__name__ and hasattr(getattr(mod, n), "get_session_dict")), None)
        if cls:
            out[app] = {"status": "ok", "output": cls(os_cfg={}, seed=int(sys.argv[3])).get_session_dict()}
            break
    else:
        out[app] = {"status": "error", "output": "no session class found"}
open(sys.argv[1], "w").write(json.dumps(out, default=str) + "\n")
print("old_env apps:", sorted(out))
'''
env = {"COMPLEXMCP_SEED": seed, "COMPLEXMCP_SEED_MODE": "seed", "COMPLEXMCP_WORLD_DATA": str(LS / "world_data"),
       "PYTHONPATH": str(LS), "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(pathlib.Path.home()),
       "UV_CACHE_DIR": os.environ.get("UV_CACHE_DIR", "/tmp/qc/uvcache"), "PYTHONDONTWRITEBYTECODE": "1"}
r = subprocess.run(["uv", "run", "--no-project", "--python", "3.12", "--with-requirements", str(LS / "requirements.txt"),
                    "python", "-c", code, str(OUT), json.dumps(apps), seed], cwd=LS, env=env, capture_output=True, text=True)
print((r.stdout + r.stderr)[-1500:])
if r.returncode == 0:
    got = json.loads(OUT.read_text())
    final = {}
    for k in order:
        if k == "_canary" and "_canary" in prev:
            final[k] = prev[k]
        elif k in got:   # same per-app keys as before (some files carry {status, output}, some {output})
            final[k] = {f: got[k][f] for f in prev[k]} if isinstance(prev.get(k), dict) else got[k]
    OUT.write_text(json.dumps(final, default=str) + "\n")
sys.exit(r.returncode)

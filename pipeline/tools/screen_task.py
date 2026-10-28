#!/usr/bin/env python3
"""screen_task.py <task dir> [...]: re-run the contamination screen (yuji-rework-screen 1.0, tools/screen.py) on a task
as harness_mcp_atlas will see it, and record the result honestly:
  1. import the task into the separate harness checkout (input/<uuid>), run the screen there
  2. keep the screen's roots/ beside the task set: <task set>/_roots/<uuid>/ (hma_build.sh uses them)
  3. write the screen's own numbers into task.toml [task.metadata.contamination_screen] (instrument, screened_on today,
     worst_non_excluded_containment, roots with their sha256)
  4. a one-line upstream_provenance string becomes the table the harness requires: origin = that same text; train_cutoff
     and license = the values every sibling task of the same factory batch records (printed, so the user can confirm)
The freeze table hashes every agent-visible file, so any later change to instruction/data/world needs a new screen.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
HMA_MAIN = ROOT / "harness_mcp_atlas_main"
PY = ROOT / "pipeline" / ".venv" / "bin" / "python"
FACTORY_CUTOFF, FACTORY_LICENSE = "2026-06-01", "internal benchmark data, not for redistribution"
INSTRUMENT = "yuji-rework-screen 1.0 (local 8-word shingle near-duplicate and freeze screen; not the CRUCIBLE screen)"

for arg in sys.argv[1:]:
    T = pathlib.Path(arg).resolve()
    U = T.name
    r = subprocess.run([str(HMA_MAIN / ".venv/bin/python"), "-m", "harness.import_task", "--from", str(T), "--name", U, "--force"],
                       cwd=HMA_MAIN, capture_output=True, text=True)
    if r.returncode:
        print(U[:8], "import failed:", (r.stdout + r.stderr)[-400:])
        continue
    inp = HMA_MAIN / "input" / U
    s = subprocess.run([str(PY), str(ROOT / "pipeline/tools/screen.py"), str(inp), U], capture_output=True, text=True)
    if s.returncode:
        print(U[:8], "screen failed:", s.stderr[-400:])
        continue
    res = json.loads(s.stdout.strip().splitlines()[-1])
    store = T.parent / "_roots" / U
    shutil.rmtree(store, ignore_errors=True)
    shutil.copytree(inp / "roots", store)

    toml = (T / "task.toml").read_text()
    notes = []
    # 4. provenance string -> table
    m = re.search(r'^upstream_provenance = "(.*)"\n', toml, re.M)
    if m:
        toml = toml.replace(m.group(0), "")
        block = ('\n[task.metadata.upstream_provenance]\norigin = "%s"\ntrain_cutoff = "%s"\nlicense = "%s"\n'
                 % (m.group(1), FACTORY_CUTOFF, FACTORY_LICENSE))
        notes.append("upstream_provenance string -> table (train_cutoff/license = factory batch values: confirm)")
    else:
        block = ""
    # 3. contamination screen table (replace an existing one, else add)
    roots = res["roots"]
    screen = ('[task.metadata.contamination_screen]\ninstrument = "%s"\nscreened_on = "%s"\nworst_non_excluded_containment = %.4f\n'
              'roots = { exclusion_list = "%s", freeze_table = "%s", near_duplicate_index = "%s" }\n'
              % (INSTRUMENT, res["screened_on"], res["worst_non_excluded"], roots["exclusion_list"], roots["freeze_table"],
                 roots["near_duplicate_index"]))
    old = re.search(r"^\[task\.metadata\.contamination_screen\]\n(?:(?!\[)[^\n]*\n)*", toml, re.M)
    if old:
        toml = toml.replace(old.group(0), screen + "\n", 1) if not old.group(0).endswith("\n\n") else toml.replace(old.group(0), screen + "\n", 1)
    else:
        block += "\n" + screen
    if block:
        anchor = re.search(r"^\[task\.metadata\.scenario\]", toml, re.M)
        toml = (toml[:anchor.start()] + block.lstrip("\n") + "\n" + toml[anchor.start():]) if anchor else toml.rstrip("\n") + "\n" + block
    import tomllib
    tomllib.loads(toml)   # must still parse
    (T / "task.toml").write_text(toml)
    print("%s screened: worst non-excluded %.4f (%s) over %d documents; roots kept in %s%s"
          % (U[:8], res["worst_non_excluded"], pathlib.Path(res["worst_doc"]).parent.name[:8] if res["worst_doc"] else "-",
             res["documents"], store.relative_to(T.parent.parent), ("; " + "; ".join(notes)) if notes else ""))

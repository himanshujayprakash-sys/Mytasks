#!/usr/bin/env python3
"""(ported to pipeline/tools from yuji-submit-sample-v2/_factory/tools/screen.py; only the corpus paths changed)
yuji-rework-screen 1.0: a local near-duplicate and freeze screen for one harness input folder.

NOT the CRUCIBLE screen (that instrument and its ENGRAM roots are not available here). What it does, and records:
  exclusion_list       the corpus documents excluded from the near-duplicate verdict, with why (the task's own
                       pre-re-author source, which states the same problem by construction)
  freeze_table         the SHA-256 of every agent-visible file of the task at screening time
  near_duplicate_index 8-word shingle containment of the task's instruction against every instruction found in
                       the local corpora (harness inputs and builds, yuji-submit, samples, yuji-submit-sample)
Writes roots/{exclusions.txt,freeze.csv,neardup.idx} under the input folder and prints the task.toml block.
"""
import hashlib, json, os, pathlib, re, sys, datetime
SRC = pathlib.Path(sys.argv[1]).resolve(); UUID = sys.argv[2]
# Corpora (pipeline port, 2026-10-28): the factory's set at the delivery folder's current path, plus the separate
# harness checkout, the other task sets, and the accepted stage-1 bundles (yuji-workspace/trajectories).
D = pathlib.Path(os.environ.get("DELIVERY", "/Users/mac/Documents/Desktop items/Mcp_tooluse_delivery"))
CORPORA = [D / p for p in ("harness_mcp_atlas/input", "harness_mcp_atlas/out/build", "harness_mcp_atlas_main/input",
                           "yuji-submit", "samples", "yuji-submit-sample", "new_10_20261026")] + \
          [D.parent / "yuji-workspace" / "trajectories"]
CORPORA = [c for c in CORPORA if c.is_dir()]
W = re.compile(r"[A-Za-z0-9']+")
def sh(t, n=8):
    w = [x.lower() for x in W.findall(re.sub(r"<!--.*?-->", " ", t, flags=re.S))]
    return {tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}
mine = sh((SRC / "instruction.md").read_text())
roots = SRC / "roots"; roots.mkdir(exist_ok=True)
docs = []
for c in CORPORA:
    for p in sorted(c.rglob("instruction.md")):
        rp = p.resolve()
        inner = next((str(rp)[len(str(c.resolve())):] for c in CORPORA if str(rp).startswith(str(c.resolve()))), str(rp))
        if rp == (SRC / "instruction.md").resolve() or "/out/jobs/" in str(rp) or "/.cache/" in str(rp) \
                or "/trajectories/" in inner or "/trajectory/" in inner:   # copies inside run folders are not tasks
            continue
        docs.append(rp)
excl, rows = [], []
for p in docs:
    s = sh(p.read_text(errors="ignore"))
    ratio = len(mine & s) / len(mine) if mine else 0.0
    own = f"/{UUID}/" in str(p)
    parent = os.environ.get("SCREEN_PARENT", "")
    if own:
        excl.append(f"{p}\tsame task ({UUID}): its pre-re-author source or a copy of this re-author")
    elif parent and f"/{parent}/" in str(p):
        own = True
        excl.append(f"{p}\tdeclared parent task ({parent}): this task is a variant of it")
    rows.append((ratio, str(p), own))
(roots / "exclusions.txt").write_text("# yuji-rework-screen 1.0 exclusion list\n" + "\n".join(excl) + "\n")
fz = ["path,sha256,bytes"]
for part in ("instruction.md", "task.toml", "data", "world_data"):
    q = SRC / part
    for f in ([q] if q.is_file() else sorted(x for x in q.rglob("*") if x.is_file())):
        if part == "task.toml":
            continue          # task.toml carries this record itself; freezing it would be circular
        b = f.read_bytes(); fz.append(f'"{f.relative_to(SRC)}",{hashlib.sha256(b).hexdigest()},{len(b)}')
(roots / "freeze.csv").write_text("\n".join(fz) + "\n")
rows.sort(reverse=True)
worst = max((r for r in rows if not r[2]), default=(0.0, "", False))
idx = [f"# yuji-rework-screen 1.0 near-duplicate index: 8-word shingle containment of {UUID} instruction.md",
       f"# documents {len(rows)}; this instruction {len(mine)} shingles; worst non-excluded {worst[0]:.4f} {worst[1]}"]
idx += [f"{r:.4f}\t{'EXCLUDED' if own else 'screened'}\t{p}" for r, p, own in rows]
(roots / "neardup.idx").write_text("\n".join(idx) + "\n")
dig = lambda n: hashlib.sha256((roots / n).read_bytes()).hexdigest()
print(json.dumps({"worst_non_excluded": worst[0], "worst_doc": worst[1], "documents": len(rows), "excluded": len(excl),
                  "roots": {"exclusion_list": f"roots/exclusions.txt@sha256:{dig('exclusions.txt')}",
                            "freeze_table": f"roots/freeze.csv@sha256:{dig('freeze.csv')}",
                            "near_duplicate_index": f"roots/neardup.idx@sha256:{dig('neardup.idx')}"},
                  "screened_on": datetime.date.today().isoformat()}))

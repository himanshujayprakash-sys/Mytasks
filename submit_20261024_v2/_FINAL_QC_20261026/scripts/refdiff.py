import sys, importlib.util, pathlib
spec = importlib.util.spec_from_file_location("fq", sys.argv[1]); fq = importlib.util.module_from_spec(spec); spec.loader.exec_module(fq)
refs = sorted(p for p in pathlib.Path(sys.argv[2]).iterdir() if p.is_dir())
class C:
    def __init__(s, b): s.b = b
    def text(s, p):
        q = pathlib.Path(p) if p.startswith("/") else s.b / p
        return q.read_text(errors="replace") if q.exists() else None
for b in sorted(pathlib.Path(sys.argv[3]).iterdir()):
    if not (b / "task.toml").exists(): continue
    row = []
    for r in refs:
        hits, notes, cl = fq._harness_diff(C(b), r)
        row.append("%s:%s" % (r.name[:4], ",".join(f.split("/")[-1] + "(%d)" % (len(d) if isinstance(d, list) else 1) for f, d in hits) or "MATCH"))
    print(b.name[:8], " | ".join(row))

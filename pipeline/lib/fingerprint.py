#!/usr/bin/env python3
"""fingerprint.py <task dir> [--files OUT.json] [--only trajectories]: one sha256 for a task's content.

The hash covers every file's relative path and bytes, in sorted order, so it is the same on any laptop (no
timestamps, permissions or absolute paths). trajectories/, .DS_Store, __pycache__ and *.pyc are left out (the
task); --only trajectories hashes just that folder (the runs). --files writes {relative path: sha256} too, so a
drift report can name the files that changed.
"""
import hashlib
import json
import pathlib
import sys

SKIP = {".DS_Store", "__pycache__"}


def files(root, only=None):
    base = root / only if only else root
    if not base.exists():
        return {}
    out = {}
    for p in sorted(base.rglob("*")):
        rel = p.relative_to(root).as_posix()
        parts = rel.split("/")
        if any(x in SKIP for x in parts) or p.suffix == ".pyc" or not p.is_file():
            continue
        if not only and parts[0] in ("trajectories", "trajectory"):
            continue
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def digest(table):
    h = hashlib.sha256()
    for rel, fh in sorted(table.items()):
        h.update(rel.encode() + b"\0" + fh.encode() + b"\n")
    return h.hexdigest()


if __name__ == "__main__":
    a = sys.argv[1:]
    only = a[a.index("--only") + 1] if "--only" in a else None
    t = files(pathlib.Path(a[0]), only)
    if "--files" in a:
        pathlib.Path(a[a.index("--files") + 1]).write_text(json.dumps({"sha256": digest(t), "files": t}, indent=1))
    print(digest(t))

#!/usr/bin/env python3
"""Clean a task's trajectories/ folder the way trajectory-cleanup-log.md describes.

Steps (per task folder, per trajectories/<model>/ and each run_* inside it):
  1. delete  trajectories/<model>/jobs.json and pass@1.json
  2. delete  run_*/verifier/{test-stdout.txt, server_tool_calls.log, rewardkit-stdout.txt,
             pytest-stdout.txt, agent_trajectory.json, grade_report.json, judge.json,
             reward_producer.json} and the run_*/verifier/judge_logs/ folder
             (final_message.md is KEPT unless --drop-final-message is given)
  3. trim    run_*/verifier/reward.json to the single key "reward"
  4. mask    every "/logs/verifier/..." string in run_*/report.json and
             run_*/verifier/reward-details.json with the same number of '*'
             (string length unchanged, JSON stays valid)
  5. check   every remaining file under trajectories/<model>/ for leftover
             "/logs/verifier" text and report it

task.toml authors are NOT touched here.

Usage:
  python3 clean_trajectories.py <task-dir> [<task-dir> ...]
  python3 clean_trajectories.py --root yuji-trajectories          # every task under it
  python3 clean_trajectories.py --dry-run <task-dir>              # show, change nothing
  python3 clean_trajectories.py --check <task-dir>                # report what is still unclean
  python3 clean_trajectories.py --model opus-5 <task-dir>         # default model folder
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

TOP_LEVEL_DELETE = ("jobs.json", "pass@1.json")
VERIFIER_DELETE = (
    "test-stdout.txt",
    "server_tool_calls.log",
    "rewardkit-stdout.txt",
    "pytest-stdout.txt",
    "agent_trajectory.json",
    "grade_report.json",
    "judge.json",
    "reward_producer.json",
)
VERIFIER_DELETE_DIRS = ("judge_logs",)
MASK_FILES = ("report.json", "verifier/reward-details.json")
PATH_RE = re.compile(r'"(/logs/verifier[A-Za-z0-9_./@-]*)"')
LEFTOVER = "/logs/verifier"


def mask_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        return '"' + "*" * len(m.group(1)) + '"'

    return PATH_RE.sub(repl, text), count


def clean_run(run: Path, *, dry: bool, check: bool, drop_final: bool, log: list[str]) -> bool:
    """Returns True if anything was (or would be) changed."""
    changed = False
    ver = run / "verifier"

    names = list(VERIFIER_DELETE) + (["final_message.md"] if drop_final else [])
    for name in names:
        p = ver / name
        if p.is_file():
            changed = True
            log.append(f"  {'would delete' if (dry or check) else 'deleted'}  {p.relative_to(run.parent)}")
            if not (dry or check):
                p.unlink()
    for name in VERIFIER_DELETE_DIRS:
        p = ver / name
        if p.is_dir():
            changed = True
            log.append(f"  {'would delete' if (dry or check) else 'deleted'}  {p.relative_to(run.parent)}/")
            if not (dry or check):
                shutil.rmtree(p)

    reward = ver / "reward.json"
    if reward.is_file():
        data = json.loads(reward.read_text())
        if set(data) != {"reward"}:
            changed = True
            extra = {k: v for k, v in data.items() if k != "reward"}
            log.append(f"  {'would trim' if (dry or check) else 'trimmed'}   {reward.relative_to(run.parent)} "
                       f"(reward={data.get('reward')}, removed {extra})")
            if not (dry or check):
                reward.write_text(json.dumps({"reward": data["reward"]}, indent=2) + "\n")

    for rel in MASK_FILES:
        p = run / rel
        if not p.is_file():
            continue
        text = p.read_text()
        new, n = mask_text(text)
        if n:
            changed = True
            log.append(f"  {'would mask' if (dry or check) else 'masked'}   {n} path(s) in {p.relative_to(run.parent)}")
            if not (dry or check):
                json.loads(new)  # must still be valid JSON
                p.write_text(new)

    return changed


def leftovers(model_dir: Path) -> list[str]:
    hits = []
    for p in sorted(model_dir.rglob("*")):
        if p.is_file():
            try:
                text = p.read_text(errors="ignore")
            except OSError:
                continue
            if LEFTOVER in text:
                hits.append(str(p.relative_to(model_dir.parent.parent)))
    return hits


def clean_task(task: Path, model: str, *, dry: bool, check: bool, drop_final: bool) -> int:
    model_dir = task / "trajectories" / model
    print(f"\n=== {task.name} ({model_dir.relative_to(task)}) ===")
    if not model_dir.is_dir():
        print("  no such trajectories folder, skipped")
        return 1
    log: list[str] = []
    changed = False

    for name in TOP_LEVEL_DELETE:
        p = model_dir / name
        if p.is_file():
            changed = True
            log.append(f"  {'would delete' if (dry or check) else 'deleted'}  {p.relative_to(task)}")
            if not (dry or check):
                p.unlink()

    runs = sorted(d for d in model_dir.glob("run_*") if d.is_dir())
    if not runs:
        log.append("  no run_* folders found")
    for run in runs:
        changed |= clean_run(run, dry=dry, check=check, drop_final=drop_final, log=log)

    print("\n".join(log) if log else "  nothing to do")

    left = leftovers(model_dir)
    if left:
        print(f"  WARNING: '{LEFTOVER}' still present in: " + ", ".join(left))
    elif not (dry or check):
        print(f"  verified: no '{LEFTOVER}' text left under trajectories/{model}/")

    for run in runs:
        ver = run / "verifier"
        if ver.is_dir():
            print(f"  {run.name}/verifier now: " + ", ".join(sorted(p.name for p in ver.iterdir())))

    if check:
        return 1 if (changed or left) else 0
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tasks", nargs="*", type=Path, help="task folders (each holds trajectories/)")
    ap.add_argument("--root", type=Path, help="clean every task folder directly under this directory")
    ap.add_argument("--model", default="opus-5", help="trajectories/<model> folder to clean (default: opus-5)")
    ap.add_argument("--dry-run", action="store_true", help="print what would change, change nothing")
    ap.add_argument("--check", action="store_true", help="report only; exit 1 if anything is still unclean")
    ap.add_argument("--drop-final-message", action="store_true",
                    help="also delete run_*/verifier/final_message.md (kept by default)")
    args = ap.parse_args()

    tasks = list(args.tasks)
    if args.root:
        tasks += sorted(d for d in args.root.iterdir() if d.is_dir() and (d / "trajectories").is_dir())
    if not tasks:
        ap.error("give at least one task folder or --root")

    rc = 0
    for t in tasks:
        t = t.resolve()
        if not t.is_dir():
            print(f"\n=== {t} === not a directory, skipped")
            rc = 1
            continue
        rc |= clean_task(t, args.model, dry=args.dry_run, check=args.check, drop_final=args.drop_final_message)
    return rc


if __name__ == "__main__":
    sys.exit(main())

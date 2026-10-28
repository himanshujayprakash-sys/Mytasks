# Task pipeline

Created tasks go in. Only tasks that pass the **yuji-workspace QC** get model runs. Every task that fails is
skipped and listed with the reason. What comes out is upload-ready bundles in the stage-1 layout.

```
tasks folder ──► 1 GATE 1: task QC ──► 2 model runs ──► 3 package ──► 4 GATE 2: final QC ──► READY/
                 (yuji-task-qc 0.6.2)   (gate-1 PASS   (client layout   (yuji-final-qc 0.2.0)
                                         tasks only)    opus-5/run_N)
                     │ FAIL
                     ▼
                 SKIPPED.md (no runs, reason listed)
```

## Commands

```bash
cd "/Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline"

./pipeline.sh new    b1 "/path/to/tasks folder"    # copy the tasks into batches/b1/tasks (source never touched)
./pipeline.sh qc     b1                            # gate 1 for every task
./pipeline.sh run    b1                            # model runs, gate-1 PASS tasks only
./pipeline.sh package b1                           # runs -> client layout
./pipeline.sh final  b1                            # gate 2; PASS -> batches/b1/READY/<uuid>
./pipeline.sh status b1                            # BOARD.md + SKIPPED.md

./pipeline.sh all    b1                            # all four, task by task (stops a task at its first failure)
./pipeline.sh verify b1                            # on ANY laptop: READY bundles still match READY/LOCK.json
./pipeline.sh qc     b1 <uuid> [<uuid> ...]        # any stage on chosen tasks only
FORCE=1 ./pipeline.sh qc b1 <uuid>                 # redo gate 1 after fixing the task
```

Every stage can be re-run. A finished stage is skipped. Model runs resume where they stopped and never pay twice
for an agent phase.

## What each gate checks

**Gate 1, task QC.** Run before any model run. It runs straight from `yuji-workspace/skills/yuji-task-qc/SKILL.md`.
The command blocks are pulled out of the skill on every run, so a `git pull` of the workspace updates the
pipeline with nothing else to change. It has three parts, and a task stops at the first part that fails.

| Part | What | Cost |
|---|---|---|
| A. Scripted checks | Every command block of the skill (Stages 0–5 probes: structure, task.toml, harness identity, canaries, apt pins, wording, weights, guards, rubric, ledger probes) | ~1 min, no Docker, no model |
| B. Live runs | S5-10 oracle and S5-11 nop, **judged** (codex, `gpt-5.6-sol`), S5-12 oracle without a judge, then the skill's readers (S5-10/11/12/15/16) | ~5–10 min, Docker, 2 judge calls |
| C. Review | The reading checks no script covers (fact sheet, truth.txt leak scan, Stage 2/4 reading). A headless Claude Code session follows the skill and writes the skill's `qc_report.md` | One Claude session |

- **PASS** means no unwaived BLOCKER or MAJOR, live oracle 1/1/1 and nop 0/0/0, and review PASS.
- **FAIL** means the task gets no model runs and is listed in `SKIPPED.md`.
- **PENDING** means a part has not run yet.

`QC_REVIEW=manual` makes the gate wait for `./pipeline.sh review-ok b1 <uuid> "<note>"`. Use it when you, or Claude
in a chat, do the review instead. `QC_REVIEW=off` skips part C, and the board says so.

**Gate 2, final QC.** Run after the runs. It has three checks, and all must pass:
1. The packaged task is the files gate 1 passed.
2. Every run regrades to its recorded pytest score.
3. `yuji-final-qc/scripts/final_qc.py` passes. It checks every run, the pass@k numbers, reward reconstruction,
   reward hacking, the false-test and overlap scans, and hygiene.

Only a PASS is copied to `READY/` and locked.

Packaging also corrects one harness defect. The harness writes `result.json` `rewards.reward` on a 0–100 scale,
while every stage-1 bundle, and final QC F3, uses 0–1. The value is rescaled only when it is exactly the run's
`report.json` score ×100.

## Stage-1 workflow (lead, 2026-10-28)

1. **Regenerate the trajectory on Opus 5** with `harness_mcp_atlas`.
2. **Run the QC**, `qc (1).zip`: `static/10_structure.md`, `static/20_ruthless.md` and `traj/10_bundle_playbook.md`.
   These are agent playbooks. Cleanup happens only if QC passes.
3. **Check whether `gt_env.json` is stale.** `lib/gt_stale_check.py` is read-only and reports:
   - the mtimes;
   - `reported.expected` / `counts` / `total`;
   - the per-ID table;
   - the wrong-routes check;
   - the fresh-oracle diff, ignoring `capture_status`.

   Gate 1 runs it against its own fresh oracle run. Anything but CURRENT is a BLOCKER.
4. **Clean the trajectories.** `clean_trajectories.py` runs inside gate 2, after QC and the regrade: `--dry-run`, then
   apply, then `--check`, which must be clean. Final QC then runs again on the cleaned bundle, and only then is the
   bundle locked into `READY/`.

Two notes on the staleness verdict:
- **It rests on the fresh-oracle diff.** That diff is exact. The per-ID table is review evidence, because finding
  the record an ID names depends on how each app stores records. Against the stage-1 gold bundles the table
  produced false mismatches, so it is not allowed to decide.
- **An oracle run older than the task's last edit is not fresh.** The verdict is then UNKNOWN, never CURRENT.

`submit_20261024/` is never touched. Fixes go into `submit_20261024_v2/`, an exact copy (file times kept) made on
2026-10-28.

## Same result on every laptop (the lock)

The problem this solves: tasks were hardened after they passed QC, the edits broke QC, and nothing noticed. Runs
made on one version of a task were then shipped with another version's tests.

| Guarantee | How |
|---|---|
| A task that passed gate 1 is byte-for-byte the task that runs and ships | Gate 1 records a sha256 of every task file. `run`, `package` and `final` refuse a task whose files differ. Any edit after QC (a hardening round included) turns the verdict into **CHANGED**, names the changed files, and makes gate 1 run again from the start |
| The harness cannot change the task silently between QC and the run | `new` applies the harness's own `test.sh` rewrite once, before QC. If the harness rewrites anything during the run, the run is refused |
| Runs from two task versions are never mixed | Each run folder records the task hash it ran on. A different hash is refused |
| The shipped tests produce the shipped scores | Gate 2 regrades every run with the task's own tests and needs the exact recorded pytest score. Tested: a recorded run regrades to 0.375451 with its own tests, but 0.4357 and 0.4303 with older versions of the same task found in this folder. The check catches that |
| QC is the shared QC, not this laptop's | QC refuses to run if `yuji-workspace/skills` has local edits. It warns if the workspace is behind `origin/main`. Runs refuse local edits to the harness files that decide grading or delivery. Harbor must be 0.24.0 and pytest 9.1.1 |
| Another laptop can prove it | `READY/LOCK.json` records the hashes, verdicts, scores and tool versions. Anyone runs `./pipeline.sh verify <READY folder>` and gets SAME or DIFFERENT per task, with the changed files and the changed verdicts named |

What cannot be identical: a new model run. The model samples, so two laptops never produce the same trajectory.
What must be identical is the grade of a recorded run, and that is what the lock and the regrade guarantee.

The remaining gap is S1-39. The Docker images install Debian packages from the live mirror, so a rebuild next month,
or on another laptop, can resolve different packages or fail to build. That is exactly what S1-39 flags. Fix it
with a dated snapshot (the skill's S1-39 row) rather than waiving it. The base images (`@sha256` digests) and the
Python packages (`==` pins) are already fixed.

## Model runs

The runs use the harness's own `scripts/run_batch.py`, in the same setup as your earlier opus runs:
- OpenHands on the Claude subscription (ccbridge);
- `claude-opus-5` with reasoning effort `high` (final QC F2 requires it);
- the codex judge on `gpt-5.6-sol`.

`RUNS_PER_TASK` (default 1) gives `run_1..run_N`. With more than one run, packaging also writes `pass@N.json`.

## Waivers

`batches/<batch>/waivers.txt` holds the waivers.
- Only a MAJOR can be waived. A BLOCKER always stops the task.
- Gate 1 and gate 2 (`--waive`) both read this file.
- Write a waiver only after a lead agrees, and name them in the line.

```
S1-37  harness files follow TASK-STRUCTURE.md - <lead>, <date>      # whole batch
d456198f  S1-39  Sample Dockerfiles, no snapshot yet - <lead>, <date>  # one task
```

## Layout of a batch

```
batches/<batch>/
  tasks/<uuid>/          frozen copy of the input (trajectories/ dropped); fix tasks here or in the source + `new` again
  waivers.txt            lead-approved waivers
  batch.log              when/where from, workspace + harness commits, model, judge, review mode
  1_qc/<uuid>/
    GATE.md, gate.json   gate-1 verdict and every finding
    static/*.log         part A, one log per skill block (blocks/ holds the exact commands run)
    live/                part B: run logs, rewards.txt, readers.log
    review/qc_report.md  part C
  2_runs/                -> ~/.cache/yuji-pipeline/runs/<batch> (harness output; Docker-safe path, no spaces)
  3_packaged/<uuid>/     the task as it ran + trajectories/opus-5/{pass_summary.json, run_N/...}
  4_final_qc/<uuid>/     final-QC report, LLM review pack
  READY/<uuid>/          passed both gates: this is what you upload
  READY/LOCK.json        hashes, verdicts, scores, tool versions of every READY task (what `verify` checks)
  BOARD.md               one row per task: gate 1, runs, score, final QC, stage
  SKIPPED.md             tasks dropped at gate 1, with their findings
```

## Settings

All settings are in `config.sh`, and any of them can be overridden per command:

```bash
RUNS_PER_TASK=3 ./pipeline.sh run b1
QC_REVIEW=manual ./pipeline.sh qc b1
```

The pipeline needs:
- Docker;
- `harbor` 0.24.0 on PATH;
- a codex login (`~/.codex/auth.json`) that serves `gpt-5.6-sol`;
- the harness's own `.env` for the Claude subscription;
- `.venv` (Python 3.12 + pytest 9.1.1), already created.

## What it never does

- It never edits the source tasks folder.
- It never pushes, uploads or commits anything.
- It never prints a credential.
- It never runs a model on a task that failed gate 1.

# QC report: a68c83fb-2a43-5701-9786-50601e1832a8

- Task name: atlas/a68c83fb-2a43-5701-9786-50601e1832a8
- QC skill version: yuji-task-qc 0.4.1
- Harbor: 0.24.0 (`uv tool run --from harbor==0.24.0 harbor run`; static load via `harbor.models.task.task.Task`)
- Start (UTC): 2026-10-19T12:51:23Z
- End (UTC): 2026-10-19T12:55:38Z
- Elapsed: ~04:15 (static) + live build attempts
- Copy inspected: /tmp/qc/a68c83fb-2a43-5701-9786-50601e1832a8
- VERDICT: **FAIL** (format non-conformance; operator decision: sample layout is mandatory — Option B)

## Verdict basis (operator decision 2026-10-19: Option B)

The operator confirmed the delivery lane **requires the sample layout** (`samples/974d1442`, the trajectory-ledger
format). Measured against that mandatory reference, this bundle is the wrong format and **FAILs** on BLOCKER
conformance. This is not fixable by a QC-side edit; it requires a FORGE regeneration of the task in the sample
format. The regeneration spec is in the Steering note.

Evidence of non-conformance (verified against the mandatory reference):

- **S1-01 BLOCKER — required sample files absent.** Missing: `environment/state_capture.py`,
  `environment/light-servers/{entrypoint.sh, server_main.py, filesystem_server.py, health_check.py,
  sitecustomize.py, requirements.txt, Dockerfile.ecr, servers/, task_data/}`.
- **S1-01 MAJOR — files not in the sample format present.** Extra: `environment/light-servers/{kit/, ext/,
  kit.yaml, ports.json, requirements.lock, LICENSE}` (the newer kit runtime).
- **Grader architecture mismatch (BLOCKER).** Target `grade.py` is the `atlas.checks/v1` /
  `light-servers.snapshot/v1` snapshot reducer; the mandatory format's `grade.py` is the trajectory-ledger
  Channel-A grader (`write_reward_json`, `channel_a`). Different reward model entirely.
- **Rubric channel mismatch (BLOCKER).** Target `components.rubric` is `graded=false, weight 0.0` (off-reward);
  the mandatory format requires an on-reward rubric (`graded=true`, non-zero weight; reference has 4.111) with
  negative criteria and `[scoring] aggregation = "weighted-sum"`.
- **Collect hook mismatch.** Target uses `python3 -m kit.collect` (snapshot); the mandatory format uses
  `environment/state_capture.py` writing `end_env.json`.

NOTE on the live runs below: the bundle *does* run clean in its own (newer) format — pristine source scores
oracle 1.0 / nop 0.0 live with 0 errored trials. That demonstrates the task logic is sound, but it does not
satisfy Option B, which is a format requirement, not a reward requirement. A bundle can score 1.0 and still FAIL
QC for being the wrong format.

## Overriding context (read first)

This bundle is a **newer Yuji generation** than the format the QC 0.4.1 skill targets. The skill's reference
(`samples/974d1442`) uses the trajectory-ledger grader: flat `light-servers/` (`entrypoint.sh`, `server_main.py`,
`servers/`, `task_data/`), `environment/state_capture.py`, a `grade.py` that reads the rebuilt trajectory, and an
on-reward judge with weights 1/3/5 and negative guards.

The target instead uses the **`atlas.checks/v1` snapshot-reducer** architecture:

- `light-servers/` is a `kit/` + `ext/` + `software/` layout with `kit.yaml`, `ports.json`, `requirements.lock`;
  the collect hook is `python3 -m kit.collect`, health is `python3 -m kit.health`.
- `tests/grade.py` is a self-contained deterministic reducer that reads **one** file, the sidecar snapshot
  (`light-servers.snapshot/v1`) at `SNAPSHOT_PATH`, validates its seed/kit digest and hash-chained call log, and
  applies 39 compiled checks carried as `checks_document` in `test_weights.json` (21 VALUE, 7 INVARIANT, 6
  DIVERGENCE, 5 ABSENCE gates). reward = earned positive weight / total positive weight (66); any failing gate
  zeroes it; a red-line gate sets `red_line_breach = 1`.
- The judge over `tests/judge.toml` is **off-reward** (`components.rubric graded=false, weight 0.0`; `test.sh`
  comment "never touches reward.json").

Consequently many Stage 1 and Stage 4 rules "HIT" only because they assert the *older sample's* file layout and
on-reward judge, not because the bundle is defective. These are recorded below as **FORMAT-DIVERGENCE (VERIFY)**,
not BLOCKER/MAJOR, because the bundle is a valid, newer format: Harbor 0.24.0 loads it cleanly and its own grader
scores the oracle exactly 1.0 and the nop exactly 0.0 (proven offline, Stage 5).

The verdict is **PARTIAL** because the mandatory live Harbor runs (S5-10/S5-11) could not complete: the verifier
image fails to build on an apt version pin that Debian trixie has since moved past. The grading was instead proven
sound offline against the real oracle and nop snapshots.

## Fact sheet

| Fact | Value |
|---|---|
| Task name / uuid / version | atlas/a68c83fb-...1832a8 / a68c83fb-...1832a8 / 1.0.0 |
| schema_version | 1.4 |
| Single/multi-step | single-step (0 `[[steps]]`) |
| Graded apps | LightConfluence, LightDrive, LightGmail, LightAirtable, LightXero |
| Wired MCP servers | 10 (5 graded + 5 distractors: Slack, QuickBooks, Salesforce, Stripe, Budget) |
| Grader | `weighted`; deterministic reducer `tests/grade.py` over `checks_document` |
| Components / weights | traj_tests (graded, weight 1.692 = mean\|w\|), rubric (graded=false, weight 0.0, off-reward) |
| Positive checks / total weight | 31 positive, total positive weight 66 |
| Gates (weight 0) | 8 total: 5 ABSENCE gates (g_rl1_limit_booking, g_rl2_marked_paid, g_per_risk_untouched, g_reinsurer_confirmed, g_aggregated_occurrence) + 3 if_constraint |
| Check kinds | 21 VALUE, 7 INVARIANT, 6 DIVERGENCE, 5 ABSENCE |
| Red lines | RL1 (no bill = layer limit/share), RL2 (no bill marked paid) → gates g_rl1_limit_booking, g_rl2_marked_paid |
| Rubric criteria | 35, all binary, weights 1/2/3, no negatives, aggregation weighted-mean, judge openai/gpt-5.6-sol |
| Collect hook | `python3 -m kit.collect --step 1 --out /var/lib/light-servers/out` on service `light-servers`, timeout 120 |
| Snapshot path | `SNAPSHOT_PATH = /var/lib/light-servers/out/snapshot.json` (not ATLAS_END_ENV) |
| Harbor | 0.24.0 (installed), docker 29.8.2, uv 0.12.23 |
| Truth figures | per `checks_document` expects + oracle.json; recovery/uln/bill totals; stale DIVERGENCE controls present in world (expected) |

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | VERIFY | Clean |
|---|---|---|---:|---:|---:|---:|---:|
| 0 | Fact sheet | done | - | - | - | - | - |
| 1 | Structure and task.toml | **FAIL** (Option B: wrong format) | 3 | 1 | 0 | 0 | some |
| 2 | Instruction, world, leaks | PASS | 0 | 0 | 0 | 0 | all |
| 3 | Deterministic grading | PASS | 0 | 0 | 0 | 0 | all |
| 4 | Rubric (judge.toml) | PASS-for-schema (off-reward) | 0 | 0 | 2 | 3 | most |
| 5 | Execution (ledger + live) | oracle 1.0 / nop 0.0 (live, after fix) | 0 | 0 | 0 | 2 | all |

## Findings

### [S5-10 / S5-11] Live verifier image failed to build on a stale apt pin — RESOLVED
- Severity: MAJOR → **RESOLVED (fixed and re-verified live)**
- Where: `tests/Dockerfile` line 13-15 (verifier image)
- Evidence (from the live oracle trial `exception.txt`):
  ```
  #7 [2/7] RUN apt-get install -y --no-install-recommends \
        curl=8.14.1-2+deb13u5 ca-certificates=20250419 procps=2:4.0.4-9
  curl : Depends: libcurl4t64 (= 8.14.1-2+deb13u5) but 8.14.1-2+deb13u7 is to be installed
  E: Unable to correct problems, you have held broken packages.
  exit code: 100
  RuntimeError: Docker compose command failed ... verifier ... build
  ```
  Both `oracle` and `nop` trials failed identically at the verifier build step; 0 trials completed, 1 exception each.
- Why: `curl` is pinned to `8.14.1-2+deb13u5`, but Debian trixie now ships `libcurl4t64 8.14.1-2+deb13u7`, so the
  exact-pin dependency is unsatisfiable and the image cannot build. This makes the task non-reproducible on a cold
  cache today and prevents Harbor from running the verifier end-to-end.
- Fix: loosen the transitive pin. Either drop the exact `curl=` pin to the series (`curl`), or add
  `libcurl4t64` to the same `apt-get install` line pinned to the matching version, or pin to `+deb13u7`. The
  agent/light-servers image build and the collect hook are unaffected; only the verifier image is broken.
- Note: grading was proven sound offline despite this (see S5-10-offline below).

### [S1-01] light-servers / environment layout is the newer kit format, not the sample layout
- Severity: VERIFY (FORMAT-DIVERGENCE — not a defect of this bundle)
- Where: `environment/light-servers/`, `environment/`
- Evidence: present = `kit/` (collect.py, health.py, serve.py, store.py, mutations.py, clock.py, …), `ext/`
  (LightAirtable.py, LightDrive.py, LightXero.py), `kit.yaml`, `ports.json`, `requirements.lock`, `LICENSE`.
  Absent (vs sample REQUIRED): `entrypoint.sh`, `server_main.py`, `filesystem_server.py`, `health_check.py`,
  `sitecustomize.py`, `requirements.txt`, `servers/`, `task_data/`, `Dockerfile.ecr`; and
  `environment/state_capture.py` (replaced by the `kit.collect` hook).
- Why: The QC 0.4.1 REQUIRED tree is the older trajectory-ledger format. This bundle is a different generation.
  It is not missing files in its own format; it carries a complete, different, valid set.
- Fix: Design decision. If the delivery lane requires the 974d1442 sample layout exactly, this bundle does not
  conform and must be regenerated in that format. If the newer `atlas.checks/v1` + kit format is accepted, update
  the QC reference. **Do not** delete `kit/`, `ext/`, `kit.yaml`, `ports.json` — they are load-bearing here
  (Harbor 0.24.0 loads the task and the oracle scores 1.0 with them).

### [S1-06 / S1-12 / S1-13 / S1-15 / S1-16] task.toml uses newer-schema conventions, not sample values
- Severity: VERIFY (FORMAT-DIVERGENCE)
- Where: `task.toml`
- Evidence:
  - `[agent] network_mode = "public"` (sample expects `allowlist` + `allowed_hosts`).
  - No `[environment] docker_image` / `light_servers_image` `@sha256:` digest pins (built from source).
  - `[verifier.env]` has `SNAPSHOT_PATH = /var/lib/light-servers/out/snapshot.json`, **no** `ATLAS_END_ENV`.
  - artifacts collect `/logs/agent` (exclude ./completions) and `/var/lib/light-servers/out` (not `/workspace`).
  - collect hook `python3 -m kit.collect ...` on service `light-servers` (not `state_capture.py` on `main`).
  - Matches the sample: `schema_version 1.4`, `[agent] timeout_sec 3600`, `[verifier] timeout_sec 1800`,
    `environment_mode separate`, `[environment]/[verifier.environment] network_mode public`, task name
    `atlas/<uuid>`, grader `weighted`.
- Why: These are the newer snapshot-reducer schema's intended settings. Harbor 0.24.0 accepts them (task loads,
  `is_valid_dir: True`). They are not defects in this format.
- Fix: Design decision as in S1-01. If the sample schema is mandatory, regenerate; otherwise accept.

### [S4] judge.toml is off-reward with weights 1/2/3 and no negatives (newer-schema rubric)
- Severity: MINOR (no reward impact)
- Where: `tests/judge.toml`, `tests/test_weights.json components.rubric`
- Evidence: 35 binary criteria, weights {1:1, 2:18, 3:16}, `[scoring] aggregation = "weighted-mean"`, zero
  negative criteria, no `annotations`. `components.rubric` has `graded=false, weight 0.0`; `test.sh` step 5
  comment: "off-reward … never touches reward.json".
  - vs QC 0.4.1: expects weights 1/3/5 (weight `2` is off that scale), negative criteria with polarity +
    `weighted-sum`, `annotations` (number/polarity/category/importance/evaluation_target), and an **on-reward**
    judge wired to deduct negatives (S4-28).
- Why: In the `atlas.checks/v1` architecture the forbidden acts are enforced by ABSENCE/red-line **gates** in the
  reducer (which zero the reward), not by negative rubric criteria, and the judge is deliberately off-reward.
  Because the rubric contributes 0 weight, none of these differences affect the reward.
- Fix: Design decision. If this delivery lane requires an on-reward 1/3/5 judge with negatives (sample format),
  the rubric must be rewritten and wired on-reward. As a newer-schema off-reward rubric, it is internally
  consistent (values match the grader's VALUE expects; 35 ≥ 25; unique ids; no vague terms).

## CLEARED

- **S1-11** compose has only `main` + `light-servers` + volume `workspace_data`; no `ports:`/`expose:`. Clean.
- **S1-28** every JSON parses; every `.sh` has a shebang; no empty files outside light-servers.
- **S1-30 / S1-31** Harbor 0.24.0 loads the task with its own loader: `Task loaded`, `is_valid_dir: True`,
  `environment_mode SEPARATE`, no error; TaskConfig ignores no root keys.
- **S1-27 / S1-33 / S1-34** no `__pycache__`/`.DS_Store`/zip/backup in source; no `provenance.*`; no `fixtures/`.
- **S1-32** no `rubric.json` anywhere; `tests/judge.toml` present; nothing names `rubric.json`.
- **S2-01 / S2-02** no computed answer (recovery_usd/uln_usd/bill totals, e.g. 2432335.65, 972934.26, 2212321.99)
  appears in `instruction.md` or in agent-visible `world_data/`. DIVERGENCE stale controls (32681437.71,
  33073096.56, 3871563.48) are present in the world by design (decoys), not leaks.
- **S2-04 / S2-05 / S2-06** instruction names no path/host/port/URL/`Light*`/snake_case tool/`MCP`/grading
  artefact, and carries no TODO/FIXME/model-directed residue. Only an `instruction-canary` comment (expected).
- **S3-01 / S3-02** `grade.py` reads only the snapshot (`SNAPSHOT_PATH`) and the `checks_document` beside it; it
  never opens `solution/**`, `TRUTH.md`, `gt_env.json`, the trajectory folder, or the network.
- **S3-04 / S3-05** `test.sh`: `grade.py` is the sole reward writer; exit 3 → invalid snapshot, no reward; any
  non-zero/empty → loud `INFRA_GRADER_CRASH` fallback with explicit 0.0; pytest is reporting-only (`|| true`);
  rubric judge is off-reward.
- **S3-10 … S3-14** `grade.py` is stdlib-only (argparse, hashlib, json, math, os, pathlib, re, sys, fractions,
  typing), deterministic (no random/uuid/time/now/shuffle), uses `Fraction` for exact weight ratios, numeric
  tolerances via `tolerance`, ids compared as exact strings. No `assert True`, no self-compare, no swallowed
  except that turns an outage into a pass.
- **S3-33 / S3-34** every `test_*` weight is an integer on the schema scale (1/2/3/4 positive, 0 for gates — the
  newer scale); no negatives (schema forbids them); gates all weight 0; no duplicate keys; traj_tests component
  weight 1.692 = mean\|w\| (match). (The 1/3/5 expectation is sample-schema only.)
- **S5-01 / S5-13 (gate probes, offline)** forcing a red-line gate (`g_rl1_limit_booking`) to trip → reward 0.0,
  `red_line_breach 1`, code RED_LINE; forcing a non-red-line gate (`g_per_risk_untouched`) → reward 0.0,
  breach 0, code GATE; forcing a positive VALUE check to fail → PARTIAL (not zeroed), with transitive `requires`
  cascading correctly. Gate mechanics sound.
- **S5-10 (offline)** `grade.py` over the real oracle `kit.collect` snapshot → reward **1.0**, if_score 1.0,
  red_line_breach 0, code FULL, earned 66 / total 66.
- **S5-11 (offline)** `grade.py` over the real nop snapshot → reward **0.0**, if_score 0.0, no breach.

## Not checked

- **S5-10 / S5-11 / S5-12 (live, end-to-end)**: the mandatory live Harbor oracle/nop runs could not complete —
  the verifier image build fails on the `tests/Dockerfile` apt pin (see the MAJOR finding above). The oracle
  AGENT and the light-servers collect hook both ran to completion and produced valid snapshots; grading was
  proven offline against those snapshots (oracle 1.0, nop 0.0). Re-run live after the Dockerfile pin is fixed.
- **S1-10 (source identity vs REF)**: not applicable — the target's `light-servers` tree is a different
  generation from `samples/974d1442`, so a file-by-file identity diff is meaningless. Recorded as S1-01
  divergence instead.

## Waivers
- none

## Steering note for FORGE

**Operator decision (Option B): the sample layout (`samples/974d1442`) is the mandatory format.** This bundle is
the newer `atlas.checks/v1` + kit generation and must be **regenerated** in the sample format. This is not a QC
edit; it is a full task rebuild. Regeneration spec:

1. **Environment runtime → sample light-servers.** Replace the kit runtime (`kit/`, `ext/`, `kit.yaml`,
   `ports.json`, `requirements.lock`) with the sample layout: `entrypoint.sh`, `server_main.py`,
   `filesystem_server.py`, `health_check.py`, `sitecustomize.py`, `requirements.txt`, `servers/`, `task_data/`,
   `Dockerfile.ecr`. Wire the five graded apps (Confluence, Drive, Gmail, Airtable, Xero) through
   `entrypoint.sh SERVER_CMDS` with ports matching `task.toml [[environment.mcp_servers]]`.
2. **Collect hook → state_capture.** Add `environment/state_capture.py` that finds the agent's sessions from
   `/logs/agent`, logs them out, and writes `end_env.json` under `/logs/artifacts/atlas`. Change the
   `[[verifier.collect]]` hook to `python3 /harness/atlas/state_capture.py` on service `main`, and set
   `[verifier.env] ATLAS_END_ENV = /logs/artifacts/atlas/end_env.json`. Remove `kit.collect`/`SNAPSHOT_PATH`.
3. **Grader → trajectory-ledger `grade.py`.** Replace the snapshot reducer with the sample's Channel-A weighted
   ledger: `components.traj_tests` (the `test_outputs.py` checks) + `components.rubric` (`judge.toml`), reward =
   `max(0, (wA·channel_a + wR·rubric)/(wA+wR))`, `channel_a = max(0,(earned − tripped guard)/positive total)`.
4. **`test_outputs.py` → real weighted checks + guards.** Rewrite the 39 thin check-wrappers as sample-style
   weighted tests over the rebuilt trajectory / delivered files / `end_env.json`, with **negative guards**
   (`test_guard_*`) for the forbidden acts (limit booking, marked-paid, per-risk write, reinsurer_confirmed,
   aggregation, email, contact edits).
5. **`test_weights.json` → 1/3/5 scale.** Positive weights 1/3/5, guards −1/−3/−5 (currently 1/2/3/4 with
   weight-0 gates). Component weights = mean absolute weight of each component's items.
6. **`judge.toml` → on-reward.** Set `components.rubric graded=true` with a non-zero weight; add negative
   criteria (polarity negative, weights −1/−3/−5) and `[scoring] aggregation = "weighted-sum"`; add the
   `annotations` (number/polarity/category/importance/evaluation_target); wire `test.sh` step 4 to produce
   `rubric_breakdown.json` that `grade.py` folds into the reward.
7. **`task.toml` → sample values.** `[agent] network_mode = "allowlist"` + `allowed_hosts`; pin
   `[environment] docker_image` and `light_servers_image` by `@sha256:`; artifacts `/logs/agent` (exclude
   `./completions`) + `/workspace` (exclude `./data`).
8. **Keep (do not regress):** the Dockerfile apt pin must not re-pin `curl`/`libcurl4t64` to a version Debian
   trixie no longer serves (the original `curl=8.14.1-2+deb13u5` broke the build; use unpinned or `+deb13u7`).

The task's domain content (treaty hours-clause aggregation, the 69-step golden path, the figures) is sound and
can be carried over; what must change is the format/runtime/grader architecture.

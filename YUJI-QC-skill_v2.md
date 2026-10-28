---
name: yuji-task-qc
description: Use this skill when a tasker wants an author-side quality check of ONE Yuji light-servers task bundle before that bundle is sent on. The bundle must have the format of yuji/samples/974d1442-244d-5164-b5da-a7a594100aa4 with tests/rubric.json replaced by tests/judge.toml; fixtures and provenance files are flagged for removal and the trajectories/ folder is never checked. It works on a copy under /tmp/qc and checks: the task itself (instruction, world and task data, grading soundness, bundle format), Harbor 0.24.0 compatibility, reward leakage, executability (grader probes, live oracle exactly 1.0, nop exactly 0.0) and strict rubric compliance of tests/judge.toml (at least 20 criteria, harbor-rewardkit schema, weights 1/3/5 and -1/-3/-5, atomic, decidable, grounded, evaluable). It proves negatives are deducted in test_weights.json and in the rubric score. It writes one qc_report.md with a PASS, FAIL or PARTIAL verdict and a steering note. Do not use it to measure difficulty, to QC model output bundles, or as a pipeline gate.
---

# Yuji task QC (0.4.1)

QC skill version: `yuji-task-qc 0.4.1`. Write this string into every report.

## 1. Purpose and status

This is author-side feedback. A tasker runs it with a coding agent on one bundle before the bundle is sent on. It includes live Harbor oracle and nop runs, so it takes longer than the old 20-minute pass (see section 4).

What it is not:

- It is not evidence of difficulty. Nothing here measures how hard the task is.
- It is never a gate. No pipeline step may read its output as a pass condition.

How findings are used. The operator reads the report and relays the "Steering note for FORGE" section to the active FORGE run as plain design instructions. The QC agent never talks to FORGE and never edits the bundle.

Scope. This QC checks only: (1) the task itself: instruction, world and task data, grading soundness, and the bundle format of section 2e; (2) Harbor 0.24.0 compatibility; (3) reward leakage; (4) task executability (grader probes, live oracle 1.0, nop 0.0); (5) rubric compliance of `tests/judge.toml`, the most important and the strictest part. Checks that only a Trinity tool, contract or seal step owned (formerly Scope `T-code` / `T-contract`) were removed in 0.2.0; their IDs are listed in section 13 and are not reused. IDs are not renumbered.

**The format (user decision 2026-10-19).** A bundle must have the format of the yuji samples
(`yuji/samples/974d1442-244d-5164-b5da-a7a594100aa4`; `92024c97-...` and `bd42b923-...` are identical in
layout), with ONE change: `tests/rubric.json` is replaced by `tests/judge.toml`. Section 2e is that format.
Where an older rule in this skill (the Std §10 constants, off-reward judge, state-only reward, exit-3 invalid
trials) contradicts the sample, the sample wins and the rule has been rewritten to match it.

Out of scope (user decisions 2026-10-19):

- **Fixtures.** The format has no `tests/fixtures/`. A bundle that ships one is flagged: remove it (S1-34, MAJOR). The fixture checks S5-03, S5-04 and S5-08 are retired.
- **Provenance.** The format has no `provenance.yaml` / `provenance.sig`. Present = flagged: remove them (S1-33, MAJOR).
- **The `trajectories/` folder.** Probe-run output is never opened, scanned or judged. It is left out of every `find` and `grep` in this skill and is never a finding. (This is the folder only: the format's grader reads the run's trajectory by design, see 2b.)
- **grounding.yaml.** The format has no `solution/grounding.yaml`. Where a check below says to read grounding.yaml, read `solution/TRUTH.md`, `task.toml [task.metadata]` (`decoy_records`, `stump_levers`, `grading`), `tests/oracle.json` and `tests/test_outputs.py` instead.

Sources folded in (cited in the "from" column of every catalog):

| Tag | Source |
|---|---|
| Sample | the format reference `yuji/samples/974d1442-244d-5164-b5da-a7a594100aa4` (same layout as `92024c97`, `bd42b923`) |
| Std §n | `Task-structure-standard.md` (section 10 is the checklist); the Sample wins where they disagree |
| FORGE n | `trinity/forge/phase-build.md` items 8, 9, 10, 10a, 10e, 10f, 11, 11a |
| v4 Sn-X | `Updated_QC_MCP_v4` pack, stage n, code X |
| RUTHLESS n | `RUTHLESS_QC.md` section n |
| Checklist X | `QC_CHECKLIST_pytest_rubric.md` code X |
| tabish X | tabish `QC/qc.md` code X |
| qc2 §n | `qc (2).md` (output-bundle QC; mostly dropped, see section 13) |

Where the Sample and an older source disagree, the Sample wins. Where the Sample is silent, the standard wins; where both are silent and FORGE speaks, FORGE wins. Anything still unclear is marked VERIFY and goes to the maintainers.

## 2. What changed from the older QC packs

Read this before the catalog. These adaptations are deliberate.

### 2a. The reward: a weighted ledger of two components

The format's `tests/grade.py` computes the reward from `tests/test_weights.json`:

- **`components.traj_tests`** (Channel A): the pytest checks in `tests/test_outputs.py`, each weighted 1, 3 or 5
  (goals) or -1, -3 or -5 (guards). `channel_a = max(0, (earned positive weight - tripped guard weight) / total
  positive weight)`. The component `weight` is the mean absolute test weight,
  rounded to 2 or 3 places and within 0.006 of the true mean (S3-34; the Sample has 3.41 for 3.412).
- **`components.rubric`**: `file = "judge.toml"`; the judge's verdicts become `/logs/verifier/rubric_breakdown.json`
  with `score = rc x (1 - rb)`, where `rc` = satisfied positive weight / positive total and `rb` = satisfied
  (i.e. committed) negative weight / negative total, both over absolute weights. The component `weight` is the
  mean absolute criterion weight, rounded the same way (S3-34; the Sample has 4.111).
- `reward = max(0, (wA x channel_a + wR x rubric) / (wA + wR))` over the components that produced a value. With no
  judge key, or a judge that returns no verdicts, there is no `rubric_breakdown.json`, the rubric is UNSCORED and
  dropped from both sums (reward = Channel A). It is never scored 0. `reward_producer.json` records which.
- `gate`, when present, zeroes the reward in three ways (`grade.py`). The samples carry no gate.
  - `require_no_guards` (a flag, not a list of names): any truthy value zeroes the reward when ANY guard trips.
  - `require_state_exact` (flag): zeroes the reward when `state_channel.json` reports `completion < 1` or
    `misbehave > 0`. `grade.py` writes that file itself from six names in `test_outputs.py` (`_OLD_ENV_PATH`,
    `_entities`, `_load_env`, `_s_available`, `_state_diff`, `_state_misbehaved`), plus `TARGET_ENTITIES`. The Sample retires the state channel, so the file says
    `available: false` and the gate never fires: set without those helpers it is inert (S3-35).
  - `floor` (number): a reward below it becomes 0.
- **Negatives are deducted in both channels.** A tripped guard in `test_weights.json` subtracts its absolute
  weight (S3-32, proven by S5-13); a satisfied negative criterion in judge.toml raises `rb` and lowers the rubric
  score (S4-28). A negative that is never subtracted, or whose weight lookup defaults to 0, rewards the
  forbidden act.

### 2b. What the reward may read

The format grades the run, not only the final state. `tests/test.sh` step 1 rebuilds a `{steps, final_message}`
trajectory from `/logs/agent` (ATIF `trajectory.json`, stream-json or OpenAI-shaped logs) into
`/tmp/agent_trajectory.json` and exports it as `ATLAS_TRAJECTORY`. The checks may read: that trajectory and its
final message, the files the run delivered under `/workspace` (collected by `[[artifacts]]`), the captured
snapshot (`ATLAS_END_ENV = /logs/artifacts/atlas/end_env.json`), `tests/old_env.json` and `tests/oracle.json`.
Grading the trajectory is by design and is never a finding. The reward must NOT read `solution/**`, `TRUTH.md`,
the `trajectories/` folder, or anything the agent can see that holds the answer.

### 2c. judge.toml replaces rubric.json

- The rubric is `tests/judge.toml` (harbor-rewardkit judge-TOML). A `rubric.json` anywhere in the bundle is a
  BLOCKER (S1-32). Criterion-quality checks that ran on `rubric.json` (v4 K, Q, J, C, P; Checklist K-P) run on
  judge.toml. The schema is read from the package source (section 9). The judge model is `gpt-5.6-sol`.
- The format's `tests/_judge/rubric_judge_cli.py` reads JSON only. So `test.sh` step 4 must feed
  `/tests/judge.toml` to a reader that parses TOML (harbor-rewardkit pinned in `tests/Dockerfile`, or an updated
  CLI) and write `rubric_breakdown.json` with the sample's shape (`score`, `rc`, `rb`, `per_criterion`). A
  `test.sh` that still passes `--rubric /tests/rubric.json` leaves the rubric silently unscored: BLOCKER (S4-16).
- Each criterion carries the old rubric.json fields as annotations: `number`, `polarity` (from `is_positive`),
  `category` (the old `type`), `importance`, `evaluation_target` (S4-21).
- **Weight scale.** Positive criteria weigh 1, 3 or 5. Negative criteria weigh -1, -3 or -5 with
  `annotations.polarity = "negative"` and `[scoring] aggregation = "weighted-sum"` (S4-24, S4-27). The same scale
  holds in `test_weights.json` (S3-33). Fewer than 20 `[[criterion]]` rows is a BLOCKER, 20-24 MINOR, 25+ passes.
- The rubric is ON the reward (2a). The judge never writes `reward.json`; only `grade.py` does.

### 2d. task.toml follows the Sample, not the Std §10 constants

The values checked in Stage 1 are the Sample's: `schema_version = "1.4"`; `[agent] timeout_sec = 3600`,
`network_mode = "allowlist"` with `allowed_hosts`; `[verifier] environment_mode = "separate"`, `timeout_sec = 1800`;
`[verifier.environment] network_mode = "public"`; `[environment]` pins `docker_image` and `light_servers_image` by
`@sha256:` digest; artifacts `/logs/agent` (exclude `./completions`) and `/workspace` (exclude `./data`); collect hook
`python3 /harness/atlas/state_capture.py`. The v4 constants (agent timeout 86400, verifier 300, empty
`ENABLED_SERVERS`, a 15/14 server floor, 20 attachments) are not used.

### 2e. Bundle format (the structure every bundle is checked against)

```
<uuid>/
  task.toml
  instruction.md
  environment/
    Dockerfile  docker-compose.yaml  state_capture.py
    light-servers/   Dockerfile Dockerfile.ecr entrypoint.sh filesystem_server.py health_check.py
                     requirements.txt server_main.py sitecustomize.py
                     servers/ software/ task_data/ world_data/
  tests/
    .dockerignore  Dockerfile  Dockerfile.ecr  docker-compose.yaml
    _judge/rubric_judge_cli.py   judge CLI shipped with the format (reads JSON only; see 2c)
    claims_lib.py                shared claim helpers for test_outputs.py
    ctrf_pytest_plugin.py        pytest -> ctrf.json report
    test.sh                      verifier entrypoint, sole writer of reward.json
    test_outputs.py              the weighted pytest checks (goals and guards)
    test_weights.json            components traj_tests + rubric, weights 1/3/5 and -1/-3/-5
    grade.py                     the weighted ledger
    old_env.json  oracle.json    seed snapshot; oracle calls and reported figures
    judge.toml                   the rubric (IN PLACE OF rubric.json)
  solution/
    TRUTH.md  gt_env.json  solve.py  solve.sh
  trajectories/                  probe runs: allowed, NEVER checked
```

- Every file above is required. A missing one is a BLOCKER (S1-01).
- We do not use `rubric.json`. Any `rubric.json` is a BLOCKER (S1-32), with the fix depending on what else is there:
  - `rubric.json` and no `judge.toml`: make `tests/judge.toml` from it (recipe under S1-32), then delete `rubric.json`.
  - `rubric.json` and `judge.toml` both present: delete `rubric.json`.
  - neither: write `tests/judge.toml`.
- `tests/fixtures/` present: MAJOR, remove it (S1-34). `provenance.yaml` / `provenance.sig` present: MAJOR, remove them (S1-33).
- Any other file not in the tree (`grounding.yaml`, `recompute.py`, `policy.yaml`, `GRADING.md`, `gradelib.py`,
  `reward.toml`, `requirements.lock`, `environment/Dockerfile.ecr`, notes): MAJOR, not part of the format, remove it
  (S1-01). A waiver may keep one if the operator records why.

## 3. Hard rules

1. **Run from outside YUJI, on a copy.** Start the agent session in a directory outside the YUJI parent repo. Copy the bundle first: `mkdir -p /tmp/qc && cp -R <bundle> /tmp/qc/<uuid>`. Work only on the copy. Reason: YUJI's feedback-capture plugin would pull a QC session started inside the repo into the active FORGE run's feedback chain and break it.
2. **Never read CRUCIBLE or audit output.** Do not open `.audit/`, any `VERDICT.md`, any CRUCIBLE result, anything under `.trinity/runtime` or `.trinity/secrets`, private keys, `~/.config/yuji/cc_oauth_token`, or any `.env` file.
3. **Never edit the source.** Write only under `/tmp/qc/` (exception: the Harbor jobs dir, see Stage 5, when the Docker VM cannot see `/tmp`). Never write in the source bundle or anywhere in YUJI. The report goes in `/tmp/qc/<uuid>-report/qc_report.md`; scratch files (`env.sh`, `truth.txt`, replay output, recompute output, the `$B.re` copy) also stay under `/tmp/qc/`.
4. **Never run Trinity machinery, model agents or proxies.** No Trinity tools, no git writes, no ccbridge or OAuth proxy. Harbor runs use only the `oracle` and `nop` agents, which need no model; unset `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` (and the judge keys) in their environment.
5. **Never print secrets.** Do not echo `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, OAuth tokens, or the contents of any env file. Grep for key names, never values.
6. **No judge API calls.** Judge keys stay unset, so the live verifier leaves the rubric UNSCORED (no `rubric_breakdown.json`, `reward_producer.json` says `channel_a_only`) and the reward is Channel A alone. Stage 5 proves an unscored rubric is dropped, not scored 0.
7. **Do not invent CLI flags.** Anything marked "adjust to bundle" must be confirmed with `--help` first.
8. **Confirmed or not reported.** A suspicion you did not confirm against the files is not a finding. Put it under CLEARED or leave it out.
9. **Never check the trajectories folder.** Do not open, scan or grade anything under `trajectories/` (or `trajectory/`). Every `find`/`grep` below prunes it. Reading a trajectory the GRADER rebuilds from `/logs/agent` is part of the format and is not this.
10. **Grader path redirects live in `$B.re` only.** If `grade.py` or `test_outputs.py` hardcodes `/tests/...`, copy the bundle to `$B.re` and rewrite that literal there for the replay (Stage 5). Never edit `$B` and never create `/tests` on the host.

## 4. Time budget

| Stage | Subject | Minutes |
|---|---|---:|
| 0 | Setup, copy, fact sheet | 2 |
| 1 | Structure, task.toml, Harbor 0.24.0 static validation | 5 |
| 2 | Instruction, world data, leakage | 5 |
| 3 | Deterministic grading | 5 |
| 4 | Rubric compliance (judge.toml), strict | 8 |
| 5 | Execution: ledger probes (fast pre-check), then live Harbor oracle and nop | 20 |
| | **Total** | **45** |

The 20-minute target of 0.1.0 no longer holds: live oracle and nop runs are mandatory. Measured on slot 29
(2026-10-17, images already cached, 4-CPU colima VM): `harbor run` oracle 30-42 s and nop 28-40 s per run;
the whole QC pass took 27 minutes of wall time, including six live runs and the diagnosis of two live failures. A first
build without cached images can add 10-20 minutes; budget up to 60 minutes when Docker caches are cold.

Record the start time before Stage 0. If you reach the budget, stop. Report `PARTIAL` and list every check you
did not reach under "Not checked". Do not skip a BLOCKER-severity check to fit a MINOR one. Within a stage, do
BLOCKERs first. Start the live runs (Stage 5) in tmux right after Stage 0 and do Stages 1-4 while they run.

## 5. Stage 0: setup and fact sheet (2 min)

### 5.1 Setup

```bash
UUID=<bundle uuid>
SRC=<path to the bundle>                     # read-only source
mkdir -p /tmp/qc "/tmp/qc/$UUID-report"
cp -R "$SRC" "/tmp/qc/$UUID"
B="/tmp/qc/$UUID"
LS="$B/environment/light-servers"
# REF = the format reference sample, read-only. Set REF yourself, or it is found next to the bundle's yuji checkout
# or anywhere under $HOME (974d1442 first; 92024c97 and bd42b923 have the same light-servers tree).
if [ -z "${REF:-}" ]; then
  for d in "$(dirname "$SRC")"/../samples "$(dirname "$SRC")"/../yuji/samples; do
    REF=$(ls -d "$d"/974d1442-* 2>/dev/null | head -1); [ -n "$REF" ] && break
  done
  [ -n "$REF" ] || REF=$(find "$HOME" -maxdepth 6 -type d -path '*samples/974d1442-*' -prune 2>/dev/null | head -1)
fi
test -d "${REF:-/nonexistent}/environment/light-servers" || { echo "STOP: no yuji sample found; set REF to your copy of yuji/samples/974d1442-... and rerun"; exit 1; }
echo "REF=$REF"
# Each Bash call in Claude Code / opencode starts a fresh shell, so persist every variable.
cat > "/tmp/qc/$UUID-report/env.sh" <<EOF
UUID="$UUID"
SRC="$SRC"
B="/tmp/qc/$UUID"
LS="/tmp/qc/$UUID/environment/light-servers"
REF="$REF"
T="/tmp/qc/$UUID/tests"
O="/tmp/qc/$UUID-report/replay"
W="/tmp/qc/$UUID/tests/test_weights.json"
GT="/tmp/qc/$UUID/solution/gt_env.json"
export PYTHONDONTWRITEBYTECODE=1
EOF
source "/tmp/qc/$UUID-report/env.sh"
date -u +%Y-%m-%dT%H:%M:%SZ                  # start time
```

Every later command block starts with `source /tmp/qc/<uuid>-report/env.sh` (replace `<uuid>` with the real uuid). Run each block in one Bash call; do not split a block across calls.

Confirm `pwd` is not inside the YUJI tree before going on.

### 5.2 Fact sheet

Fill this in before any check. Every later check is judged against it. Put it at the top of the report.

| Fact | Where to read it | Value |
|---|---|---|
| Task name, uuid, version | `task.toml [task]` | |
| Single or multi-step | `instruction.md`, `task.toml` | |
| Light apps and ports | `task.toml [[environment.mcp_servers]]`, `entrypoint.sh` | |
| Graded apps vs distractors | `task.toml [task.metadata] apps` vs `mcp_servers` | |
| Session id(s) | `world_data/`, `environment/state_capture.py` | |
| Graded keys (calls, records, reported figures) | `test_outputs.py`, `tests/oracle.json` (`oracle`, `reported`) | |
| Components and weights (traj_tests, rubric), positive checks, guards, gate | `tests/test_weights.json` (S3-25 command) | |
| Guards (negative checks) and what each forbids | `test_outputs.py` docstrings, `test_weights.json` | |
| Red-lines (catastrophic acts) | `TRUTH.md`, `task.toml [task.metadata] trap` | |
| Rubric criterion count, positive / negative weight, weight scale | `tests/judge.toml` (Stage 4 command) | |
| Harbor version used | `harbor --version` (must be 0.24.0, see Stage 1) | |
| Decoys and wrong figures | `task.toml [task.metadata] decoy_records`, `TRUTH.md` | |
| Truth figures (every graded value) | `solution/TRUTH.md`, `tests/oracle.json reported` | |
| Grader env vars (end_env, old_env, output) | `grep environ tests/grade.py tests/test_outputs.py` | |

```bash
source /tmp/qc/<uuid>-report/env.sh
python3 -c "import tomllib,sys;d=tomllib.load(open(sys.argv[1],'rb'));print(d['task']);[print(s) for s in d['environment']['mcp_servers']]" "$B/task.toml"
python3 -c "import tomllib,sys;m=tomllib.load(open(sys.argv[1],'rb'))['task'].get('metadata',{});[print(k,'=',str(m.get(k))[:200]) for k in ('apps','mcp_servers','decoy_records','grader','components')]" "$B/task.toml"
ls "$B/tests" "$B/solution"
grep -nE 'environ' "$T/grade.py" "$T/test_outputs.py" | head -20
```

## 6. Stage 1: structure, task.toml, Harbor 0.24.0 (5 min)

Severity scale: BLOCKER (fails the bundle), MAJOR (fails unless waived), MINOR (note), VERIFY (ask maintainers, never blocks).

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S1-01 | Tree matches the section 2e format (the Sample with judge.toml for rubric.json): every listed file present (missing = BLOCKER); any file not in the tree is MAJOR, remove it. `trajectories/` is ignored. | BLOCKER | cmd S1-01 | Sample, section 2e |
| S1-33 | No provenance files: `provenance.yaml`, `provenance.sig` or any `provenance.*` (outside `trajectories/`). Not part of the format: remove them. | MAJOR | cmd S1-01 | user decision 2026-10-19 |
| S1-34 | No fixtures: a `tests/fixtures/` dir (or any `fixtures/` outside `trajectories/`). Not part of the format: remove it. | MAJOR | cmd S1-01 | user decision 2026-10-19 |
| S1-35 | `schema_version = "1.4"` at the top of task.toml; `[task] name = "atlas/<uuid>"`, `version`, `description`, `keywords`, `authors` (each `{name, email}`); `[task.metadata]` carries `apps`, `mcp_servers`, `grader = "weighted"`, `grading`, `components` describing the 2a ledger. | MAJOR | cmd S1-12 | Sample |
| S1-32 | We do not use `rubric.json`; the rubric is `tests/judge.toml`. Any `rubric.json` (outside `trajectories/`) is a BLOCKER. Fix by case: (a) `rubric.json` without `judge.toml`: make `tests/judge.toml` from it (recipe below), then delete `rubric.json`; (b) both present: delete `rubric.json` (the judge.toml is then checked in Stage 4); (c) neither: write `tests/judge.toml`. Also point every reference to `rubric.json` in `test.sh`, `test_weights.json components.rubric.file` and `task.toml [task.metadata]` at `judge.toml`. | BLOCKER | cmd S1-01 | user decision 2026-10-19 |
| S1-06 | `[environment]` pins `docker_image` and `light_servers_image` by `@sha256:` digest, and the compose `LIGHT_SERVERS_IMAGE` / tests compose `JUDGE_IMAGE` defaults are digest-pinned too. A floating tag (`:latest`, no digest) is a BLOCKER. | BLOCKER | cmd S1-06 | Sample |
| S1-08 | Every `[[environment.mcp_servers]]` entry has exactly `name`, `transport = "streamable-http"`, `url = "http://light-servers:<port>/mcp"`, and the port equals the `--port` in `entrypoint.sh SERVER_CMDS` for that name. No two entries share a port. | BLOCKER | cmd S1-08 | Std §10.3, v4 S2-SV1..SV6 |
| S1-09 | Every declared Light app is in compose `ENABLED_SERVERS`. (The v4 "empty ENABLED_SERVERS" rule does not apply.) | BLOCKER | cmd S1-09 | Std §10.3 |
| S1-10 | Light-servers source is identical to the reference sample, ignoring the per-task `# harbor-canary GUID` line (every task has its own; it is never a finding), the task's own `world_data/` and `task_data/`, and `software/LightAirtable/airtable.py` (the one server file allowed to differ). If `$REF` does not exist, set it to any yuji sample before marking S1-10 Not checked. | BLOCKER | cmd S1-10 | Std §10.4, Sample |
| S1-11 | Compose has only services `main` and `light-servers` and the volume `workspace_data`. No `ports:` or `expose:`. | BLOCKER | cmd S1-11 | Std §10.5, v4 S4-DF1/DF5 |
| S1-12 | `[agent] network_mode = "allowlist"` with a non-empty `allowed_hosts` (model API hosts only); `[verifier.environment] network_mode = "public"`; `[environment] network_mode = "public"`. | BLOCKER | cmd S1-12 | Sample |
| S1-13 | `[verifier.env]` holds `JUDGE_WIRE`, `JUDGE_MODEL`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, each as `${NAME:-}` (a default after `:-` is allowed for `JUDGE_MODEL`/`JUDGE_WIRE`), and `ATLAS_END_ENV = "/logs/artifacts/atlas/end_env.json"`. No literal key value. | BLOCKER | cmd S1-13 | Sample |
| S1-14 | `[agent] timeout_sec = 3600`, `[verifier] timeout_sec = 1800`, `[verifier] environment_mode = "separate"`. Integers, not floats or formulas. | BLOCKER | cmd S1-12 | Sample |
| S1-15 | `artifacts` collects `/logs/agent` with `exclude = ["./completions"]` and `/workspace` with `exclude = ["./data"]` (the grader reads the files the run delivered). | MAJOR | cmd S1-12 | Sample |
| S1-16 | `[[verifier.collect]]`: `service = "main"`, `command = "python3 /harness/atlas/state_capture.py"`, `timeout_sec = 300`; `environment/Dockerfile` puts `state_capture.py` at `/harness/atlas/`. | MAJOR | cmd S1-12 | Sample |
| S1-17 | `state_capture.py` finds the sessions the agent used from `/logs/agent`, logs each out, and writes `end_env.json` under `ATLAS_STATE_DIR` (default `/logs/artifacts/atlas`). It never writes `/logs/verifier` and never reads `tests/` or `solution/`. Do NOT ask for fixed session ids declared in world_data/grounding.yaml: every Light app mints `session_{uuid()}` at login, no server takes a declared id, S1-10 forbids editing server code, and the Sample reads `/logs/agent` by design. That request is never a finding or a steering note. | MAJOR | cmd S1-17 | Sample, `software/*/session.py` |
| S1-19 | Multi-step bundle carries top-level `multi_step_reward_strategy = "final"`. `[metadata] steps_aggregation` is ignored and does not count. | BLOCKER | cmd S1-12 | Std §10.11 |
| S1-27 | Forbidden files: `__pycache__/`, `.pytest_cache/`, `.DS_Store`, `* (N).*`, `.zip`, editor backups (in the source bundle, not created by your copy). `trajectory/` is never scanned. | MAJOR | cmd S1-27 | v4 S2-HY1, S4-DF10 |
| S1-28 | No empty or whitespace-only file. Every JSON parses. Every shell script has a shebang. (`trajectory/` excluded.) | MAJOR | cmd S1-28 | v4 S4-FC2, FC7 |
| S1-30 | Harbor 0.24.0 is the version used (`harbor --version` prints `0.24.0`; if the installed `harbor` differs, say so and use `uv tool run --from harbor==0.24.0 harbor`). The bundle copy loads with Harbor 0.24.0's own task loader with no error: `TaskConfig` parses task.toml (keys and types), input paths are contained, `instruction.md` and `tests/test.sh` (or a bundled-tests verifier image) exist. Harbor 0.24.0 has no `harbor validate` subcommand (`harbor --help`), and `harbor check` runs a model agent, so it is not used. | BLOCKER | cmd S1-30 | Harbor 0.24.0 `harbor/models/task/task.py`, `config.py` |
| S1-31 | task.toml values Harbor 0.24.0 accepts: `network_mode` in `no-network`, `public`, `allowlist`; `[verifier] environment_mode` in `shared`, `separate`; MCP `transport` in `stdio`, `sse`, `streamable-http` with a `url` for the HTTP ones; `multi_step_reward_strategy` in `mean`, `final` and at the TOP level when `[[steps]]` exist (under `[metadata]` it is ignored); every `[[steps]]` has `name` and a `steps/<name>/` dir. Root keys Harbor ignores (`[mcp_atlas]`, `[upstream_provenance]`) are a MINOR note. | BLOCKER | cmd S1-30 | Harbor 0.24.0 `TaskConfig`, `StepConfig`, `MultiStepRewardStrategy` |

Commands for Stage 1:

```bash
source /tmp/qc/<uuid>-report/env.sh
# S1-01 / S1-32 / S1-33 / S1-34  format of section 2e (trajectories/ is never walked)
cat > /tmp/qc/layout_check.py <<'PY'
import sys, pathlib
b = pathlib.Path(sys.argv[1])
SKIP = {"trajectories", "trajectory", "__pycache__", ".DS_Store"}
REQUIRED = ["task.toml", "instruction.md",
    "environment/Dockerfile", "environment/docker-compose.yaml", "environment/state_capture.py",
    "environment/light-servers/Dockerfile", "environment/light-servers/Dockerfile.ecr",
    "environment/light-servers/entrypoint.sh", "environment/light-servers/filesystem_server.py",
    "environment/light-servers/health_check.py", "environment/light-servers/requirements.txt",
    "environment/light-servers/server_main.py", "environment/light-servers/sitecustomize.py",
    "environment/light-servers/servers", "environment/light-servers/software",
    "environment/light-servers/task_data", "environment/light-servers/world_data",
    "tests/.dockerignore", "tests/Dockerfile", "tests/Dockerfile.ecr", "tests/docker-compose.yaml",
    "tests/_judge/rubric_judge_cli.py", "tests/claims_lib.py", "tests/ctrf_pytest_plugin.py",
    "tests/test.sh", "tests/test_outputs.py", "tests/test_weights.json", "tests/grade.py",
    "tests/old_env.json", "tests/oracle.json",
    "solution/TRUTH.md", "solution/gt_env.json", "solution/solve.py", "solution/solve.sh"]
for p in REQUIRED:
    if not (b / p).exists(): print("S1-01 BLOCKER missing:", p)
def found(pattern):
    return sorted(str(f.relative_to(b)) for f in b.rglob(pattern) if not SKIP & set(f.relative_to(b).parts))
rj, jt = found("rubric.json"), (b / "tests/judge.toml").exists()
if rj and not jt: print("S1-32 BLOCKER rubric.json present and no tests/judge.toml: make tests/judge.toml from it, then remove", rj)
elif rj and jt:   print("S1-32 BLOCKER tests/judge.toml exists: remove", rj)
elif not jt:      print("S1-32 BLOCKER tests/judge.toml missing: write it")
refs = [p for p in ("tests/test.sh", "tests/test_weights.json", "task.toml") if (b / p).exists() and "rubric.json" in (b / p).read_text()]
if refs: print("S1-32 BLOCKER still names rubric.json, point it at judge.toml:", refs)
if found("provenance.*"): print("S1-33 MAJOR provenance files present, remove them:", found("provenance.*"))
fx = [p for p in found("fixtures") if (b / p).is_dir()]
if fx: print("S1-34 MAJOR fixtures present, remove them:", fx)
# everything outside light-servers' own tree that the format does not list
allowed = set(REQUIRED) | {"tests/judge.toml", "tests/_judge", "environment", "tests", "solution", "environment/light-servers"}
for f in sorted(b.rglob("*")):
    r = f.relative_to(b); parts = r.parts
    if SKIP & set(parts) or str(r) in allowed: continue
    if parts[:2] == ("environment", "light-servers") and len(parts) > 3: continue      # servers/, software/, data
    if f.name in ("rubric.json",) or f.name.startswith("provenance.") or "fixtures" in parts: continue
    print("S1-01 MAJOR not in the format, remove it:", r)
print("S1-01 format check done")
PY
python3 /tmp/qc/layout_check.py "$B"
# S1-09
grep -n 'ENABLED_SERVERS' "$B/environment/docker-compose.yaml"
# S1-11
grep -nE '^[A-Za-z_]+:|^  [A-Za-z0-9_-]+:|ports:|expose:' "$B/environment/docker-compose.yaml"
# S1-13  key names only, never values
python3 - "$B/task.toml" <<'EOF'
# prints NAME and a status only; never prints a value or a line
import re, sys
t = open(sys.argv[1]).read()
for n in ("JUDGE_MODEL", "JUDGE_WIRE", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
    vals = re.findall(r'(?m)^' + n + r'\s*=\s*(.*?)\s*(?:#.*)?$', t)
    default = r'' if n.endswith('_API_KEY') else r'[^}"]*'   # API keys must default to empty
    ok = vals and all(re.fullmatch(r'"\$\{' + n + r':-' + default + r'\}"', v) for v in vals)
    print(n, 'MISSING' if not vals else ('ok' if ok else 'LITERAL'))
EOF
# S1-17
grep -nE 'ATLAS_AGENT_LOGS|ATLAS_STATE_DIR|logout|/logs/verifier|/tests|/solution' "$B/environment/state_capture.py" | head -20
# S1-27  run on the SOURCE bundle, not the copy; trajectory/ is pruned
find "$SRC" \( -name trajectory -o -name trajectories \) -prune -o \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.DS_Store' -o -name '*([0-9])*' -o -name '*.zip' -o -name '*~' \) -print
# S1-28
find "$B" \( -name trajectory -o -name trajectories \) -prune -o -type f -not -path "$LS/*" -size -2c -print
find "$B" \( -name trajectory -o -name trajectories \) -prune -o -name '*.json' -not -path "$LS/*" -exec python3 -c "import json,sys;json.load(open(sys.argv[1]))" {} \; 2>&1 | grep -i error
for f in $(find "$B" \( -name trajectory -o -name trajectories \) -prune -o -name '*.sh' -print); do head -1 "$f" | grep -q '^#!' || echo "no shebang: $f"; done
```

S1-32 fix recipe, `rubric.json` -> `tests/judge.toml` (quote it in the report's Fix line; the QC never edits the
bundle). Field mapping: `criterion` -> `description`; `score` -> `weight`, made negative when `is_positive` is false
(5/3/1 stay 5/3/1, a negative 5 becomes -5); `number`, `is_positive` (as `polarity`), `type` (as `category`),
`importance`, `evaluation_target` -> `annotations`; `id = name = "r<number, 3 digits>"`; `type = "binary"`;
`[scoring] aggregation = "weighted-sum"`; `[judge] files` = evidence the Sample's `test.sh` already writes before
step 4: `/tmp/agent_trajectory.json` (step 1: final message, calls with arguments) and `/logs/verifier/end_env.json`
(step 3). Add the collected `/workspace` copy only when a criterion judges a delivered file. Never name a file
no step writes (S4-13).
A dry conversion into the report area (then run the Stage 4 command on it):

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/rubric_to_judge.py <<'PY'
import json, sys
raw = json.load(open(sys.argv[1])); crit = raw["criteria"] if isinstance(raw, dict) else raw
q = json.dumps
out = ['[judge]', 'judge = "openai/gpt-5.6-sol"', 'files = ["/tmp/agent_trajectory.json", "/logs/verifier/end_env.json"]', 'mode = "batched"',
       'timeout = 1200', '', '[scoring]', 'aggregation = "weighted-sum"', '']
for c in crit:
    n = int(c["number"]); pos = c.get("is_positive", True); w = abs(int(c["score"])) * (1 if pos else -1)
    out += ['[[criterion]]', 'id = "r%03d"' % n, 'name = "r%03d"' % n, 'description = ' + q(c["criterion"]), 'type = "binary"',
            'weight = %d' % w, 'annotations = { number = %s, polarity = %s, category = %s, importance = %s, evaluation_target = %s }' % (
            q(str(c["number"])), q("positive" if pos else "negative"), q(c.get("type", "")),
            q(c.get("importance", "")), q(c.get("evaluation_target", ""))), '']
open(sys.argv[2], "w").write("\n".join(out)); print(len(crit), "criteria ->", sys.argv[2])
PY
test -f "$T/rubric.json" && python3 /tmp/qc/rubric_to_judge.py "$T/rubric.json" "/tmp/qc/$UUID-report/judge.from_rubric.toml"
```

S1-30 / S1-31, Harbor version and static validation. `/tmp/qc/harbor_validate.py` loads the task with Harbor's
own `Task` class (save it from the block below if it is missing):

```bash
source /tmp/qc/<uuid>-report/env.sh
harbor --version                                   # if not 0.24.0, use the uv form below
export UV_TOOL_DIR=/tmp/qc/uvtools UV_CACHE_DIR=/tmp/qc/uvcache
uv tool run --from harbor==0.24.0 harbor --version  # prints 0.24.0
uv tool run --from harbor==0.24.0 harbor --help     # confirm: no validate subcommand
cat > /tmp/qc/harbor_validate.py <<'PY'
import sys, tomllib
from importlib.metadata import version
from pathlib import Path
from harbor.models.task.config import TaskConfig
from harbor.models.task.task import Task
d = Path(sys.argv[1]).resolve(); print("harbor", version("harbor"))
raw = tomllib.loads((d / "task.toml").read_text())
print("root keys ignored by TaskConfig:", sorted(set(raw) - set(TaskConfig.model_fields)) or "none")
try:
    t = Task(d)
except Exception as e:
    print("INVALID:", type(e).__name__, e); sys.exit(1)
c = t.config
print("Task loaded:", t.name, "| is_valid_dir:", Task.is_valid_dir(d), "| steps", len(c.steps or []),
      "| multi_step_reward_strategy", c.multi_step_reward_strategy, "| environment_mode", c.verifier.environment_mode)
if c.steps and "multi_step_reward_strategy" not in raw:
    print("INVALID: multi-step without top-level multi_step_reward_strategy"); sys.exit(1)
PY
uv run --no-project --with harbor==0.24.0 python /tmp/qc/harbor_validate.py "$B"
```

S1-08, port registry against task.toml:

```bash
source /tmp/qc/<uuid>-report/env.sh
python3 - "$B" <<'PY'
import tomllib, re, sys, pathlib
b = pathlib.Path(sys.argv[1])
t = tomllib.load(open(b/'task.toml','rb'))
ep = (b/'environment/light-servers/entrypoint.sh').read_text()
reg = dict(re.findall(r'SERVER_CMDS\["([^"]+)"\]=.*?--port (\d+)', ep))
seen = {}
for s in t['environment']['mcp_servers']:
    extra = set(s) - {'name','transport','url'}
    m = re.fullmatch(r'http://light-servers:(\d+)/mcp', s['url'])
    port = m.group(1) if m else None
    print(s['name'], port, 'reg=' + str(reg.get(s['name'])),
          'OK' if (m and s['transport']=='streamable-http' and reg.get(s['name'])==port and not extra) else 'HIT', extra or '')
    if port in seen: print('HIT shared port', port, seen[port], s['name'])
    seen[port] = s['name']
PY
```

S1-10, source identity (canary GUID lines ignored; only `software/LightAirtable/airtable.py` may differ):

```bash
source /tmp/qc/<uuid>-report/env.sh
test -d "$REF/environment/light-servers" || { echo "S1-10: REF missing; set REF to your copy of yuji/samples/974d1442-... in env.sh"; exit 1; }
diff -r -q -I 'harbor-canary GUID' -x __pycache__ -x world_data -x task_data \
  "$REF/environment/light-servers" "$LS"
# expected output: nothing, or exactly one line for software/LightAirtable/airtable.py
```

S1-06, S1-12 to S1-16, S1-19, S1-35: task.toml against the Sample's values:

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/toml_check.py <<'PY'
# S1-06 S1-12..S1-16 S1-19 S1-35  task.toml values against the Sample (prints names and statuses, never key values)
import re, sys, tomllib, pathlib
b = pathlib.Path(sys.argv[1]); raw = (b / "task.toml").read_text(); t = tomllib.loads(raw)
def chk(cid, cond, what): print(cid, "ok " if cond else "HIT", what)
a, v, e = t.get("agent", {}), t.get("verifier", {}), t.get("environment", {})
ve = v.get("environment", {}) or {}
pin = lambda x: isinstance(x, str) and "@sha256:" in x
chk("S1-06", pin(e.get("docker_image")), "[environment] docker_image pinned by digest")
chk("S1-06", pin(e.get("light_servers_image")), "[environment] light_servers_image pinned by digest")
for comp, var in (("environment/docker-compose.yaml", "LIGHT_SERVERS_IMAGE"), ("tests/docker-compose.yaml", "JUDGE_IMAGE")):
    m = re.search(var + r":-([^}]+)\}", (b / comp).read_text()) if (b / comp).exists() else None
    chk("S1-06", bool(m) and "@sha256:" in m.group(1), comp + " " + var + " default pinned by digest")
chk("S1-12", a.get("network_mode") == "allowlist" and bool(a.get("allowed_hosts")), "agent allowlist + allowed_hosts %s" % a.get("allowed_hosts"))
chk("S1-12", ve.get("network_mode") == "public", "[verifier.environment] network_mode public")
chk("S1-12", e.get("network_mode") == "public", "[environment] network_mode public")
chk("S1-13", (v.get("env") or {}).get("ATLAS_END_ENV") == "/logs/artifacts/atlas/end_env.json", "[verifier.env] ATLAS_END_ENV")
chk("S1-14", a.get("timeout_sec") == 3600 and type(a.get("timeout_sec")) is int, "agent timeout_sec 3600")
chk("S1-14", v.get("timeout_sec") == 1800 and type(v.get("timeout_sec")) is int, "verifier timeout_sec 1800")
chk("S1-14", v.get("environment_mode") == "separate", "verifier environment_mode separate")
arts = {x.get("source"): x.get("exclude") for x in t.get("artifacts", []) if isinstance(x, dict)}
chk("S1-15", arts.get("/logs/agent") == ["./completions"], "artifact /logs/agent exclude ./completions")
chk("S1-15", arts.get("/workspace") == ["./data"], "artifact /workspace exclude ./data")
col = v.get("collect") or []
chk("S1-16", len(col) == 1 and col[0].get("service") == "main" and col[0].get("command") == "python3 /harness/atlas/state_capture.py"
    and col[0].get("timeout_sec") == 300, "collect hook main / /harness/atlas/state_capture.py / 300")
chk("S1-16", "/harness/atlas" in (b / "environment/Dockerfile").read_text(), "environment/Dockerfile places state_capture.py under /harness/atlas")
chk("S1-19", not t.get("steps") or t.get("multi_step_reward_strategy") == "final", "multi-step strategy (single-step: n/a)")
k = t.get("task", {}); m = k.get("metadata", {})
chk("S1-35", t.get("schema_version") == "1.4", "schema_version 1.4")
chk("S1-35", k.get("name") == "atlas/" + b.name.split(".")[0], "task name atlas/<uuid> (%s)" % k.get("name"))
chk("S1-35", all(isinstance(x, dict) and x.get("name") and x.get("email") for x in k.get("authors", [None])), "authors {name, email}")
for f in ("version", "description", "keywords"): chk("S1-35", bool(k.get(f)), "[task] " + f)
for f in ("apps", "mcp_servers", "grading", "components"): chk("S1-35", bool(m.get(f)), "[task.metadata] " + f)
chk("S1-35", m.get("grader") == "weighted", "[task.metadata] grader = weighted")
chk("S1-35", "rubric.json" not in str(m.get("grading", "")) + str(m.get("components", "")), "[task.metadata] grading/components name judge.toml, not rubric.json")
PY
python3 /tmp/qc/toml_check.py "$B"          # every HIT line is a finding at the row's severity
```

## 7. Stage 2: instruction, world data, leakage (5 min)

Visible surface: `instruction.md`, everything under `task_data/` (names and contents), and everything the wired apps serve from `world_data/`. Invisible: `task.toml`, `tests/**`, `solution/**`. A value that exists only in an invisible file cannot be produced by any run.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S2-01 | No reward leakage. A truth or answer value from `TRUTH.md` / `grounding.yaml` (figures, target ids, chosen names) in `instruction.md` (or a delivered `prompt.txt`) is a BLOCKER. In agent-visible `task_data/` or `world_data/` it is a BLOCKER only when it is a derived answer (a computed result the agent should produce, stated ready to copy); discovery inputs there are expected and decoys are notes. Ignore shared server source (`light-servers/software/`, `servers/`), values under 6 characters and plain dates. | BLOCKER | cmd S2-01 | FORGE 11, v4 S0-LK2/LK4, S2-WD13, tabish E4/M8 |
| S2-02 | No wrong figure or decoy id printed in the instruction. A printed trap is not a trap. | BLOCKER | cmd S2-01 | v4 S0-LK3, S2-MD2 |
| S2-03 | Nothing in `task_data/` reveals the answer (worked totals, a filled-in deliverable, a key). | BLOCKER | read | Std §10.12 |
| S2-04 | Instruction names no machinery: no path or directory, no host or harness path, no URL or port, no `Light*` app name, no snake_case tool name, no `MCP`, `server`, `tool call`, `endpoint`, `API`, `mock`, no slug, uuid or seed. | BLOCKER | cmd S2-04 | v4 S0-PA1..PA8 |
| S2-05 | Instruction names no grading artefact: `tests/`, `solution/`, `test_outputs.py`, `test_weights.json`, `grade.py`, `oracle.json`, `judge.toml`, `reward.json`, `rubric_score.json`, `grounding.yaml`, `TRUTH.md`. | BLOCKER | cmd S2-04 | v4 S0-PA1 |
| S2-06 | No authoring residue: HTML comment, `TODO`, `FIXME`, `NOTE:`, placeholders, text addressed to a model ("think step by step", "You are a"). | BLOCKER | cmd S2-06 | v4 S0-CM1..CM3 |
| S2-08 | Deliverable is stated: the run can tell which record or state change is the answer. | BLOCKER | read | v4 S0-SP1 |
| S2-09 | Instruction does not walk the procedure, does the arithmetic in words, say which source wins, state a rule with its application, or count the evidence or traps. | MAJOR | read | v4 S0-SP2, SP3, LK5, LK6, LK7 |
| S2-10 | Instruction does not coach ("first check", "make sure", "be careful", "look for", "cross-check", "remember", "note that", "hint"). | MAJOR | cmd S2-10 | v4 S0-SP4 |
| S2-11 | Instruction does not point at the evidence (exact document title, thread subject, field, person holding the answer, a date range that isolates it). | MAJOR | search titles/subjects from world_data and TRUTH.md | v4 S0-SP5 |
| S2-12 | Every graded decision has a cue in the visible surface. A graded choice the instruction and world never motivate is unwinnable. | BLOCKER | trace each predicate to a cue | tabish B3, RUTHLESS 3.2 |
| S2-13 | No contradictory rules or guards: one graded outcome only (FORGE 10a statement-ambiguity rule). | BLOCKER | read predicates against instruction | tabish B2, FORGE 10a |
| S2-14 | Conventions the graders assume (units, rounding, date format, currency scale, id format) are stated in the instruction or carried by the world. | MAJOR | read | tabish B4, v4 S4-TR11 |
| S2-15 | Every decoy is planted in the served world and is killed by a stated rule a careful run can find. A decoy with no killing rule is ambiguity, not difficulty. | MAJOR | trace each control in grounding to a world row and a rule | tabish B5, B6, v4 S2-CP6 |
| S2-16 | `world_data/<App>.json` filename equals the app name byte-for-byte, exists for every graded app, and none exists for an app that is not wired. | BLOCKER | cmd S2-16 | v4 S2-WD1..WD3 |
| S2-17 | Every top-level container in an overlay resolves in the app: a corpus yaml key, a `get_session_dict()` key, or a `self.<name>` attribute. Keys beginning `_` are markers. | BLOCKER | read app `corpus/*.yaml` and `__init__` | v4 S2-WD4 |
| S2-18 | Container form (list vs dict keyed by id), field names, value types (overlays are not coerced) and enum values match the corpus row. Evidence path only. | MAJOR | compare one corpus row per container used | v4 S2-WD5..WD9 |
| S2-19 | Authored ids do not collide with corpus ids (overlays append). Task logic that says "the only", "the earliest", "the last" survives corpus rows being present. | BLOCKER | cmd S2-19 | v4 S2-WD10, WD11 |
| S2-20 | Session ids the agent needs are declared in `world_data/` and are the ones `state_capture.py` logs out. | BLOCKER | grep session id across files | Std §10.9, Sample |
| S2-21 | No authoring smell readable as a hint in world rows (`_comment`, ids like `decoy-2`, notes naming the trap). | MINOR | cmd S2-21 | v4 S2-WD15 |
| S2-22 | Images in `task_data/`: none confirmed AI-generated; none clearly code-drawn (two or more signs: flat background, clean system font, pixel-perfect rules, no scan artifacts, code layout quirks). Uncertain origin is not a finding. | MINOR | brief visual look | v4 S1-GN1, GN2 |
| S2-23 | No copy of `solution/` or `tests/` (or `TRUTH.md`, `grounding.yaml`, `judge.toml`, `oracle.json`, `test_weights.json`, `gt_env.json`) into any agent-side image: no `COPY`/`ADD` of them in `environment/**/Dockerfile*`, and nothing from them under `task_data/` or `world_data/`. The verifier image built from `tests/Dockerfile` is the one allowed exception. | BLOCKER | cmd S2-23 | tabish E1, leakage policy |
| S2-24 | `tests/judge.toml`, `tests/oracle.json`, `tests/test_weights.json`, `solution/gt_env.json` and `solution/TRUTH.md` are never agent-visible: not in an agent image, not mounted into `main` or `light-servers`, not under `task_data/` or `world_data/`. | BLOCKER | cmd S2-23 | leakage policy |

Commands for Stage 2. Build `truth.txt` once by hand from `TRUTH.md` and `tests/oracle.json` (`reported`, the written values in `oracle`) (one figure or id per line, and add variants without thousands separators or currency).

```bash
source /tmp/qc/<uuid>-report/env.sh
# S2-01 / S2-02  leak scan of truth figures and decoys across the visible surface
VIS="$B/instruction.md $LS/task_data $(find "$B/environment" -name 'Dockerfile*')"
while IFS= read -r n; do [ -n "$n" ] && grep -rlF -- "$n" $VIS 2>/dev/null | sed "s|^|LEAK '$n' in |"; done < "/tmp/qc/$UUID-report/truth.txt"
# world_data separately: a hit there is a leak only if it is the derived answer, not seeded evidence
while IFS= read -r n; do [ -n "$n" ] && grep -rcF -- "$n" "$LS/world_data" | grep -v ':0$' | sed "s|^|WORLD '$n' |"; done < "/tmp/qc/$UUID-report/truth.txt"
# S2-04 / S2-05
grep -nE '/|\\|https?:|localhost|light-servers|:[0-9]{2,5}\b|\bMCP\b|tool call|endpoint|\bAPI\b|\bmock\b|\bserver\b' "$B/instruction.md"
grep -noE '\b[a-z]+_[a-z_]+\b' "$B/instruction.md" | sort -u          # snake_case tool names
grep -nE 'Light[A-Z][A-Za-z]+|test_output|judge\.toml|reward|rubric|grounding|TRUTH' "$B/instruction.md"
# S2-06
grep -nE '<!--|TODO|FIXME|NOTE:|XXX|<[a-z_]+>|step by step|You are a|do not hallucinate' "$B/instruction.md"
# S2-10
grep -niE '\b(first|then|make sure|be careful|remember|don.t forget|look for|cross-check|check|note that|hint|tip)\b' "$B/instruction.md"
# S2-16
ls "$LS/world_data"; grep -n 'name = ' "$B/task.toml"
# S2-19  list authored ids and look for each in the app corpus
python3 -c "import json,sys,re;d=json.load(open(sys.argv[1]));print(sorted(set(re.findall(r'\"id\": *\"([^\"]+)\"',json.dumps(d))))[:60])" "$LS/world_data/<App>.json"
grep -c '<authored id>' "$LS/software/<App>/corpus/"*.yaml
# S2-21
grep -rnE '"_comment"|decoy|trap|wrong|poison' "$LS/world_data"
# S2-23 / S2-24
grep -rnE '^(COPY|ADD).*(solution|tests|TRUTH|grounding|judge\.toml|oracle\.json|test_weights|gt_env)' "$B/environment" --include='Dockerfile*'
grep -rlE 'judge\.toml|TRUTH\.md|oracle\.json|test_weights|gt_env' "$B/environment/docker-compose.yaml" "$LS/task_data" "$LS/world_data"
find "$B/environment" \( -name 'judge.toml' -o -name 'TRUTH*' -o -name 'grounding.yaml' -o -name 'oracle.json' -o -name 'test_weights.json' -o -name 'gt_env.json' \) -print
```

## 8. Stage 3: deterministic grading (5 min)

Files: `tests/test.sh`, `tests/test_outputs.py`, `tests/claims_lib.py`, `tests/test_weights.json`, `tests/grade.py`, `tests/old_env.json`, `tests/oracle.json`, `tests/judge.toml`, `solution/gt_env.json`, `solution/TRUTH.md`, `solution/solve.sh`. No fixtures.

Ground rules for this stage:

- The reward reads only what section 2b allows: the trajectory `test.sh` rebuilt (`ATLAS_TRAJECTORY`), the files the run delivered under `/workspace`, the snapshot (`ATLAS_END_ENV`), `tests/old_env.json`, `tests/oracle.json`, and the rubric score in `rubric_breakdown.json`. Nothing else may decide the reward.
- Read every predicate down to the field it reads and the literal it compares. A docstring or an id is a claim; the relation is the fact.
- Check the sign or role first. A guard is meant to describe the bad state.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S3-01 | Reward is computed only from the 2b inputs: rebuilt trajectory and final message, delivered `/workspace` files, `end_env.json`, `tests/old_env.json`, `tests/oracle.json`, and `rubric_breakdown.json`'s `score`. | BLOCKER | cmd S3-01 | Sample, adaptation 2b |
| S3-02 | Reward never reads `solution/**`, `TRUTH.md`, `gt_env.json`, the `trajectories/` folder, network resources, or a file that was in the agent's view BEFORE the run and states the answer. Reading the rebuilt trajectory, the final message and the files the run itself delivered under `/workspace` (for example a `/workspace/output/*.json` the instruction asks for) is allowed by the format (2b): never flag a file deliverable or ask to move it into a Light app record. The deliverable's path and shape must be stated in the instruction (S2-08). | BLOCKER | cmd S3-01 | Sample, adaptation 2b |
| S3-03 | A missing or empty snapshot does not break the reward: `test.sh` writes `state_capture_failed.txt` and the checks fall back to the trajectory; a reward file is still written. A missing judge key or failed judge leaves no `rubric_breakdown.json` and the rubric is dropped from the ledger, never scored 0. | BLOCKER | cmd S3-03, probe S5-05 | Sample |
| S3-04 | Every failure path is loud: a `grade.py` crash makes `test.sh` exit non-zero (`\|\| { ...; exit 1; }`); a check that raises is scored false (not a pass); no path exits 0 with no `reward.json`. | BLOCKER | cmd S3-03 | Sample |
| S3-05 | `test.sh` runs, in order: (1) rebuild the trajectory, (2) judge wire + key check, (3) copy the snapshot, (4) rubric from `/tests/judge.toml` -> `rubric_breakdown.json`, (5) pytest with `-p ctrf_pytest_plugin` (reporting only, `\|\| true` allowed), (6) `grade.py` (never softened), (7) `reward.json` + `reward_producer.json`. | BLOCKER | cmd S3-03 | Sample |
| S3-10 | Assert hygiene: no check with no assert or no comparison; no constant assert (`assert True`, `assert 1`); no self-compare (`x == x`); no `or True`; no swallowed `except` that turns an outage into a pass; no silent early `return` in a check; no `pytest.skip`/`xfail` on a graded check. | BLOCKER | cmd S3-10 | qc2 §5, RUTHLESS 3.1b, Checklist J5..J7 |
| S3-11 | Unguarded indexing (`rows[0]`, `[-1]`) on captured state that raises on a short or empty world. | MAJOR | cmd S3-10 | RUTHLESS 3.1d, v4 S3-E5 |
| S3-12 | No exact float equality on money or measures. A tolerance (`approx`) is stated in the instruction or is a rounding the world defines. | MAJOR | cmd S3-10 | RUTHLESS 3.1d, tabish C5 |
| S3-13 | Phantom dependencies: every import in `tests/` is stdlib, a sibling module in `tests/`, or pinned (`==`) in the `pip install` of `tests/Dockerfile` (or `tests/requirements.lock` if the bundle has one). | BLOCKER | cmd S3-13 | Checklist I2, v4 S3-E1 |
| S3-14 | Determinism: no `random`, `uuid`, `time.time`, `datetime.now`, `shuffle`, dict-order or set-order dependence, network, or test-order dependence in grading. | BLOCKER | cmd S3-14 | tabish D4, RUTHLESS 3.1e, v4 S3-E12 |
| S3-15 | Substring self-pass: a loose `in` or `contains` that matches by accident (`"two" in "network"`), or a case mismatch that fails a correct value. | MAJOR | read every `contains`/`startswith`/`in` relation | Checklist D2, v4 S3-N8 |
| S3-16 | Value coercion: the grader does not lowercase, strip, round or cast the captured value into a tolerance the instruction never states. Normalisations apply to both sides or only remove formatting. | MAJOR | read `_canon` and comparisons | Checklist W5, tabish C8, v4 S3-H5 |
| S3-17 | Numeric fields compared numerically, ids compared as exact strings. | MAJOR | read | tabish C7 |
| S3-18 | Ids the graders key on are seeded ids from the world, never ids the agent invents at runtime. A created record is located by its identifying fields, not by a guessed id. | BLOCKER | read relations against seed | Checklist A3, W2, v4 S3-G2, H2 |
| S3-19 | Literal grounding: every graded value is visible to the agent or derivable from the served world. A value that exists only in `tests/` or `solution/` is unwinnable. | BLOCKER | trace each literal | RUTHLESS 3.1a, Checklist A1, v4 S3-G4 |
| S3-20 | Every computed total the graders assert is verified by hand from the world rows. Write the arithmetic in the report. | BLOCKER | hand recompute | Checklist A2, tabish A6 |
| S3-21 | No seeded-state free credit: no gate predicate holds on the seed world. Check by reading against `tests/old_env.json` and by replaying it as the end state (S5-02). | BLOCKER | read, Stage 5 | RUTHLESS 3.1b, Checklist J2, v4 S3-G3 |
| S3-22 | An ABSENCE or INVARIANT predicate used as a gate is paired with an EFFECT predicate, so a run that does nothing cannot pass by restraint. | BLOCKER | read predicate kinds | v4 S3-D1 (adapted) |
| S3-23 | Every red-line (the catastrophic acts in TRUTH.md and `[task.metadata] trap`) has a negative check in `test_outputs.py` weighted -5 (or a gate that zeroes the reward). A red-line stated only in prose or only in judge.toml is a hit. | BLOCKER | read TRUTH.md against test_weights.json | FORGE 9, RUTHLESS 3.2 |
| S3-24 | Guard direction: no guard fires on the oracle's run. Read each guard against `solution/solve.sh` / `solve.py` and `tests/oracle.json` (every write the oracle makes); the live oracle's `grade_report.md` (S5-10) must list no tripped guard. | BLOCKER | read, S5-10 | RUTHLESS 3.1c, Checklist F1/F2, v4 S3-O2 |
| S3-25 | Penalty proportionality on `tests/test_weights.json`: no single penalty is at least the total positive weight; no single positive item is more than half the positive weight; `sum(abs(neg)) - sum(pos) <= 3`. Report the floor `-sum(abs(neg))/sum(pos)`. | MAJOR | cmd S3-25 | RUTHLESS 3.3, Checklist H3/I4/I5, v4 S3-D6, G7 |
| S3-26 | No positive predicate demands an act the instruction never asks for, and no two positive predicates make contradictory demands on one record. | BLOCKER | read | v4 S3-G5, G6, Checklist I3 |                                                                                                             `                                                                                                                                                                                                   
| S3-27 | Brittleness against an allowed alternative: no exact match on a field the instruction leaves open, no call-count style `== 1` on records where a retry is legal, no ordering requirement the instruction does not state. | MAJOR | read | v4 S3-G9, O9, RUTHLESS 3.1 |
| S3-28 | A composite key is not graded on one half where the world holds look-alikes sharing that half. | MAJOR | read | v4 S3-G1 |
| S3-29 | Collateral writes are guarded: an edit to a distractor app or an untouched record in a graded app fires a guard. | MAJOR | read guards (example G4-G6) | tabish C6, v4 S3-S3 |
| S3-30 | Volatile fields the harness rewrites on every write (`updated_at`, `modifiedTime`, `version`, `SyncToken`, counters) are excluded from unchanged/preserved comparisons, and no graded field is excluded. | MAJOR | read the volatile list | v4 S3-F7, S3-S4 |
| S3-31 | `task.toml [task.metadata] grading` and `components` describe the ledger `grade.py` actually computes (components, weights, gate) and name `judge.toml`, not `rubric.json`. | MINOR | read | Sample |
| S3-32 | **The pytest negatives are deducted.** (a) Every guard check (the format names them `test_guard_*`) has a negative weight in `test_weights.json`, and every negative weight names a check `test_outputs.py` defines (for a parametrised name `f[x]`, the function `f`). (b) `grade.py` subtracts the absolute weight of every tripped negative from the earned positive weight before dividing by the positive total, clamps at 0, and, when `gate.require_no_guards` is truthy, zeroes the reward on any tripped guard (a flag: a list of names is read as true and gates every guard). (c) No weight lookup for a charged guard defaults a missing name to 0 (`weights.get(name, 0)` on an unchecked name), no `abs()`/sign slip turns a penalty into credit, and no negative is filtered out before summing. Any miss means a forbidden act is not penalised: BLOCKER. Proven live on a replay by S5-13. | BLOCKER | cmd S3-32, replay S5-13 | user decision 2026-10-19 |
| S3-33 | **`test_weights.json` rates every check properly.** (a) Every weight is an integer on the scale: positive 1, 3 or 5; negative -1, -3 or -5. A 0, 2, 4, 10, 0.5, a string, a bool or a null on a `test_*` key is a BLOCKER (metadata keys such as `test_file` are not weights). (b) Sign matches role: a guard (a check that is true when the run did the forbidden thing) is negative, a goal is positive; a guard-named check with a positive weight is a BLOCKER. (c) Every pytest check in `test_outputs.py` is rated: when `grade.py` scores through `test_outputs.py`, an unweighted check scores nothing (MAJOR); when `grade.py` charges by its own names, list the unweighted functions as VERIFY and confirm the fact is weighted under another name. (d) The rating follows importance: a 5 goes to the load-bearing figures and red-line guards, a 1 to bookkeeping (read the top and bottom of the list; a red-line guard at -1 or a filing-presence check at 5 is a MAJOR). (e) No duplicate key with two different weights. | BLOCKER | cmd S3-25, then read | user decision 2026-10-19 |
| S3-34 | **Ledger components.** `test_weights.json components` has exactly `traj_tests` (`graded = true`, `test_file = "test_outputs.py"`, `tests` = the check weights) and `rubric` (`graded = true`, `file = "judge.toml"`). Each component `weight` equals the mean absolute weight of its items rounded to 2 or 3 places (the Sample has 3.41 for a mean of 3.412) (traj_tests: the `tests` values; rubric: the judge.toml criterion weights). `file = "rubric.json"` is a BLOCKER (the rubric would never be read); a wrong mean is a MAJOR. `grade.py` reads both components and drops an unscored one from numerator and denominator. | BLOCKER | cmd S3-25 | Sample |
| S3-35 | **Gates are live.** `test_weights.json gate` holds only `require_no_guards` (bool), `require_state_exact` (bool) and `floor` (number); another key is ignored by `grade.py` (MAJOR). `require_no_guards` given as a list is a MINOR (it gates every guard, not the names listed; write `true`). `require_state_exact` set while `test_outputs.py` lacks any of `_OLD_ENV_PATH`, `_entities`, `_load_env`, `_s_available`, `_state_diff`, `_state_misbehaved` is inert (and without `TARGET_ENTITIES` the live channel crashes `grade.py`), since `state_channel.json` stays `available: false` and the gate never fires: MAJOR. When it is live, S5-14 proves it zeroes an inexact state. | MAJOR | cmd S3-32, probe S5-14 | Sample `grade.py` |

Commands for Stage 3:

```bash
source /tmp/qc/<uuid>-report/env.sh
# S3-01 / S3-02  what the graders open
grep -nE 'open\(|read_text|json\.load|environ|/logs/|/workspace|trajectory|claude|completions|rubric_score' "$T"/*.py "$T/test.sh"
# S3-03 / S3-04 / S3-05  (pytest step may be `|| true`; the grade.py step may not)
grep -nE '^# -+ [0-9]|exit|reward\.json|reward_producer|rubric_breakdown|rubric\.json|judge\.toml|rewardkit|state_capture_failed|end_env|\|\| *true|set \+e|2>/dev/null|ctrf_pytest_plugin|grade\.py' "$T/test.sh"
grep -nE 'exit\(|sys\.exit|SystemExit|except|rubric_breakdown|components|unscored|retired|def write_reward_json' "$T/grade.py"
# S3-10 / S3-11 / S3-12  assert hygiene
grep -nE 'assert +(True|1|"|\x27)|or True|except[^:]*:\s*(pass|return)|pytest\.(skip|xfail)|\[0\]|\[-1\]|== *[0-9]+\.[0-9]+' "$T"/*.py
python3 - "$T/test_outputs.py" <<'PY'
import ast, sys
src = open(sys.argv[1]).read(); tree = ast.parse(src)
for n in ast.walk(tree):
    if isinstance(n, ast.Compare) and len(n.comparators) == 1 and ast.dump(n.left) == ast.dump(n.comparators[0]):
        print('SELF_COMPARE line', n.lineno)
    if isinstance(n, ast.Assert) and isinstance(n.test, ast.Constant):
        print('CONST_ASSERT line', n.lineno)
    if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):
        if not any(isinstance(x, (ast.Assert, ast.Return)) for x in ast.walk(n)):
            print('NO_ASSERT', n.name, n.lineno)
PY
# S3-13  imports vs the verifier image pins
grep -hoE '^(import|from) [A-Za-z_][A-Za-z0-9_]*' "$T"/*.py | awk '{print $2}' | sort -u
grep -nE 'pip install' "$T/Dockerfile"; ls "$T"/*.py
# S3-14
grep -nE 'random|uuid|time\.time|time\(\)|datetime\.now|shuffle|set\(' "$T"/*.py
```

S3-25 proportionality, S3-32 negative deduction, S3-33 rating and S3-34 ledger components, from `tests/test_weights.json` (weights may sit at
`tests`, `components.*.tests` or deeper; every numeric value keyed `test_*` is a check weight):

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/neg_static.py <<'PY'
# S3-25 / S3-32  test_weights.json against the checks test_outputs.py defines and the names grade.py charges
import ast, collections, json, re, sys, pathlib
T = pathlib.Path(sys.argv[1])
def walk(o, p=()):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, p + (k,))
    elif isinstance(o, (int, float)) and not isinstance(o, bool): yield p, o
raw = (T / "test_weights.json").read_text()
doc = json.loads(raw)
META = {"test_file", "test_files", "test_dir"}                # metadata keys, not weights
def walk_all(o, p=()):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk_all(v, p + (k,))
    else: yield p, o
ALL = [(p[-1], v) for p, v in walk_all(doc) if p and str(p[-1]).startswith("test_") and p[-1] not in META]
bad_type = sorted((k, v) for k, v in ALL if isinstance(v, bool) or not isinstance(v, (int, float)))
off_scale = sorted((k, v) for k, v in ALL if not isinstance(v, bool) and isinstance(v, (int, float))
                   and (v not in (1, 3, 5, -1, -3, -5) or isinstance(v, float)))
print("S3-33 BLOCKER weights that are not numbers:", bad_type or "none")
print("S3-33 BLOCKER weights off the 1/3/5, -1/-3/-5 integer scale:", off_scale or "none")
dups = collections.Counter(re.findall(r'"(test_[^"]+)"\s*:', raw))
print("S3-33 duplicate keys in the file:", sorted(k for k, n in dups.items() if n > 1) or "none")
W = {p[-1]: v for p, v in walk(doc) if str(p[-1]).startswith("test_") and p[-1] not in META}
fns = {n.name for n in ast.walk(ast.parse((T / "test_outputs.py").read_text()))
       if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")}
gsrc = (T / "grade.py").read_text()
pats = []                                   # every test_* name pattern grade.py can build
for n in ast.walk(ast.parse(gsrc)):
    if isinstance(n, ast.JoinedStr):
        s = "".join(re.escape(v.value) if isinstance(v, ast.Constant) else ".+" for v in n.values)
    elif isinstance(n, ast.Constant) and isinstance(n.value, str):
        s = re.sub(r"%[sd]|\\\{[^}]*\\\}", ".+", re.escape(n.value))
    else:
        continue
    if s.startswith("test_"): pats.append(s)
generic = "test_outputs" in gsrc            # grade.py calls the pytest checks by weight name
pos = {k: v for k, v in W.items() if v > 0}; neg = {k: v for k, v in W.items() if v < 0}
P, N = sum(pos.values()), sum(-v for v in neg.values())
print("S3-25 checks", len(W), "| positive", len(pos), "total", P, "| negative", len(neg), "total", N,
      "| floor", round(-N / P, 3) if P else "n/a")
print("S3-25 largest positive share", round(max(pos.values()) / P, 3) if P else "n/a", "(<= 0.5)",
      "| largest penalty", max(neg.values(), key=abs) if neg else 0, "(< positive total)", "| N - P", N - P, "(<= 3)")
print("S3-32 weight scale", sorted(set(W.values())), "| grade.py imports test_outputs:", generic)
def reached(k):
    return (generic and k.split("[")[0] in fns) or any(re.fullmatch(p, k) for p in pats)
print("S3-32 BLOCKER negative weights grade.py never charges:", sorted(k for k in neg if not reached(k)) or "none")
guardish = sorted(f for f in fns if re.search(r"^test_guard_", f))
loose = [f for f in guardish if not any(k.split("[")[0] == f for k in neg)]
wrong_sign = sorted(k for k, v in pos.items() if re.search(r"^test_guard_", k.split("[")[0]))
print("S3-33 BLOCKER guard-named checks rated positive:", wrong_sign or "none")
print("S3-33 MINOR negative checks not named test_guard_* (the format's convention):", sorted(k for k in neg if not k.startswith("test_guard_")) or "none")
unrated = sorted(f for f in fns if not any(k.split("[")[0] == f for k in W))
print("S3-33", "MAJOR" if generic else "VERIFY", "pytest checks with no weight:", unrated or "none")
print("S3-33 rating counts:", dict(sorted(collections.Counter(W.values()).items())))
for k, v in sorted(W.items(), key=lambda kv: (-abs(kv[1]), kv[0])):
    print("S3-33 read %4s  %s" % (v, k))
print("S3-32 VERIFY guard-named pytest checks with no same-named negative weight (confirm grade.py charges the fact):", loose or "none")
gate = doc.get("gate") or {}
print("S3-35 gate:", gate or "none", "| keys grade.py ignores (MAJOR):", sorted(set(gate) - {"require_no_guards", "require_state_exact", "floor"}) or "none")
rng = gate.get("require_no_guards")
if rng is not None and not isinstance(rng, bool):
    print("S3-35 MINOR require_no_guards is a %s; grade.py reads it as a flag, so %s" % (type(rng).__name__,
          "every tripped guard zeroes the reward, not only the names listed" if rng else "it is off"))
if rng:
    print("S3-32 gated: any of the", len(neg), "negative checks zeroes the reward when tripped")
if gate.get("require_state_exact"):
    tsrc = (T / "test_outputs.py").read_text()
    miss = [h for h in ("_OLD_ENV_PATH", "_entities", "_load_env", "_s_available", "_state_diff", "_state_misbehaved", "TARGET_ENTITIES") if not re.search(r"^def %s\b|^%s *=" % (h, h), tsrc, re.M)]
    print("S3-35 require_state_exact:", "MAJOR inert, test_outputs.py lacks " + ", ".join(miss) if miss else "helpers present, prove it with S5-14")
comps = doc.get("components") or {}
tt, rb = comps.get("traj_tests") or {}, comps.get("rubric") or {}
print("S3-34 components:", sorted(comps), "(must be exactly ['rubric', 'traj_tests'])")
tw = [abs(v) for v in (tt.get("tests") or {}).values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
want_t = round(sum(tw) / len(tw), 3) if tw else None
print("S3-34 traj_tests graded=%s test_file=%s weight=%s mean|w|=%s -> %s" % (tt.get("graded"), tt.get("test_file"),
      tt.get("weight"), want_t, "ok" if tt.get("graded") is True and tt.get("test_file") == "test_outputs.py" and want_t is not None and abs(float(tt.get("weight") or 0) - want_t) < 0.006 else "HIT"))
try:
    import tomllib
    jw = [abs(c.get("weight", 0)) for c in tomllib.load(open(T / "judge.toml", "rb")).get("criterion", [])]
except Exception as e:
    jw = []; print("S3-34 judge.toml unreadable:", e)
want_r = round(sum(jw) / len(jw), 3) if jw else None
print("S3-34 rubric graded=%s file=%s weight=%s mean|w| of judge.toml=%s -> %s" % (rb.get("graded"), rb.get("file"), rb.get("weight"),
      want_r, "BLOCKER file must be judge.toml" if rb.get("file") != "judge.toml" else ("ok" if rb.get("graded") is True and want_r is not None and abs(float(rb.get("weight") or 0) - want_r) < 0.006 else "HIT")))
for i, line in enumerate(gsrc.splitlines(), 1):
    if re.search(r"penalt|neg *=|< *0\b|require_no_guards|max\(0|\.get\([^)]*, *0\)\)?$", line):
        print("S3-32 read grade.py:%d: %s" % (i, line.strip()[:110]))
PY
python3 /tmp/qc/neg_static.py "$T"
```

Reading the S3-32 output:

- `negative weights grade.py never charges` non-empty: BLOCKER. That weight is never subtracted.
- `VERIFY guard-named pytest checks ...`: grade.py may charge the same fact under another weight name (example
  7f1a9224: pytest `test_guard_total_is_not_trap[x]`, weight `test_guard_total_is_not_x`). Open grade.py and
  confirm the charge exists; if the fact is charged nowhere, it is a BLOCKER, otherwise CLEARED.
- Read every `S3-32 read grade.py` line: the penalty must be `earned - sum(|w| tripped)`, divided by the
  positive total, clamped with `max(0, ...)`, and gated to 0. A `.get(name, 0)` on a guard weight is a HIT only
  if the name can be missing from `test_weights.json` (the check above proves it cannot).
- Then prove it on a replay (S5-13).
- S3-33: the `S3-33 read` lines list every check from heaviest to lightest. Read them against the instruction and
  TRUTH.md for (d): the 5s should be the figures and red-line guards the task turns on, the 1s the bookkeeping.

## 9. Stage 4: rubric compliance, tests/judge.toml (8 min, strict)

The rubric is `tests/judge.toml`; it replaces `rubric.json` (a `rubric.json` is a BLOCKER, S1-32). This is
the most important stage: be strict and correct. A missing judge.toml is a BLOCKER (0 criteria, S4-18).

Weight scale (user decision 2026-10-19): a positive criterion weighs 1, 3 or 5; a negative criterion weighs
-1, -3 or -5. Floats of the same value (`3.0`, `-5.0`) are fine. Nothing else is allowed (S4-27).

Schema source (cite it in the report): harbor-rewardkit, the package that grades judge TOMLs. Read from the
installed package, never from memory: `pip download --no-deps harbor-rewardkit==<pinned> -d /tmp/qc/rk` and
unzip, then `rewardkit/models.py` (`JudgeTomlConfig`, `JudgeConfig`, `CriterionConfig`, `ScoringConfig`, all
pydantic `extra="forbid"`) and `rewardkit/reward.py` (`_validate_weights`, `aggregate_scores`). The version is
the one `tests/Dockerfile` pins in its `pip install` (or `tests/requirements.lock`, if present) (0.2.3 for the 2026-10 staging bundles; the judge-TOML models are
identical in 0.2.2 and 0.2.3; 0.2.1, current when Harbor 0.24.0 was released, lacked `type = "rubric"` and
`levels`). Allowed keys in 0.2.3:

- top level: `judge` (table), `criterion` (array of tables, at least 1), `scoring` (table). Nothing else.
- `[judge]`: `judge`, `model`, `version`, `files`, `mode` (`batched`|`individual`), `timeout` (int),
  `reasoning_effort`, `isolated` (bool), `cwd`, `reference`, `atif-trajectory`, `mcp_servers`, `weight` (float),
  `prompt_template`, `samples` (int >= 1), `guard` (`off`|`flag`|`penalize`).
- `[[criterion]]`: `description` (required), `type` (`binary`|`likert`|`numeric`|`rubric`, default `binary`),
  `name`, `id`, `points`, `levels` (`rubric` needs >= 2), `min`, `max`, `weight` (float, default 1.0), `files`,
  `negate` (bool), `optional` (bool), `annotations` (free-form table, not validated by rewardkit).
- `[scoring]`: `aggregation` (`weighted-mean` default, `weighted-sum`, `all-pass`, `any-pass`, `threshold`,
  `required-pass`), `threshold`. Negative weights raise unless `aggregation = "weighted-sum"`.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S4-07 | Note only: a criterion that reduces to an exact value, count, presence or absence, mime type, size, or field equality could be compiled into `test_outputs.py`. This no longer blocks (it conflicts with the 20-criterion rule); record it. | MINOR | read each description | FORGE 10f |
| S4-08 | No overlap with a compiled criterion: no judged criterion grades the same fact, record or field as a `test_outputs.py` check (double counting). | MAJOR | cross-reference table | RUTHLESS 2, Checklist X1, v4 S3-X1 |
| S4-09 | Atomic: one ask per criterion. No `and`/`or`/comma list joining two independent facts. | BLOCKER | read | v4 S3-J4/J5, Checklist M4 |
| S4-10 | Operational and decidable: no vague standard (`appropriate`, `reasonable`, `professional`, `clear`, `concise`, `tidy`, `courteous`, `tasteful`, `useful`, `good`, `well`) without a decision line a judge can apply to the evidence; no internal state (`understands`, `realises`). | BLOCKER | cmd S4-10 | v4 S3-J2/J3, Checklist M2/M3 |
| S4-11 | Grounded in `instruction.md` and `TRUTH.md`: every criterion grades something the instruction asked for (never a requirement the instruction did not state), and every figure or record it turns on appears in TRUTH.md and in the served world. | BLOCKER | search each needle | v4 S3-Q1/Q2, Checklist L1/L2 |
| S4-12 | No hint leak: no exact deliverable filename, no sentence lifted from the reference answer, no decoy adopted as correct. | MAJOR | read against TRUTH.md | v4 S3-J8/Q3, Checklist M6/L3 |
| S4-13 | Evaluable from the evidence the judge receives: `[judge].files` (plus any `criterion.files`) is non-empty and lists files `test.sh` writes BEFORE the judge step. In the Sample format those are `/tmp/agent_trajectory.json` (step 1: final message, calls with arguments) and `/logs/verifier/end_env.json` (step 3), as the S1-32 recipe sets them; any other path (for example a `judge_state.json`) must be built by a `test.sh` line before step 4. Every annotation `evidence` path is one of them, and the fact each criterion needs is in that file: a criterion with `evaluation_target = "final_answer"` needs the final message, one on `trajectory` needs the calls. A file that only exists after the judge runs, or that drops what a criterion needs, is a BLOCKER. | BLOCKER | cmd S4-18 (judge files line), read test.sh steps 1-4 | Sample, adaptation 2b |
| S4-16 | The rubric reaches the reward the way the format expects: `test.sh` step 4 feeds `/tests/judge.toml` (never `rubric.json`) to a TOML-reading judge whose package is installed in `tests/Dockerfile` (harbor-rewardkit pinned with `==`, or a CLI that parses TOML); writes `/logs/verifier/rubric_breakdown.json` with `score`, `rc`, `rb`, `per_criterion`; runs rewardkit on a scratch copy holding judge.toml alone, never over `/tests` (rewardkit would write its own reward file there); and on no key, judge error or zero verdicts writes NO breakdown (rubric unscored, dropped from the ledger), never a breakdown with score 0. | BLOCKER | read `test.sh` step 4, cmd S4-16 | Sample, adaptation 2c |
| S4-18 | Criterion count: fewer than 20 `[[criterion]]` rows (or no judge.toml) is a BLOCKER; 20-24 is a MINOR warning (non-blocking); 25 or more passes. | BLOCKER / MINOR | cmd S4-18 | user decision 2026-10-17 |
| S4-19 | judge.toml parses as TOML. | BLOCKER | cmd S4-18 | rewardkit `_load_toml` |
| S4-20 | Schema: only the rewardkit keys above, with the right types and enum values, at top level, in `[judge]`, `[[criterion]]` and `[scoring]`. | BLOCKER | cmd S4-18 | rewardkit `models.py` (extra="forbid") |
| S4-21 | Every criterion has a unique non-empty `id` (and `name = id`, since rewardkit names criteria from the description otherwise), a non-empty `description`, a numeric `weight` (not a string, not bool), `type = "binary"` (another rewardkit type is a MINOR note; a type outside rewardkit is a BLOCKER), and `annotations` carrying the old rubric.json fields `number`, `polarity`, `category`, `importance`, `evaluation_target` (a missing annotation field is a MAJOR). | BLOCKER | cmd S4-18 | rewardkit `CriterionConfig`, Sample rubric.json fields |
| S4-22 | No duplicate or paraphrased criteria (same fact asked twice in other words). | BLOCKER | cmd S4-18, then read | Checklist M5 |
| S4-23 | Weights: positive total > 0; no single criterion carries more than half the positive weight. | BLOCKER | cmd S4-18 | RUTHLESS 3.3 |
| S4-24 | Negative criteria are written and wired so the judge DEDUCTS them: (a) the weight is negative (-1, -3 or -5); (b) `annotations.polarity = "negative"` on every negative criterion (missing on a positive criterion is a MINOR note), and sign and polarity agree (a criterion with polarity negative and a positive weight, or the reverse, pays the run for the forbidden act); (c) the description states the forbidden behaviour as a fact that is TRUE when the run did it ("The run entered ... on the closed group"), never as its absence; (d) no `negate = true` on a negative-weight criterion (double negation) and no `annotations.type` containing "negative" (rewardkit sets `negate` from it silently); (e) the absolute negative total does not exceed the positive total; (f) `[scoring] aggregation = "weighted-sum"` (rewardkit raises otherwise). | BLOCKER | cmd S4-18, then read | rewardkit `_validate_weights`, user decision 2026-10-19 |
| S4-25 | `[verifier] environment_mode = "separate"` when judge.toml exists, so the judge never runs in the agent's container. | BLOCKER | cmd S1-12 | Harbor 0.24.0 `VerifierEnvironmentMode` |
| S4-26 | No answer leakage through the rubric: judge.toml is never agent-visible (S2-24), and criterion text adds no answer the agent could see. | BLOCKER | cmd S2-23 | leakage policy |
| S4-27 | Weight scale: every positive `weight` is 1, 3 or 5 and every negative `weight` is -1, -3 or -5. A 0, 2, 4, 0.5, 10 or a string is a BLOCKER. Report the count at each step. | BLOCKER | cmd S4-18 | user decision 2026-10-19 |
| S4-28 | **Negative criteria lower the rubric score.** The judge.toml -> `rubric_breakdown.json` converter in `test.sh` computes `rc` over the positive weights and `rb` over the ABSOLUTE negative weights (`abs()` or the polarity, never the raw signed sum mixed with positives), and `score = rc x (1 - rb)` cut to 2 places, as the Sample's `_compute_scores` does. Probe: all positives satisfied and no negative satisfied gives `score = 1.0`; then one -5 negative satisfied gives `rb = 5 / negative total` and the score falls to `cut(1 - rb)`. A score that does not fall, rises, or exceeds 1.0 is a BLOCKER. | BLOCKER | probe S4-28 | Sample `rubric_judge_cli._compute_scores`, user decision 2026-10-19 |

Commands for Stage 4:

```bash
source /tmp/qc/<uuid>-report/env.sh
# S4-18 .. S4-27  count, parse, schema, ids, weights, scale, polarity, duplicates, evidence (rewardkit 0.2.3 rules)
python3 - "$B/tests/judge.toml" "$B/tests/test.sh" <<'PY'
import math, re, sys, tomllib
try:
    d = tomllib.load(open(sys.argv[1], 'rb'))
except FileNotFoundError:
    print('S4-18 BLOCKER: no tests/judge.toml (0 criteria)'); sys.exit()
except tomllib.TOMLDecodeError as e:
    print('S4-19 BLOCKER: does not parse:', e); sys.exit()
J = {'judge': str, 'model': str, 'version': str, 'files': list, 'mode': str, 'timeout': int, 'reasoning_effort': str,
     'isolated': bool, 'cwd': str, 'reference': str, 'atif-trajectory': str, 'atif_trajectory': str, 'mcp_servers': list,
     'weight': (int, float), 'prompt_template': str, 'samples': int, 'guard': str}
C = {'description': str, 'type': str, 'name': str, 'id': str, 'points': int, 'levels': list, 'min': (int, float),
     'max': (int, float), 'weight': (int, float), 'files': list, 'negate': bool, 'optional': bool, 'annotations': dict}
ok = lambda v, t: not (isinstance(v, bool) and t in (int, (int, float))) and isinstance(v, t)
crit = d.get('criterion', []); n = len(crit)
print('S4-18 count', n, '->', 'BLOCKER (<20)' if n < 20 else 'MINOR (20-24)' if n < 25 else 'pass')
print('S4-20 top-level extra:', sorted(set(d) - {'judge', 'criterion', 'scoring'}) or 'none')
j = d.get('judge', {}); s = d.get('scoring', {})
print('S4-20 [judge] bad:', [k for k, v in j.items() if k not in J or not ok(v, J[k])] or 'none',
      '| [scoring] extra:', sorted(set(s) - {'aggregation', 'threshold'}) or 'none', '| aggregation:', s.get('aggregation', 'weighted-mean'))
files = j.get('files') or []
tsh = open(sys.argv[2]).read() if len(sys.argv) > 2 else ''
known = {'/tmp/agent_trajectory.json', '/logs/verifier/end_env.json'}      # Sample test.sh steps 1 and 3
print('S4-13 judge files:', files, '->', 'BLOCKER: empty' if not files else 'ok')
print('S4-13 BLOCKER judge files test.sh never names (nothing writes them):',
      [f for f in files if str(f) not in known and str(f) not in tsh] or 'none')
print('S4-13 VERIFY written before step 4:', [f for f in files if str(f) not in known and str(f) in tsh] or 'none')
ids, seen, pos, neg = set(), {}, [], []
for i, c in enumerate(crit):
    bad = [f'key {k}' for k in c if k not in C] + [f'type of {k}' for k, t in C.items() if k in c and not ok(c[k], t)]
    cid = c.get('id')
    if not isinstance(cid, str) or not cid.strip(): bad.append('no id')
    elif cid in ids: bad.append('duplicate id')
    ids.add(cid)
    if not str(c.get('description', '')).strip(): bad.append('empty description')
    w = c.get('weight')
    if not ok(w, (int, float)) or (isinstance(w, float) and not math.isfinite(w)): bad.append('weight not numeric')
    else:
        (pos if w > 0 else neg).append(w)
        if w not in (1, 3, 5, -1, -3, -5): bad.append(f'S4-27 weight {w} not in 1/3/5 or -1/-3/-5')
        ann = c.get('annotations') or {}
        pol = ann.get('polarity')
        if pol not in ('positive', 'negative'):
            bad.append(('S4-24 BLOCKER' if w < 0 else 'S4-24 MINOR') + f' polarity {pol!r} missing or not positive/negative')
        elif (w < 0) != (pol == 'negative'): bad.append(f'S4-24 sign/polarity mismatch: weight {w}, polarity {pol}')
        if c.get('negate') and w < 0: bad.append('S4-24 negate=true on a negative weight (double negation)')
        if 'negative' in str(ann.get('type', '')).lower(): bad.append('S4-24 annotations.type says negative (rewardkit sets negate)')
    if c.get('type', 'binary') not in ('binary', 'likert', 'numeric', 'rubric'): bad.append('type not in rewardkit')
    elif c.get('type', 'binary') != 'binary': bad.append('MINOR non-binary type')
    ev = (c.get('annotations') or {}).get('evidence') or []
    bad += [f'evidence {e!r} not received by judge' for e in ev if str(e).startswith('/') and e not in files + (c.get('files') or [])]
    key = ' '.join(re.findall(r'[a-z0-9]+', str(c.get('description', '')).lower()))
    if key in seen: bad.append(f'duplicate description of {seen[key]}')
    seen[key] = cid
    print(cid, w, c.get('type'), 'OK' if not bad else bad)
P, N = sum(pos), sum(abs(x) for x in neg)
print('S4-23 positive', P, 'max share', (max(pos) / P) if P else 'n/a', '(must be <= 0.5)')
print('S4-24 negative', N, '(must be <= positive)' if neg else '(none)',
      '| aggregation', s.get('aggregation', 'weighted-mean'),
      '-> BLOCKER: negatives need weighted-sum' if neg and s.get('aggregation') != 'weighted-sum' else '')
import collections
print('S4-27 weight scale', dict(sorted(collections.Counter(c.get('weight') for c in crit).items(), key=lambda kv: str(kv[0]))))
PY
# S4-09 / S4-10  read every description; these words need a decision line
grep -niE '\b(appropriate|reasonabl|professional|clear|concise|tidy|courteous|tasteful|useful|plausible|good|well|properly|adequate|quality|understands|reali[sz]es)' "$B/tests/judge.toml"
# S4-11 / S4-13  print each description beside the instruction's asks, then read
python3 -c "import tomllib,sys;[print(c.get('id'),'|',c.get('description')) for c in tomllib.load(open(sys.argv[1],'rb')).get('criterion',[])]" "$B/tests/judge.toml"
# S4-16  judge wiring
grep -nE 'rubric_breakdown|rubric\.json|judge\.toml|rewardkit|rubric_judge_cli|reward\.json|reward_producer' "$B/tests/test.sh"
```

S4-16 / S4-28, the judge.toml -> `rubric_breakdown.json` converter. Read step 4 of `test.sh` first (it must name
`/tests/judge.toml`, never `rubric.json`, and install its judge package in `tests/Dockerfile`), then feed it fake
verdicts. The probe runs test.sh's own converter code on a copy; nothing calls a judge.

```bash
source /tmp/qc/<uuid>-report/env.sh
grep -nE 'rubric\.json|judge\.toml|rewardkit|rubric_judge_cli|rubric_breakdown|reward-details' "$T/test.sh"
grep -nE 'pip install' "$T/Dockerfile"
cat > /tmp/qc/rubric_probe.py <<'PY'
# S4-28  feed fake verdicts through test.sh's own judge.toml -> rubric_breakdown.json converter
# usage: rubric_probe.py <tests dir> <work dir>
import json, os, re, shlex, subprocess, sys, tomllib
T, W = sys.argv[1], sys.argv[2]; os.makedirs(W, exist_ok=True)
sh = open(os.path.join(T, "test.sh")).read()
blocks = re.findall(r"python3 - ([^\n<]*?)<<'?(\w+)'?\n(.*?)\n\2\n", sh, re.S)
conv = [(args, body) for args, tag, body in blocks if "rubric_breakdown" in args + body and ("judge.toml" in args + body or "tomllib" in body)]
if not conv:
    sys.exit("S4-28 HIT: test.sh has no converter from judge.toml to rubric_breakdown.json (step 4 still reads rubric.json?)")
args, body = conv[0]
crit = tomllib.load(open(os.path.join(T, "judge.toml"), "rb"))["criterion"]
neg = lambda c: c["weight"] < 0 or (c.get("annotations") or {}).get("polarity") == "negative"
N = sum(abs(c["weight"]) for c in crit if neg(c))
probe = next((c for c in crit if neg(c) and abs(c["weight"]) == 5), next((c for c in crit if neg(c)), None))
def run(tag, tripped):
    det = {"judge": {"criteria": [{"id": c["id"], "name": c["id"], "value": 1.0 if (not neg(c) or c is tripped) else 0.0,
                                   "error": None, "reasoning": "probe"} for c in crit]}}
    dp, bp = os.path.join(W, tag + "_details.json"), os.path.join(W, tag + "_breakdown.json")
    json.dump(det, open(dp, "w"))
    argv = []
    for a in shlex.split(args.replace("$work/out/", "").replace("$LOGS/", "")):
        argv.append(dp if "details" in a else os.path.join(T, "judge.toml") if "judge.toml" in a else bp if "breakdown" in a else a)
    r = subprocess.run([sys.executable, "-", *argv], input=body, text=True, capture_output=True)
    try: return json.load(open(bp))
    except Exception: print("S4-28", tag, "converter failed:", (r.stderr or r.stdout)[-300:]); return {}
base = run("all_good", None)
print("S4-28 all positives met, no negative: score=%s rc=%s rb=%s (want 1.0)" % (base.get("score"), base.get("rc"), base.get("rb")))
if probe is None:
    print("S4-28 no negative criterion in judge.toml: nothing to deduct (S4-24 decides whether that is allowed)")
else:
    hit = run("one_negative", probe)
    import decimal
    want = float(decimal.Decimal(repr(1 - abs(probe["weight"]) / N)).quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_DOWN))
    ok = base.get("score") == 1.0 and hit.get("score") is not None and abs(hit["score"] - want) < 0.011
    print("S4-28 %s (w=%s) committed: score=%s rb=%s, expected %.2f -> %s" % (probe["id"], probe["weight"], hit.get("score"), hit.get("rb"), want,
          "ok, the negative is deducted" if ok else "HIT: negative NOT deducted properly"))
PY
python3 /tmp/qc/rubric_probe.py "$T" "$O/rubric_probe"
```

Expected: `score=1.0` with all positives met, then `ok, the negative is deducted`. "no converter" means the rubric
is never scored from judge.toml (S4-16 BLOCKER); a score that does not fall is S4-28 BLOCKER.

For S4-09 to S4-11 and S4-22 write one line per criterion in the report: id, verdict, and the reason
(for example "J1 BLOCKER S4-10: 'reads as a grower-facing settlement ... an order a grower can follow' has no
decision line; S4-09: deliveries, exclusions and deductions are three asks").

## 10. Stage 5: execution (20 min, mandatory)

Grader probes are the fast pre-check (seconds) and run first. The format's grader reads the run's trajectory, so `gt_env.json` alone cannot reproduce the oracle's 1.0; the probes test the ledger instead, by forcing check outcomes through the bundle's own `grade.py`. The oracle's real 1.0 is proven live (S5-10). The live Harbor runs (S5-10, S5-11) are mandatory BLOCKERs: a bundle whose oracle does not score exactly 1.0, or whose nop does not score exactly 0.0, on Harbor 0.24.0 FAILs. If Docker is unavailable the verdict is `PARTIAL` with S5-10/S5-11 under "Not checked", never `PASS`.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S5-01 | Ledger ceiling: with every goal check met and no guard tripped (forced), `grade.py` gives exactly 1.0 with the rubric unscored. | BLOCKER | probe `allgood` | tabish A1, v4 S3-O3 |
| S5-02 | No-op: an empty trajectory, seed state (`tests/old_env.json` as the snapshot) and an empty `/workspace` score exactly 0.0. | BLOCKER | probe `noop` | tabish C1/M1, v4 S3-O7 |
| S5-05 | No snapshot: with `ATLAS_END_ENV` missing, `grade.py` still writes a reward file (S3-03). | BLOCKER | probe `nosnap` | Sample |
| S5-06 | Determinism: the no-op probe run twice gives identical reward documents. | BLOCKER | probe `noop` + `noop2` | tabish D4 |
| S5-07 | Rubric on the ledger: with all checks met and a `rubric_breakdown.json` score of 0.5, reward = `(wA + 0.5 x wR) / (wA + wR)`; with no breakdown the rubric is dropped (S5-01 gives 1.0, not `wA / (wA + wR)`). | BLOCKER | probe `rubric_half`, `allgood` | Sample, adaptation 2a |
| S5-13 | **Negatives deducted.** From the all-met baseline, each negative check tripped alone lowers the reward to exactly `(P - abs(w)) / P` (P = positive total, rubric unscored), or to 0 when `gate.require_no_guards` is truthy (it gates every guard). | BLOCKER | probe `trip_*` | user decision 2026-10-19 |
| S5-14 | **State gate fires.** Only when `gate.require_state_exact` is set: the all-met plan with the state forced exact gives 1.0 (S5-01); forced `completion < 1` (a changed entity) or `misbehave > 0` (a drifted entity) gives exactly 0.0. A `state_channel.json` that reports `available: false` on the all-met run means the gate is inert (S3-35 MAJOR). | BLOCKER | probe `state_*` | Sample `grade.py` |
| S5-10 | Live executability: `harbor run` (Harbor 0.24.0) with the `oracle` agent on the bundle copy produces `verifier/reward.json` with `reward` exactly 1.0 (Channel A alone, judge keys unset), and no trial exception. | BLOCKER | live run below | user decision 2026-10-17 |
| S5-11 | Live null run: `harbor run` with the `nop` agent produces `reward` exactly 0.0 (a reward file must exist; a missing reward file or exception is a FAIL of this check, not a 0). | BLOCKER | live run below | user decision 2026-10-17 |
| S5-12 | Live rubric unscored, not zeroed: with judge keys unset the live verifier writes no `rubric_breakdown.json`, `reward_producer.json` says `channel_a_only`, and the oracle reward is Channel A's 1.0. | BLOCKER | live run below | Sample |

Grader probes (S5-01, S5-02, S5-05, S5-06, S5-07, S5-13, S5-14). The script copies the bundle to `$B.re`, points any
hardcoded `/tests` literal there (hard rule 10), sets the env vars the Sample's grader reads (`ATLAS_TRAJECTORY`,
`ATLAS_END_ENV`, `ATLAS_OLD_ENV`, `ATLAS_OUTPUT_ROOTS`, `AUTH_REWARD_PATH`, `AUTH_GRADE_REPORT`, `AUTH_STATE_PATH`,
`AUTH_RUBRIC_PATH`, `AUTH_CLAIMS_PATH`; add any other the bundle reads, see `grep environ`), unsets every
`*_API_KEY`, and forces check outcomes by patching `test_outputs` before `grade.py` runs. `$B` is never touched.

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/ledger_probe.py <<'PY'
# S5-01 S5-02 S5-05 S5-06 S5-07 S5-13 S5-14  probes of the bundle's own grade.py ledger (no fixtures, no judge, no Docker)
# usage: ledger_probe.py <bundle copy B> <out dir O>   -> works on B.re (any "/tests" literal redirected there)
import json, os, re, shutil, subprocess, sys
B, O = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
if len(sys.argv) == 5:                                     # child: patch checks, then run grade.py
    T, plan = sys.argv[3], json.loads(sys.argv[4])
    sys.path.insert(0, T); import test_outputs
    for name, val in plan.items(): setattr(test_outputs, name, (lambda v: (lambda *a, **k: v))(val))
    sys.argv = [os.path.join(T, "grade.py")]
    import runpy
    try: runpy.run_path(sys.argv[0], run_name="__main__")
    except SystemExit: pass
    sys.exit(0)
RE = B + ".re"; shutil.rmtree(RE, ignore_errors=True); shutil.rmtree(O, ignore_errors=True)
shutil.copytree(B, RE, ignore=shutil.ignore_patterns("trajectories", "trajectory", "__pycache__"))
T = os.path.join(RE, "tests")
for fn in os.listdir(T):
    if fn.endswith(".py"):
        p = os.path.join(T, fn); src = open(p).read()
        new = re.sub(r"(['\"])/tests(/|\1)", lambda m: m.group(1) + T + m.group(2), src)
        if new != src: open(p, "w").write(new); print("redirected /tests in tests/" + fn)
doc = json.load(open(os.path.join(T, "test_weights.json")))
comps = doc.get("components") or {}
W = (comps.get("traj_tests") or {}).get("tests") or {}
W = {k: v for k, v in W.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
P = sum(v for v in W.values() if v > 0)
wA = float((comps.get("traj_tests") or {}).get("weight") or 0); wR = float((comps.get("rubric") or {}).get("weight") or 0)
gate = doc.get("gate") or {}
gated = bool(gate.get("require_no_guards"))                # a flag: any tripped guard zeroes the reward
state_exact = bool(gate.get("require_state_exact"))
empty = os.path.join(O, "inputs"); os.makedirs(os.path.join(empty, "workspace"), exist_ok=True)
traj = os.path.join(empty, "empty_trajectory.json"); json.dump({"steps": [], "final_message": ""}, open(traj, "w"))
old_end = os.path.join(empty, "end_env.json"); shutil.copy(os.path.join(T, "old_env.json"), old_end)
def run(tag, plan=None, end=old_end, rubric=None):
    o = os.path.join(O, tag); os.makedirs(o, exist_ok=True)
    if rubric is not None: json.dump({"score": rubric, "per_criterion": [{}]}, open(os.path.join(o, "rubric_breakdown.json"), "w"))
    env = {k: v for k, v in os.environ.items() if not k.endswith("_API_KEY")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=T, ATLAS_TRAJECTORY=traj, MCPATLAS_TRAJECTORY=traj, COMPLEXMCP_TRAJECTORY=traj,
               ATLAS_END_ENV=end, ATLAS_OLD_ENV=os.path.join(T, "old_env.json"), ATLAS_OUTPUT_ROOTS=os.path.join(empty, "workspace"),
               ATLAS_WORKSPACE=os.path.join(empty, "workspace"), ATLAS_LOGS=o, ATLAS_TESTS=T,
               AUTH_REWARD_PATH=os.path.join(o, "reward_channel_a.json"), AUTH_GRADE_REPORT=os.path.join(o, "grade_report.md"),
               AUTH_STATE_PATH=os.path.join(o, "state_channel.json"), AUTH_RUBRIC_PATH=os.path.join(o, "rubric_breakdown.json"),
               AUTH_CLAIMS_PATH=os.path.join(o, "claims_coverage.json"))
    cmd = [sys.executable, os.path.abspath(__file__), B, O, T, json.dumps(plan)] if plan else [sys.executable, os.path.join(T, "grade.py")]
    r = subprocess.run(cmd, cwd=T, env=env, capture_output=True, text=True)
    open(os.path.join(o, "stdout"), "w").write(r.stdout + r.stderr)
    try: return json.load(open(os.path.join(o, "reward_channel_a.json")))
    except Exception: return None
def show(cid, tag, d, want, case=None):
    got = None if d is None else d.get("reward")
    ok = got is not None and abs(got - want) < 1e-4
    print("%-6s %-34s reward=%s expected=%.6f %s" % (cid, tag, got, want, "ok" if ok else "HIT (see %s/%s/stdout)" % (O, case or tag)))
    return ok
good = {k: v > 0 for k, v in W.items()}                          # every goal met, no guard tripped
if state_exact: good.update(_state_diff=[[], [], []], _state_misbehaved=[])   # and the state exact
show("S5-02", "no-op (seed state, empty run)", run("noop"), 0.0, "noop")
a, b = run("noop"), run("noop2")
print("S5-06  determinism (no-op twice)", "ok" if a == b else "HIT: rewards differ")
d = run("nosnap", end=os.path.join(empty, "missing_end_env.json"))
print("S5-05  no snapshot: reward file", "written ok" if d is not None else "HIT: no reward file")
show("S5-01", "all checks met, rubric unscored", run("allgood", good), 1.0, "allgood")
show("S5-07", "all checks met, rubric score 0.5", run("rubric_half", good, rubric=0.5), (wA + 0.5 * wR) / (wA + wR) if wA + wR else 0, "rubric_half")
bad = 0
for g in sorted(k for k, v in W.items() if v < 0):
    want = 0.0 if gated else max(0.0, (P - abs(W[g])) / P)
    bad += not show("S5-13", g[:34], run("trip_" + g, dict(good, **{g: True})), want, "trip_" + g)
print("S5-13 ", "every negative deducted" if not bad else "%d negative(s) NOT deducted" % bad)
if state_exact:
    try: avail = json.load(open(os.path.join(O, "allgood", "state_channel.json"))).get("available")
    except Exception: avail = None
    if not avail:
        print("S3-35  MAJOR gate.require_state_exact is inert: state_channel.json available=%s on the all-met run" % avail)
    else:
        show("S5-14", "state inexact (changed entity)", run("state_inexact", dict(good, _state_diff=[[], [], ["probe"]])), 0.0, "state_inexact")
        show("S5-14", "state misbehave > 0", run("state_misbehave", dict(good, _state_misbehaved=["probe"])), 0.0, "state_misbehave")
PY
python3 /tmp/qc/ledger_probe.py "$B" "$O"
```

Every line must end `ok`. On a HIT open `$O/<case>/stdout` and `$O/<case>/grade_report.md`, quote the failing
component or check, and name the relation. A no-op above 0.0 is seeded-state free credit (S3-21).

S5-10 to S5-12, live Harbor 0.24.0 runs. The flags below were read from `harbor run --help` (0.24.0):
`-p/--path` task dir, `-a/--agent` (`oracle`, `nop` are built in: `harbor/models/agent/name.py`), `-e/--env docker`,
`-o/--jobs-dir`, `--job-name`, `-n/--n-concurrent`, `-y/--yes`, `--cpus` / `--memory` enforcement policy
(`auto|limit|request|guarantee|ignore`).

Docker preflight:

```bash
docker context ls                       # colima or Docker Desktop
docker info --format 'cpus={{.NCPU}} mem={{.MemTotal}}'
df -h / ; docker system df             # need >= 20 GB free
# only if space is short: prune builder cache, dangling images, anonymous volumes. Nothing else.
docker builder prune -f ; docker image prune -f ; docker volume prune -f
```

Registry images (Sample format): task.toml pins `docker_image` / `light_servers_image` to a private ECR registry.
Harbor 0.24.0 pulls `docker_image` unless `--force-build` is passed (`should_use_prebuilt_docker_image` in
`harbor/environments/docker`); with it Harbor builds `environment/Dockerfile`, and the compose files default to the
public-base `Dockerfile` (not `Dockerfile.ecr`) for light-servers and the verifier. So always pass `--force-build`
(it changes no grading). If a build still fails on ECR access, the live checks are Not checked (PARTIAL); never
drop `docker_image` from the copy to make it run. VERIFY: the agent's `allowlist` network needs Harbor's egress
sidecar image; if `harbor run` fails on it, record the exact error and mark S5-10/S5-11 Not checked.

Two host facts found on slot 29 (2026-10-17):

- The task asks for `cpus = 8` / `memory_mb = 12288`. On a smaller VM `--cpus auto` becomes a hard limit and
  `docker compose up` fails, so pass `--cpus ignore --memory ignore` (this changes no grading).
- With colima (and any VM that shares only `$HOME`), bind mounts of `/tmp/...` resolve inside the VM: the
  trial's `/logs/agent`, `/logs/artifacts` and `/logs/verifier` come back empty and Harbor reports
  `RewardFileNotFoundError`. Put the jobs dir under `$HOME`, outside YUJI (example
  `~/.cache/yuji-qc/jobs`). This is the one write outside `/tmp/qc`.

Run in tmux (long timeout; each run took 30-45 s with cached images):

```bash
source /tmp/qc/<uuid>-report/env.sh
J="$HOME/.cache/yuji-qc/jobs"; mkdir -p "$J"
cat > /tmp/qc/$UUID-report/live.sh <<EOF
#!/bin/bash
unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN OPENAI_API_KEY GEMINI_API_KEY
export UV_TOOL_DIR=/tmp/qc/uvtools UV_CACHE_DIR=/tmp/qc/uvcache
for a in oracle nop; do
  s=\$(date +%s)
  uv tool run --from harbor==0.24.0 harbor run -p "$B" -a "\$a" -e docker --force-build --cpus ignore --memory ignore \\
    -n 1 -o "$J" --job-name "$UUID-\$a" -y > "/tmp/qc/$UUID-report/run_\$a.log" 2>&1
  echo "\$a rc=\$? secs=\$(( \$(date +%s) - s ))" >> "/tmp/qc/$UUID-report/live_times.txt"
done
echo ALLDONE >> "/tmp/qc/$UUID-report/live_times.txt"
EOF
tmux new-session -d -s "qc-$UUID" "bash /tmp/qc/$UUID-report/live.sh"
# later:
cat "/tmp/qc/$UUID-report/live_times.txt"
for a in oracle nop; do cat "$J/$UUID-$a"/*/verifier/reward.json; tail -3 "$J/$UUID-$a"/*/exception.txt 2>/dev/null; done
cat "$J/$UUID-oracle"/*/verifier/reward_producer.json; ls "$J/$UUID-oracle"/*/verifier/rubric_breakdown.json 2>/dev/null || echo "rubric unscored (expected with keys unset)"; tail -25 "$J/$UUID-oracle"/*/verifier/grade_report.md
```

Where to read results: `<jobs>/<job-name>/<trial>/verifier/reward.json` (the reward),
`reward_channel_a.json` and `grade_report.md` (the ledger, missed checks, tripped guards), `reward_producer.json`, `rubric_breakdown.json` (absent when unscored),
`junit.xml` / `pytest-stdout.txt` (the pytest view; guards are inverted there: a guard that FAILS means the run
behaved), `ctrf.json`; `<trial>/exception.txt` for a trial error; `<trial>/artifacts/logs/artifacts/atlas/end_env.json`
for the captured state. Quote failures verbatim in the report. When the oracle is below 1.0, read `grade_report.md` (missed checks, tripped guards) and `pytest-stdout.txt` in the trial's verifier dir and name the failing check. A diagnostic variant (for example a copy without an unpullable `docker_image`) may be run to localise a failure; label it diagnostic, it never clears S5-10.

Never run CRUCIBLE from this skill.

## 11. Verdict rules

- Any BLOCKER: `FAIL`.
- Any MAJOR: `FAIL`, unless the operator records a waiver in the report (who, which ID, why).
- MINOR and VERIFY never block.
- Time ran out before every BLOCKER-severity check was done: `PARTIAL`, with the unchecked IDs listed.
- `FAIL` takes priority over `PARTIAL`: if any BLOCKER (or unwaived MAJOR) was already found, the verdict is `FAIL` even when time ran out; still list the unchecked IDs.
- The live checks S5-10 to S5-12 are BLOCKER checks. If Docker or Harbor 0.24.0 is missing they are "Not checked" and the verdict is at best `PARTIAL`.
- A rubric with 20-24 criteria is a MINOR warning and never blocks on its own.
- Otherwise: `PASS`.

A PASS here means only that this QC found nothing in its five areas. It does not say the task is hard.

## 12. Report template

Write exactly this shape to `/tmp/qc/<uuid>-report/qc_report.md`.

```markdown
# QC report: <bundle uuid>

- Task name: <task.toml [task] name>
- QC skill version: yuji-task-qc 0.4.1
- Harbor: <version>, validate/run commands used
- Start (UTC): <yyyy-mm-ddThh:mm:ssZ>
- End (UTC): <yyyy-mm-ddThh:mm:ssZ>
- Elapsed: <mm:ss>
- Copy inspected: /tmp/qc/<uuid>
- VERDICT: PASS | FAIL | PARTIAL

## Fact sheet
<the table from Stage 0, filled in>

## Stage results
| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | VERIFY | Clean checks |
|---|---|---|---:|---:|---:|---:|---:|
| 0 | Fact sheet | done / partial | - | - | - | - | - |
| 1 | Structure and task.toml | PASS / FAIL / PARTIAL | | | | | |
| 2 | Instruction, world, leaks | | | | | | |
| 3 | Deterministic grading | | | | | | |
| 4 | Rubric (judge.toml) | | | | | | |
| 5 | Execution (ledger probes + live oracle/nop) | <oracle reward> / <nop reward> | | | | | |

## Findings
### [<ID>] <one-line defect>
- Severity: BLOCKER | MAJOR | MINOR | VERIFY
- Where: <file:line, or file -> key path, or fixture name>
- Evidence: "<quoted text, value or command output>"
- Why: <what a correct run loses, or what the bundle gives away>
- Fix: <the exact change: the line as it should read, the key to delete, the file to regenerate. If it is a design decision, say so.>

(repeat, BLOCKERs first, then MAJOR, MINOR, VERIFY)

## Waivers
- <ID>: waived by <operator>, reason: <text>   (or "none")

## CLEARED
- <ID>: <what was checked and why it is not a finding>

## Not checked
- <ID>: <reason: time, tooling, missing reference>   (or "none")

## Steering note for FORGE
1. <design-level instruction, one per line, written so the operator can paste it.
   Name the file and the intent, not the QC ID internals. No CRUCIBLE content,
   no audit content, no scores from any run.>
2. ...
```

Rules for the steering note:

- Write it as instructions about the design: "Move the attendee-count check from judge.toml into test_outputs.py as a weighted check", not "S4-07 failed".
- One instruction per BLOCKER or MAJOR. Group MINORs into one line.
- Never include CRUCIBLE output, audit content, verdict text, or anything from `.audit/`.
- Never include secrets or key values.

## 13. Dropped and why

| Dropped or inverted check | Source | Why |
|---|---|---|
| Pytest grades only tool calls; no state, file-content, agent-text or final-message checks (and 0.2.0's reverse rule: state only, never the trajectory) | RUTHLESS C1-C5; Checklist Rule 4, V1-V5, D1-D4, B1-B5, C1, J1 | Both withdrawn in 0.4.0. The Sample grades the rebuilt trajectory, the final message, the delivered `/workspace` files and the snapshot (2b). Trajectory-based checks get the same hygiene as any other (S3-10 to S3-30). |
| Audit-log endpoint and grader-traffic checks | Checklist E1, E4, J3, W4 | Dropped. No audit log is graded. |
| Reporting gates on the final message | v4 S3-N1-N6 | Not imported. The final message is graded by ordinary weighted checks and judge criteria, never by a separate gate. |
| rubric.json schema and craft (K, Q, J, C, P) | v4 S3 Part 2; Checklist K-P | Replaced by judge.toml checks (Stage 4). A rubric.json in the bundle is now a BLOCKER (S1-32). |
| v4 reward_channel_a.json wA/wB two-channel formula, v4 grade.py gates | v4 S3-L1-L15, F1-F18, W1-W10 | Different formula. This layout's grade.py and test_weights.json are checked by S3-25, S3-32 and S5-13 instead. |
| v4 oracle.json / old_env.json / gt_env.json diff formulas | v4 S3-O5, O11-O13; S4-FC3, FC11, FC12 | The files are in the format (2e); the v4 diff rules are not. The ledger probes (Stage 5) and the live oracle run cover the same ground. |
| Golden Steer Flow ten-section TRUTH.md | v4 S4-TR1-TR15 | TRUTH.md is generated by recompute.py; its banner and drift checks were Trinity-owned and are removed. |
| Reference compose shape, `ENABLED_SERVERS: ""`, headroom flag, `extra_hosts` | v4 S4-DF2, DF4, DF12, DF13 | Superseded by Std §10.3 and §10.5. |
| Agent timeout 86400, verifier 300, cpus/memory constants | v4 qc_constants.env, S2-RS1-RS4 | Superseded by Std §10.8 (3600 / 1800). |
| Server floor 15 wired / 14 distractors; 20 attachments | v4 S2-SV5, CP14 | Not in the standard. Raise as a maintainer question if wanted. |
| `trajectories/` forbidden; any check of the trajectories folder | v4 S4-FC1b | The Sample ships `trajectories/`; it is allowed and never checked (user decision 2026-10-19). |
| Fixtures: S5-03 (control-*), S5-04 (alternate-*), S5-08 (grounding controls = fixture dirs); fixture forms of S5-01, S5-02, S5-05 | FORGE 10, 10a; tabish C3 | Removed 2026-10-19: not part of the format. A shipped `fixtures/` is now flagged for removal (S1-34). S5-01/02/05/06 are ledger probes. S5-03, S5-04, S5-08 are retired, not reused. |
| Model identity across run files | qc2 §1 | Output-bundle check. Nothing is run here. |
| Score sanity on a run, truncation, blind judge | qc2 §1.5 | Output-bundle check. |
| pass@k aggregates, failure breakdown | qc2 §1.6 | Output-bundle check, multi-run. |
| Environment vs model failure buckets | qc2 §2 | Output-bundle check. |
| Thinking signatures | qc2 §3 | Output-bundle check. |
| Weighted overlap score (Jaccard formula) | qc2 §4 | Replaced by the plain overlap check S4-08. |
| State-only deliverable: "move the /workspace output into a Light app record graded against oracle.json" | 0.2.0/0.3.0 S3-01, S3-02 | Withdrawn in 0.4.0. The Sample grades files the run delivers under `/workspace`; a file deliverable is never a finding. |
| Every check formerly Scope `T-code` or `T-contract`: S1-02, S1-03, S1-04, S1-05, S1-07, S1-18, S1-20, S1-21, S1-22, S1-23, S1-24, S1-25, S1-26, S1-29, S2-07, S3-06, S3-07, S3-08, S3-09, S4-01, S4-02, S4-03, S4-04, S4-05, S4-06, S4-14, S4-15, S4-17, S5-09 | `YUJI-QC-check-classification.md` | Removed 2026-10-17 by user decision: owned by Trinity tools, contract or seal, not by this QC. IDs are retired, not reused. The "Trinity advisories" report section and ADVISORY verdict rule are removed with them. |
| "Deterministically reducible must be compiled" BLOCKER | FORGE 10f | Downgraded to the MINOR note S4-07: it conflicts with the 20-criterion rubric rule. |
| Stubbed-MCP oracle (emit.py), its foils and the M-ladder | tabish run_qc.sh, A1, E5, C1, M1-M8 | Its oracle never starts servers; reads return `old_env` and writes return `ok`. That is not evidence that the real apps accept the writes. Real evidence is the replay through the bundle's own grade.py (Stage 5) or a Harbor run. |
| Mean-reward push policy (at most 0.20), at least 21 servers | tabish Tier-3, M7 | Difficulty and batch policy, not authoring correctness. |
| Hardness run | v4 README, hardness_qc | Difficulty evidence. Out of scope by design. |

| Std §10 constants that contradict the Sample: no `docker_image`/`light_servers_image`, agent `network_mode = "public"`, invalid trial = exit 3 with no reward, judge OFF the reward writing `rubric_score.json`, fixed session ids declared in world_data/grounding.yaml, state_capture never reading `/logs/agent` | Std §5, §10.6, §10.7, §10.9, §10.10 | Replaced 2026-10-19 by the Sample (user decision): images pinned by digest (S1-06), agent allowlist (S1-12), missing snapshot still scored (S3-03), rubric ON the ledger (2a, S4-16), state_capture finds the agent's sessions from `/logs/agent` (S1-17). Light apps mint `session_{uuid()}`, so fixed session ids cannot exist. |
| grounding.yaml, recompute.py, policy.yaml, GRADING.md as bundle files | FORGE authoring outputs | Not in the format; flagged for removal (S1-01). Their facts are read from TRUTH.md, task.toml metadata, oracle.json and test_outputs.py. |

## 14. Notes for maintainers

1. **Reference sample path.** S1-10 uses `REF`. Setup takes `REF` from the environment, else finds `yuji/samples/974d1442-*` next to the bundle's checkout or under `$HOME`, and stops if none is found (it never runs S1-10 without a reference). `92024c97` and `bd42b923` have the same light-servers tree, so `REF` may point at either. The canary GUID line in `light-servers/Dockerfile*` differs per task and is ignored.
2. **Rubric source version.** S4-20 reads harbor-rewardkit from the version `tests/Dockerfile` pins (0.2.3 on 2026-10-19). If the pin moves, re-read `rewardkit/models.py` before trusting the key list in section 9.
3. **Docker host.** Live runs need the Harbor jobs dir on a path the Docker VM mounts (under `$HOME` on colima), and `--cpus ignore --memory ignore` on hosts smaller than the task's declared resources.
4. **Conflicts found while drafting.**
   - The standard requires every Light app in `ENABLED_SERVERS`. The v4 pack required it empty. This skill follows the standard.
   - The standard gives `/logs/artifacts/` for `end_env.json` without a full filename. This skill uses the Sample's `/logs/artifacts/atlas/end_env.json` (`ATLAS_END_ENV`).
5. **0.3.0 changes (2026-10-19; superseded by 0.4.0 below wherever they differ).** Layout of section 2e is the structure checked (S1-01, S1-32: judge.toml in
   place of rubric.json). Fixtures dropped (S5-03, S5-04, S5-08 retired; replay uses gt_env/old_env). The
   trajectory folder is never checked. judge.toml weights are 1/3/5 and -1/-3/-5 (S4-27) and negatives must be
   negative-weighted with matching polarity (S4-24). The pytest negatives must be deducted by grade.py (S3-32,
   proven by S5-13). `test_weights.json` uses the same 1/3/5, -1/-3/-5 integer scale with guards negative and every
   check rated (S3-33). `provenance.yaml` / `provenance.sig` are not part of the bundle; present = MAJOR (S1-33).
6. **0.4.0 changes (2026-10-19).** The format is `yuji/samples/974d1442-...` with `tests/rubric.json` replaced by
   `tests/judge.toml` (section 2e, S1-01). task.toml values follow the Sample (S1-06, S1-12 to S1-17, S1-35).
   Fixtures and provenance files are flagged for removal (S1-33, S1-34). The rubric is on the ledger (2a); its
   converter must deduct negatives (S4-28) and the component weights must equal the mean absolute weights
   (S3-34). Grading the trajectory is by design (2b). Stage 5 probes the ledger instead of replaying gt_env.
   S1-10 ignores the per-task canary GUID line; setup finds `REF` (974d1442) or stops (note 1).
7. **0.4.1 fixes (2026-10-19, external review).** The S1-32 recipe points `[judge] files` at the evidence test.sh
   already writes (`/tmp/agent_trajectory.json`, `/logs/verifier/end_env.json`), not an unwritten
   `judge_state.json`, and S4-13 checks the same paths. 2a's component-weight rounding matches S3-34. Gates follow
   `grade.py`: `require_no_guards` is a flag (S3-32, S5-13 no longer iterate it), and `require_state_exact` is
   checked for being live (S3-35) and proven (S5-14). `REF` no longer defaults to one machine's path.

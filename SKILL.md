---
name: yuji-task-qc
description: Use this skill when a tasker wants an author-side quality check of ONE Yuji light-servers task bundle before that bundle is sent on. The bundle must have exactly the format of the reference sample 5b10675f-e16b-5f22-ae7f-d8040f6324c4 (tests/reward/ with reward.toml, pytest/ledger.py and a compiled rubric/judge.toml; no tests/grade.py, no top-level tests/judge.toml, no rubric.json); fixtures and provenance files are flagged for removal and the trajectories/ folder is never checked. It works on a copy under /tmp/qc and checks: the task itself (instruction, world and task data, grading soundness, bundle format and harness files identical to the sample; task data must be textual only: plain text, text-only .docx and text-only .svg), Harbor 0.24.0 compatibility, reward leakage, executability (ledger probes, live oracle exactly 1.0, nop exactly 0.0, no guard tripped on either) and strict rubric compliance of tests/reward/rubric/judge.toml (at least 20 criteria, harbor-rewardkit schema, source weights 1/3/5 and -1/-3/-5, compiled weights normalised, tagged, decidable, grounded). It proves negatives are deducted in test_weights.json (with the declared guard_polarity) and in the rubric score. It writes one qc_report.md with a PASS, FAIL or PARTIAL verdict and a steering note. Do not use it to measure difficulty, to QC model output bundles, or as a pipeline gate.
---

# Yuji task QC (0.6.0)

QC skill version: `yuji-task-qc 0.6.0`. Write this string into every report.

## 1. Purpose and status

This is author-side feedback. A tasker runs it with a coding agent on one bundle before the bundle is sent on. It includes live Harbor oracle and nop runs, so it takes longer than the old 20-minute pass (see section 4).

What it is not:

- It is not evidence of difficulty. Nothing here measures how hard the task is.
- It is never a gate. No pipeline step may read its output as a pass condition.

How findings are used. The operator reads the report and relays the "Steering note for FORGE" section to the active FORGE run as plain design instructions. The QC agent never talks to FORGE and never edits the bundle.

Scope. This QC checks only: (1) the task itself: instruction, world and task data, grading soundness, and the bundle format of section 2c; (2) Harbor 0.24.0 compatibility; (3) reward leakage; (4) task executability (ledger probes, live oracle 1.0, nop 0.0); (5) rubric compliance of `tests/reward/rubric/judge.toml`, the most important and the strictest part. IDs are never renumbered; retired IDs are listed in section 13 and are not reused.

**The format (user decision 2026-10-23: strictly the sample).** A bundle must have the format of the reference
sample `5b10675f-e16b-5f22-ae7f-d8040f6324c4` (task, environment, tests and solution files; its `trajectories/`
folder is never used). Section 2 describes it. Every rule in this skill is written to match that sample. A rule from
an older source that the sample contradicts has been removed, not kept beside it (section 13 lists what went and
why). The earlier format (`tests/grade.py`, `tests/_judge/`, top-level `tests/judge.toml`, `rubric_breakdown.json`) is
not accepted: its files are flagged as not in the format (S1-01).

Out of scope:

- **Fixtures.** The format has no `tests/fixtures/`. A bundle that ships one is flagged: remove it (S1-34, MAJOR).
- **Provenance.** The format has no `provenance.yaml` / `provenance.sig`. Present = flagged: remove them (S1-33, MAJOR).
- **The `trajectories/` folder.** Probe-run output is never opened, scanned or judged. It is left out of every `find` and `grep` in this skill and is never a finding. (This is the folder only: the format's grader reads the run's rebuilt trajectory by design, see 2b.)
- **Non-textual task data.** `environment/light-servers/task_data/` may hold textual data only: any plain-text file, text-only `.docx` Word documents, and images as text-only `.svg` (the sample ships exactly these). Anything else is not accepted and is flagged (S2-25, BLOCKER).
- **grounding.yaml.** The format has no `solution/grounding.yaml`. Read the facts from `solution/TRUTH.md`, `task.toml [task.metadata]` (`decoy_records`, `wrong_figures`, `stump_levers`, `grading`, `scenario.trap`, `difficulty_explanation`, `verification_explanation`), `tests/oracle.json` (`oracle`, `reported`, including `reported.claims`) and `tests/test_outputs.py` instead.

Sources folded in (cited in the "from" column of every catalog):

| Tag | Source |
|---|---|
| Sample | the format reference `5b10675f-e16b-5f22-ae7f-d8040f6324c4` (task, environment, tests and solution files only) |
| Std §n | `Task-structure-standard.md` (section 10 is the checklist); the Sample wins where they disagree |
| FORGE n | `trinity/forge/phase-build.md` items 8, 9, 10, 10a, 10e, 10f, 11, 11a |
| v4 Sn-X | `Updated_QC_MCP_v4` pack, stage n, code X |
| RUTHLESS n | `RUTHLESS_QC.md` section n |
| Checklist X | `QC_CHECKLIST_pytest_rubric.md` code X |
| tabish X | tabish `QC/qc.md` code X |
| qc2 §n | `qc (2).md` (output-bundle QC; mostly dropped, see section 13) |

Where the Sample and an older source disagree, the Sample wins and the older rule is removed. Where the Sample is silent, the standard applies; where both are silent and FORGE speaks, FORGE applies. Anything still unclear is marked VERIFY and goes to the maintainers. A check that would flag the Sample itself is wrong and must not be reported.

## 2. The format (read before the catalog)

### 2a. The reward: two channels mixed by reward.toml

Read from the Sample's `tests/test.sh`, `tests/reward/**` and `tests/test_weights.json`:

- **Pytest channel.** `tests/reward/pytest/ledger.py` imports `test_outputs`, calls every check named in
  `test_weights.json` (`components.traj_tests.tests`, or top-level `tests`) and scores
  `pytest = max(0, (earned positive weight - charged guard weight) / total positive weight)`. It writes
  `/logs/verifier/grade_report.json` (`reward`, `earned`, `penalty`, `total_positive`, `guard_polarity`, `gate`,
  `missed`, `guards_tripped`, `errors`, `tests`). It reads `ATLAS_TESTS_DIR` (default `/tests`) and
  `ATLAS_VERIFIER_LOGS` (default `/logs/verifier`), so it runs standalone.
- **Verdicts.** By the check's `verdict_style`: `return` passes on a truthy return and FAILS on `None`; `assert`
  passes by not raising; `mixed` passes on a truthy explicit value or by falling off the end after its asserts held;
  `none` (neither asserts nor returns a value) never passes. A check that raises fails with its reason recorded. A
  weight name with no function in `test_outputs.py` fails.
- **Guard polarity.** `test_weights.json guard_polarity` is `fail_charges` (default: a guard is charged when it
  FAILS) or `pass_charges` (charged when it PASSES; the Sample uses this, and every `test_guard_*` asserts or returns
  true when the forbidden act shows). Any other value makes the ledger raise. A polarity that does not match how the
  guards are written inverts every guard. The `max(0, ...)` clamp still gives the nop run exactly 0.0, so the live
  nop cannot catch the inversion; S3-36 and the no-op probe do.
- **Gates.** `ledger.py` reads only `gate.require_no_guards` (truthy: any tripped guard zeroes the pytest channel)
  and `gate.floor` (a number: a score below it becomes 0). The Sample has no gate.
- **Rubric channel.** `tests/reward/rubric/judge.toml` is compiled by the harness from the author's rubric ("do not
  edit, edit the source"). Each criterion keeps the author's weight in `annotations.source_weight` (1/3/5 or
  -1/-3/-5); its `weight` is `source_weight / total_positive_weight`, signed, so the positive weights sum to 1.0.
  `[scoring] aggregation = "weighted-sum"`, so the channel is `(satisfied positive - committed negative) / positive
  total` and can be negative. test.sh step 5 clamps a negative rubric to 0 (`rubric_unclamped` keeps the raw value)
  and recombines the channels with the `reward.toml` weights.
- **Mixing.** `tests/reward/reward.toml` has one `[[reward]]`: `name = "reward"`, `aggregation = "weighted-mean"`,
  `weights = { pytest = 0.5, rubric = 0.5 }` (harness policy, not the author's). The `components.*.weight` values in
  `test_weights.json` are not read by `ledger.py` or rewardkit; they document the ledger (S3-34).
- **Unscored rubric.** No `JUDGE_MODEL`, no judge login, `JUDGE_SKIP=1`, no `rubric/judge.toml`, a rewardkit error,
  a judge time-out, or every criterion errored: the rubric is dropped and never scored 0. test.sh writes
  `reward.json = {"pytest": x, "reward": x}`, `rubric_judge_failed.txt` (the reason), `judge.json` with `ran: false`,
  and `reward_producer.json` with `channels: ["pytest"]`, `weights: {"pytest": 1.0}`. If the pytest ledger itself
  fails, test.sh exits 1 and writes no reward.
- **Negatives are deducted in both channels.** A tripped guard subtracts its absolute weight in the ledger (S3-32,
  proven by S5-13); a satisfied negative criterion lowers the weighted sum (S4-28). A negative that is never
  subtracted rewards the forbidden act.

### 2b. What the reward may read

The format grades the run, not only the final state. `tests/test.sh` step 1 rebuilds a `{steps, final_message}`
trajectory from `/logs/agent` (`claude-code.txt` / `oracle.txt` stream-json, Harbor's ATIF `trajectory.json`, or
OpenAI-shaped logs) into `/tmp/agent_trajectory.json` and exports it as `ATLAS_TRAJECTORY`. The checks may read: that
trajectory and its final message, the files the run delivered under `/workspace` (collected by `artifacts`), the
captured snapshot (`ATLAS_END_ENV`, copied to `/logs/verifier/end_env.json`), the servers' tool-call log
(`ATLAS_SERVER_LOG`, copied to `/logs/verifier/server_tool_calls.log`), `tests/old_env.json` and `tests/oracle.json`.
The judge reads `judge_ws/` (2d). Grading the rebuilt trajectory is by design and is never a finding. The reward must
NOT read `solution/**`, `TRUTH.md`, the `trajectories/` folder, or anything the agent can see that holds the answer.

### 2c. Bundle format (the structure every bundle is checked against)

```
<uuid>/
  task.toml
  instruction.md                 first line: <!-- instruction-canary <uuid> -->
  environment/
    Dockerfile  docker-compose.yaml  state_capture.py
    light-servers/   Dockerfile Dockerfile.ecr entrypoint.sh filesystem_server.py health_check.py
                     requirements.txt server_main.py sitecustomize.py
                     servers/ software/ task_data/ world_data/
  tests/
    .dockerignore  Dockerfile  Dockerfile.ecr  docker-compose.yaml
    claims_lib.py                shared claim, trajectory and number helpers for test_outputs.py
    ctrf_pytest_plugin.py        pytest -> ctrf.json report (same verdict rule as the ledger)
    test.sh                      verifier entrypoint (5 steps, 2e)
    test_outputs.py              the weighted pytest checks (goals and test_guard_* guards)
    test_weights.json            components traj_tests + rubric, weights 1/3/5 and -1/-3/-5, guard_polarity
    old_env.json  oracle.json    seed snapshot; oracle calls and reported figures (incl. claims)
    reward/
      reward.toml                mixes the channels
      pytest/ledger.py           the weighted ledger over test_outputs.py
      rubric/judge.toml          the rubric, compiled (2a)
      rubric/prompt.md           the judge prompt template ({criteria})
      rubric/instruction.md      byte-identical copy of instruction.md
  solution/
    TRUTH.md  gt_env.json  solve.py  solve.sh
  trajectories/                  probe runs: allowed, NEVER checked
```

- Every file above is required. A missing one is a BLOCKER (S1-01); a missing `tests/reward/rubric/judge.toml` is
  also 0 criteria (S4-18).
- Any `rubric.json` is a BLOCKER (S1-32).
- `task_data/` holds textual data only (S2-25).
- `tests/fixtures/` present: MAJOR, remove it (S1-34). `provenance.yaml` / `provenance.sig` present: MAJOR, remove them (S1-33).
- Any other file not in the tree is MAJOR, not part of the format, remove it (S1-01). This includes the earlier
  format's `tests/grade.py`, `tests/_judge/`, a top-level `tests/judge.toml`, and `grounding.yaml`, `recompute.py`,
  `policy.yaml`, `GRADING.md`, `gradelib.py`, `requirements.lock`, `environment/Dockerfile.ecr`, notes. A waiver may
  keep one if the operator records why.
- The harness files are the Sample's, byte for byte apart from the canary lines and the per-task values the harness
  fills in (S1-37).

### 2d. task.toml, environment and judge (the Sample's values)

- `task.toml` is built by the harness: a fixed header (everything before `[task]`), then the author's `[task]` and
  `[task.metadata]` blocks, then the generated `[[environment.mcp_servers]]` list. The header carries:
  `schema_version = "1.4"`; `artifacts` `/logs/agent` (exclude `./completions`) and `/workspace` (exclude `./data`);
  `[agent] timeout_sec = 3600`, `network_mode = "public"`, `user`; `[verifier] environment_mode = "separate"`,
  `timeout_sec = 1800`, `user`; `[verifier.env]` `JUDGE_MODEL`, `JUDGE_TRANSPORT`, `CODEX_AUTH_B64`,
  `CLAUDE_CODE_OAUTH_TOKEN` (from `${JUDGE_CLAUDE_TOKEN:-}`), `ATLAS_END_ENV = "/logs/artifacts/atlas/end_env.json"`;
  `[verifier.environment]` `workdir = "/tests"`, `build_timeout_sec`, resources, `network_mode = "public"`;
  `[[verifier.collect]]` `service = "main"`, `command = "python3 /harness/atlas/state_capture.py"`, `timeout_sec = 300`;
  `[environment]` resources and `network_mode = "public"`, with NO `docker_image` / `light_servers_image` (Harbor
  builds from the Dockerfiles; every base image and compose image default is digest-pinned).
- `[task.metadata]` in the Sample: `category`, `subcategory`, `tags`, `capability_level`, `stump_levers`, `seed`,
  `apps`, `mcp_servers`, `decoy_records`, `wrong_figures`, `attachments` (one `{type, path}` per `task_data/` file),
  `dimensions`, `expert_time_estimate_hours`, `authoring_date`, `upstream_provenance`, `gradeable`,
  `grader = "weighted"`, `grading`, `gt_env_status`, `components`, `difficulty_explanation`,
  `verification_explanation`, and `[task.metadata.scenario]` `summary`, `output_shape`, `pivot`, `trap`.
- Compose: services `main` and `light-servers`; volumes `workspace_data` and `light_logs`. `light_logs` is mounted
  read-write in `light-servers` at `/var/log/light-servers` and read-only in `main` at `/harness/light-logs`, so the
  agent cannot alter what the servers recorded. `main` has `extra_hosts: host.docker.internal:host-gateway`.
  `light-servers` sets `COMPLEXMCP_SEED` and `ATLAS_SEED` to the task's seed and `ENABLED_SERVERS` to every wired app.
- `light-servers/Dockerfile` copies `task_data/` to `/workspace/data` and `world_data/` to `/world_data`, both made
  read-only (`chmod -R a-w`).
- `state_capture.py` (collect hook, in `main`) finds the sessions the agent opened from `/logs/agent`, logs each out
  (how a Light server hands its state back), writes `end_env.json` under `ATLAS_STATE_DIR` (default
  `/logs/artifacts/atlas`), and copies `/harness/light-logs/tool_calls.log` to
  `/logs/artifacts/atlas/server_tool_calls.log`. Light apps mint `session_{uuid()}` at login; there are no declared
  session ids.
- Judge: `[judge] judge = "codex"`, `timeout = 1200`, `cwd = "/logs/verifier/judge_ws"`,
  `atif-trajectory = "/logs/verifier/judge_ws/trajectory.json"`, `prompt_template = "prompt.md"`, `weight = 1.0`. The
  model is `JUDGE_MODEL` at run time (passed as `REWARDKIT_MODEL`), never in the TOML. test.sh builds `judge_ws/` from
  `rubric/instruction.md`, `final_message.md` (the rebuilt final message), a copy of `/workspace`, `end_env.json` (when
  captured) and `trajectory.json` (Harbor's ATIF file, else the rebuilt trajectory). `prompt.md` tells the judge to
  read each criterion by its tag: `[final answer]` (final_message.md, and delivered files it refers to),
  `[trajectory]` (the trajectory), `[end state]` (end_env.json, with the write calls as support).
- Verifier image (`tests/Dockerfile`): digest-pinned `python:3.12-slim`, `pytest==9.1.1`, `harbor-rewardkit==0.2.3`,
  `@openai/codex@0.154.0`, `COPY . /tests/` (tests are baked in; Harbor does not upload them to a separate verifier).

### 2e. test.sh steps (the Sample's)

1. **trajectory**: rebuild `{steps, final_message}` from the agent log into `/tmp/agent_trajectory.json`, copy it to
   `/logs/verifier/agent_trajectory.json`.
2. **state**: export `ATLAS_TRAJECTORY` (and the `MCPATLAS_` / `COMPLEXMCP_` aliases) and `ATLAS_OLD_ENV`; copy the
   snapshot to `/logs/verifier/end_env.json` and give it both snapshot shapes; copy the server tool-call log. Each
   missing input goes to `state_capture_failed.txt` and the checks that need it fail closed.
3. **pytest** (reporting only): `pytest /tests/test_outputs.py -p ctrf_pytest_plugin` -> `junit.xml`, `ctrf.json`,
   `pytest-stdout.txt`.
4. **reward**: decide whether a judge is usable (skip reason otherwise), unset `CODEX_AUTH_B64`, build `judge_ws/`,
   run `rewardkit /tests/reward` (both channels) or `rewardkit /tests/reward/pytest` alone; exit 1 when the ledger
   fails.
5. **record**: drop a timed-out or all-errored judge, clamp a negative rubric and recombine with `reward.toml`, write
   `judge.json` and `reward_producer.json`.

## 3. Hard rules

1. **Run from outside YUJI, on a copy.** Start the agent session in a directory outside the YUJI parent repo. Copy the bundle first: `mkdir -p /tmp/qc && cp -R <bundle> /tmp/qc/<uuid>`. Work only on the copy. Reason: YUJI's feedback-capture plugin would pull a QC session started inside the repo into the active FORGE run's feedback chain and break it.
2. **Never read CRUCIBLE or audit output.** Do not open `.audit/`, any `VERDICT.md`, any CRUCIBLE result, anything under `.trinity/runtime` or `.trinity/secrets`, private keys, `~/.config/yuji/cc_oauth_token`, `~/.codex/auth.json`, or any `.env` file.
3. **Never edit the source.** Write only under `/tmp/qc/` (exception: the Harbor jobs dir, see Stage 5, when the Docker VM cannot see `/tmp`). Never write in the source bundle, the reference sample, or anywhere in YUJI. The report goes in `/tmp/qc/<uuid>-report/qc_report.md`; scratch files (`env.sh`, `truth.txt`, `wrong.txt`, probe output, the `$B.re` copy) also stay under `/tmp/qc/`.
4. **Never run Trinity machinery, model agents or proxies.** No Trinity tools, no git writes, no ccbridge or OAuth proxy. Harbor runs use only the `oracle` and `nop` agents, which need no model; unset `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `OPENAI_API_KEY`, `GEMINI_API_KEY` and the judge inputs `JUDGE_MODEL`, `CODEX_AUTH_B64`, `JUDGE_CLAUDE_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` in their environment.
5. **Never print secrets.** Do not echo API keys, `CODEX_AUTH_B64`, `CLAUDE_CODE_OAUTH_TOKEN`, OAuth tokens, or the contents of any env or auth file. Grep for key names, never values.
6. **No judge calls.** The judge inputs stay unset, so the live verifier leaves the rubric UNSCORED: `reward.json` has no `rubric` key, `rubric_judge_failed.txt` gives the reason, `reward_producer.json` lists `channels: ["pytest"]`, and the reward is the pytest channel alone. Stage 5 proves an unscored rubric is dropped, not scored 0.
7. **Do not invent CLI flags.** Anything marked "adjust to bundle" must be confirmed with `--help` first.
8. **Confirmed or not reported.** A suspicion you did not confirm against the files is not a finding. Put it under CLEARED or leave it out.
9. **Never check the trajectories folder.** Do not open, scan or grade anything under `trajectories/` (or `trajectory/`), in the bundle or in the reference sample. Every `find`/`grep` below prunes it. Reading the trajectory the GRADER rebuilds from `/logs/agent` is part of the format and is not this.
10. **Grader path redirects live in `$B.re` only.** Run `ledger.py` with `ATLAS_TESTS_DIR` / `ATLAS_VERIFIER_LOGS` pointed into `$B.re`; if `test_outputs.py` or `claims_lib.py` still hardcodes `/tests/...` without an env override, rewrite that literal in `$B.re` only. Never edit `$B` and never create `/tests` on the host.

## 4. Time budget

| Stage | Subject | Minutes |
|---|---|---:|
| 0 | Setup, copy, fact sheet | 2 |
| 1 | Structure, task.toml, harness identity, Harbor 0.24.0 static validation | 5 |
| 2 | Instruction, world data, leakage | 5 |
| 3 | Deterministic grading | 5 |
| 4 | Rubric compliance (judge.toml), strict | 8 |
| 5 | Execution: ledger probes (fast pre-check), then live Harbor oracle and nop | 20 |
| | **Total** | **45** |

Live oracle and nop runs are mandatory. Measured on slot 29 (2026-10-17, images already cached, 4-CPU colima VM):
`harbor run` oracle 30-42 s and nop 28-40 s per run; a first build without cached images can add 10-20 minutes
(the verifier image installs rewardkit and the codex CLI); budget up to 60 minutes when Docker caches are cold.

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
# REF = the reference sample 5b10675f, read-only (only its non-trajectory files are read). Set REF yourself, or it is
# found next to the bundle, in a yuji samples dir, or anywhere under $HOME (including a yuji-trajectories folder).
if [ -z "${REF:-}" ]; then
  for d in "$(dirname "$SRC")" "$(dirname "$SRC")"/../samples "$(dirname "$SRC")"/../yuji/samples; do
    REF=$(ls -d "$d"/5b10675f-* 2>/dev/null | head -1); [ -n "$REF" ] && break
  done
  [ -n "$REF" ] || REF=$(find "$HOME" -maxdepth 7 -type d -name '5b10675f-*' -not -path '*/trajectories/*' -prune 2>/dev/null | head -1)
fi
test -d "${REF:-/nonexistent}/tests/reward" || { echo "STOP: reference sample not found; set REF to your copy of 5b10675f-e16b-5f22-ae7f-d8040f6324c4 and rerun"; exit 1; }
echo "REF=$REF"
# Each Bash call in Claude Code / opencode starts a fresh shell, so persist every variable.
cat > "/tmp/qc/$UUID-report/env.sh" <<EOF
UUID="$UUID"
SRC="$SRC"
B="/tmp/qc/$UUID"
LS="/tmp/qc/$UUID/environment/light-servers"
REF="$REF"
T="/tmp/qc/$UUID/tests"
RK="/tmp/qc/$UUID/tests/reward"
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
| REF used | `REF` in `env.sh` | |
| Single or multi-step | `instruction.md`, `task.toml` | |
| Light apps and ports | `task.toml [[environment.mcp_servers]]`, `entrypoint.sh` | |
| Graded apps vs distractors | `task.toml [task.metadata] apps` vs `mcp_servers` | |
| Seed | `[task.metadata] seed`, compose `COMPLEXMCP_SEED` / `ATLAS_SEED` | |
| Graded keys (calls, records, reported figures, claims) | `test_outputs.py`, `tests/oracle.json` (`oracle`, `reported`) | |
| Components and weights (traj_tests, rubric), positive checks, guards, gate | `tests/test_weights.json` (S3-25 command) | |
| Channel mix and guard polarity | `tests/reward/reward.toml` weights; `test_weights.json guard_polarity` (default `fail_charges`) | |
| Guards (negative checks) and what each forbids | `test_outputs.py` docstrings, `test_weights.json` | |
| Red-lines (catastrophic acts) | `TRUTH.md`, `[task.metadata.scenario] trap`, `difficulty_explanation` | |
| Rubric criterion count, positive / negative source weight, scale | `tests/reward/rubric/judge.toml` `annotations.source_weight` (Stage 4 commands) | |
| Harbor version used | `harbor --version` (must be 0.24.0, see Stage 1) | |
| Decoys and wrong figures | `[task.metadata] decoy_records`, `wrong_figures`, `TRUTH.md` | |
| Truth figures (every graded value) | `solution/TRUTH.md`, `tests/oracle.json reported` (and `reported.claims` terms) | |
| Grader env vars | `grep environ tests/test_outputs.py tests/claims_lib.py tests/reward/pytest/ledger.py` | |

```bash
source /tmp/qc/<uuid>-report/env.sh
python3 -c "import tomllib,sys;d=tomllib.load(open(sys.argv[1],'rb'));print({k:v for k,v in d['task'].items() if k!='metadata'});[print(s) for s in d['environment']['mcp_servers']]" "$B/task.toml"
python3 -c "import tomllib,sys;m=tomllib.load(open(sys.argv[1],'rb'))['task'].get('metadata',{});[print(k,'=',str(m.get(k))[:200]) for k in ('seed','apps','mcp_servers','decoy_records','wrong_figures','grader','components','scenario')]" "$B/task.toml"
ls "$B/tests" "$B/solution"; ls -R "$RK"; cat "$RK/reward.toml"
grep -nE 'environ' "$T/test_outputs.py" "$T/claims_lib.py" "$RK/pytest/ledger.py" | head -30
python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print('guard_polarity =',d.get('guard_polarity','fail_charges (default)'),'| gate =',d.get('gate'))" "$W"
```

## 6. Stage 1: structure, task.toml, harness identity, Harbor 0.24.0 (5 min)

Severity scale: BLOCKER (fails the bundle), MAJOR (fails unless waived), MINOR (note), VERIFY (ask maintainers, never blocks).

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S1-01 | Tree matches section 2c: every listed file present (missing = BLOCKER); any file not in the tree is MAJOR, remove it (including the earlier format's `tests/grade.py`, `tests/_judge/`, a top-level `tests/judge.toml`). `trajectories/` is ignored. | BLOCKER | cmd S1-01 | Sample |
| S1-33 | No provenance files: `provenance.yaml`, `provenance.sig` or any `provenance.*` (outside `trajectories/`). Not part of the format: remove them. | MAJOR | cmd S1-01 | user decision 2026-10-19 |
| S1-34 | No fixtures: a `tests/fixtures/` dir (or any `fixtures/` outside `trajectories/`). Not part of the format: remove it. | MAJOR | cmd S1-01 | user decision 2026-10-19 |
| S1-32 | No `rubric.json` anywhere (outside `trajectories/`): BLOCKER. The rubric is `tests/reward/rubric/judge.toml`, compiled by the harness build from the author's rubric; the fix for a `rubric.json`-only bundle is to write the author's rubric and recompile, then delete `rubric.json`. No file (`test.sh`, `test_weights.json components.rubric.file`, `task.toml [task.metadata]`) may name `rubric.json`. | BLOCKER | cmd S1-01 | Sample |
| S1-35 | `schema_version = "1.4"`; `[task] name = "atlas/<uuid>"`, `version`, `description`, `keywords`, `authors` (each `{name, email}`); `[task.metadata]` carries `apps`, `mcp_servers`, `grader = "weighted"`, `grading`, `components` (missing: MAJOR) and the Sample's other keys (`seed`, `decoy_records`, `wrong_figures`, `attachments`, `scenario` with `summary`/`output_shape`/`pivot`/`trap`, `difficulty_explanation`, `verification_explanation`, `gt_env_status`; missing: MINOR). `[task.metadata] seed` equals compose `COMPLEXMCP_SEED` and `ATLAS_SEED` (a mismatch serves a different world from the one `gt_env.json` was baked with: MAJOR). | MAJOR | cmd S1-12 | Sample |
| S1-06 | Every image is digest-pinned: each `FROM` and `COPY --from=` image in `environment/**/Dockerfile*` and `tests/Dockerfile*` (an `ARG`-fed `FROM ${X}` counts as pinned when the ARG default is), and the compose `LIGHT_SERVERS_IMAGE` / `JUDGE_IMAGE` defaults. A floating tag is a BLOCKER. `[environment] docker_image` / `light_servers_image` are absent as in the Sample; present = MAJOR (Harbor would pull instead of building the bundle's environment). | BLOCKER | cmd S1-12 | Sample |
| S1-08 | Every `[[environment.mcp_servers]]` entry has exactly `name`, `transport = "streamable-http"`, `url = "http://light-servers:<port>/mcp"`, and the port equals the `--port` in `entrypoint.sh SERVER_CMDS` for that name. No two entries share a port. | BLOCKER | cmd S1-08 | Std §10.3, v4 S2-SV1..SV6 |
| S1-09 | Every declared Light app (`mcp_servers`) is in compose `ENABLED_SERVERS`. | BLOCKER | cmd S1-09 | Std §10.3, Sample |
| S1-10 | Light-servers source is identical to the Sample's, ignoring `# harbor-canary GUID` lines, the task's own `world_data/` and `task_data/`, and `software/LightAirtable/airtable.py` (the one server file a task may change; the Sample's mid-run re-deliveries live there). `light-servers/Dockerfile` included. Any other change is a hit. | BLOCKER | cmd S1-10 | Std §10.4, Sample |
| S1-11 | Compose matches 2d: only services `main` and `light-servers`, volumes `workspace_data` and `light_logs`; `light_logs` read-only (`:ro`) in `main` at `/harness/light-logs` (writable there = BLOCKER: the agent could alter the server log) and read-write in `light-servers` at `/var/log/light-servers`. No `ports:` or `expose:`. | BLOCKER | cmd S1-11 | Std §10.5, v4 S4-DF1/DF5, Sample |
| S1-12 | `[agent] network_mode = "public"`; `[verifier.environment] network_mode = "public"`; `[environment] network_mode = "public"`. | BLOCKER | cmd S1-12 | Sample |
| S1-13 | `[verifier.env]` holds exactly `JUDGE_MODEL`, `JUDGE_TRANSPORT`, `CODEX_AUTH_B64`, `CLAUDE_CODE_OAUTH_TOKEN`, `ATLAS_END_ENV`. Each judge key is `"${NAME:-default}"`; credentials (`CODEX_AUTH_B64`, `CLAUDE_CODE_OAUTH_TOKEN`) default to empty, `JUDGE_MODEL` defaults to empty, `JUDGE_TRANSPORT` may default to `codex`. `ATLAS_END_ENV = "/logs/artifacts/atlas/end_env.json"`. No literal key value. | BLOCKER | cmd S1-13 | Sample |
| S1-14 | `[agent] timeout_sec = 3600`, `[verifier] timeout_sec = 1800`, `[verifier] environment_mode = "separate"`, `[verifier.environment] workdir = "/tests"`. Integers, not floats or formulas. | BLOCKER | cmd S1-12 | Sample |
| S1-15 | `artifacts` collects `/logs/agent` with `exclude = ["./completions"]` and `/workspace` with `exclude = ["./data"]`. | MAJOR | cmd S1-12 | Sample |
| S1-16 | `[[verifier.collect]]`: `service = "main"`, `command = "python3 /harness/atlas/state_capture.py"`, `timeout_sec = 300`; `environment/Dockerfile` puts `state_capture.py` at `/harness/atlas/`. | MAJOR | cmd S1-12 | Sample |
| S1-17 | `state_capture.py` is the Sample's (S1-37): it finds the sessions the agent used from `/logs/agent`, logs each out, writes `end_env.json` under `ATLAS_STATE_DIR` (default `/logs/artifacts/atlas`), copies the server tool-call log to `server_tool_calls.log` there, never writes `/logs/verifier` and never reads `tests/` or `solution/`. Never ask for fixed session ids: Light apps mint `session_{uuid()}` at login. | MAJOR | cmd S1-17 | Sample, `software/*/session.py` |
| S1-19 | Multi-step bundle carries top-level `multi_step_reward_strategy = "final"`. `[metadata] steps_aggregation` is ignored and does not count. (The Sample is single-step.) | BLOCKER | cmd S1-12 | Std §10.11 |
| S1-27 | Forbidden files: `__pycache__/`, `.pytest_cache/`, `.DS_Store`, `* (N).*`, `.zip`, editor backups (in the source bundle, not created by your copy). `trajectory/` is never scanned. | MAJOR | cmd S1-27 | v4 S2-HY1, S4-DF10 |
| S1-28 | No empty or whitespace-only file. Every JSON parses. Every shell script has a shebang on line 1 or directly below the leading canary comment lines (the Sample's `tests/test.sh` has it on line 3; that form is accepted). (`trajectory/` excluded; `light-servers/` is covered by S1-10, since the Sample's shared `servers/*/start.sh` carry no shebang.) | MAJOR | cmd S1-28 | v4 S4-FC2, FC7, Sample |
| S1-30 | Harbor 0.24.0 is the version used (`harbor --version` prints `0.24.0`; if the installed `harbor` differs, say so and use `uv tool run --from harbor==0.24.0 harbor`). The bundle copy loads with Harbor 0.24.0's own task loader with no error: `TaskConfig` parses task.toml (keys and types), input paths are contained, `instruction.md` and `tests/test.sh` exist. Harbor 0.24.0 has no `harbor validate` subcommand (`harbor --help`), and `harbor check` runs a model agent, so it is not used. | BLOCKER | cmd S1-30 | Harbor 0.24.0 `harbor/models/task/task.py`, `config.py` |
| S1-31 | task.toml values Harbor 0.24.0 accepts: `network_mode` in `no-network`, `public`, `allowlist`; `[verifier] environment_mode` in `shared`, `separate`; MCP `transport` in `stdio`, `sse`, `streamable-http` with a `url` for the HTTP ones; `multi_step_reward_strategy` in `mean`, `final` and at the TOP level when `[[steps]]` exist; every `[[steps]]` has `name` and a `steps/<name>/` dir. Root keys Harbor ignores are a MINOR note. | BLOCKER | cmd S1-30 | Harbor 0.24.0 `TaskConfig`, `StepConfig`, `MultiStepRewardStrategy` |
| S1-36 | `[task.metadata] attachments` lists every file under `task_data/` exactly once, every `path` exists (a listed file that does not exist: MAJOR), and each `type` agrees with the extension (`docx`, `svg`, `csv`, `json`, `markdown` for `.md`, `text` for `.txt`; mismatch or unlisted file: MINOR). | MAJOR / MINOR | cmd S1-36 | Sample |
| S1-37 | **Harness files are the Sample's.** Identical to REF apart from lines containing `harbor-canary GUID`: `tests/test.sh`, `tests/reward/reward.toml`, `tests/reward/pytest/ledger.py`, `tests/reward/rubric/prompt.md`, `tests/ctrf_pytest_plugin.py`, `tests/Dockerfile`, `tests/Dockerfile.ecr`, `tests/docker-compose.yaml`, `tests/.dockerignore`, `environment/Dockerfile`, `environment/state_capture.py`. `environment/docker-compose.yaml` may differ only in `COMPLEXMCP_SEED`, `ATLAS_SEED` and `ENABLED_SERVERS`; the `task.toml` header (everything before `[task]`) only in canary lines. Any other difference is MAJOR: quote it, because it changes how the bundle is built or graded. `tests/claims_lib.py` differing is VERIFY (read the diff). | MAJOR | cmd S1-37 | Sample (harness/build.py comments) |

Commands for Stage 1:

```bash
source /tmp/qc/<uuid>-report/env.sh
# S1-01 / S1-32 / S1-33 / S1-34  format of section 2c (trajectories/ is never walked)
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
    "tests/claims_lib.py", "tests/ctrf_pytest_plugin.py", "tests/test.sh", "tests/test_outputs.py",
    "tests/test_weights.json", "tests/old_env.json", "tests/oracle.json",
    "tests/reward/reward.toml", "tests/reward/pytest/ledger.py", "tests/reward/rubric/judge.toml",
    "tests/reward/rubric/prompt.md", "tests/reward/rubric/instruction.md",
    "solution/TRUTH.md", "solution/gt_env.json", "solution/solve.py", "solution/solve.sh"]
for p in REQUIRED:
    if not (b / p).exists(): print("S1-01 BLOCKER missing:", p)
def found(pattern):
    return sorted(str(f.relative_to(b)) for f in b.rglob(pattern) if not SKIP & set(f.relative_to(b).parts))
if found("rubric.json"): print("S1-32 BLOCKER rubric.json present: write the author's rubric, recompile tests/reward/rubric/judge.toml, remove", found("rubric.json"))
refs = [p for p in ("tests/test.sh", "tests/test_weights.json", "task.toml") if (b / p).exists() and "rubric.json" in (b / p).read_text()]
if refs: print("S1-32 BLOCKER still names rubric.json:", refs)
if found("provenance.*"): print("S1-33 MAJOR provenance files present, remove them:", found("provenance.*"))
fx = [p for p in found("fixtures") if (b / p).is_dir()]
if fx: print("S1-34 MAJOR fixtures present, remove them:", fx)
# everything outside light-servers' own tree that the format does not list
allowed = set(REQUIRED) | {"environment", "tests", "solution", "environment/light-servers",
                           "tests/reward", "tests/reward/pytest", "tests/reward/rubric"}
for f in sorted(b.rglob("*")):
    r = f.relative_to(b); parts = r.parts
    if SKIP & set(parts) or str(r) in allowed: continue
    if parts[:2] == ("environment", "light-servers") and len(parts) > 3: continue      # servers/, software/, data
    if f.name == "rubric.json" or f.name.startswith("provenance.") or "fixtures" in parts: continue
    print("S1-01 MAJOR not in the format, remove it:", r)
print("S1-01 format check done")
PY
python3 /tmp/qc/layout_check.py "$B"
# S1-09
grep -n 'ENABLED_SERVERS' "$B/environment/docker-compose.yaml"
# S1-11  (light_logs must be ':ro' in main)
grep -nE '^[A-Za-z_]+:|^  [A-Za-z0-9_-]+:|ports:|expose:|extra_hosts|light_logs|workspace_data' "$B/environment/docker-compose.yaml"
# S1-13  key names only, never values
python3 - "$B/task.toml" <<'EOF'
# prints NAME and a status only; never prints a value or a line
import re, sys, tomllib
env = (tomllib.loads(open(sys.argv[1]).read()).get("verifier", {}) or {}).get("env", {}) or {}
need = ("JUDGE_MODEL", "JUDGE_TRANSPORT", "CODEX_AUTH_B64", "CLAUDE_CODE_OAUTH_TOKEN")
for n in sorted(set(need) | set(env) - {"ATLAS_END_ENV"}):
    v = env.get(n)
    m = re.fullmatch(r'\$\{([A-Z0-9_]+):-([^}]*)\}', v) if isinstance(v, str) else None
    ok = bool(m) and (n == "JUDGE_TRANSPORT" or m.group(2) == '')     # only the transport may have a default
    print(n, 'MISSING' if v is None else ('ok' if ok else 'LITERAL or non-empty default'), '' if n in need else '(extra key, not in the Sample)')
print('ATLAS_END_ENV', 'ok' if env.get('ATLAS_END_ENV') == '/logs/artifacts/atlas/end_env.json' else 'HIT')
EOF
# S1-36  attachments metadata against task_data/
python3 - "$B" <<'EOF'
import pathlib, sys, tomllib
b = pathlib.Path(sys.argv[1]); td = b / "environment/light-servers/task_data"
att = tomllib.load(open(b / "task.toml", "rb")).get("task", {}).get("metadata", {}).get("attachments")
if att is None: print("S1-36 MINOR no [task.metadata] attachments (the Sample lists every task_data file)"); sys.exit()
EXT = {"docx": ".docx", "svg": ".svg", "csv": ".csv", "json": ".json", "markdown": ".md", "text": ".txt"}
paths = [a.get("path", "") for a in att]
for a in att:
    p = b / a.get("path", "")
    if not p.is_file(): print("S1-36 MAJOR listed but missing:", a.get("path"))
    elif a.get("type") in EXT and p.suffix.lower() != EXT[a["type"]]: print("S1-36 MINOR type", a.get("type"), "vs", p.name)
files = sorted(str(f.relative_to(b)) for f in td.rglob("*") if f.is_file() and f.name != ".DS_Store")
print("S1-36 MINOR task_data files not listed:", sorted(set(files) - set(paths)) or "none",
      "| listed twice:", sorted({p for p in paths if paths.count(p) > 1}) or "none")
EOF
# S1-17
grep -nE 'ATLAS_AGENT_LOGS|ATLAS_STATE_DIR|ATLAS_SERVER_LOG|logout|/logs/verifier|/tests|/solution' "$B/environment/state_capture.py" | head -20
# S1-27  run on the SOURCE bundle, not the copy; trajectory/ is pruned
find "$SRC" \( -name trajectory -o -name trajectories \) -prune -o \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.DS_Store' -o -name '*([0-9])*' -o -name '*.zip' -o -name '*~' \) -print
# S1-28
find "$B" \( -name trajectory -o -name trajectories \) -prune -o -type f -not -path "$LS/*" -size -2c -print
find "$B" \( -name trajectory -o -name trajectories \) -prune -o -name '*.json' -not -path "$LS/*" -exec python3 -c "import json,sys;json.load(open(sys.argv[1]))" {} \; 2>&1 | grep -i error
for f in $(find "$B" \( -name trajectory -o -name trajectories -o -path "$LS" \) -prune -o -name '*.sh' -print); do   # light-servers: S1-10
  awk 'NR==1 && /^#!/ {ok=1; exit} /^#!/ {ok=1; exit} !/^#/ {exit} END {exit !ok}' "$f" || echo "S1-28 MAJOR no shebang on line 1 or below the canary header: $f"
done
```

S1-30 / S1-31, Harbor version and static validation. `/tmp/qc/harbor_validate.py` loads the task with Harbor's
own `Task` class:

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

S1-10, light-servers source identity, and S1-37, harness identity (canary lines ignored):

```bash
source /tmp/qc/<uuid>-report/env.sh
test -d "$REF/tests/reward" || { echo "S1-10/S1-37: REF missing; set REF in env.sh to your copy of 5b10675f-..."; exit 1; }
# S1-10  expected output: nothing, or exactly one line for software/LightAirtable/airtable.py
diff -r -q -I 'harbor-canary GUID' -x __pycache__ -x world_data -x task_data "$REF/environment/light-servers" "$LS"
# S1-37
for f in tests/test.sh tests/reward/reward.toml tests/reward/pytest/ledger.py tests/reward/rubric/prompt.md \
         tests/ctrf_pytest_plugin.py tests/Dockerfile tests/Dockerfile.ecr tests/docker-compose.yaml tests/.dockerignore \
         environment/Dockerfile environment/state_capture.py; do
  diff -q -I 'harbor-canary GUID' "$REF/$f" "$B/$f" >/dev/null 2>&1 || echo "S1-37 MAJOR differs from the Sample: $f (diff -I 'harbor-canary GUID' \"\$REF/$f\" \"\$B/$f\")"
done
diff -q -I 'harbor-canary GUID' "$REF/tests/claims_lib.py" "$T/claims_lib.py" >/dev/null || echo "S1-37 VERIFY tests/claims_lib.py differs from the Sample: read the diff"
cnorm() { grep -v 'harbor-canary GUID' "$1" | sed -E 's/(COMPLEXMCP_SEED|ATLAS_SEED): "[0-9]+"/\1: "<seed>"/; s/ENABLED_SERVERS: "[^"]*"/ENABLED_SERVERS: "<servers>"/'; }
diff <(cnorm "$REF/environment/docker-compose.yaml") <(cnorm "$B/environment/docker-compose.yaml") && echo "S1-37 compose ok"
diff <(sed '/^\[task\]/,$d' "$REF/task.toml" | grep -v 'harbor-canary GUID') <(sed '/^\[task\]/,$d' "$B/task.toml" | grep -v 'harbor-canary GUID') && echo "S1-37 task.toml header ok"
```

S1-06, S1-12 to S1-16, S1-19, S1-35: task.toml and images against the Sample's values:

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
for key in ("docker_image", "light_servers_image"):
    chk("S1-06", key not in e, "[environment] %s absent (MAJOR when present)" % key)
for comp, var in (("environment/docker-compose.yaml", "LIGHT_SERVERS_IMAGE"), ("tests/docker-compose.yaml", "JUDGE_IMAGE")):
    m = re.search(var + r":-([^}]+)\}", (b / comp).read_text()) if (b / comp).exists() else None
    chk("S1-06", bool(m) and "@sha256:" in m.group(1), comp + " " + var + " default pinned by digest")
for df in sorted(list((b / "environment").rglob("Dockerfile*")) + list((b / "tests").glob("Dockerfile*"))):
    src = df.read_text(); args = dict(re.findall(r"(?m)^ARG\s+(\w+)=(\S+)", src))
    for ref in re.findall(r"(?m)^FROM\s+(\S+)|COPY\s+--from=(\S+)", src):
        img = next(x for x in ref if x); img = args.get(img.strip("${}"), img)
        if re.fullmatch(r"[a-z0-9_-]+", img): continue          # a build stage name, not an image
        chk("S1-06", pin(img), "%s base image %s pinned by digest" % (df.relative_to(b), img.split("@")[0]))
chk("S1-12", a.get("network_mode") == "public", "[agent] network_mode public")
chk("S1-12", ve.get("network_mode") == "public", "[verifier.environment] network_mode public")
chk("S1-12", e.get("network_mode") == "public", "[environment] network_mode public")
chk("S1-13", (v.get("env") or {}).get("ATLAS_END_ENV") == "/logs/artifacts/atlas/end_env.json", "[verifier.env] ATLAS_END_ENV")
chk("S1-14", a.get("timeout_sec") == 3600 and type(a.get("timeout_sec")) is int, "agent timeout_sec 3600")
chk("S1-14", v.get("timeout_sec") == 1800 and type(v.get("timeout_sec")) is int, "verifier timeout_sec 1800")
chk("S1-14", v.get("environment_mode") == "separate", "verifier environment_mode separate")
chk("S1-14", ve.get("workdir") == "/tests", "[verifier.environment] workdir /tests")
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
for f in ("apps", "mcp_servers", "grading", "components"): chk("S1-35", bool(m.get(f)), "[task.metadata] " + f + " (MAJOR)")
chk("S1-35", m.get("grader") == "weighted", "[task.metadata] grader = weighted (MAJOR)")
for f in ("seed", "decoy_records", "wrong_figures", "attachments", "difficulty_explanation", "verification_explanation", "gt_env_status"):
    chk("S1-35", f in m, "[task.metadata] " + f + " (MINOR)")
sc = m.get("scenario") or {}
chk("S1-35", all(sc.get(f) for f in ("summary", "output_shape", "pivot", "trap")), "[task.metadata.scenario] summary/output_shape/pivot/trap (MINOR)")
comp = (b / "environment/docker-compose.yaml").read_text()
seeds = set(re.findall(r'(?:COMPLEXMCP_SEED|ATLAS_SEED): "(\d+)"', comp))
chk("S1-35", seeds == {str(m.get("seed"))}, "seed %s == compose COMPLEXMCP_SEED / ATLAS_SEED %s (MAJOR)" % (m.get("seed"), sorted(seeds)))
PY
python3 /tmp/qc/toml_check.py "$B"          # every HIT line is a finding at the row's severity
```

## 7. Stage 2: instruction, world data, leakage (5 min)

Visible surface: `instruction.md`, everything under `task_data/` (served read-only at `/workspace/data`, names and contents), and everything the wired apps serve from `world_data/`. Invisible: `task.toml`, `tests/**`, `solution/**`. A value that exists only in an invisible file cannot be produced by any run.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S2-01 | No reward leakage. A truth or answer value from `TRUTH.md` / `oracle.json reported` (figures, target ids, chosen names, claim terms) in `instruction.md` is a BLOCKER. In agent-visible `task_data/` or `world_data/` it is a BLOCKER only when it is a derived answer (a computed result the agent should produce, stated ready to copy); discovery inputs there are expected and decoys are notes. Ignore shared server source (`light-servers/software/`, `servers/`), values under 6 characters and plain dates. | BLOCKER | cmd S2-01 | FORGE 11, v4 S0-LK2/LK4, S2-WD13, tabish E4/M8 |
| S2-02 | No wrong figure or decoy id printed in the instruction. A printed trap is not a trap. Read the wrong values from `TRUTH.md`, `[task.metadata] wrong_figures` and `decoy_records`. Naming a decoy's existence in general terms ("the folder also holds an analytics board's drop estimates and an old owner roster", as the Sample does) is allowed; its file name, id or figure is not. | BLOCKER | cmd S2-01 | v4 S0-LK3, S2-MD2, Sample |
| S2-03 | Nothing in `task_data/` reveals the answer (worked totals, a filled-in deliverable, a key). | BLOCKER | read | Std §10.12 |
| S2-04 | Instruction names no machinery: no path or directory, no host or harness path, no URL or port, no `Light*` app name, no snake_case tool name, no `MCP`, `server`, `tool call`, `endpoint`, `API`, `mock`, no slug, uuid or seed. Exempt: the first-line `<!-- instruction-canary <uuid> -->`. Systems named by their business role ("the team tracker", "the Log shipper base", "the data folder of the workspace") are fine. | BLOCKER | cmd S2-04 | v4 S0-PA1..PA8, Sample |
| S2-05 | Instruction names no grading artefact: `tests/`, `solution/`, `test_outputs.py`, `test_weights.json`, `ledger.py`, `reward.toml`, `oracle.json`, `judge.toml`, `reward.json`, `TRUTH.md`. A plain-language "How the work is judged" section naming the records the reader will look at (as the Sample's) is allowed. | BLOCKER | cmd S2-04 | v4 S0-PA1, Sample |
| S2-06 | No authoring residue: HTML comment, `TODO`, `FIXME`, `NOTE:`, placeholders, text addressed to a model ("think step by step", "You are a"). Exempt: the one first-line `<!-- instruction-canary <uuid> -->` comment. Any other HTML comment, or a canary comment not on line 1 or carrying more than the uuid, is a hit. Format examples the deliverable needs (`drops.example-pipeline: 1234`, a subject template) are not placeholders. | BLOCKER | cmd S2-06 | v4 S0-CM1..CM3, Sample |
| S2-08 | Deliverable is stated: the run can tell which record, state change, field format or reply is the answer. | BLOCKER | read | v4 S0-SP1 |
| S2-09 | Instruction does not walk the procedure, does the arithmetic in words, say which source wins, state a rule with its application, or count the evidence or traps. Stating the deliverable's required steps and constraints (preview before set, roll once, write only in named places, as the Sample does) is not walking the procedure. | MAJOR | read | v4 S0-SP2, SP3, LK5, LK6, LK7, Sample |
| S2-10 | Instruction does not coach ("make sure", "be careful", "look for", "cross-check", "remember", "note that", "hint"). | MAJOR | cmd S2-10 | v4 S0-SP4 |
| S2-11 | Instruction does not point at the evidence (exact document title, thread subject, field, person holding the answer, a date range that isolates it). Naming the deliverable's own targets (the ticket id, the tables to write) is fine. | MAJOR | search titles/subjects from world_data and TRUTH.md | v4 S0-SP5 |
| S2-12 | Every graded decision has a cue in the visible surface. A graded choice the instruction and world never motivate is unwinnable. | BLOCKER | trace each predicate to a cue | tabish B3, RUTHLESS 3.2 |
| S2-13 | No contradictory rules or guards: one graded outcome only (FORGE 10a statement-ambiguity rule). | BLOCKER | read predicates against instruction | tabish B2, FORGE 10a |
| S2-14 | Conventions the graders assume (units, rounding, date format, currency scale, id format, field line format) are stated in the instruction or carried by the world. | MAJOR | read | tabish B4, v4 S4-TR11 |
| S2-15 | Every decoy is planted in the served world or `task_data/` and is killed by a stated rule a careful run can find. A decoy with no killing rule is ambiguity, not difficulty. Every entry of `decoy_records` resolves to a real file or record. | MAJOR | trace each `decoy_records` entry to a world row or file and a rule | tabish B5, B6, v4 S2-CP6 |
| S2-16 | `world_data/<App>.json` filename equals the app name byte-for-byte and exists for every app in `mcp_servers` (an empty `{}` for an unused distractor, as in the Sample, is fine); none exists for an app that is not wired. | BLOCKER | cmd S2-16 | v4 S2-WD1..WD3, Sample |
| S2-17 | Every top-level container in an overlay resolves in the app: a corpus yaml key, a `get_session_dict()` key, or a `self.<name>` attribute. Keys beginning `_` are markers. | BLOCKER | read app `corpus/*.yaml` and `__init__` | v4 S2-WD4 |
| S2-18 | Container form (list vs dict keyed by id), field names, value types (overlays are not coerced) and enum values match the corpus row. Evidence path only. | MAJOR | compare one corpus row per container used | v4 S2-WD5..WD9 |
| S2-19 | Authored ids do not collide with corpus ids (overlays append). Task logic that says "the only", "the earliest", "the last" survives corpus rows being present. | BLOCKER | cmd S2-19 | v4 S2-WD10, WD11 |
| S2-21 | No authoring smell readable as a hint in world rows (`_comment`, ids like `decoy-2`, notes naming the trap). | MINOR | cmd S2-21 | v4 S2-WD15 |
| S2-23 | No copy of `solution/` or `tests/` (or `TRUTH.md`, `judge.toml`, `oracle.json`, `test_weights.json`, `gt_env.json`, `reward.toml`, `ledger.py`) into any agent-side image: no `COPY`/`ADD` of them in `environment/**/Dockerfile*`, and nothing from them under `task_data/` or `world_data/`. The verifier image built from `tests/Dockerfile` is the one allowed exception. | BLOCKER | cmd S2-23 | tabish E1, leakage policy |
| S2-24 | `tests/**` (including `tests/reward/**`), `solution/gt_env.json` and `solution/TRUTH.md` are never agent-visible: not in an agent image, not mounted into `main` or `light-servers`, not under `task_data/` or `world_data/`. | BLOCKER | cmd S2-23 | leakage policy |
| S2-25 | **Task data is textual only.** Every file under `task_data/` (recursively) must be textual data. Three kinds are accepted, nothing else: (1) **Plain text of any kind** (`.txt`, `.md`, `.csv`, `.tsv`, `.json`, `.jsonl`, `.yaml`, `.xml`, `.html`, `.eml`, `.ics`, `.vcf`, `.log`, `.rtf`, source code, ...): judged by content, not extension: strict UTF-8, no NUL bytes, no binary magic header, no embedded binary (`data:image/...;base64` URIs, RTF `\pict` / `\objdata`). (2) **`.docx`**: a real Word document (a zip holding `[Content_Types].xml` and `word/document.xml` with the `wordprocessingml.document.main` content type), containing text (`<w:t>`), not macro-enabled, and with no embedded non-text parts (`word/media/`, `word/embeddings/`, `word/activeX/`, `vbaProject.bin`). (3) **`.svg`**: well-formed UTF-8 XML whose root is `<svg>`, drawn with vector elements and `<text>` (put every figure the task needs in a text node, so the agent reads it without OCR; an SVG with no text is accepted with a note), with no `<image>`, no `<foreignObject>`, no `<script>`, no `data:` URI and no external `href`/`xlink:href` (an in-document `#id` reference is fine). Everything else is flagged: raster images, `.svgz`, an `.svg` that breaks any rule in (3), `.eps`, `.ps`, `.pdf`, `.doc`, `.docm`, `.xlsx`, `.xls`, `.pptx`, `.odt` and other office files, audio, video, archives, executables, pickles, databases, a binary file renamed to a text extension, a `.docx` that is not a valid Word document, and a `.docx` carrying images or embedded objects. Fix: convert as the Sample does (recorded in its `task_data/CREDITS.txt`): PDFs to text-only `.docx`, spreadsheets to Markdown tables (one per sheet), figures to `.svg` with every value in `<text>`; or remove the file. S2-25 judges the file that ships, not its original. No waiver. | BLOCKER | cmd S2-25 | user decision 2026-10-21/22, Sample |
| S2-26 | `task_data/` is served to the agent read-only at `/workspace/data` (`COPY task_data/ /workspace/data/` and `chmod -R a-w /workspace/data /world_data` in `light-servers/Dockerfile`; S1-10 also enforces the Sample's Dockerfile), and the `/workspace` artifact excludes `./data` (S1-15). | MAJOR | cmd S2-23 | Sample |

Commands for Stage 2. Build `truth.txt` once by hand from `TRUTH.md` and `tests/oracle.json` (`reported`, the written values in `oracle`, and the `all_terms` / `any_terms` of every `reported.claims` entry) (one figure or id per line, and add variants without thousands separators or currency). Build `wrong.txt` the same way from `[task.metadata] wrong_figures` (the figure part of each entry), `decoy_records`, and TRUTH.md's wrong-results section; it feeds S2-02 on `instruction.md` only.

```bash
source /tmp/qc/<uuid>-report/env.sh
# S2-01  leak scan of truth figures across the visible surface
VIS="$B/instruction.md $LS/task_data $(find "$B/environment" -name 'Dockerfile*')"
while IFS= read -r n; do [ -n "$n" ] && grep -rlF -- "$n" $VIS 2>/dev/null | sed "s|^|LEAK '$n' in |"; done < "/tmp/qc/$UUID-report/truth.txt"
# world_data separately: a hit there is a leak only if it is the derived answer, not seeded evidence
while IFS= read -r n; do [ -n "$n" ] && grep -rcF -- "$n" "$LS/world_data" | grep -v ':0$' | sed "s|^|WORLD '$n' |"; done < "/tmp/qc/$UUID-report/truth.txt"
# S2-02  wrong figures and decoy names printed in the instruction
while IFS= read -r n; do [ -n "$n" ] && grep -nF -- "$n" "$B/instruction.md" | sed "s|^|S2-02 WRONG '$n' line |"; done < "/tmp/qc/$UUID-report/wrong.txt"
# S2-04 / S2-05  (line 1 canary excluded)
tail -n +2 "$B/instruction.md" | grep -nE '/|\\|https?:|localhost|light-servers|:[0-9]{2,5}\b|\bMCP\b|tool call|endpoint|\bAPI\b|\bmock\b|\bserver\b|[0-9a-f]{8}-[0-9a-f]{4}-'
tail -n +2 "$B/instruction.md" | grep -noE '\b[a-z]+_[a-z_]+\b' | sort -u          # snake_case tool names
grep -nE 'Light[A-Z][A-Za-z]+|test_output|judge\.toml|reward\.|ledger|rubric|grounding|TRUTH|oracle' "$B/instruction.md"
# S2-06  (a first-line `<!-- instruction-canary <uuid> -->` is exempt)
grep -nE '<!--|TODO|FIXME|NOTE:|XXX|<[a-z_]+>|step by step|You are a|do not hallucinate' "$B/instruction.md" \
  | grep -vE '^1:<!-- instruction-canary [0-9a-f-]{36} -->$'
# S2-10
grep -niE '\b(first|then|make sure|be careful|remember|don.t forget|look for|cross-check|check|note that|hint|tip)\b' "$B/instruction.md"
# S2-16
ls "$LS/world_data"; python3 -c "import tomllib,sys;print(sorted(tomllib.load(open(sys.argv[1],'rb'))['task']['metadata']['mcp_servers']))" "$B/task.toml"
# S2-19  list authored ids and look for each in the app corpus
python3 -c "import json,sys,re;d=json.load(open(sys.argv[1]));print(sorted(set(re.findall(r'\"id\": *\"([^\"]+)\"',json.dumps(d))))[:60])" "$LS/world_data/<App>.json"
grep -c '<authored id>' "$LS/software/<App>/corpus/"*.yaml
# S2-21
grep -rnE '"_comment"|decoy|trap|wrong|poison' "$LS/world_data"
# S2-23 / S2-24
grep -rnE '^(COPY|ADD).*(solution|tests|TRUTH|grounding|judge\.toml|oracle\.json|test_weights|gt_env|reward)' "$B/environment" --include='Dockerfile*'
grep -rlE 'judge\.toml|TRUTH\.md|oracle\.json|test_weights|gt_env|reward\.toml' "$B/environment/docker-compose.yaml" "$LS/task_data" "$LS/world_data"
find "$B/environment" \( -name 'judge.toml' -o -name 'TRUTH*' -o -name 'grounding.yaml' -o -name 'oracle.json' -o -name 'test_weights.json' -o -name 'gt_env.json' -o -name 'reward.toml' -o -name 'ledger.py' \) -print
# S2-26  evidence mount read-only, /workspace artifact excludes ./data
grep -nE 'task_data|/workspace/data|a-w' "$LS/Dockerfile"; grep -nE 'source = "/workspace"' "$B/task.toml"
# S2-25  task_data must be textual only; every non-text file is flagged (BLOCKER)
cat > /tmp/qc/textonly_check.py <<'PY'
# accepted: (1) any plain-text file (judged by content), (2) a text-only .docx, (3) a text-only .svg. Everything else is flagged.
import io, re, sys, pathlib, zipfile
td = pathlib.Path(sys.argv[1])
MAGIC = {b"\x89PNG": "png", b"\xff\xd8\xff": "jpeg", b"GIF8": "gif", b"%PDF": "pdf", b"PK\x03\x04": "zip/office",
         b"\xd0\xcf\x11\xe0": "ole (doc/xls/ppt or encrypted office)", b"RIFF": "riff (webp/wav/avi)", b"\x1f\x8b": "gzip",
         b"BZh": "bzip2", b"7z\xbc\xaf": "7z", b"Rar!": "rar", b"\x7fELF": "elf", b"MZ": "exe", b"\xca\xfe\xba\xbe": "mach-o",
         b"\xcf\xfa\xed\xfe": "mach-o", b"SQLite format 3": "sqlite", b"\x80\x04": "pickle", b"\x80\x05": "pickle",
         b"ID3": "mp3", b"OggS": "ogg", b"fLaC": "flac", b"II*\x00": "tiff", b"MM\x00*": "tiff", b"BM": "bmp",
         b"\x00\x00\x01\x00": "ico", b"%!PS": "postscript"}
IMAGE_TEXT_EXT = {".svgz", ".eps", ".ps"}                    # text-encoded but image data: not accepted (.svg: check_svg)
DOCX_MAIN = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
def magic(head):
    if head[4:12] in (b"ftypheic", b"ftypmp42", b"ftypisom", b"ftypM4A ", b"ftypqt  ", b"ftypavif"): return "iso media"
    return next((k for m, k in MAGIC.items() if head.startswith(m)), None)
def check_docx(data):
    why = []
    try: z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile: return ["not a valid .docx (not a zip)"]
    names = set(z.namelist())
    if "[Content_Types].xml" not in names or "word/document.xml" not in names:
        return ["not a valid .docx (no [Content_Types].xml / word/document.xml)"]
    if DOCX_MAIN not in z.read("[Content_Types].xml").decode("utf-8", "replace"):
        why.append("not a plain Word document (macro-enabled or other type)")
    emb = sorted(n for n in names if re.match(r"word/(media|embeddings|activeX)/", n) or n.endswith("vbaProject.bin"))
    if emb: why.append("embedded non-text parts: " + ", ".join(emb[:5]) + (" ..." if len(emb) > 5 else ""))
    if not re.search(rb"<w:t[ >][^<]*\S", z.read("word/document.xml")): why.append("no text in the document")
    return why
def check_svg(s):
    import xml.etree.ElementTree as ET
    try: root = ET.fromstring(s)
    except ET.ParseError as e: return ["svg is not well-formed XML: %s" % e]
    tag = lambda el: el.tag.rsplit("}", 1)[-1].lower()
    if tag(root) != "svg": return ["root element is <%s>, not <svg>" % tag(root)]
    why, texts = [], 0
    for el in root.iter():
        t = tag(el)
        if t in ("image", "foreignobject", "script"): why.append("svg contains <%s>" % t)
        if t in ("text", "tspan", "textpath") and "".join(el.itertext()).strip(): texts += 1
        for k, v in el.attrib.items():
            if k.rsplit("}", 1)[-1] == "href" and not v.startswith("#"): why.append("svg external href %r" % v[:60])
    if re.search(r"data:[\w.+-]+/[\w.+-]+[;,]", s): why.append("svg embeds a data: URI")
    if not texts: print("S2-25 note: svg has no <text> nodes (vector image only); any figure the task needs must be readable from it")
    return sorted(set(why))
def check_text(f, data):
    k = magic(data[:16])
    if k: return ["binary header: " + k]
    if b"\x00" in data: return ["contains NUL bytes"]
    try: s = data.decode("utf-8")
    except UnicodeDecodeError as e: return ["not textual (invalid UTF-8 at byte %d)" % e.start]
    why = []
    if f.suffix.lower() == ".svg" or re.search(r"<svg[\s>]", s[:4096], re.I): return check_svg(s)
    if f.suffix.lower() in IMAGE_TEXT_EXT: why.append("image data (svgz/eps/ps)")
    if re.search(r"data:(image|audio|video|application)/[\w.+-]+;base64,", s): why.append("embedded base64 binary (data: URI)")
    if s.lstrip().startswith("{\\rtf") and re.search(r"\\(pict|objdata|object)\b", s): why.append("RTF with embedded picture/object")
    return why
if not td.is_dir():
    print("S2-25 task_data/ missing (S1-01 covers it)"); sys.exit()
bad = ok = 0
for f in sorted(p for p in td.rglob("*") if p.is_file()):
    if f.name == ".DS_Store": continue                      # S1-27 covers it
    data = f.read_bytes()
    why = check_docx(data) if f.suffix.lower() == ".docx" else check_text(f, data)
    if why: bad += 1; print("S2-25 BLOCKER non-textual task data, not accepted:", f.relative_to(td), "|", "; ".join(why))
    else: ok += 1
print("S2-25 accepted %d textual file(s);" % ok, "nothing flagged" if not bad else "%d non-textual file(s) flagged" % bad)
PY
python3 /tmp/qc/textonly_check.py "$LS/task_data"
```

## 8. Stage 3: deterministic grading (5 min)

Files: `tests/test.sh`, `tests/test_outputs.py`, `tests/claims_lib.py`, `tests/test_weights.json`, `tests/reward/reward.toml`, `tests/reward/pytest/ledger.py`, `tests/old_env.json`, `tests/oracle.json`, `solution/gt_env.json`, `solution/TRUTH.md`, `solution/solve.sh`, `solution/solve.py`. No fixtures.

Ground rules for this stage:

- The reward reads only what section 2b allows. Nothing else may decide the reward.
- Read every predicate down to the field it reads and the literal it compares. A docstring or an id is a claim; the relation is the fact.
- Check the sign or role first. A guard describes the bad state, and its verdict must match `guard_polarity`.
- `test.sh`, `ledger.py`, `reward.toml` and `ctrf_pytest_plugin.py` are the Sample's (S1-37); the author's grading lives in `test_outputs.py`, `test_weights.json` and `oracle.json`. Spend the stage there.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S3-01 | Reward is computed only from the 2b inputs: rebuilt trajectory and final message, delivered `/workspace` files, `end_env.json`, the server tool-call log, `tests/old_env.json`, `tests/oracle.json`, and the judged rubric. | BLOCKER | cmd S3-01 | Sample, 2b |
| S3-02 | Reward never reads `solution/**`, `TRUTH.md`, `gt_env.json`, the `trajectories/` folder, network resources, or a file that was in the agent's view BEFORE the run and states the answer. Reading the rebuilt trajectory, the final message and the files the run itself delivered under `/workspace` is allowed (2b): never flag a file deliverable or ask to move it into a Light app record. The deliverable's path and shape must be stated in the instruction (S2-08). | BLOCKER | cmd S3-01 | Sample, 2b |
| S3-03 | A missing or empty snapshot or server log does not break the reward: test.sh records it in `state_capture_failed.txt`, the checks that need it fail closed, and a reward file is still written. A missing judge input or failed judge leaves no `rubric` channel (`rubric_judge_failed.txt`, `judge.json ran: false`), never a rubric of 0. | BLOCKER | cmd S3-03, probe S5-05 | Sample |
| S3-04 | Every failure path is loud: a failed pytest ledger makes `test.sh` exit 1 with no reward; a check that raises is scored false (not a pass); no path exits 0 with no `reward.json`. (Proved by S1-37 identity plus S5-05.) | BLOCKER | cmd S3-03 | Sample |
| S3-05 | `test.sh` runs the five steps of 2e in order. (Proved by S1-37; a differing test.sh is read against 2e step by step.) | BLOCKER | cmd S3-03 | Sample |
| S3-10 | Assert hygiene: no check with no assert or no comparison; no constant assert (`assert True`, `assert 1`) as the only verdict; no self-compare (`x == x`); no `or True`; no swallowed `except` that turns an outage into a pass; no silent early `return` in a check; no `pytest.skip`/`xfail` inside a graded check body. A trailing `return True` after a real assert (the Sample's `mixed` style) is fine. `claims_lib.install_skip_fixture`'s autouse fixture (skips every check on a run the platform killed, unless `ATLAS_SCORE_INVALID_RUNS=1`) affects only the reporting pytest step, not the ledger; it is not a finding. | BLOCKER | cmd S3-10 | qc2 §5, RUTHLESS 3.1b, Checklist J5..J7, Sample |
| S3-11 | Unguarded indexing (`rows[0]`, `[-1]`) on captured state that raises on a short or empty world. (The no-op probe lists checks that raise.) | MAJOR | cmd S3-10, probe S5-02 | RUTHLESS 3.1d, v4 S3-E5 |
| S3-12 | No exact float equality on money or measures. A tolerance (`approx`) is stated in the instruction or is a rounding the world defines. | MAJOR | cmd S3-10 | RUTHLESS 3.1d, tabish C5 |
| S3-13 | Phantom dependencies: every import in `tests/` is stdlib, a sibling module in `tests/`, or pinned (`==`) in `tests/Dockerfile` (`pytest==9.1.1`, `harbor-rewardkit==0.2.3`). | BLOCKER | cmd S3-13 | Checklist I2, v4 S3-E1 |
| S3-14 | Determinism: no `random`, `uuid`, `time.time`, `datetime.now`, `shuffle`, dict-order or set-order dependence, network, or test-order dependence in grading. | BLOCKER | cmd S3-14 | tabish D4, RUTHLESS 3.1e, v4 S3-E12 |
| S3-15 | Substring self-pass: a loose `in` or `contains` that matches by accident (`"two" in "network"`), or a case mismatch that fails a correct value. | MAJOR | read every `contains`/`startswith`/`in` relation | Checklist D2, v4 S3-N8 |
| S3-16 | Value coercion: the grader does not lowercase, strip, round or cast the captured value into a tolerance the instruction never states. Normalisations apply to both sides or only remove formatting. | MAJOR | read `_canon` and comparisons | Checklist W5, tabish C8, v4 S3-H5 |
| S3-17 | Numeric fields compared numerically, ids compared as exact strings. | MAJOR | read | tabish C7 |
| S3-18 | Ids the graders key on are seeded ids from the world, never ids the agent invents at runtime. A created record is located by its identifying fields, not by a guessed id. | BLOCKER | read relations against seed | Checklist A3, W2, v4 S3-G2, H2 |
| S3-19 | Literal grounding: every graded value is visible to the agent or derivable from the served world. A value that exists only in `tests/` or `solution/` is unwinnable. This includes the `all_terms` / `any_terms` of every `oracle.json reported.claims` entry graded by the claim-coverage check (the Sample's `test_final_answer_claim_coverage_passes_075`, passing at coverage >= 0.75); each claim also answers something the instruction's handover asks for. | BLOCKER | trace each literal | RUTHLESS 3.1a, Checklist A1, v4 S3-G4, Sample |
| S3-20 | Every computed total the graders assert is verified by hand from the world rows. Write the arithmetic in the report. | BLOCKER | hand recompute | Checklist A2, tabish A6 |
| S3-21 | No seeded-state free credit: no positive check holds on the seed world. Check by reading against `tests/old_env.json` and by the no-op probe (S5-02). | BLOCKER | read, Stage 5 | RUTHLESS 3.1b, Checklist J2, v4 S3-G3 |
| S3-22 | An ABSENCE or INVARIANT predicate (restraint, "nothing else moved") is paired with an EFFECT predicate, so a run that does nothing cannot pass by restraint (the Sample's `test_restraint_with_the_accounting_right` holds only when the graded entries are right). | BLOCKER | read predicate kinds | v4 S3-D1 (adapted), Sample |
| S3-23 | Every red-line (the catastrophic acts in TRUTH.md, `[task.metadata.scenario] trap` and the instruction's "never" rules) has a guard in `test_outputs.py` weighted -5 (or a `gate.require_no_guards`). A red-line stated only in prose or only in the rubric is a hit. | BLOCKER | read TRUTH.md against test_weights.json | FORGE 9, RUTHLESS 3.2 |
| S3-24 | Guard direction: no guard fires on the oracle's run. Read each guard against `solution/solve.py` and `tests/oracle.json` (every write the oracle makes); the live oracle's `grade_report.json guards_tripped` (S5-10) must be empty. | BLOCKER | read, S5-10 | RUTHLESS 3.1c, Checklist F1/F2, v4 S3-O2 |
| S3-25 | Penalty proportionality on `tests/test_weights.json`: no single penalty is at least the total positive weight; no single positive item is more than half the positive weight; `sum(abs(neg)) - sum(pos) <= 3`. Report the floor `-sum(abs(neg))/sum(pos)`. | MAJOR | cmd S3-25 | RUTHLESS 3.3, Checklist H3/I4/I5, v4 S3-D6, G7 |
| S3-26 | No positive predicate demands an act the instruction never asks for, and no two positive predicates make contradictory demands on one record. | BLOCKER | read | v4 S3-G5, G6, Checklist I3 |
| S3-27 | Brittleness against an allowed alternative: no exact match on a field the instruction leaves open, no call-count style `== 1` on records where the instruction allows a retry, no ordering requirement the instruction does not state. | MAJOR | read | v4 S3-G9, O9, RUTHLESS 3.1 |
| S3-28 | A composite key is not graded on one half where the world holds look-alikes sharing that half. | MAJOR | read | v4 S3-G1 |
| S3-29 | Collateral writes are guarded: a write in a read-only or distractor app, or an edit to an untouched record in a graded app, fires a guard. | MAJOR | read guards | tabish C6, v4 S3-S3 |
| S3-30 | Volatile fields the harness rewrites on every write (`updated_at`, `modifiedTime`, `version`, `SyncToken`, counters) are excluded from unchanged/preserved comparisons, and no graded field is excluded. | MAJOR | read the volatile list | v4 S3-F7, S3-S4 |
| S3-32 | **The pytest negatives are deducted.** (a) Every guard check (named `test_guard_*`) has a negative weight in `test_weights.json`, and every negative weight names a check `test_outputs.py` defines. (b) `ledger.py` (the Sample's, S1-37) subtracts the absolute weight of every tripped negative, where "tripped" follows `guard_polarity` (S3-36), divides by the positive total, clamps at 0, and zeroes on any tripped guard when `gate.require_no_guards` is truthy. (c) No negative is left out of `test_weights.json` (the ledger scores only listed names). Any miss means a forbidden act is not penalised: BLOCKER. Proven by S5-13. | BLOCKER | cmd S3-25, probe S5-13 | Sample `ledger.py` |
| S3-33 | **`test_weights.json` rates every check properly.** (a) Every weight is an integer on the scale: positive 1, 3 or 5; negative -1, -3 or -5. A 0, 2, 4, 10, 0.5, a string, a bool or a null on a `test_*` key is a BLOCKER (metadata keys such as `test_file` are not weights). (b) Sign matches role: a guard is negative, a goal is positive; a guard-named check with a positive weight is a BLOCKER. (c) Every `test_*` function in `test_outputs.py` is weighted; the ledger scores only listed names, so an unweighted check scores nothing (MAJOR). (d) The rating follows importance: a 5 goes to the load-bearing aggregates, the claim coverage and red-line guards, a 1 to per-entry and read-order checks (the Sample: 5 on limits, ticket, owners told, claim coverage, the red-line guard at -5; 1 on per-pipeline and per-notice entries). A red-line guard at -1 or a filing-presence check at 5 is a MAJOR. (e) No duplicate key with two different weights. | BLOCKER | cmd S3-25, then read | user decision 2026-10-19, Sample |
| S3-34 | **Ledger components (documentation).** `test_weights.json components` has exactly `traj_tests` (`graded = true`, `test_file = "test_outputs.py"`, `tests` = the check weights) and `rubric` (`graded = true`, `file = "judge.toml"`). Each component `weight` equals the mean absolute weight of its items rounded to 2 or 3 places, within 0.006 (traj_tests over the `tests` values; rubric over `annotations.source_weight`; the Sample: 2.03 for 2.0303 and 2.143 for 2.1429). These weights are not read by the ledger (`reward.toml` mixes the channels), so a wrong mean is MINOR; a missing component or `file = "rubric.json"` is MAJOR. | MAJOR / MINOR | cmd S3-25 | Sample |
| S3-35 | **Gates are live.** `test_weights.json gate`, when present, holds only `require_no_guards` (bool) and `floor` (number), the two keys `ledger.py` reads; any other key (including `require_state_exact`) is ignored: MAJOR. `require_no_guards` given as a list is a MINOR (it gates every guard; write `true`). | MAJOR | cmd S3-25 | Sample `ledger.py` |
| S3-36 | **Every weighted check gives a verdict, and the guards match `guard_polarity`.** (a) `guard_polarity` is absent (= `fail_charges`) or one of `fail_charges`, `pass_charges`; anything else makes the ledger raise (BLOCKER). (b) Every weighted name is a function whose `verdict_style` is `return`, `assert` or `mixed`; `none` or a missing function never passes (a positive never earns; a `fail_charges` guard is always charged): BLOCKER. (c) Every guard is written for the declared polarity: under `pass_charges` (the Sample) it asserts or returns true when the forbidden act shows (`assert hits, "no shipper was scaled down"` then `return True`); under `fail_charges` it passes when the run behaved. (d) Proof: on the no-op probe (S5-02) `grade_report.json guards_tripped` and `errors` are empty, and the live oracle's and nop's `guards_tripped` are empty (S3-24). A no-op that trips guards is inverted polarity even at reward 0.0 (BLOCKER). | BLOCKER | cmd S3-36, probe S5-02 | Sample `ledger.py`, `ctrf_pytest_plugin.py` |
| S3-37 | **Channel mix.** `tests/reward/reward.toml` is the Sample's (S1-37): one `[[reward]]`, `name = "reward"`, `aggregation = "weighted-mean"`, `weights = { pytest = 0.5, rubric = 0.5 }`, the keys naming the channel dirs under `tests/reward/`. A missing or extra channel key drops or breaks a channel: BLOCKER. | BLOCKER | cmd S4-RK | Sample |

Commands for Stage 3:

```bash
source /tmp/qc/<uuid>-report/env.sh
# S3-01 / S3-02  what the graders open
grep -nE 'open\(|read_text|json\.load|environ|/logs/|/workspace|trajectory|completions|server_tool_calls|solution|TRUTH|gt_env' "$T/test_outputs.py" "$T/claims_lib.py"
# S3-03 / S3-04 / S3-05  (identity with the Sample is S1-37; read only if test.sh differs)
grep -nE '^# -+ [0-9]|exit|reward\.json|reward_producer|rubric_judge_failed|rubric_unclamped|state_capture_failed|judge_ws|SKIP_REASON|ctrf_pytest_plugin' "$T/test.sh"
# S3-10 / S3-11 / S3-12  assert hygiene
grep -nE 'assert +(True|1|"|\x27)|or True|except[^:]*:\s*(pass|return)|pytest\.(skip|xfail)|\[0\]|\[-1\]|== *[0-9]+\.[0-9]+' "$T/test_outputs.py"
python3 - "$T/test_outputs.py" <<'PY'
import ast, sys
src = open(sys.argv[1]).read(); tree = ast.parse(src)
for n in ast.walk(tree):
    if isinstance(n, ast.Compare) and len(n.comparators) == 1 and ast.dump(n.left) == ast.dump(n.comparators[0]):
        print('SELF_COMPARE line', n.lineno)
    if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):
        body = [x for x in ast.walk(n)]
        if not any(isinstance(x, (ast.Assert, ast.Return)) for x in body):
            print('NO_ASSERT', n.name, n.lineno)
        if any(isinstance(x, ast.Assert) and isinstance(x.test, ast.Constant) for x in body) and \
           not any(isinstance(x, ast.Assert) and not isinstance(x.test, ast.Constant) for x in body):
            print('CONST_ASSERT only', n.name, n.lineno)
PY
# S3-13  imports vs the verifier image pins
grep -hoE '^(import|from) [A-Za-z_][A-Za-z0-9_]*' "$T"/*.py "$RK/pytest/ledger.py" | awk '{print $2}' | sort -u
grep -nE 'pip install' "$T/Dockerfile"; ls "$T"/*.py
# S3-14
grep -nE 'random|uuid|time\.time|time\(\)|datetime\.now|shuffle|set\(' "$T/test_outputs.py" "$T/claims_lib.py"
```

S3-25 proportionality, S3-32 negative deduction, S3-33 rating, S3-34 components and S3-35 gates, from
`tests/test_weights.json` (every numeric value keyed `test_*` is a check weight):

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/neg_static.py <<'PY'
# S3-25 / S3-32 / S3-33 / S3-34 / S3-35  test_weights.json against the checks test_outputs.py defines
import ast, collections, json, re, sys, pathlib, tomllib
T = pathlib.Path(sys.argv[1])
raw = (T / "test_weights.json").read_text(); doc = json.loads(raw)
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
W = {k: v for k, v in ALL if isinstance(v, (int, float)) and not isinstance(v, bool)}
fns = {n.name for n in ast.walk(ast.parse((T / "test_outputs.py").read_text()))
       if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")}
pos = {k: v for k, v in W.items() if v > 0}; neg = {k: v for k, v in W.items() if v < 0}
P, N = sum(pos.values()), sum(-v for v in neg.values())
print("guard_polarity:", doc.get("guard_polarity", "fail_charges (default)"))
print("S3-25 checks", len(W), "| positive", len(pos), "total", P, "| negative", len(neg), "total", N,
      "| floor", round(-N / P, 3) if P else "n/a")
print("S3-25 largest positive share", round(max(pos.values()) / P, 3) if P else "n/a", "(<= 0.5)",
      "| largest penalty", max(neg.values(), key=abs) if neg else 0, "(< positive total)", "| N - P", N - P, "(<= 3)")
print("S3-32 BLOCKER negative weights naming no test_outputs.py function:", sorted(k for k in neg if k not in fns) or "none")
print("S3-32 BLOCKER test_guard_* functions with no negative weight:", sorted(f for f in fns if f.startswith("test_guard_") and f not in neg) or "none")
print("S3-33 BLOCKER guard-named checks rated positive:", sorted(k for k in pos if k.startswith("test_guard_")) or "none")
print("S3-33 MINOR negative checks not named test_guard_*:", sorted(k for k in neg if not k.startswith("test_guard_")) or "none")
print("S3-33 MAJOR test_outputs.py checks with no weight (score nothing):", sorted(fns - set(W)) or "none")
print("S3-33 rating counts:", dict(sorted(collections.Counter(W.values()).items())))
for k, v in sorted(W.items(), key=lambda kv: (-abs(kv[1]), kv[0])):
    print("S3-33 read %4s  %s" % (v, k))
gate = doc.get("gate") or {}
print("S3-35 gate:", gate or "none", "| keys ledger.py ignores (MAJOR):", sorted(set(gate) - {"require_no_guards", "floor"}) or "none")
rng = gate.get("require_no_guards")
if rng is not None and not isinstance(rng, bool):
    print("S3-35 MINOR require_no_guards is a %s; ledger.py reads it as a flag" % type(rng).__name__)
comps = doc.get("components") or {}
tt, rb = comps.get("traj_tests") or {}, comps.get("rubric") or {}
print("S3-34 components:", sorted(comps), "(must be exactly ['rubric', 'traj_tests'])")
tw = [abs(v) for v in (tt.get("tests") or {}).values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
want_t = round(sum(tw) / len(tw), 3) if tw else None
print("S3-34 traj_tests graded=%s test_file=%s weight=%s mean|w|=%s -> %s" % (tt.get("graded"), tt.get("test_file"),
      tt.get("weight"), want_t, "ok" if tt.get("graded") is True and tt.get("test_file") == "test_outputs.py" and want_t is not None and abs(float(tt.get("weight") or 0) - want_t) < 0.006 else "HIT"))
try:
    jw = [abs((c.get("annotations") or {}).get("source_weight", 0)) for c in tomllib.load(open(T / "reward/rubric/judge.toml", "rb")).get("criterion", [])]
except Exception as e:
    jw = []; print("S3-34 judge.toml unreadable:", e)
want_r = round(sum(jw) / len(jw), 3) if jw else None
print("S3-34 rubric graded=%s file=%s weight=%s mean|source_weight|=%s -> %s" % (rb.get("graded"), rb.get("file"), rb.get("weight"), want_r,
      "MAJOR file must be judge.toml" if rb.get("file") != "judge.toml" else ("ok" if rb.get("graded") is True and want_r is not None and abs(float(rb.get("weight") or 0) - want_r) < 0.006 else "HIT (MINOR)")))
PY
python3 /tmp/qc/neg_static.py "$T"
```

Reading the output: any BLOCKER line that is not `none` is a finding. The `S3-33 read` lines list every check from
heaviest to lightest; read them against the instruction and TRUTH.md for S3-33(d).

S3-36, verdict styles and guard polarity, using the bundle's own `ledger.verdict_style` (imports `test_outputs`
from the copy; the no-op probe in Stage 5 is the proof):

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/rk_verdict_style.py <<'PY'
# S3-36  every weighted check gives a verdict the ledger can read, and guards match guard_polarity
# usage: rk_verdict_style.py <tests dir>
import collections, json, pathlib, sys
T = pathlib.Path(sys.argv[1]); sys.path[:0] = [str(T), str(T / "reward" / "pytest")]
import ledger, test_outputs
doc = json.loads((T / "test_weights.json").read_text()); W = ledger._tests_of(doc)
pol = doc.get("guard_polarity", "fail_charges")
print("S3-36 guard_polarity:", pol, "(valid)" if pol in ledger.POLARITIES else "BLOCKER not one of %s" % (ledger.POLARITIES,))
styles = collections.Counter()
for n, w in W.items():
    fn = getattr(test_outputs, n, None)
    st = ledger.verdict_style(fn) if callable(fn) else "MISSING"
    styles[st] += 1
    if st in ("none", "MISSING"): print("S3-36 BLOCKER", n, w, "verdict style", st, "(never passes: a positive never earns; a fail_charges guard always trips)")
    if w < 0: print("S3-36 read guard %-70s style=%s doc=%s" % (n, st, ((fn.__doc__ or "").strip().splitlines() or [""])[0][:70] if callable(fn) else ""))
print("S3-36 verdict styles:", dict(styles))
PY
(cd "$T" && python3 /tmp/qc/rk_verdict_style.py "$T")
```

Read every `S3-36 read guard` line against the declared polarity: under `pass_charges` the docstring names the
forbidden act and the body asserts or returns true when it shows; under `fail_charges` the body passes when the run
behaved.

## 9. Stage 4: rubric compliance, tests/reward/rubric/judge.toml (8 min, strict)

The rubric is the compiled `tests/reward/rubric/judge.toml` (2a, 2d). This is the most important stage: be strict
and correct. A missing judge.toml is a BLOCKER (0 criteria, S4-18). Every rule below holds for the Sample's rubric;
a rule that would flag it is wrong.

Weight scale (user decision 2026-10-19): an author's positive criterion weighs 1, 3 or 5; a negative one -1, -3 or
-5. In the compiled file that scale is `annotations.source_weight`; the compiled `weight` is
`source_weight / total_positive_weight` (S4-27).

Schema source (cite it in the report): harbor-rewardkit, read from the installed package, never from memory:
`pip download --no-deps harbor-rewardkit==0.2.3 -d /tmp/qc/rk` (the version `tests/Dockerfile` pins) and unzip, then
`rewardkit/models.py` (`JudgeTomlConfig`, `JudgeConfig`, `CriterionConfig`, `ScoringConfig`, all pydantic
`extra="forbid"`) and `rewardkit/reward.py` (`_validate_weights`, `aggregate_scores`). Allowed keys in 0.2.3:

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
| S4-08 | No double counting with a deterministic check: no judged criterion grades the same state record, field or trajectory act that a `test_outputs.py` check grades directly. A criterion about what the final reply SAYS (the Sample's `[final answer]` criteria) does not overlap a check on the state; restating a fact the claim-coverage check also scores is allowed (the Sample does both). | MAJOR | cross-reference table | RUTHLESS 2, Checklist X1, v4 S3-X1, Sample |
| S4-09 | Atomic: one finding per criterion. A list of the members of one finding (all re-delivered counts, all recipients told, as in the Sample) is one finding; `and`/`or` joining two independent findings is a hit. | BLOCKER | read | v4 S3-J4/J5, Checklist M4, Sample |
| S4-10 | Operational and decidable: no vague standard (`appropriate`, `reasonable`, `professional`, `clear`, `concise`, `tidy`, `courteous`, `tasteful`, `useful`, `good`, `well`) without a decision line a judge can apply to the evidence; no internal state (`understands`, `realises`). Exact figures, names and ids (the Sample's style) are decidable. | BLOCKER | cmd S4-10 | v4 S3-J2/J3, Checklist M2/M3 |
| S4-11 | Grounded in `instruction.md` and `TRUTH.md`: every criterion grades something the instruction asked for (for `[final answer]`, an item of the requested handover), and every figure or record it turns on appears in TRUTH.md and in the served world. | BLOCKER | search each needle | v4 S3-Q1/Q2, Checklist L1/L2 |
| S4-12 | No hint leak: no exact deliverable filename the instruction does not give, no decoy adopted as correct (a negative criterion naming a decoy as the forbidden outcome is fine). | MAJOR | read against TRUTH.md | v4 S3-J8/Q3, Checklist M6/L3 |
| S4-13 | Evaluable from what the judge receives: `[judge] cwd = "/logs/verifier/judge_ws"` (the directory test.sh builds before rewardkit runs) and `atif-trajectory` a file test.sh writes there (`judge_ws/trajectory.json`); no `[judge] files`. A `[final answer]` criterion needs only `final_message.md` (and delivered files it refers to); `[trajectory]` needs `trajectory.json`; `[end state]` needs `end_env.json` (copied only when captured; the prompt then sends the judge to the write calls). `annotations.evidence` is informational (the Sample names `/tmp/agent_trajectory.json`, the source of `final_message.md`). | BLOCKER | cmd S4-RK, read test.sh step 4 | Sample |
| S4-16 | The rubric reaches the reward as the Sample's test.sh does (S1-37): rewardkit over `/tests/reward` when `JUDGE_MODEL` and a login for `JUDGE_TRANSPORT` are present and `rubric/judge.toml` is non-empty; else the pytest channel alone plus `rubric_judge_failed.txt`; a timed-out or all-errored judge is dropped; `harbor-rewardkit==0.2.3` pinned in `tests/Dockerfile` and `tests/Dockerfile.ecr`, `@openai/codex@0.154.0` in `tests/Dockerfile`. | BLOCKER | cmd S1-37, cmd S4-16 | Sample |
| S4-18 | Criterion count: fewer than 20 `[[criterion]]` rows (or no judge.toml) is a BLOCKER; 20-24 is a MINOR warning (non-blocking); 25 or more passes (the Sample has 35). | BLOCKER / MINOR | cmd S4-18 | user decision 2026-10-17 |
| S4-19 | judge.toml parses as TOML. | BLOCKER | cmd S4-18 | rewardkit `_load_toml` |
| S4-20 | Schema: only the rewardkit keys above, with the right types and enum values, at top level, in `[judge]`, `[[criterion]]` and `[scoring]`. `[judge]` matches 2d (`judge = "codex"`, `timeout = 1200`, `cwd`, `atif-trajectory`, `prompt_template = "prompt.md"`, `weight = 1.0`; no `model`). | BLOCKER | cmd S4-18 | rewardkit `models.py` (extra="forbid"), Sample |
| S4-21 | Every criterion has a unique non-empty `id` (the Sample numbers them `"1"`, `"2"`, ...), a unique non-empty `name` slug (`j-...` for positive, `n-...` for negative in the Sample), a non-empty `description`, a numeric `weight`, `type = "binary"`, and `annotations` with `number`, `source_weight`, `total_positive_weight`, `is_positive`, `evaluation_target`, `category`, `priority`, `evidence` (a missing annotation field is a MAJOR). | BLOCKER | cmd S4-18, cmd S4-RK | rewardkit `CriterionConfig`, Sample |
| S4-22 | No duplicate or paraphrased criteria (same fact asked twice in other words). | BLOCKER | cmd S4-18, then read | Checklist M5 |
| S4-23 | Weights: positive source total > 0; no single criterion carries more than half the positive source weight. | BLOCKER | cmd S4-RK | RUTHLESS 3.3 |
| S4-24 | Negative criteria are written and wired so the judge DEDUCTS them: (a) `source_weight` is -1, -3 or -5 and the compiled `weight` is negative; (b) `is_positive = false` on every negative criterion and `true` on every positive one (sign and flag agree); (c) the description states the forbidden behaviour as a fact that is TRUE when the run did it ("The handover reply says a shipper was scaled to zero ..."), never as its absence; (d) no `negate = true`, and no `annotations.type` containing "negative" (rewardkit 0.2.3 `runner.py` then sets `negate` silently, which flips the verdict and double-negates a negative weight); (e) the absolute negative source total does not exceed the positive total; (f) `[scoring] aggregation = "weighted-sum"`. | BLOCKER | cmd S4-RK, then read | rewardkit `_validate_weights`, user decision 2026-10-19 |
| S4-25 | `[verifier] environment_mode = "separate"`, so the judge never runs in the agent's container. | BLOCKER | cmd S1-12 | Harbor 0.24.0 `VerifierEnvironmentMode` |
| S4-26 | No answer leakage through the rubric: `tests/reward/**` is never agent-visible (S2-24), and criterion text adds no answer the agent could see. | BLOCKER | cmd S2-23 | leakage policy |
| S4-27 | Weight scale: every `source_weight` is 1, 3, 5, -1, -3 or -5 (a 0, 2, 4, 0.5, 10 or a string is a BLOCKER). Every compiled `weight` equals `source_weight / total_positive_weight`, and `total_positive_weight` is the same on every criterion and equals the sum of positive source weights, so the positive weights sum to 1.0 (the Sample: 64, so 5 -> 0.078125). Report the count at each step. | BLOCKER | cmd S4-RK | user decision 2026-10-19, Sample |
| S4-28 | **Negative criteria lower the rubric score.** rewardkit 0.2.3 (verified in source 2026-10-23, see the note under the table) scores each binary criterion 1.0 or 0.0, weights it by the compiled `weight`, and for `weighted-sum` returns `sum(value x weight)` with no normalisation and no clamp. So all positives met with no negative committed gives 1.0, and one committed -5 gives `1 - 5 / total_positive_weight`. Every negative committed with no positive met goes below 0. test.sh step 5 clamps a negative channel to 0 (keeping `rubric_unclamped`) and recombines with `reward.toml` (S1-37). A score that does not fall, rises, or exceeds 1.0 is a BLOCKER. | BLOCKER | cmd S4-RK | rewardkit 0.2.3 `reward.aggregate_scores`, Sample, user decision 2026-10-19 |
| S4-29 | Every `description` starts with the tag for its `annotations.evaluation_target`: `[final answer]` for `final_answer`, `[trajectory]` for `trajectory`, `[end state]` for an end-state target. `prompt.md` tells the judge which evidence each tag uses; an untagged or mis-tagged criterion is judged on the wrong evidence. | MAJOR | cmd S4-RK | Sample `prompt.md` |
| S4-30 | `[judge] prompt_template` is `prompt.md` beside judge.toml, the Sample's (S1-37), with the `{criteria}` placeholder. `tests/reward/rubric/instruction.md` is byte-identical to the bundle's `instruction.md`: the judge grades against the task the agent was given. | MAJOR | cmd S4-RK | Sample `prompt.md`, `test.sh` step 4 |

Commands for Stage 4:

```bash
source /tmp/qc/<uuid>-report/env.sh
# S4-18 .. S4-22  count, parse, schema, ids, names, duplicates (rewardkit 0.2.3 rules)
JT="$RK/rubric/judge.toml"
python3 - "$JT" <<'PY'
import math, re, sys, tomllib
try:
    d = tomllib.load(open(sys.argv[1], 'rb'))
except FileNotFoundError:
    print('S4-18 BLOCKER: no tests/reward/rubric/judge.toml (0 criteria)'); sys.exit()
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
want = {'judge': 'codex', 'timeout': 1200, 'cwd': '/logs/verifier/judge_ws', 'atif-trajectory': '/logs/verifier/judge_ws/trajectory.json',
        'prompt_template': 'prompt.md', 'weight': 1.0}
print('S4-20 [judge] differs from the Sample:', {k: j.get(k) for k in set(want) | set(j) if j.get(k) != want.get(k)} or 'none')
ids, names, seen = set(), set(), {}
for c in crit:
    bad = [f'key {k}' for k in c if k not in C] + [f'type of {k}' for k, t in C.items() if k in c and not ok(c[k], t)]
    for f, pool in (('id', ids), ('name', names)):
        v = c.get(f)
        if not isinstance(v, str) or not v.strip(): bad.append('no ' + f)
        elif v in pool: bad.append('duplicate ' + f)
        pool.add(v)
    if not str(c.get('description', '')).strip(): bad.append('empty description')
    w = c.get('weight')
    if not ok(w, (int, float)) or (isinstance(w, float) and not math.isfinite(w)): bad.append('weight not numeric')
    if c.get('type', 'binary') != 'binary': bad.append('type is not binary')
    key = ' '.join(re.findall(r'[a-z0-9]+', str(c.get('description', '')).lower()))
    if key in seen: bad.append(f'duplicate description of {seen[key]}')
    seen[key] = c.get('id')
    print(c.get('id'), c.get('name'), 'OK' if not bad else bad)
PY
# S4-09 / S4-10  read every description; these words need a decision line
grep -niE '\b(appropriate|reasonabl|professional|clear|concise|tidy|courteous|tasteful|useful|plausible|good|well|properly|adequate|quality|understands|reali[sz]es)' "$JT"
# S4-08 / S4-11  print each description beside the instruction's asks and the claims, then read
python3 -c "import tomllib,sys;[print(c.get('id'),c.get('name'),(c.get('annotations') or {}).get('source_weight'),'|',c.get('description')) for c in tomllib.load(open(sys.argv[1],'rb')).get('criterion',[])]" "$JT"
python3 -c "import json,sys;[print('claim',c.get('id'),'|',c.get('text')) for c in json.load(open(sys.argv[1])).get('reported',{}).get('claims',[])]" "$T/oracle.json"
# S4-16  judge wiring and pins
grep -nE 'rewardkit|JUDGE_SKIP|JUDGE_TRANSPORT|rubric_judge_failed|judge_ws' "$T/test.sh"
grep -nE 'rewardkit|codex' "$T"/Dockerfile*
```

`cmd S4-RK`: the compiled rubric's weights, polarity, tags, judge inputs and the channel mix (S3-34, S3-37, S4-13,
S4-21, S4-23, S4-24, S4-27 to S4-30). It is static; the S4-28 lines simulate rewardkit's weighted sum with the
compiled weights:

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/rk_rubric_check.py <<'PY'
# S4-13 S4-21 S4-23 S4-24 S4-27 S4-28 S4-29 S4-30 S3-34 S3-37  compiled tests/reward/rubric/judge.toml and its wiring
# usage: rk_rubric_check.py <bundle copy B>
import json, math, pathlib, re, sys, tomllib
b = pathlib.Path(sys.argv[1]); T = b / "tests"; RK = T / "reward"; R = RK / "rubric"
def chk(cid, cond, what): print(cid, "ok " if cond else "HIT", what)
d = tomllib.load(open(R / "judge.toml", "rb")); crit = d.get("criterion", []); j = d.get("judge", {})
tsh = (T / "test.sh").read_text()
TAG = {"final_answer": "[final answer]", "trajectory": "[trajectory]", "end_state": "[end state]"}
ANN = ("number", "source_weight", "total_positive_weight", "is_positive", "evaluation_target", "category", "priority", "evidence")
sw = []; tps = set()
for c in crit:
    a = c.get("annotations") or {}; s = a.get("source_weight"); tp = a.get("total_positive_weight"); w = c.get("weight")
    bad = ["S4-21 annotation %s missing" % f for f in ANN if f not in a]
    if s not in (1, 3, 5, -1, -3, -5) or isinstance(s, bool): bad.append("S4-27 source_weight %r off the 1/3/5, -1/-3/-5 scale" % (s,))
    pos = a.get("is_positive")
    if not isinstance(pos, bool): bad.append("S4-24 is_positive missing or not a bool")
    elif isinstance(s, (int, float)) and (s > 0) != pos: bad.append("S4-24 sign/flag mismatch: source_weight %s is_positive %s" % (s, pos))
    if isinstance(s, (int, float)) and isinstance(tp, (int, float)) and tp and isinstance(w, (int, float)) and not math.isclose(w, s / tp, abs_tol=1e-9):
        bad.append("S4-27 weight %s != source_weight/total_positive_weight %s" % (w, s / tp))
    if c.get("negate"): bad.append("S4-24 negate=true")
    if "negative" in str(a.get("type", "")).lower(): bad.append("S4-24 annotations.type says negative (rewardkit sets negate)")
    tag = TAG.get(a.get("evaluation_target"))
    if not str(c.get("description", "")).startswith(tag or "\0"): bad.append("S4-29 description does not start with the %s tag" % (tag or "known evaluation_target"))
    if isinstance(s, (int, float)): sw.append((c.get("id"), s))
    tps.add(tp)
    print(c.get("id"), c.get("name"), s, "OK" if not bad else bad)
P = sum(s for _, s in sw if s > 0); N = sum(-s for _, s in sw if s < 0)
chk("S4-27", tps == {P}, "total_positive_weight %s equals the positive source total %s" % (sorted(tps, key=str), P))
chk("S4-24", d.get("scoring", {}).get("aggregation") == "weighted-sum", "[scoring] aggregation weighted-sum")
chk("S4-24", N <= P, "negative source total %s <= positive %s" % (N, P))
chk("S4-23", bool(P) and max(s for _, s in sw if s > 0) / P <= 0.5, "no criterion over half the positive weight")
# S4-28: rewardkit 0.2.3 weighted-sum = sum(value * weight), binary value 1.0/0.0 (verified in source 2026-10-23)
wt = {c.get("id"): c.get("weight", 0) for c in crit}
allgood = sum(w for w in wt.values() if w > 0)
negs = sorted((s, i) for i, s in sw if s < 0)
chk("S4-28", math.isclose(allgood, 1.0, abs_tol=1e-6), "all positives met, no negative: %.6f (want 1.0)" % allgood)
if negs:
    s, i = negs[0]; chk("S4-28", math.isclose(allgood + wt[i], 1 + s / P, abs_tol=1e-6), "%s (source %s) committed: %.6f (want %.6f)" % (i, s, allgood + wt[i], 1 + s / P))
chk("S4-28", "rubric_unclamped" in tsh and re.search(r'reward\["rubric"\] *< *0', tsh) is not None, "test.sh clamps a negative rubric channel to 0 and recombines")
# S4-13 / S4-30 judge inputs
cwd = j.get("cwd", ""); at = j.get("atif-trajectory", "")
chk("S4-13", cwd == "/logs/verifier/judge_ws" and 'JW="$LOGS/judge_ws"' in tsh, "[judge] cwd is the judge_ws dir test.sh builds (%s)" % cwd)
chk("S4-13", at.startswith(cwd + "/") and pathlib.PurePath(at).name in tsh, "[judge] atif-trajectory %s is written by test.sh" % at)
chk("S4-13", "files" not in j, "[judge] has no files (the judge reads its cwd)")
pt = R / str(j.get("prompt_template", ""))
chk("S4-30", pt.is_file() and "{criteria}" in pt.read_text(), "prompt_template %s exists and has {criteria}" % pt.name)
chk("S4-30", (R / "instruction.md").is_file() and (R / "instruction.md").read_bytes() == (b / "instruction.md").read_bytes(), "rubric/instruction.md is byte-identical to instruction.md")
# S3-37 reward.toml
rt = tomllib.load(open(RK / "reward.toml", "rb")).get("reward") or []
r0 = rt[0] if rt else {}
chans = sorted(p.name for p in RK.iterdir() if p.is_dir() and p.name != "__pycache__")
chk("S3-37", len(rt) == 1 and r0.get("name") == "reward" and r0.get("aggregation") == "weighted-mean", "reward.toml one [[reward]] name=reward weighted-mean")
chk("S3-37", (r0.get("weights") or {}) == {"pytest": 0.5, "rubric": 0.5} and sorted(r0.get("weights") or {}) == chans,
    "reward.toml weights %s (Sample: pytest 0.5, rubric 0.5) name the channel dirs %s" % (r0.get("weights"), chans))
tw = json.load(open(T / "test_weights.json")); rb = (tw.get("components") or {}).get("rubric") or {}
mean = round(sum(abs(s) for _, s in sw) / len(sw), 3) if sw else None
print("S3-34 rubric component weight %s vs mean |source_weight| %s (documentation; a mismatch is MINOR)" % (rb.get("weight"), mean))
PY
python3 /tmp/qc/rk_rubric_check.py "$B"
```

Every `HIT` and every per-criterion list is a finding at the row's severity.

rewardkit 0.2.3 behaviour behind S4-24, S4-28, S3-37 and S5-12 was read from the `harbor-rewardkit==0.2.3` wheel
(source only, not executed) on 2026-10-23:

- `reward.aggregate_scores`: `weighted-sum` returns `sum(s.value * s.weight)` with no normalisation and no clamp.
  `weighted-mean` returns `sum(v * w) / sum(w)`. Negative weights raise unless the aggregation is `weighted-sum`.
- `runner.py`: criterion weights are `[c.weight for c in config.criterion]`. A binary verdict is 1.0 or 0.0.
  `negate` is set from `annotations.type` containing "negative" when `negate` is not given.
- `runner._aggregate_named`: the `[[reward]]` channels in `reward.toml` are combined with `aggregate_scores` using the
  `weights` overrides and rounded to 4 places.
- `reward.Reward.score`: the `[judge] guard = "penalize"` setting caps the score at 0. The default is `"off"`, and the
  Sample sets no guard.
- `judges._timeout_scores`: a timed-out judge returns errored 0.0 scores. That is why test.sh step 5 drops a
  timed-out or all-errored judge rather than keeping a 0.

If `tests/Dockerfile` pins another version, re-read these four places before relying on S4-28.

For S4-08 to S4-12 and S4-22 write one line per criterion in the report: id, verdict, and the reason (for example
"7 BLOCKER S4-10: 'reads as a grower-facing settlement ... an order a grower can follow' has no decision line;
S4-09: deliveries, exclusions and deductions are three independent findings").

## 10. Stage 5: execution (20 min, mandatory)

Ledger probes are the fast pre-check (seconds) and run first. The grader reads the run's trajectory, so `gt_env.json` alone cannot reproduce the oracle's 1.0; the probes test the ledger instead, by forcing check outcomes through the bundle's own `ledger.py`. The oracle's real 1.0 is proven live (S5-10). The live Harbor runs (S5-10, S5-11) are mandatory BLOCKERs: a bundle whose oracle does not score exactly 1.0, or whose nop does not score exactly 0.0, on Harbor 0.24.0 FAILs. If Docker is unavailable the verdict is `PARTIAL` with S5-10/S5-11 under "Not checked", never `PASS`.

| ID | Rule | Sev | How to check | From |
|---|---|---|---|---|
| S5-01 | Ledger ceiling: with every goal check met and no guard tripped (forced), `ledger.py` gives exactly 1.0. | BLOCKER | probe `allgood` | tabish A1, v4 S3-O3 |
| S5-02 | No-op: an empty trajectory, seed state (`tests/old_env.json` as the snapshot) and an empty `/workspace` score exactly 0.0, with `grade_report.json guards_tripped` and `errors` empty (S3-36(d), S3-11). | BLOCKER | probe `noop` | tabish C1/M1, v4 S3-O7, Sample |
| S5-05 | No snapshot: with `ATLAS_END_ENV` missing, `ledger.py` still writes `grade_report.json` (S3-03). | BLOCKER | probe `nosnap` | Sample |
| S5-06 | Determinism: the no-op probe run twice gives the same reward and the same tripped guards. | BLOCKER | probe `noop` + `noop2` | tabish D4 |
| S5-07 | Rubric on the ledger: not probed (rewardkit mixes the channels with the judge). Proved by S1-37 identity of `test.sh` and `reward.toml` plus S4-28. Record under CLEARED with the identity result. | BLOCKER | S1-37, S4-28 | Sample |
| S5-13 | **Negatives deducted.** From the all-met baseline, each negative check tripped alone (its charging verdict under `guard_polarity`) lowers the reward to exactly `(P - abs(w)) / P` (P = positive total), or to 0 when `gate.require_no_guards` is truthy. | BLOCKER | probe `trip_*` | user decision 2026-10-19, Sample |
| S5-10 | Live executability: `harbor run` (Harbor 0.24.0) with the `oracle` agent on the bundle copy produces `verifier/reward.json` with `reward` exactly 1.0 (pytest channel alone, judge inputs unset), `grade_report.json` with empty `missed`, `guards_tripped` and `errors`, and no trial exception. | BLOCKER | live run below | user decision 2026-10-17 |
| S5-11 | Live null run: `harbor run` with the `nop` agent produces `reward` exactly 0.0 with empty `guards_tripped` (a reward file must exist; a missing reward file or exception is a FAIL of this check, not a 0). The Sample records the same measurement in `test_weights.json null_floor_measured`. | BLOCKER | live run below | user decision 2026-10-17, Sample |
| S5-12 | Live rubric unscored, not zeroed: `reward.json` is `{"pytest": 1.0, "reward": 1.0}` with no `rubric` key, `rubric_judge_failed.txt` names the reason (`JUDGE_MODEL is empty`), `judge.json` has `ran: false`, `reward_producer.json` has `channels: ["pytest"]`, `weights: {"pytest": 1.0}`. | BLOCKER | live run below | Sample |

Ledger probes (S5-01, S5-02, S5-05, S5-06, S5-13, plus the S3-36 proof) run the bundle's own
`tests/reward/pytest/ledger.py` on `$B.re`, standalone with `ATLAS_TESTS_DIR` / `ATLAS_VERIFIER_LOGS`, patching
`test_outputs` before the ledger imports it. A forced "behaved" guard returns the value that does not charge under
`guard_polarity`. Judge credentials and `JUDGE_MODEL` are removed from the environment. `$B` is never touched.
Checked on the Sample's files on 2026-10-23: every line `ok`; a copy with `guard_polarity` flipped kept the no-op
at 0.0 but listed all seven guards as tripped, which is the inversion this probe exists to catch.

```bash
source /tmp/qc/<uuid>-report/env.sh
cat > /tmp/qc/ledger_probe_rk.py <<'PY'
# S5-01 S5-02 S5-05 S5-06 S5-13 + S3-36  probes of tests/reward/pytest/ledger.py (no judge, no Docker)
# usage: ledger_probe_rk.py <bundle copy B> <out dir O>   -> works on B.re
import json, os, shutil, subprocess, sys
B, O = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
if len(sys.argv) == 5:                                     # child: patch checks, then run the bundle's own ledger
    T, plan = sys.argv[3], json.loads(sys.argv[4])
    sys.path.insert(0, T); import test_outputs
    for name, val in plan.items(): setattr(test_outputs, name, (lambda v: (lambda *a, **k: v))(val))
    sys.path.insert(0, os.path.join(T, "reward", "pytest")); import ledger
    ledger.run_ledger(); sys.exit(0)
RE = B + ".re"; shutil.rmtree(RE, ignore_errors=True); shutil.rmtree(O, ignore_errors=True)
shutil.copytree(B, RE, ignore=shutil.ignore_patterns("trajectories", "trajectory", "__pycache__"))
T = os.path.join(RE, "tests")
doc = json.load(open(os.path.join(T, "test_weights.json")))
W = ((doc.get("components") or {}).get("traj_tests") or {}).get("tests") or doc.get("tests") or {}
W = {k: v for k, v in W.items() if isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0}
P = sum(v for v in W.values() if v > 0)
pol = doc.get("guard_polarity", "fail_charges")
gate = doc.get("gate") or {}; gated = bool(gate.get("require_no_guards"))
print("guard_polarity", pol, "| positive total", P, "| gate", gate or "none")
inp = os.path.join(O, "inputs"); os.makedirs(os.path.join(inp, "workspace"), exist_ok=True)
traj = os.path.join(inp, "empty_trajectory.json"); json.dump({"steps": [], "final_message": ""}, open(traj, "w"))
old_end = os.path.join(inp, "end_env.json"); shutil.copy(os.path.join(T, "old_env.json"), old_end)
def run(tag, plan=None, end=old_end):
    o = os.path.join(O, tag); os.makedirs(o, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.endswith(("_API_KEY", "_TOKEN", "_B64")) and k != "JUDGE_MODEL"}
    env.update(PYTHONDONTWRITEBYTECODE="1", ATLAS_TESTS_DIR=T, ATLAS_VERIFIER_LOGS=o, ATLAS_TRAJECTORY=traj,
               MCPATLAS_TRAJECTORY=traj, COMPLEXMCP_TRAJECTORY=traj, ATLAS_END_ENV=end,
               ATLAS_OLD_ENV=os.path.join(T, "old_env.json"), ATLAS_ORACLE=os.path.join(T, "oracle.json"),
               ATLAS_OUTPUT_ROOTS=os.path.join(inp, "workspace"), ATLAS_SERVER_LOG=os.path.join(inp, "missing_server.log"),
               AUTH_CLAIMS_PATH=os.path.join(o, "claims_coverage.json"))
    r = subprocess.run([sys.executable, os.path.abspath(__file__), B, O, T, json.dumps(plan or {})], cwd=T, env=env, capture_output=True, text=True)
    open(os.path.join(o, "stdout"), "w").write(r.stdout + r.stderr)
    try: return json.load(open(os.path.join(o, "grade_report.json")))
    except Exception: return None
def show(cid, tag, d, want):
    got = None if d is None else d.get("reward")
    ok = got is not None and abs(got - want) < 1e-4
    print("%-6s %-40s reward=%s expected=%.6f %s" % (cid, tag[:40], got, want, "ok" if ok else "HIT (see %s/%s/stdout)" % (O, tag)))
    return ok
calm = pol == "fail_charges"                       # the value a guard returns when the run behaved
good = {k: (True if v > 0 else calm) for k, v in W.items()}
a = run("noop"); show("S5-02", "noop", a, 0.0)
print("S3-36  no-op guards tripped (must be none; the 0-clamp hides them in the reward):", (a or {}).get("guards_tripped"))
print("S3-36  no-op checks that raised:", (a or {}).get("errors"))
b = run("noop2"); print("S5-06  determinism (no-op twice)", "ok" if a and b and a.get("reward") == b.get("reward") and a.get("guards_tripped") == b.get("guards_tripped") else "HIT")
d = run("nosnap", end=os.path.join(inp, "missing_end_env.json")); print("S5-05  no snapshot: ledger report", "written ok" if d is not None else "HIT: none written")
show("S5-01", "allgood", run("allgood", good), 1.0)
bad = 0
for g in sorted(k for k, v in W.items() if v < 0):
    want = 0.0 if gated else max(0.0, (P - abs(W[g])) / P)
    bad += not show("S5-13", "trip_" + g, run("trip_" + g, dict(good, **{g: not calm})), want)
print("S5-13 ", "every negative deducted" if not bad else "%d negative(s) NOT deducted" % bad)
PY
python3 /tmp/qc/ledger_probe_rk.py "$B" "$O"
```

Every reward line must end `ok`, and both `S3-36` lists must be empty. A `no-op checks that raised` entry is a
check that crashes on an empty run; read its reason in `$O/noop/grade_report.json` (S3-11). On a HIT open
`$O/<case>/stdout` and `$O/<case>/grade_report.json` (`missed`, `guards_tripped`, `errors`, per-test `reason`). A
no-op above 0.0 is seeded-state free credit (S3-21).

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

Images: the bundle has no `docker_image`, so Harbor builds `environment/Dockerfile`, the light-servers image from
`light-servers/Dockerfile` (compose default; `LIGHT_SERVERS_DOCKERFILE=Dockerfile.ecr` selects the ECR variant) and
the verifier from `tests/Dockerfile` (`JUDGE_DOCKERFILE=Dockerfile.ecr` selects the linux/amd64 ECR variant). Leave
both selectors unset. Pass `--force-build` (it changes no grading). If a build fails (for example an apt pin the live
Debian mirror no longer serves, or ECR access), record the exact error: S5-10/S5-11 are then FAIL when the bundle's
own Dockerfile cannot build, Not checked (PARTIAL) when the host cannot reach a registry.

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
unset JUDGE_MODEL CODEX_AUTH_B64 JUDGE_CLAUDE_TOKEN CLAUDE_CODE_OAUTH_TOKEN JUDGE_DOCKERFILE LIGHT_SERVERS_DOCKERFILE
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
cat "$J/$UUID-oracle"/*/verifier/reward_producer.json "$J/$UUID-oracle"/*/verifier/rubric_judge_failed.txt "$J/$UUID-oracle"/*/verifier/judge.json
for a in oracle nop; do python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(sys.argv[2],'reward',d['reward'],'missed',d['missed'],'guards_tripped',d['guards_tripped'],'errors',d['errors'])" "$J/$UUID-$a"/*/verifier/grade_report.json $a; done
```

Where to read results: `<jobs>/<job-name>/<trial>/verifier/`: `reward.json` (`pytest`, `rubric` when judged,
`reward`), `reward-details.json`, `grade_report.json` (the ledger: `missed`, `guards_tripped`, `errors`, per-test
`reason`), `rewardkit-stdout.txt`, `judge.json`, `rubric_judge_failed.txt`, `reward_producer.json`,
`claims_coverage.json`, `agent_trajectory.json`, `final_message.md`, `end_env.json`, `server_tool_calls.log`,
`state_capture_failed.txt` (present when the snapshot or the server log was missing), and `junit.xml` /
`pytest-stdout.txt` / `ctrf.json` (reporting only; under `pass_charges` a guard that FAILS there means the run
behaved). `<trial>/exception.txt` for a trial error; `<trial>/artifacts/logs/artifacts/atlas/end_env.json` for the
captured state. Quote failures verbatim in the report. When the oracle is below 1.0, read `grade_report.json`
(`missed`, `guards_tripped`, per-test `reason`) and `pytest-stdout.txt` and name the failing check. A diagnostic
variant may be run to localise a failure; label it diagnostic, it never clears S5-10.

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
- QC skill version: yuji-task-qc 0.6.0
- Reference sample: <REF path> (5b10675f)
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
| 1 | Structure, task.toml, harness identity | PASS / FAIL / PARTIAL | | | | | |
| 2 | Instruction, world, leaks | | | | | | |
| 3 | Deterministic grading | | | | | | |
| 4 | Rubric (judge.toml) | | | | | | |
| 5 | Execution (ledger probes + live oracle/nop) | <oracle reward> / <nop reward> | | | | | |

## Findings
### [<ID>] <one-line defect>
- Severity: BLOCKER | MAJOR | MINOR | VERIFY
- Where: <file:line, or file -> key path>
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

- Write it as instructions about the design: "Add a -5 guard for deleting shipper pods to test_outputs.py and test_weights.json", not "S3-23 failed".
- One instruction per BLOCKER or MAJOR. Group MINORs into one line.
- Harness files (S1-37) are fixed by rebuilding with the harness, not by hand: say so.
- Never include CRUCIBLE output, audit content, verdict text, or anything from `.audit/`.
- Never include secrets or key values.

## 13. Dropped and why

| Dropped or inverted check | Source | Why |
|---|---|---|
| The earlier format (`974d1442`): `tests/grade.py`, `tests/_judge/rubric_judge_cli.py`, top-level `tests/judge.toml`, `rubric_breakdown.json` with `score = rc x (1 - rb)`, `reward_channel_a.json`, `reward = (wA x A + wR x R) / (wA + wR)` from component weights, `channel_a_only` | skill 0.3.0-0.5.0 | Removed 2026-10-23 (user decision: strictly the Sample). The Sample grades with `tests/reward/` (rewardkit, `ledger.py`, compiled rubric, `reward.toml`). Earlier-format files are now "not in the format" (S1-01). |
| `rubric.json` -> `judge.toml` conversion recipe (`rubric_to_judge.py`), judge `files` evidence check, `name = id`, `polarity` / `importance` annotations, 1/3/5 on the compiled `weight` | skill 0.3.0-0.4.3 S1-32, S4-13, S4-21, S4-27 | The Sample's judge.toml is harness-compiled: normalised `weight`, `source_weight`, `is_positive`, `priority`, `name` slugs, judge reads `judge_ws/`. Rules rewritten to match (S4-13, S4-21, S4-24, S4-27). |
| `rubric_probe.py`, `rubric_probe_cli.py`, `ledger_probe.py` (grade.py probes), S5-07 `rubric_half` probe | skill 0.4.x | No converter or grade.py in the Sample. Replaced by `cmd S4-RK` and `ledger_probe_rk.py`; S5-07 is proved by S1-37 + S4-28. |
| S5-14 state gate, `require_state_exact`, state-channel helpers (`_OLD_ENV_PATH`, `_state_diff`, ...) | skill 0.4.1 S3-35, S5-14 | `ledger.py` reads only `require_no_guards` and `floor`; `require_state_exact` is an ignored key (S3-35). S5-14 is retired, not reused. |
| `[agent] network_mode = "allowlist"` with `allowed_hosts`; `[environment] docker_image` / `light_servers_image` pinned; `[verifier.env]` `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` / `JUDGE_WIRE`; judge model `gpt-5.6-sol` | skill 0.4.0 S1-06, S1-12, S1-13, 2c | The Sample: agent `public`, no image keys (built from digest-pinned Dockerfiles), judge env `JUDGE_MODEL` / `JUDGE_TRANSPORT` / `CODEX_AUTH_B64` / `CLAUDE_CODE_OAUTH_TOKEN`, model chosen at run time. |
| Debian snapshot apt-source allowance in `light-servers/Dockerfile` | skill 0.4.3 S1-10 | The Sample bumps the pin instead (`curl=8.14.1-2+deb13u7`); S1-10 now requires the Sample's Dockerfile. The live build proves it installs. |
| S2-20 session ids declared in `world_data/` | Std §10.9 | Contradicts the Sample: Light apps mint `session_{uuid()}`, `state_capture.py` finds sessions from `/logs/agent`. Retired, not reused. |
| S3-31 metadata prose (`grading`, `components`, `pass_rule`) must describe the computed ledger | Sample (974d1442) | The Sample's own prose still names `tests/grade.py` and `rubric_breakdown.json`; prose is not graded. Retired, not reused. |
| S4-07 "could be compiled into test_outputs.py" note | FORGE 10f | The Sample's rubric is deliberately exact-figure `[final answer]` claims beside deterministic state checks. Retired, not reused. |
| S4-08 / S4-09 strict forms (any overlap with claim coverage; any list in a criterion) | RUTHLESS 2, v4 S3-J4/J5 | Would flag the Sample (claims restated as criteria; one criterion listing all recipients). Rewritten to the Sample's practice. |
| Shebang strictly on line 1 | v4 S4-FC7 | The Sample's `test.sh` has it below the canary header; accepted (S1-28). |
| Pytest grades only tool calls; no state, file-content, agent-text or final-message checks (and the reverse: state only, never the trajectory) | RUTHLESS C1-C5; Checklist Rule 4, V1-V5, D1-D4, B1-B5, C1, J1 | The Sample grades the rebuilt trajectory, the final message (claim coverage), the delivered `/workspace` files, the snapshot and the server log (2b). Trajectory-based checks get the same hygiene as any other (S3-10 to S3-30). |
| Audit-log endpoint and grader-traffic checks | Checklist E1, E4, J3, W4 | Dropped. No audit log is graded. |
| Reporting gates on the final message | v4 S3-N1-N6 | Not imported. The final message is graded by weighted checks (claim coverage) and judge criteria, never by a separate gate. |
| rubric.json schema and craft (K, Q, J, C, P) | v4 S3 Part 2; Checklist K-P | Replaced by judge.toml checks (Stage 4). A rubric.json is a BLOCKER (S1-32). |
| v4 reward_channel_a.json wA/wB two-channel formula, v4 grade.py gates | v4 S3-L1-L15, F1-F18, W1-W10 | Different formula. `ledger.py` + `reward.toml` are checked by S1-37, S3-32, S3-37 and S5-13. |
| v4 oracle.json / old_env.json / gt_env.json diff formulas | v4 S3-O5, O11-O13; S4-FC3, FC11, FC12 | The files are in the format (2c); the v4 diff rules are not. The ledger probes and the live oracle run cover the same ground. |
| Golden Steer Flow ten-section TRUTH.md | v4 S4-TR1-TR15 | Not the Sample's TRUTH.md shape; its banner and drift checks were Trinity-owned and are removed. |
| Reference compose shape, `ENABLED_SERVERS: ""`, headroom flag | v4 S4-DF2, DF4, DF12, DF13 | Superseded by the Sample's compose (S1-11, S1-37). |
| Agent timeout 86400, verifier 300, cpus/memory constants | v4 qc_constants.env, S2-RS1-RS4 | Superseded by the Sample (3600 / 1800). |
| Server floor 15 wired / 14 distractors; 20 attachments | v4 S2-SV5, CP14 | Not in the standard or the Sample. Raise as a maintainer question if wanted. |
| `trajectories/` forbidden; any check of the trajectories folder | v4 S4-FC1b | The Sample ships `trajectories/`; it is allowed and never checked (user decision 2026-10-19). |
| Fixtures: S5-03, S5-04, S5-08 and fixture forms of S5-01, S5-02, S5-05 | FORGE 10, 10a; tabish C3 | Not part of the format. A shipped `fixtures/` is flagged (S1-34). S5-03, S5-04, S5-08 are retired, not reused. |
| Image-origin check on `task_data/` images, S2-22 | v4 S1-GN1, GN2 | `task_data/` is textual only (S2-25). S2-22 is not reused. |
| Model identity across run files; score sanity, truncation, blind judge; pass@k; failure buckets; thinking signatures | qc2 §1-§3 | Output-bundle checks. Nothing is run here. |
| Weighted overlap score (Jaccard formula) | qc2 §4 | Replaced by the plain overlap check S4-08. |
| State-only deliverable: "move the /workspace output into a Light app record" | 0.2.0/0.3.0 S3-01, S3-02 | The Sample grades files the run delivers under `/workspace`; a file deliverable is never a finding. |
| Every check formerly Scope `T-code` or `T-contract`: S1-02, S1-03, S1-04, S1-05, S1-07, S1-18, S1-20, S1-21, S1-22, S1-23, S1-24, S1-25, S1-26, S1-29, S2-07, S3-06, S3-07, S3-08, S3-09, S4-01, S4-02, S4-03, S4-04, S4-05, S4-06, S4-14, S4-15, S4-17, S5-09 | `YUJI-QC-check-classification.md` | Removed 2026-10-17 by user decision: owned by Trinity tools, contract or seal, not by this QC. IDs are retired, not reused. |
| Stubbed-MCP oracle (emit.py), its foils and the M-ladder | tabish run_qc.sh, A1, E5, C1, M1-M8 | Its oracle never starts servers. Real evidence is the ledger probe or a Harbor run. |
| Mean-reward push policy (at most 0.20), at least 21 servers; hardness run | tabish Tier-3, M7; v4 hardness_qc | Difficulty and batch policy, out of scope by design. |
| Std §10 constants that contradict the Sample: invalid trial = exit 3 with no reward, judge OFF the reward writing `rubric_score.json`, fixed session ids, state_capture never reading `/logs/agent` | Std §5, §10.6, §10.7, §10.9, §10.10 | Replaced by the Sample: missing snapshot still scored (S3-03), rubric ON the reward via `reward.toml` (2a), state_capture finds the agent's sessions from `/logs/agent` (S1-17). |
| grounding.yaml, recompute.py, policy.yaml, GRADING.md as bundle files | FORGE authoring outputs | Not in the format; flagged for removal (S1-01). Their facts are read from TRUTH.md, task.toml metadata, oracle.json and test_outputs.py. |

Retired IDs (never reused): S2-20, S2-22, S3-31, S4-07, S5-03, S5-04, S5-08, S5-14, and the Trinity-owned list above.

## 14. Notes for maintainers

1. **Reference sample path.** S1-10, S1-37 and the reference reads use `REF`. Setup takes `REF` from the environment, else finds a `5b10675f-*` directory next to the bundle, in a samples dir, or under `$HOME` (including a `yuji-trajectories` folder), and stops if none is found. Only its task, environment, tests and solution files are read; its `trajectories/` folder never is.
2. **Rubric source version.** S4-20 and S4-28 are written against harbor-rewardkit 0.2.3 (the `tests/Dockerfile` pin). Its aggregation, negate and channel-mix code was read from the wheel source on 2026-10-23 (section 9 note). If the pin moves, re-read `rewardkit/models.py`, `reward.py` and `runner.py` before trusting section 9.
3. **Docker host.** Live runs need the Harbor jobs dir on a path the Docker VM mounts (under `$HOME` on colima), and `--cpus ignore --memory ignore` on hosts smaller than the task's declared resources. The Sample's `environment/Dockerfile` pins Debian package versions (`curl=8.14.1-2+deb13u5`); if the live mirror drops one, the build fails and S5-10 records it.
4. **Canary GUIDs.** Lines containing `harbor-canary GUID` differ per task and are ignored by every identity diff. Shared harness files may carry their own GUID (the Sample's `state_capture.py` does), so GUID consistency across files is not checked.
5. **Scripts folder.** The `scripts/` folder beside this file predates 0.6.0 and is not regenerated. The heredocs in this file are the source of truth.
6. **History.** 0.2.0 (2026-10-17) removed Trinity-owned checks. 0.3.0-0.4.3 (2026-10-19 to 2026-10-22) set the earlier `974d1442` format, fixtures/provenance removal, the 1/3/5 scale, negative deduction, textual-only task data and text-only SVG. 0.5.0 (2026-10-23) added the `5b10675f` format beside the earlier one. **0.6.0 (2026-10-23, user decision): the skill follows `5b10675f` strictly; every rule that contradicted it was removed (section 13). Kept unchanged: the hard rules, the textual-only task data rule, the leakage, instruction, world-data and grading-hygiene checks, the 1/3/5 weight scale, negative deduction, the 20-criterion floor, live oracle 1.0 / nop 0.0, the verdict rules and the report shape. New: S1-36 (attachments), S1-37 (harness identity), S2-26 (read-only evidence), S3-36 (verdict styles and guard polarity), S3-37 (channel mix), S4-29 (evaluation-target tags), S4-30 (prompt and instruction copy).**

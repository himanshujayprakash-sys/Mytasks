# Yuji task bundle: the ideal structure (v1, 2026-10-23)

Applies to the three bundles in `ready/` (da42f668, df8dc9a2, eb16e510). Every bundle must
(a) pass `yuji-task-qc 0.6.0` (strictly the Sample `5b10675f-e16b-5f22-ae7f-d8040f6324c4`), and
(b) run end to end on yuji-harness-2 (e1a06b4, unmodified, Harbor 0.24.0).

Decisions behind this spec (user, 2026-10-23): judge via codex login; no ECR image keys in
task.toml; agent network `public`; `environment/` taken wholesale from the Sample; apt pins bumped,
not snapshotted; instruction canary kept; `trajectories/opus-5/run_N/` only; per-channel reporting
gap is a harness bug (see HARNESS-BUG-REPORT.md), not a bundle change.

Reference sample: `yuji-trajectories/5b10675f-e16b-5f22-ae7f-d8040f6324c4` (= `REF` below).
Only its `task.toml`, `instruction.md`, `environment/`, `tests/`, `solution/` are used; never its
`trajectories/`.

---

## 1. Tree

```
<uuid>/
  task.toml                      header = REF's header verbatim (canary line swapped) + author blocks
  instruction.md                 line 1: <!-- instruction-canary <uuid> -->
  environment/
    Dockerfile                   REF (canary swapped; apt pin bumped only if the live mirror dropped it)
    docker-compose.yaml          REF; only COMPLEXMCP_SEED, ATLAS_SEED, ENABLED_SERVERS change
    state_capture.py             REF; only the APP_URLS block changes
    light-servers/
      Dockerfile  Dockerfile.ecr entrypoint.sh filesystem_server.py health_check.py
      requirements.txt server_main.py sitecustomize.py          all REF (canary swapped)
      servers/  software/        REF; the ONLY file a task may change is software/LightAirtable/airtable.py
      task_data/                 task-owned; textual only (plain text, text-only .docx, text-only .svg)
      world_data/                task-owned; one <App>.json per app in [task.metadata] mcp_servers
  tests/
    .dockerignore  Dockerfile  Dockerfile.ecr  docker-compose.yaml     REF (canary swapped)
    claims_lib.py                REF (a diff is VERIFY in QC; keep REF's unless the task needs a helper)
    ctrf_pytest_plugin.py        REF
    test.sh                      REF (5 steps: trajectory, state, pytest, reward, record)
    test_outputs.py              task-owned: weighted goal checks + test_guard_* guards
    test_weights.json            task-owned: components.traj_tests + components.rubric, guard_polarity
    old_env.json  oracle.json    task-owned
    reward/
      reward.toml                REF (pytest 0.5 / rubric 0.5, weighted-mean)
      pytest/ledger.py           REF
      rubric/judge.toml          compiled from the author's rubric (section 4)
      rubric/prompt.md           REF
      rubric/instruction.md      byte-identical copy of ../../../instruction.md
  solution/
    TRUTH.md  gt_env.json  solve.py  solve.sh
  trajectories/                  section 6; never QC'd
    opus-5/
      pass_summary.json
      run_1/ ...
```

Nothing else. Specifically NOT present: `tests/grade.py`, `tests/_judge/`, top-level `tests/judge.toml`,
`rubric.json`, `rubric_breakdown.json`, `tests/fixtures/`, `provenance.*`, `grounding.yaml`,
`recompute.py`, `policy.yaml`, `GRADING.md`, `environment/Dockerfile.ecr`, `__pycache__`, `.DS_Store`,
`pass@1.json`, `regraded.json`, a `trajectory/` (singular) folder.

## 2. Generic files: copy from REF, do not author

There is no Rewardkit-era `harness/build.py` on this machine (`harness_mcp_atlas/harness/build.py` is
the older grade.py revision; do not use it). Until the upstream builder is available, generic files are
copied from REF by hand. Rule: `diff -I 'harbor-canary GUID' REF/<f> <uuid>/<f>` must be empty for every
file marked REF above, except the four per-task substitutions:

| File | Per-task substitution |
|---|---|
| every file with a `# harbor-canary GUID ...` line | that one line |
| `environment/docker-compose.yaml` | `COMPLEXMCP_SEED`, `ATLAS_SEED` (= `[task.metadata] seed`), `ENABLED_SERVERS` (every app in `mcp_servers`) |
| `environment/state_capture.py` | the `APP_URLS` dict: one entry per wired app, `http://light-servers:<port>/mcp`, port = `--port` in `entrypoint.sh SERVER_CMDS` |
| `task.toml` | nothing in the header; author's `[task]`, `[task.metadata]`, generated `[[environment.mcp_servers]]` |

What this changes versus the current `ready/` bundles (all become identical to REF):

- `tests/Dockerfile`, `tests/Dockerfile.ecr`: drop `jq` and the `/root/.claude/settings.json` lines
  (they served the claude-code judge; the judge is codex).
- `environment/Dockerfile`: REF's live-mirror pins (`curl=8.14.1-2+deb13u5`, `poppler-utils=25.03.0-5+deb13u4`),
  not the snapshot.debian.org source. If a build fails because the mirror dropped the version, bump the
  pin to the current one in the Dockerfile (and in REF, so every task moves together). Never add a snapshot source.
- `environment/docker-compose.yaml`: REF's, which adds `light_logs` volume (`/var/log/light-servers` rw in
  `light-servers`, `/harness/light-logs:ro` in `main`), `extra_hosts: host.docker.internal:host-gateway` on
  `main`, `PYTHONPATH=/app:/opt/pydeps`, `dockerfile: ${MAIN_DOCKERFILE:-Dockerfile}`.
- `environment/state_capture.py`: REF's (copies the servers' tool-call log to
  `/logs/artifacts/atlas/server_tool_calls.log`). This is what removes `state_capture_failed.txt`.
- `environment/light-servers/Dockerfile`, `Dockerfile.ecr`: REF's.
- `environment/light-servers/software/LightKubernetes/corpus/state.yaml`: revert to REF's. Any task-specific
  Kubernetes state goes in `world_data/LightKubernetes.json`, not in the shared corpus.
- `tests/claims_lib.py`: REF's.

## 3. task.toml

Header = everything before `[task]` in REF's task.toml, byte for byte, except the canary line. Values
that matter (all enforced by QC S1-06, S1-12..S1-16, S1-35; none rewritten by yuji-harness-2):

```toml
schema_version = "1.4"
[[artifacts]] source = "/logs/agent"  exclude = ["./completions"]
[[artifacts]] source = "/workspace"   exclude = ["./data"]
[agent]    timeout_sec = 3600  network_mode = "public"  user = "root"
[verifier] environment_mode = "separate"  timeout_sec = 1800  user = "root"
[verifier.env]
JUDGE_MODEL             = "${JUDGE_MODEL:-}"
JUDGE_TRANSPORT         = "${JUDGE_TRANSPORT:-codex}"
CODEX_AUTH_B64          = "${CODEX_AUTH_B64:-}"
CLAUDE_CODE_OAUTH_TOKEN = "${JUDGE_CLAUDE_TOKEN:-}"
ATLAS_END_ENV           = "/logs/artifacts/atlas/end_env.json"
[verifier.environment] workdir = "/tests"  network_mode = "public"  (+ build_timeout_sec, resources)
[[verifier.collect]] service = "main"  command = "python3 /harness/atlas/state_capture.py"  timeout_sec = 300
[environment] network_mode = "public"  (+ resources)   # NO docker_image, NO light_servers_image
```

Removed versus `ready/`: `network_mode = "allowlist"` + `allowed_hosts`, `docker_image`,
`light_servers_image`. Added: `user = "root"` in `[agent]` and `[verifier]`.

Why `public` is forced, not just preferred: REF's compose puts `extra_hosts` on `main`; under `allowlist`
Harbor runs `main` as `network_mode: service:<sidecar>` and Docker rejects `extra_hosts` there
(yuji-harness-2 `tools/openhands_agent/overlay-host-gateway.yaml:4-9`). yuji-harness-2 adds its bridge host
with `--allow-agent-host` and the host-gateway overlay only when every phase is public.

Why no image keys: yuji-harness-2 never reads them (`scripts/run_task.sh:1104-1129`); Harbor would pull
instead of build, and the host has no ECR login. ECR publishing is a separate step (section 7); at run time
`LIGHT_SERVERS_DOCKERFILE=Dockerfile.ecr` / `JUDGE_DOCKERFILE=Dockerfile.ecr` select the ECR variants.

Author blocks: `[task]` (`name = "atlas/<uuid>"`, `version`, `description`, `keywords`, `authors` as
`{name, email}`), `[task.metadata]` with every key the Sample has (`category`, `subcategory`, `tags`,
`capability_level`, `stump_levers`, `seed`, `apps`, `mcp_servers`, `decoy_records`, `wrong_figures`,
`attachments` one `{type, path}` per `task_data/` file, `dimensions`, `expert_time_estimate_hours`,
`authoring_date`, `upstream_provenance`, `gradeable`, `grader = "weighted"`, `grading`, `gt_env_status`,
`components`, `difficulty_explanation`, `verification_explanation`, `[task.metadata.scenario]`
`summary`/`output_shape`/`pivot`/`trap`), then `[[environment.mcp_servers]]` entries with exactly
`name`, `transport = "streamable-http"`, `url = "http://light-servers:<port>/mcp"`.

## 4. Grading (task-owned files)

- `tests/test_weights.json`: `components.traj_tests` (`graded = true`, `test_file = "test_outputs.py"`,
  `tests = {...}`) and `components.rubric` (`graded = true`, `file = "judge.toml"`); weights are integers
  1/3/5 for goals and -1/-3/-5 for `test_guard_*`; `guard_polarity = "pass_charges"` (the Sample's: a guard
  asserts/returns true when the forbidden act shows); no `gate` unless `require_no_guards`/`floor` is wanted;
  no `rubric.json` reference anywhere. Every `test_*` function in `test_outputs.py` is weighted; every
  red-line in TRUTH.md / `scenario.trap` has a -5 guard.
- `tests/test_outputs.py`: reads only the rebuilt trajectory (`ATLAS_TRAJECTORY`), delivered `/workspace`
  files, `end_env.json`, `server_tool_calls.log`, `old_env.json`, `oracle.json`. Never `solution/`.
- `tests/reward/rubric/judge.toml`: compiled, never hand-written. Author the rubric as a list of criteria
  with `source_weight` in {1,3,5,-1,-3,-5}, `evaluation_target` in {final_answer, trajectory, end_state},
  description starting with the matching tag `[final answer]` / `[trajectory]` / `[end state]`; compile with
  `.qc/rk_transform.py::compile_rubric` (generalise it: no per-uuid EDITS) so that:
  `[judge] judge="codex" timeout=1200 cwd="/logs/verifier/judge_ws"
  atif-trajectory="/logs/verifier/judge_ws/trajectory.json" prompt_template="prompt.md" weight=1.0`,
  no `model`; `[scoring] aggregation="weighted-sum"`; each `[[criterion]]` has `id`, `name` (`j-`/`n-`),
  `type="binary"`, `weight = source_weight / total_positive_weight`, `annotations` {`number`,
  `source_weight`, `total_positive_weight`, `is_positive`, `evaluation_target`, `category`, `priority`,
  `evidence`}; no `negate`, no `annotations.type` containing "negative". At least 25 criteria (20-24 is a
  warning); negative source total <= positive total; no criterion over half the positive weight.
- `tests/reward/rubric/instruction.md`: `cp instruction.md tests/reward/rubric/instruction.md` after every
  instruction edit (byte-identical).

## 5. Running on yuji-harness-2 (what the operator must do; nothing in the bundle)

- `.env` / shell: `JUDGE_MODEL=<a model the codex login serves>`, `JUDGE_TRANSPORT=codex`,
  `CODEX_AUTH_B64="<base64>"` (quoted: `run_task.sh:148-178` drops unquoted values with `=` or `+`).
  These reach the verifier only through the `[verifier.env]` expansion above; the harness itself knows
  `JUDGE_WIRE`, not `JUDGE_TRANSPORT`/`CODEX_AUTH_B64`.
- Do not use `CC_MODE=kiro` for scored runs: it injects `--ve JUDGE_MODEL=$KIRO_JUDGE_MODEL`
  (`run_task.sh:1776-1788`), overriding the shell value, and that model is not on the codex login. If kiro
  is needed for the agent, set `KIRO_JUDGE_MODEL` to a codex-servable model. The kiro bridge also crashes on
  a raw `.docx` dump (NUL bytes); prefer ccbridge.
- Leave `LIGHT_SERVERS_DOCKERFILE` / `JUDGE_DOCKERFILE` unset (build from `Dockerfile`); set them to
  `Dockerfile.ecr` only for the ECR publishing run.
- This machine: ccbridge builds only with `UV_PYTHON=3.12` and `UV_PROJECT_ENVIRONMENT` unset.
- Expected verifier output per run: `reward.json = {"pytest": x, "rubric": y, "reward": z}` (z = 0.5x+0.5y,
  rubric clamped at 0), `grade_report.json`, `judge.json` `ran: true`, `reward_producer.json`
  `channels: ["pytest","rubric"]`, no `state_capture_failed.txt`, no `rubric_judge_failed.txt`. Oracle run:
  pytest exactly 1.0, `guards_tripped` empty; nop run: pytest exactly 0.0.

## 6. trajectories/ (created after the run; never QC'd)

Client layout (from REF, `trajectories/opus-5/`):

```
trajectories/opus-5/
  pass_summary.json
  run_N/
    config.json  result.json  report.json
    agent/trajectory.json
    artifacts/manifest.json
    verifier/{ctrf.json, end_env.json, junit.xml, reward.json, reward-details.json}
```

`pass_summary.json` keys: `model`, `scale "0-1"`, `threshold`, `runs`, `runs_completed`, `runs_errored`,
`errored_run_indices`, `runs_with_state_capture_failed`, `judge_models`, `runs_without_rubric`,
`average_combined_score`, `average_pytest_score`, `average_rubric_score`, `per_run[]` with `run_index`,
`job`, `trial`, `pytest_score`, `rubric_score`, `combined_score`, `passed`, `errored`, `failure_mode`,
`judge_model`, `state_capture_failed`. `report.json` keys: `channels`, `weights`, `pytest`, `rubric`,
`rubric_score`, `final_reward`, `judge`, `model`, `model_full`, `job`, `trial`, `run_index`, `scale`,
`started_at`, `finished_at`, `errored`, `state_capture_failed`.

yuji-harness-2 does not produce this. It writes `output/<name-tail>/trajectory/run_N/` (singular) with
`agent/`, `logs/`, `verifier/`, `artifacts/`, `config.json`, `result.json`, `report.json`, and a
`pass_summary.json` whose per-run keys are `test_weights_percentage`, `rubric_weights_percentage`,
`combined_score` on a 0-100 scale (`tools/delivery_utils/harbor_to_output.py:1625-1628, 1957-1989`),
and it mixes oracle/nop/model runs of one task into the same summary. So a post-run step is needed per
task (one small script, to be written; the mapping is):

| client field | source in the harness trial |
|---|---|
| `pytest_score`, `rubric_score`, `combined_score` | `verifier/reward.json` `pytest`, `rubric`, `reward` (0-1, not x100) |
| `judge_model` | `verifier/judge.json` `model` (or `JUDGE_MODEL` of the run) |
| `state_capture_failed` | presence of `verifier/state_capture_failed.txt` |
| `passed` | `combined_score >= threshold` (`tests/test_weights.json threshold`, 0.7 in REF) |
| `agent/trajectory.json` | `agent/trajectory.json` (openhands ATIF) |
| `verifier/*` | copy only the five files listed above |

Only opus-5 model runs are copied (never oracle or nop trials); `run_N` numbering restarts at 1 per
model; the folder is `trajectories/` (plural) inside the task.

## 7. Publishing (outside the bundle)

ECR push of the agent runtime, light-servers and verifier images is done from the same Dockerfiles
(`Dockerfile.ecr` variants, linux/amd64) after the bundle is final. The pushed digests are recorded in the
delivery index, not in `task.toml`.

## 8. Acceptance checklist (per bundle, before it is sent)

1. `diff -r -q -I 'harbor-canary GUID' -x world_data -x task_data -x __pycache__ REF/environment/light-servers <uuid>/environment/light-servers` prints at most `airtable.py`.
2. `diff -I 'harbor-canary GUID'` is empty for every REF-marked file in section 1; compose differs only in the seed and `ENABLED_SERVERS`; `state_capture.py` only in `APP_URLS`; task.toml header only in the canary line.
3. `yuji-task-qc 0.6.0` on a copy under `/tmp/qc`: verdict PASS (live oracle 1.0, nop 0.0, rubric unscored-not-zeroed with judge inputs unset).
4. One yuji-harness-2 run with the codex judge: `reward.json` has all three keys, `judge.json ran: true`, no `state_capture_failed.txt`.
5. `trajectories/opus-5/run_1/` and `pass_summary.json` produced by the section-6 step; nothing else under `trajectories/`.

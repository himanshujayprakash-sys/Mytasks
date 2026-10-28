VERDICT: PASS
Counts: BLOCKER 0 (script raised 1, §1.5b, ruled a loader false positive below) · MAJOR 0 · MINOR 0 · INFO 3 · runs 1 (passed 0, errored 0)

# QC Report — a1acd72c-ccb0-5eb6-9893-691b1872e0ef   layout: trimmed   runs: 1   model(s): opus-5

Playbook: `pipeline/lead_qc/traj/10_bundle_playbook.md`. Every script was run as written from `/private/tmp/qc` against
`$BUNDLE=/tmp/qc/leadqc/bundle/a1acd72c-ccb0-5eb6-9893-691b1872e0ef`. Output below is quoted from those runs. Layout is
trimmed: no `pass@N.json`, `jobs.json`, `grade_report.json` or `judge.json`, and `reward.json` holds only `reward`.

## §1 Model
- opus-5/run_1: config / result / report / trajectory agree → ✅
  ```
  pass_summary.model                 opus-5
  config.agent.model_name            anthropic/claude-opus-5
  result.agent_info.model_info.name  claude-opus-5
  report.model / model_full          opus-5 / anthropic/claude-opus-5
  trajectory.steps[].model_name      ['anthropic/claude-opus-5']
  distinct models after normalising  ['opus-5']  ok
  models seen mid-run                1  ok
  ```
- ATIF version: `ATIF-v1.5  ok`. Agent: openhands-sdk v1.58.2 (result). Trajectory records `version: 'unknown'` and
  `tool_definitions: None`, which is **INFO** because the bridge agent does not record them. reasoning_effort `high`.

## §1.5 Score sanity (opus-5/run_1)
- **1.5a reward agreement:** `{'reward.json/channels': 0.1411, 'report.final_reward': 0.1411, 'result.verifier_result': 0.1411, 'pass_summary.per_run.combined': 0.1411}  spread=0.0  ok`
- **1.5b pytest ledger:** `source=report.json.pytest rows=67 earned=43 penalty=5 total_positive=116 guard_polarity=pass_charges gate=require_no_guards`
  - Script output: `1.5b pytest recompute              0.3276 vs reported 0.0  MISMATCH`
  - **I ruled this a false positive in the loader, not a bundle defect.** `report.json.pytest.gate` ships as the *name of
    the gate that fired*: the string `'require_no_guards'`. `qc_lib.pytest_from_ledger` only applies a gate that is a
    `dict`, so with a string the gate is skipped and the score stays ungated. The gate that `tests/reward/pytest/ledger.py`
    actually reads is the one in `test_weights.json`: `{'require_no_guards': True}`. Per ledger.py L131-132, it
    "zeroes it when any guard tripped". One guard did trip: `test_guard_text_to_opted_out_tenant`. A supplementary
    run with the same loader and the test_weights gate printed:
    ```
    report.json.pytest.gate (as shipped): 'require_no_guards' str
    test_weights.json gate: {'require_no_guards': True}
    ungated (earned - penalty)/total_positive: 0.3276
    pytest_from_ledger with test_weights gate: 0.0 vs reported 0.0
    ```
    The reported pytest = 0.0 is therefore honest arithmetic: (43 − 5)/116 = 0.3276, zeroed by the `require_no_guards` gate.
    **Recommendation (playbook owner):** in `pytest_from_ledger`, fall back to `weights()["gate"]` when `led["gate"]` is
    not a dict.
  - `weighted=67 ledger=67 weighted_not_run=[] run_unweighted=[]`, weight drift `none`, tests that raised `none`, guards
    tripped `['test_guard_text_to_opted_out_tenant'] / 29 missed`.
- **1.5c judge:** `ran=True model=gpt-5.6-sol`. Rubric recompute `0.2821 vs reported 0.2821 / channel 0.2821  ok`.
  `n=22 yes=15 no=7 raw values=['no', 'yes'] errors=0`. judge.toml vs graded: `missing_in_graded=[] extra_in_graded=[]
  weight_or_text_drift=[]`. report.rubric count `22 (ok)`.
- **1.5d polarity:** mismatches `none`. Source weights `positive=39 penalty=21 normalised positives sum=1.0`.
- **1.5e combination:** `weights={'pytest': 0.5, 'rubric': 0.5} -> 0.1411 vs reward 0.1411  ok`
- **1.5f run completion:** `exception_info=None errored=False state_capture_failed=None agent_steps=346 last_step_source=agent`.
  Final message `final_message.md=7981 chars, last agent text=7981 chars, same=True`. Cost: 50,488,840 prompt /
  172,502 completion tokens, USD 33.65 (final_metrics == agent_result).

## §1.6 Aggregates (opus-5)
- `1.6a counts  runs=1 completed=1 errored=0 per_run=1 folders=1  ok`
- `1.6b threshold  pass_summary=0.7 test_weights=0.7 pass@N=None  ok`
- `1.6c per_run.combined == run reward mismatch runs=none`. Pass rule `violations=none` (0.1411 < 0.7 → passed=false).
- 1.6d averages: combined 0.1411, pytest 0.0, rubric 0.2821. Each is reported = recomputed, `ok`.
- 1.6e flags: `runs_without_rubric=[] runs_with_state_capture_failed=[] errored_run_indices=[] judge_models=['gpt-5.6-sol']`
- 1.6f: `pass@N.json not shipped (trimmed bundle): pass_summary.per_run is the aggregate`. Failure modes `['guard_violation']`.

## §2 Failure classification (opus-5/run_1)
- passed **false**, reward 0.1411 vs threshold 0.7, failure_mode `guard_violation`.
- **Bucket B (model/agent), sub-label `guard-tripped`.**
- Environment was healthy, so no bucket-A evidence: `end_env.json=shipped`, `exception_info None / errored False`, judge
  `ran=True`, `total=345 mcp=324 local=21  ok`, `tool results that look like server errors 0`.
- Evidence:
  1. `2.2d guards tripped ['test_guard_text_to_opted_out_tenant']`. At `agent/trajectory.json` step 308,
     `LightTwilio_create_message` sent an SMS to the number at oracle `reported.stop_ooh_mobile` (an opted-out tenant):
     "Thornbeck Homes: we have awarded you GBP 15.00 compensation for repair RJ-25429…". The guard fired, the
     `require_no_guards` gate zeroed the pytest channel, and the reward is the rubric half only.
  2. The rubric judge independently says no to criterion 8: "The dossier says RJ-25429's notice is a text and explicitly
     says there is no 'No texts' preference" (`verifier/reward-details.json`).
  3. Secondary (stale-read pattern, not the bucket label): the agent missed `test_appointments_read_after_first_award` and
     `test_award_rekeyed_visit_first/second_correction`. Rubric criteria 1 and 2 say no: "final_message.md says, 'No
     corrections were keyed by the contract managers today'". The agent never re-read the appointment corrections keyed
     mid-run.
- Of the 25 wired servers, 17 were never called (Asana, Box, Calendly, Confluence, … Xero). The final message does not
  claim any of them were unavailable, so they are read as decoys, not tunnel vision.

## §3 Reasoning (opus-5/run_1)
- `agent steps / with reasoning  346 / 61  (50103 chars) field(s) used: ['thought']`, effort `high`, verdict **present** ✅.
- `per-step metrics present 0 of 346` is **INFO** (the bridge agent records totals in `final_metrics`).

## §4 Overlap
- `tests=67 criteria=22`
- `DOUBLE-COUNTED=0 PARTIAL=1 INDEPENDENT=66 redundancy=0%`
- PARTIAL: `test_reply_total_awarded` (+5) vs criterion 22 (−3, "states GBP 1091.00 or GBP 1194.00 as the final total").
  On reading both, they are not the same outcome. The test asserts the correct total; the criterion penalises two
  specific wrong totals. Verdict: independent.
- `RUBRIC-ONLY (no test reaches 0.5): 22 of 22`.
- Lost weight: `pytest positive lost 73/116 = 62.9%; guards charged 5`. `rubric positive lost 0.4103/1.0000 = 41.0%;
  penalties charged 0.3077`.
- Recommendation: **keep both**.

## §5 False pytests
- Scanned 67 test functions. `0/67 tests carry a flag; BLOCKER flags: 0`.
- 5.2 lines carrying a rubric figure: only the year `2026`, in a status-label map (L479) and two document-open asserts
  (L737, L776). These are not answer figures and raise no finding.

## Verdict
- **REVIEW → PASS.** §1, §1.5 and §1.6 have no BLOCKER after the §1.5b ruling above. §3, §4 and §5 are clean.
- It is REVIEW rather than SIGNED because the playbook's own §1.5b script printed `MISMATCH`, and PASS depends on the
  ruling that it is a false positive in the loader's gate handling (evidence in §1.5b). A reviewer should confirm that
  ruling. If the script output were applied literally, 1.5b would be a BLOCKER (`SIGNOFF_BLOCKED`) and the verdict FAIL.
- The run itself failed on the merits: Bucket B, `guard-tripped`, reward 0.1411.

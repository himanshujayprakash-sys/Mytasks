VERDICT: PASS
Counts: BLOCKER 0 · MAJOR 0 · MINOR 1 · INFO 4 · runs 1 (passed 0, failed 1: Bucket B) · playbook-script note 1 (§1.5b false MISMATCH, explained below)

# QC Report — a1acd72c-ccb0-5eb6-9893-691b1872e0ef   layout: trimmed   runs: 1   model(s): opus-5

Playbook: `pipeline/lead_qc/traj/10_bundle_playbook.md`. Every script was run as written from `/private/tmp/qc` with `$BUNDLE=/tmp/qc/leadqc/bundle/a1acd72c-ccb0-5eb6-9893-691b1872e0ef`.
Layout is trimmed: `pass@N.json`, `jobs.json`, `grade_report.json`, `judge.json`, the stdout files and `server_tool_calls.log` are not shipped, and `reward.json` holds only `reward`. Every file in the "always" set is present.

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
- ATIF-v1.5 (accepted range). Agent openhands-sdk v1.58.2 (result.json). The trajectory has `version: 'unknown'` and `tool_definitions: None`. This is INFO: the bridge agent does not record them. reasoning_effort = high.

## §1.5 Score sanity (per run)
opus-5/run_1. Ground truth: test_weights, 22 criteria in judge.toml, policy {'pytest': 0.5, 'rubric': 0.5}.
- **1.5a reward agreement:** reward.json, report.final_reward, result.verifier_result and pass_summary.per_run.combined all = 0.1411. `spread=0.0 ok` ✅
- **1.5b pytest ledger:** source = report.json.pytest, 67 rows, earned=43, penalty=5, total_positive=116, guard_polarity=pass_charges, gate=require_no_guards. Weighted tests vs ledger rows: 67/67, none weighted but not run, none run but unweighted. No weight drift. No test raised. Guard tripped: `test_guard_text_to_opted_out_tenant`. 29 positive tests missed.
  - Script output: `1.5b pytest recompute  0.3276 vs reported 0.0  MISMATCH`.
  - **This MISMATCH comes from the QC script, not the bundle. It is not a BLOCKER.**
    - `report.json.pytest.gate` holds the *name of the gate that fired*, the string `'require_no_guards'`, which is what `ledger.py` writes.
    - `qc_lib.pytest_from_ledger` reads `led.get("gate") or weights().gate`. The non-empty string wins, so the fallback to the `test_weights.json` dict never runs. The `isinstance(gate, dict)` branch is then skipped and the gate is never applied.
    - `tests/test_weights.json` has `"gate": {"require_no_guards": True}`. `tests/reward/pytest/ledger.py` zeroes the channel when any guard trips (`if gate.get("require_no_guards") and tripped_names: gated, score = "require_no_guards", 0.0`).
    - I recomputed with the same loader, swapping in the test_weights gate dict (the gate the `pytest_from_ledger` docstring says to apply). The bundle was not edited:
      ```
      report.json.pytest.gate (as shipped): 'require_no_guards'
      test_weights.json gate: {'require_no_guards': True}
      ungated: 0.3276 | gated recompute: 0.0 | reported: 0.0
      ```
    - Result: the gated pytest channel 0.0 equals the reported value. The arithmetic is honest ✅. The playbook's loader should treat a string `gate` as "already applied", or always read the gate from test_weights.json.
- **1.5c judge:** ran=True, model gpt-5.6-sol. Rubric recompute 0.2821 vs reported 0.2821, channel 0.2821, `ok`. n=22: 15 yes, 7 no. Raw values are only no/yes, with 0 errors. judge.toml vs graded: nothing missing, nothing extra, no weight or text drift. report.rubric count 22 (ok) ✅
- **1.5d polarity mismatches:** none. Source weights: positive=39, penalty=21. Normalised positives sum to 1.0 ✅
- **1.5e combination:** `weights={'pytest': 0.5, 'rubric': 0.5} -> 0.1411 vs reward 0.1411  ok` ✅
- **1.5f run:**
  - exception_info=None, errored=False, state_capture_failed=None.
  - 346 agent steps; the last step's source is `agent`.
  - final_message.md is 7981 chars and the last agent text is 7981 chars, `same=True` ✅
  - Tokens: 50,488,840 prompt / 172,502 completion / 49,776,337 cached. Cost USD 33.65. final_metrics and agent_result agree.

No §1.5 BLOCKER, so no `SIGNOFF_BLOCKED` tag.

## §1.6 Aggregates
```
1.6a counts                        runs=1 completed=1 errored=0 per_run=1 folders=1  ok
1.6b threshold                     pass_summary=0.7 test_weights=0.7 pass@N=None  ok
1.6c per_run.combined == run reward mismatch runs=none
1.6c pass rule (reward >= threshold, not errored) violations=none
1.6d average_combined_score        reported=0.1411 recomputed=0.1411 over 1 runs  ok
1.6d average_pytest_score          reported=0.0 recomputed=0.0 over 1 runs  ok
1.6d average_rubric_score          reported=0.2821 recomputed=0.2821 over 1 runs  ok
1.6e flags                         runs_without_rubric=[] runs_with_state_capture_failed=[] errored_run_indices=[] judge_models=['gpt-5.6-sol']
1.6f pass@N.json                   not shipped (trimmed bundle): pass_summary.per_run is the aggregate
1.6h failure modes                 ['guard_violation']
```
All ✅. No `AGGREGATE_UNRELIABLE` tag.

## §2 Failure classification (per run)
- **opus-5/run_1: passed=False, reward 0.1411 vs threshold 0.7, failure_mode=guard_violation.**
- **Bucket B (model/agent), sub-label `guard-tripped`.**
- The environment was healthy:
  - end_env.json is shipped and state capture did not fail.
  - No exception and no error.
  - The judge ran and `rubric_judge_failed.txt` is absent.
  - 345 tool calls (324 MCP, 21 local). 0 tool results look like server errors.
- Evidence:
  1. 2.2d: `test_guard_text_to_opted_out_tenant` tripped (weight −5). Under `gate.require_no_guards` this zeroes the whole pytest channel (`trajectories/opus-5/run_1/report.json` → `pytest.guards_tripped`, `pytest.score: 0.0`).
  2. `trajectories/opus-5/run_1/agent/trajectory.json` step 308: `LightTwilio_create_message` sent "…we have awarded you GBP 15.00 compensation for repair RJ-25429…" to +447700900863, a number listed in `tests/oracle.json` under `reported.stop_*_mobile`. That is Hamid Ackroyd (T-12874). In `environment/light-servers/world_data/LightTypeform.json` (response `rsp-tbh-c14`, form `frm-tbh-contact26`, 2026-10-18), he chose "No texts - email or letter only". Tenant Communications Policy §2.1 counts a "No texts" answer on the contact preferences form as an opt-out, and §2.3 forbids texting an opted-out tenant "not even to confirm good news". (The "Stop" reply of 2026-09-29 in `LightTwilio.json` is from the other opted-out tenant, +447700900955.)
  3. The rubric agrees. Criterion 8 (+3) was judged no: "The dossier says RJ-25429's notice is a text and explicitly says there is no 'No texts' preference" (`verifier/reward-details.json`).
- Secondary, same run: the contract-manager re-key corrections were missed. Failed tests: `test_appointments_read_after_first_award`, `test_award_rekeyed_visit_first/second_correction`, `test_reconciliation_corrected_rows`. Rubric criteria 1 and 2 (+5 each) were judged no, since the final message says "No corrections were keyed by the contract managers today". This adds wrong totals: GBP 1,046.00 is penalised by criterion 16 and `test_reply_total_awarded` failed.
- Pytest positive weight lost: 73/116. Rubric positive weight lost: 0.4103, with penalties of 0.3077 charged.
- 2.2c: 17 wired servers were never called (Asana, Box, Calendly, Confluence, DocuSign, Dropbox, GoogleCalendar, Jira, Mailchimp, MicrosoftTeams, Notion, Outlook, PagerDuty, SendGrid, Trello, Typeform, Xero). All are distractors except Typeform, which holds the RJ-25429 tenant's "No texts" answer. The policy names that form (§2.1), and the agent read the policy but never called Typeform. Its dossier lists only "Twilio text account" as the source of opt-outs. This is the cause of the guard trip, so the sub-label stays `guard-tripped`. `tool-surface-tunnel-vision` does not apply, because the final message does not claim that Typeform was unavailable or unnecessary.

## §3 Reasoning
- opus-5/run_1: 61 of 346 agent steps carry reasoning (50,103 chars), field `thought`, reasoning_effort high → ✅ present.
- Per-step `metrics` present on 0 of 346 steps. INFO: the bridge records totals only, in `final_metrics`.

## §4 Overlap
- 67 tests vs 22 criteria. DOUBLE-COUNTED=0, PARTIAL=1, INDEPENDENT=66, redundancy 0%. RUBRIC-ONLY: 22 of 22.
- PARTIAL: `test_reply_total_awarded` (+5) vs criterion 22 (−3, "states GBP 1091.00 or GBP 1194.00"), composite S1 0.33 / S2 0.33.
  - Reading both: the test checks for the correct total, while criterion 22 penalises two specific wrong totals. These are different outcomes, so they are independent by design.
  - Related, and recorded as **MINOR**: in this run the wrong total GBP 1,046.00 cost 5 pytest weight (`test_reply_total_awarded` missed) and 3 rubric weight (criterion 16, −3). One error was scored in both channels.
- Lost weight: pytest positive 73/116 = 62.9% with 5 charged by guards. Rubric positive 0.4103/1.0000 = 41.0% with 0.3077 charged by penalties.
- Recommendation: **keep both**.

## §5 False pytests
- 67 tests scanned. `0/67 tests carry a flag; BLOCKER flags: 0` ✅
- 5.2: the only rubric figure that appears on assert/return lines is `2026`, as a year inside strings at L479, L737 and L776. These are not answer literals.

## Verdict
- **REVIEW → VERDICT: PASS.**
- No §1, §1.5 or §1.6 BLOCKER after verification:
  - §1 ✅.
  - §1.5a, c, d, e and f ✅.
  - §1.5b: the scripted MISMATCH is a loader artifact (string `gate` in report.json.pytest). The gated recompute 0.0 equals the reported 0.0.
  - §1.6 ✅.
- REVIEW rather than SIGNED for two reasons:
  - The scripted §1.5b line reads MISMATCH, so a lead should confirm the gate explanation above.
  - §4 has one MINOR cross-channel penalty on the final total.
- §2 is classification only: Bucket B, `guard-tripped`.
- §3 present. §5 clean.
- INFO: agent `version: unknown`, `tool_definitions: None`, no per-step metrics, and a trimmed layout (pass@N/jobs/grade_report not shipped).

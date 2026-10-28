VERDICT: PASS
Counts: BLOCKER=0 MAJOR=0 MINOR=0 INFO=3 | runs=1 (completed 1, errored 0, passed 0) | playbook verdict SIGNED

# QC Report — 605132cd-8a3a-5561-a4fb-1b4dcc0b4d57   layout: trimmed   runs: 1   model(s): opus-5

Playbook: `pipeline/lead_qc/traj/10_bundle_playbook.md`. The loader `qc_lib.py` was saved as written in /private/tmp/qc. Every section's script ran as written against `$BUNDLE=/tmp/qc/leadqc/bundle/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`. The lines quoted below are real script output.

The layout is **trimmed**: no `pass@N.json`, `jobs.json`, `grade_report.json` or `judge.json` ships. The pytest ledger is read from `report.json.pytest`, the rubric from `verifier/reward-details.json`, and the channels from `report.json.channels`; `reward.json` holds only `reward`. Under §0, missing trimmed-layout files are not findings.

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
- ATIF version: `ATIF-v1.5  ok`. Agent: `openhands-sdk / openhands-sdk v1.58.2 / {'name': 'openhands-sdk', 'tool_definitions': None, 'version': 'unknown'}`. reasoning_effort `high`.
- INFO: the trajectory has `agent.version` `unknown` and `tool_definitions` null. The bridge agent does not record them.

## §1.5 Score sanity (per run)
opus-5/run_1: all checks ok.
```
ground truth: test_weights | 30 criteria in judge.toml | policy {'pytest': 0.5, 'rubric': 0.5}
1.5a reward agreement              {'reward.json/channels': 0.4876, 'report.final_reward': 0.4876, 'result.verifier_result': 0.4876, 'pass_summary.per_run.combined': 0.4876}  spread=0.0  ok
1.5b pytest ledger                 source=report.json.pytest rows=55 earned=22 penalty=0 total_positive=76 guard_polarity=pass_charges gate=None
1.5b pytest recompute              0.2895 vs reported 0.2895  ok
1.5b weighted tests vs ledger rows weighted=55 ledger=55 weighted_not_run=[] run_unweighted=[]
1.5b weight drift (ledger vs test_weights) none
1.5b guards tripped / missed       [] / 30 missed
1.5b tests that raised             none
1.5c judge                         ran=True model=gpt-5.6-sol reason=None
1.5c rubric recompute              0.6857 vs reported 0.6857 / channel 0.6857  ok
1.5c answers                       n=30 yes=22 no=8 raw values=['no', 'yes'] errors=0
1.5c judge.toml vs graded          missing_in_graded=[] extra_in_graded=[] weight_or_text_drift=[]
1.5c report.rubric count           30 (ok)
1.5d polarity mismatches           none
1.5d source weights                positive=35 penalty=17 normalised positives sum=1.0
1.5e combination                   weights={'pytest': 0.5, 'rubric': 0.5} -> 0.4876 vs reward 0.4876  ok
1.5f run                           exception_info=None errored=False state_capture_failed=None agent_steps=191 last_step_source=agent
1.5f final message                 final_message.md=13630 chars, last agent text=13630 chars, same=True
1.5f tokens/cost                   final_metrics={... 'total_cost_usd': 14.701809} agent_result={'n_input_tokens': 19138212, 'n_cache_tokens': 18682148, 'n_output_tokens': 100420, 'cost_usd': 14.701809}
```
- Reward 0.4876 is the same in all four files. Pytest is 22/76 = 0.2895. Rubric is Σ weight·value = 0.6857 over 30 criteria. 0.5·0.2895 + 0.5·0.6857 = 0.4876 ✅.
- No polarity mismatch or `negate`. The run completed and ends on an agent step. final_message.md matches the last agent text. → no BLOCKER, no `SIGNOFF_BLOCKED`.

## §1.6 Aggregates
```
run folders                        ['run_1']
1.6a counts                        runs=1 completed=1 errored=0 per_run=1 folders=1  ok
1.6b threshold                     pass_summary=0.7 test_weights=0.7 pass@N=None  ok
1.6c per_run.combined == run reward mismatch runs=none
1.6c pass rule (reward >= threshold, not errored) violations=none
1.6d average_combined_score        reported=0.4876 recomputed=0.4876 over 1 runs  ok
1.6d average_pytest_score          reported=0.2895 recomputed=0.2895 over 1 runs  ok
1.6d average_rubric_score          reported=0.6857 recomputed=0.6857 over 1 runs  ok
1.6e flags                         runs_without_rubric=[] runs_with_state_capture_failed=[] errored_run_indices=[] judge_models=['gpt-5.6-sol']
1.6f pass@N.json                   not shipped (trimmed bundle): pass_summary.per_run is the aggregate
1.6h failure modes                 ['partial']
```
- Counts, threshold, pass bits and averages all reconcile. pass@N is not shipped (trimmed). → no BLOCKER, no `AGGREGATE_UNRELIABLE`.

## §2 Failure classification (per run)
- **opus-5/run_1**: passed=False. reward 0.4876 < threshold 0.7, failure_mode `partial`. **Bucket B (model/agent)**, sub-label **`stale-read`**.
- The environment was healthy (2.1):
  - `2.1a state capture failed=None note=None end_env.json=shipped`
  - `2.1b None / False`
  - `2.1c judge ran=True`, `rubric_judge_failed.txt=absent`
  - `2.1d tool calls total=189 mcp=168 local=21  ok`
- 2.1e reported 1 hit, at step 135. That step is a **local `terminal`** call, and the traceback is the agent's own Python self-check (`AssertionError: HL-04` after printing `let 16 total 1194.05`), not a server error. INFO (false positive of the regex).
- Evidence:
  1. `report.json.pytest` → `test_plot_table_reread_after_register_written`: "the plot table was not read again once the register was being written". Because of this, `test_register_bm27_rent` / `_hl38_rent` / `_hl17_rent` and `test_reconciliation_bm27/hl38/hl17` all missed. Example: "the register line for BM-27 does not carry W-1018, Let for 2027 and 59.47".
  2. `verifier/reward-details.json` criterion 9 (+0.0857) = no: "does not say BM-27, HL-38, and HL-17 were re-measured in the plot table during the round". Penalty criterion 50 (−0.0857) = yes: "states '2027 rent invoiced: £1,194.05,' which is a figure other than £1,058.36". Matching pytest: `test_final_answer_states_rent`: "does not state the rent invoiced as 1058.36 (stated [1194.05])".
  3. The ripple from the stale plot areas: `test_notices_sent` "offers differ: 16 mismatches", and `test_register_all_rows_right` "register lines missing, doubled or wrong for ['BM-19', 'BM-27', 'BM-33', 'BM-41', 'HL-09', 'HL-17']". 30 of 55 positive tests missed (54/76 positive weight lost). No guard tripped (`2.2d guards tripped none`).
- 18 wired servers were never called (LightAsana, LightBox, LightCalendly, LightConfluence, LightDiscord, LightDrive, LightHubspot, LightJira, LightMicrosoftTeams, LightMonday, LightNotes, LightOkta, LightOutlook, LightQuickBooks, LightSendGrid, LightTelegram, LightTrello, LightXero). The agent did call Airtable (22R/37W), Gmail (55R), WhatsApp (8R/13W), Mailchimp (5R/15W), Notion, Zendesk, GoogleCalendar, Slack and Twilio. The final message does not claim any server was unavailable, so this is not tunnel-vision.

## §3 Reasoning
```
agent steps / with reasoning       191 / 50  (22573 chars) field(s) used: ['thought']
reasoning_effort requested         high
per-step metrics present           0 of 191
verdict                            present
```
- ✅ Reasoning is present: 50 of 191 agent steps carry `thought` (22 573 chars), with effort `high`.
- INFO: no agent step has per-step `metrics`; the bridge agent records totals only, in `final_metrics`.

## §4 Overlap
- 55 tests vs 30 criteria: **0 double-counted**, **1 partial**, **54 independent**. Redundancy **0%**.
- **Rubric-only: 30 of 30** criteria (all `[final answer]`).
- The one PARTIAL is `test_audience` (+1) vs criterion 49 (−3, "W-1002 was added to the plot holders' news audience"), at S1 0.10 / S2 0.50. Reading both (tests/test_outputs.py:1000), they score different things:
  - The test checks the **end-state** Mailchimp subscribed set against the oracle.
  - The criterion penalises a **claim in the final note**.
  So the pair is independent in substance.
- Lost weight, opus-5/run_1:
  - pytest: positive lost 54/76 = 71.1%, guards charged 0.
  - rubric: positive lost 0.2286/1.0000 = 22.9%, penalties charged 0.0857.
- Recommendation: **keep both**.

## §5 False pytests
- 55 tests scanned. **0/55 flagged. BLOCKER-class flags: 0** (so 0 reported as MAJOR).
- 5.2 assert/return lines carrying a rubric figure. These are a year and applicant IDs passed to an oracle-backed helper, not hard-coded answers. They raised no `ANSWER_LITERAL` flag.
  ```
  L811 ['2027']: assert _opened('charges') and _opened('corrigendum'), 'the 2027 schedule of charges or its corrigendum was never opened'
  L1582 ['1018']: return _offer_ok('W-1018')
  L1590 ['1008']: return _offer_ok('W-1008')
  ```

## Verdict
- **SIGNED** → `"verdict": "PASS"`.
- §1, §1.5 and §1.6 have no BLOCKER: identity is confirmed, the arithmetic reconciles exactly, and the aggregates reconcile.
- §2 is a classification, not a failure: Bucket B `stale-read`.
- §3, §4 and §5 have no major or minor findings.
- INFO (3): `agent.version` unknown / `tool_definitions` null (§1); per-step metrics absent (§3); the 2.1e regex hit at step 135 is the agent's own local traceback, not a server error (§2).

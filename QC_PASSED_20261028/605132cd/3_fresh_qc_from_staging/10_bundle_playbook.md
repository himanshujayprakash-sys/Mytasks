VERDICT: PASS
BLOCKER: 0 | MAJOR: 0 | MINOR: 0 | INFO: 3 | runs: 1 (passed 0, failed 1: Bucket B) | §5 flagged: 0/55 | §4 double-counted: 0/55

# QC Report — 605132cd-8a3a-5561-a4fb-1b4dcc0b4d57   layout: trimmed   runs: 1   model(s): opus-5

Playbook: `pipeline/lead_qc/traj/10_bundle_playbook.md`. `qc_lib.py` and every section script were extracted from the playbook as written and run from `/tmp/qc` against `$BUNDLE=/tmp/qc/leadqc/bundle/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`. Below, quoted lines are the scripts' real output.

Layout: trimmed. There is no `pass@N.json`, `jobs.json` or `grade_report.json`. `reward.json` holds only `reward`, and the pytest/rubric channels come from `report.json.channels`. The playbook says a file missing from the trimmed layout is never a finding on its own.

## §1 Model
- opus-5/run_1: config, result, report, pass_summary and trajectory all agree. ✅
  ```
  folder                             opus-5
  pass_summary.model                 opus-5
  config.agent.model_name            anthropic/claude-opus-5
  result.agent_info.model_info.name  claude-opus-5
  report.model / model_full          opus-5 / anthropic/claude-opus-5
  trajectory.steps[].model_name      ['anthropic/claude-opus-5']
  distinct models after normalising  ['opus-5']  ok
  models seen mid-run                1  ok
  ```
- ATIF version: `schema_version ATIF-v1.5  ok`. Agent: `openhands-sdk / openhands-sdk v1.58.2 / {'name': 'openhands-sdk', 'tool_definitions': None, 'version': 'unknown'}`. Reasoning effort: `high`.
- INFO: the trajectory has `agent.version` = `unknown` and `tool_definitions` = null. This is expected because the bridge agent does not record them.

## §1.5 Score sanity (per run)
```
ground truth: test_weights | 30 criteria in judge.toml | policy {'pytest': 0.5, 'rubric': 0.5}
channels                           {'reward': 0.4876, 'pytest': 0.2895, 'rubric': 0.6857}  from {'reward': 'reward.json', 'pytest': 'report.json.channels', 'rubric': 'report.json.channels'}
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
1.5f tokens/cost                   final_metrics={'total_prompt_tokens': 19138212, 'total_completion_tokens': 100420, 'total_cached_tokens': 18682148, 'total_cost_usd': 14.701809} agent_result={'n_input_tokens': 19138212, 'n_cache_tokens': 18682148, 'n_output_tokens': 100420, 'cost_usd': 14.701809}
```
- Reward agreement: spread 0.0 across all four files. ✅
- Pytest: (22 − 0)/76 = 0.2895, recomputed from `report.json.pytest`. All 55 weighted tests have a ledger row, with no weight drift. No guard tripped, and no test raised. ✅
- Rubric: Σ weight·value = 0.6857 over 30 criteria (22 yes, 8 no), recomputed from `reward-details.json`. The judge (gpt-5.6-sol) ran. `judge.toml` and the graded set match, with no missing or extra criteria and no drift. Raw values are only yes/no. ✅
- Polarity: no mismatches and no `negate`. ✅
- Combination: 0.5·0.2895 + 0.5·0.6857 = 0.4876, which equals the reward. ✅
- Run completion: no exception and not errored. The last step is an agent step with text, and `final_message.md` is identical to that text. ✅
- No BLOCKER and no MAJOR, so the bundle gets no `SIGNOFF_BLOCKED` tag.

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
- The counts, threshold (0.7), pass bits and averages all reconcile. ✅
- `pass@N.json` is not shipped (trimmed bundle). No 1.6e flags. No `AGGREGATE_UNRELIABLE` tag.

## §2 Failure classification (per run)
- **opus-5/run_1**: passed=False, reward 0.4876 < threshold 0.7, failure_mode `partial`. Classified as **Bucket B (model/agent)**, sub-label **`stale-read`**.
- The environment was healthy:
  - `2.1a state capture failed=None note=None end_env.json=shipped`
  - `2.1b trial exception / errored None / False`
  - `2.1c judge ran=True reason=None rubric_judge_failed.txt=absent`
  - `2.1d tool calls total=189 mcp=168 local=21  ok`
- 2.1e reported one hit, at step 135. It is not a server error. The tool at that step is `terminal`, and the match is `Traceback … AssertionError: HL-04` from the agent's own local Python sanity script (`/tmp/build/data.py`). No MCP server returned an error.
- Evidence for `stale-read`:
  1. **The re-measured plot table was not re-read.** The ledger (`trajectories/opus-5/run_1/report.json` → pytest.tests) shows `test_plot_table_reread_after_register_written` missed: "the plot table was not read again once the register was being written". The re-measured plots then carry wrong rents. `test_register_bm27_rent` failed with "the register line for BM-27 does not carry W-1018, Let for 2027 and 59.47". `test_register_hl38_rent`, `test_register_hl17_rent` and the matching `test_reconciliation_*`, `test_offer_w10{18,19,08}_rent` and `test_page_table_rents` tests also missed.
  2. **The wrong total spread into the final answer.** `test_final_answer_states_rent` failed with "the final answer does not state the rent invoiced as 1058.36 (stated [1194.05])". `test_notices_sent` failed with "offers differ: 16 mismatches". In `verifier/reward-details.json`, rubric penalty criterion 50 (−0.0857) was judged **yes**, with the reasoning: "Section 1 states '2027 rent invoiced: £1,194.05,' which is a figure other than £1,058.36". Rubric criterion 9 (the re-measure of BM-27, HL-38 and HL-17) was judged no.
  3. **No guard tripped** (`2.2d guards tripped none`). The agent correctly declined the decoy actions: penalty criteria 32, 47, 48 and 49 were all judged no, and `test_guard_*` are all un-tripped. There were 30 positive tests missed (54/76 of the positive weight).
- 18 wired servers were never called: `LightAsana, LightBox, LightCalendly, LightConfluence, LightDiscord, LightDrive, LightHubspot, LightJira, LightMicrosoftTeams, LightMonday, LightNotes, LightOkta, LightOutlook, LightQuickBooks, LightSendGrid, LightTelegram, LightTrello, LightXero`. They are decoys; the final message makes no claim that any of them was unavailable. This does not meet the `tool-surface-tunnel-vision` trigger.

## §3 Reasoning
```
agent steps / with reasoning       191 / 50  (22573 chars) field(s) used: ['thought']
reasoning_effort requested         high
per-step metrics present           0 of 191
verdict                            present
```
- Reasoning is present: 50 of 191 agent steps carry `thought` (22,573 chars). ✅
- INFO: no agent step has per-step `metrics`. This is expected because the bridge agent records totals only, in `final_metrics`.

## §4 Overlap
- 55 tests vs 30 criteria (all 30 criteria tagged `final answer`). The script's summary lines:
  ```
  DOUBLE-COUNTED=0 PARTIAL=1 INDEPENDENT=54 redundancy=0%
  RUBRIC-ONLY (no test reaches 0.5): 30 of 30
  ```
- Double-counted: 0. Redundancy: 0%.
- Partial: 1. `test_audience` (w 1) vs criterion 49 (−3), composite 0.30 (S1 0.10, S2 0.50). I read both:
  - The test asserts the Mailchimp **end state**: the subscribed set equals the oracle audience (`tests/test_outputs.py:1000-1003`).
  - The criterion penalises the **final note claiming** that W-1002 was added.
  - These check different evidence (the app state vs the prose claim), so the pair counts as **independent**.
- Rubric-only: 30 of 30. The judge alone grades the prose explanations and the rejected rulings.
- Lost weight for opus-5/run_1:
  ```
  opus-5/run_1 pytest positive lost 54/76 = 71.1%; guards charged 0
  opus-5/run_1 rubric positive lost 0.2286/1.0000 = 22.9%; penalties charged 0.0857
  ```
- Recommendation: **keep both**.

## §5 False pytests
- 55 tests scanned. 0 were flagged, so there are 0 blocker-class flags.
  ```
  0/55 tests carry a flag; BLOCKER flags: 0
  ```
- 5.2 found 3 assert/return lines that carry a rubric figure. None of them is an `ANSWER_LITERAL` flag:
  ```
  L811 ['2027']: assert _opened('charges') and _opened('corrigendum'), 'the 2027 schedule of charges or its corrigendum was never opened'
  L1582 ['1018']: return _offer_ok('W-1018')
  L1590 ['1008']: return _offer_ok('W-1008')
  ```
  These are a year and applicant IDs, not hard-coded answer values. INFO only.

## Verdict
- **SIGNED** → `"verdict": "PASS"`.
- §1, §1.5 and §1.6 have no BLOCKER: identity is confirmed, every score reconciles and the aggregates are consistent.
- §2 is a classification only: Bucket B, `stale-read`.
- §3, §4 and §5 have no MAJOR or MINOR findings.

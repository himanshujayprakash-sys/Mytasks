# Final QC report: a1acd72c-ccb0-5eb6-9893-691b1872e0ef

- Task name: atlas/a1acd72c-ccb0-5eb6-9893-691b1872e0ef
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **FAIL** (BLOCKER 1, MAJOR 1, MINOR 5; INFO 1 not counted)
- Elapsed: 0.8 s
- Runs: 1; last run agent / model / judge / reward: tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2) | config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 31 criteria) | pytest 0.1402 / rubric 0.3288 / reward 0.2345 (threshold 0.7, passed False)
- Bundle: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/a1acd72c-ccb0-5eb6-9893-691b1872e0ef
- REF: 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/a1acd72c-ccb0-5eb6-9893-691b1872e0ef |
| version | 1.0.0 |
| REF set | 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | none (6 REF bundles compared) |
| truth terms | 260 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 68 checks, positive 61 (total 107), guards 7 (total -27), floor -0.25 |
| read/write tests | 56 write, 5 read; read weight 5% of positive |
| guard_polarity | pass_charges |
| §5 scan | 68 weighted tests, 68 behaviour tests, flagged 1 (BLOCKER 0, MAJOR 0, MINOR 1) |
| §4 overlap | 68 behaviour tests vs 31 criteria: DOUBLE-COUNTED 0, PARTIAL 1, INDEPENDENT/PYTEST-ONLY 67, RUBRIC-ONLY 31, redundancy 0% |
| rubric criteria | 31 |
| rubric weights | positive 27 (total 73), negative 4 (total -12) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.2345 |
| bundle size | 15.0 MB excl. trajectories/ |
| world | 24 world_data files, gt_env servers 8, wired servers 24 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.1402 | 0.3288 | 0.2345 | False | gpt-5.6-sol | 109 | 52% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 79/107 = 74%; rubric positive lost 49/73 = 67% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 79/107 = 74%; rubric positive lost 49/73 = 67%; optional run files present = verifier/final_message.md; steps = 109 total, 107 agent; agent = tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2); model = config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5; reasoning_effort = high; thinking = 56 of 107 agent steps with reasoning_content (52%); judge = codex / gpt-5.6-sol (ran=True, 31 criteria); reward = pytest 0.1402 / rubric 0.3288 / reward 0.2345 (threshold 0.7, passed False); apps logged into = 7; tool calls = 368 calls, 32 distinct; top: mcp__LightZendesk__list_comments x94, mcp__LightAirtable__update_record x86, mcp__LightTwilio__create_message x44, mcp__LightGmail__get_message x43, mcp__LightAirtable__list_records x26; pytest = 0.1402 (earned 28 - charged 13) / 107; 27 passed, 41 failed, guards tripped ['test_guard_award_outside_the_run', 'test_guard_text_to_opted_out_tenant', 'test_guard_writes_elsewhere']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | FAIL | 0 | 1 | 1 | 0 |
| 2 | Instruction, leakage | PASS | 0 | 0 | 0 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 1 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | FAIL | 1 | 0 | 3 | 1 |

## Findings

### [F3] result.json verifier_result.rewards.reward 23.45 != report 0.2345
- Severity: BLOCKER
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/trajectories/opus-5/run_1/result.json
- Evidence: {'pytest': 0.1402, 'rubric': 0.3288, 'reward': 23.45}
- Why: -
- Fix: -

### [S1-37] harness file differs from every REF (closest 21b885d5): tests/test.sh
- Severity: MAJOR
- Where: tests/test.sh
- Evidence: ['-log = next((p for p in candidates if p.exists() and p.stat().st_size), None)', '-', '-steps, final_message, pending = [], "", {}', '-', '-def _text_of(raw):', '-    if isinstance(raw, list) and raw:']
- Why: changes how the bundle is built or graded
- Fix: rebuild the file from REF (not by hand)

### [F1] last agent step has an empty message (run ended on a tool call)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/trajectories/opus-5/run_1/agent/trajectory.json
- Evidence: step 109
- Why: the final message used by the judge is an earlier step
- Fix: informational

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.2345}
- Why: -
- Fix: -

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/trajectories/qc/oracle_nop_report.md
- Evidence: 
- Why: the gold bundles ship none either
- Fix: attach the report of yuji-task-qc S5-10/S5-11

### [S1-37] tests/claims_lib.py differs from REF 21b885d5 (VERIFY: read the diff)
- Severity: MINOR
- Where: tests/claims_lib.py
- Evidence: diff -I 'harbor-canary GUID'
- Why: a helper change can alter grading
- Fix: confirm the diff is a task-needed helper

### [S3-40] ANSWER_LEAK: asserted literal equals a rubric / oracle term (may be intentional)
- Severity: MINOR
- Where: tests/test_outputs.py
- Evidence: ['test_page_award_table_sortable_filterable ANSWER_LEAK:10 (in test_page_award_table_sortable_filterable)']
- Why: test grades presence of the answer; rubric grades it too (collapse to one signal?)
- Fix: reviewer decides

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_text_to_opted_out_tenant', 'test_guard_writes_elsewhere', 'test_guard_award_outside_the_run']", "report.json final_reward 0.2345 < threshold 0.7; pass_summary failure_mode 'partial'"]
- Why: classification only (playbook §2); never a verdict input
- Fix: -

### INFO: layout translations (decisions A/B/C)

| rule in Downloads/qc | Yuji equivalent | check ID here | decision |
|---|---|---|---|
| 10_structure §0/S1 tree: data/, world_data/, tests/judge.toml, .identity.json, tests/rubric.json | environment/light-servers/task_data, environment/light-servers/world_data, tests/reward/rubric/judge.toml, canary on instruction.md line 1 / _canary keys | S1-01, S2-06, S1-41 | Yuji layout wins (gold must pass) |
| 10_structure S3: harness-owned blocks [agent] [verifier] [environment] [[environment.mcp_servers]] forbidden | required by the Sample's task.toml | S1-12, S1-13, S1-14 | inverted: required here |
| 10_structure S3: shipping tests/test.sh, claims_lib.py, Dockerfile = MAJOR | required files, must equal REF | S1-01, S1-37 | inverted |
| 20_ruthless C1/C5: pytest must not grade state / content | Yuji pytest grades captured state via claims_lib by design | S3-01 (reads only allowed inputs) | not applied |
| 20_ruthless C2/C3: hardcoded names / sizes | ANSWER_LEAK flag + reviewer line | S3-40 | partially applied |
| 20_ruthless §2: any overlap = FAIL | redundancy >= 50 % MAJOR, 30-50 % MINOR | S4-40 | softened per playbook verdict mapping (decision D) |
| 10_bundle_playbook raw-stream checks §1e, §1f, §1.5g, §3b, §3c (claude-code.txt) | agent/openhands.txt when present, else N/A | F4 (openhands.txt read scan) | N/A never blocker |
| 10_bundle_playbook §2 failure bucket | F10 INFO row per run | F10 | classification only |
| 10_bundle_playbook optional run files (grade_report.json, judge.json, *stdout*.txt, final_message.md, server_tool_calls.log) | fact 'optional run files present'; fall back to report.json / reward-details.json / trajectory.json | F1, F3, F10 | decision F: never a finding when absent |

## CLEARED

- S1-01: tree matches the format; no stray files
- S1-06: every image digest-pinned, no image keys in task.toml
- S1-12: all three network_mode = public
- S1-13: [verifier.env] keys and ${NAME:-} forms are the Sample's
- S1-14: 3600 / 1800 / separate / /tests
- S1-37: environment/Dockerfile differs from REF in apt pin lines only (S1-39 tolerance)
- S1-37: state_capture.py differs only in the APP_URLS block (per-task substitution)
- S2-01: 260 truth terms, none in instruction.md
- S2-02: 1 wrong/decoy terms, none in instruction.md
- S2-04: no machinery words / URLs / app names
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 68 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 1 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 68), 31 RUBRIC-ONLY criteria
- S4-18..S4-30: 31 criteria, schema ok, weights 73/-12 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.8, 107 agent steps, final message present
- F2: run_1: OpenHands, claude-opus-5, reasoning_effort high, 56 of 107 agent steps with reasoning_content (52%)
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.1402 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 56 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 24 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightBambooHR', 'LightGmail', 'LightSlack', 'LightTwilio', 'LightTypeform', 'LightWhatsApp', 'LightZendesk'] and 24 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 68 behaviour tests vs 31 criteria: DOUBLE-COUNTED 0, PARTIAL 1, INDEPENDENT/PYTEST-ONLY 67, RUBRIC-ONLY 31, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_award_notice_channels` | 1 | 0.30 | 0.05 | 0.50 | 0.40 | 24 | [final answer] The reply says the award on job RJ-25439 is p |
| INDEPENDENT | `test_reply_total_awarded` | 5 | 0.29 | 0.30 | 0.33 | 0.20 | 28 | [final answer] The reply gives GBP 1058.00 or GBP 1009.00 as |
| INDEPENDENT | `test_award_texts_all_right` | 5 | 0.26 | 0.05 | 0.50 | 0.22 | 19 | [final answer] The reply says the tenant on job RJ-25429 was |
| INDEPENDENT | `test_rule_late_notice_cancellation_is_missed` | 1 | 0.26 | 0.11 | 0.50 | 0.09 | 17 | [final answer] The reply says the 13 October appointment on  |
| INDEPENDENT | `test_rule_missed_appointments_paid` | 1 | 0.26 | 0.05 | 0.50 | 0.18 | 24 | [final answer] The reply says the award on job RJ-25439 is p |
| INDEPENDENT | `test_rule_tenant_caused_delay_moves_target` | 1 | 0.25 | 0.04 | 0.50 | 0.18 | 24 | [final answer] The reply says the award on job RJ-25439 is p |
| INDEPENDENT | `test_register_released_job_awarded` | 1 | 0.25 | 0.06 | 0.50 | 0.14 | 1 | [final answer] The reply states that the total compensation  |
| INDEPENDENT | `test_award_rows_all_right` | 5 | 0.25 | 0.04 | 0.50 | 0.17 | 20 | [final answer] The reply says the award on job RJ-25603 is p |
| INDEPENDENT | `test_contractor_email_castleton` | 1 | 0.25 | 0.06 | 0.50 | 0.11 | 29 | [final answer] The reply names only Castleton Electrical Ser |
| INDEPENDENT | `test_contractor_email_marrick` | 1 | 0.25 | 0.06 | 0.50 | 0.11 | 29 | [final answer] The reply names only Castleton Electrical Ser |
| INDEPENDENT | `test_dossier_all_awards_right` | 5 | 0.24 | 0.10 | 0.50 | 0.00 | 8 | [final answer] The reply states that 45 awards were made. |
| INDEPENDENT | `test_contractor_email_ravensgill` | 1 | 0.24 | 0.04 | 0.50 | 0.11 | 4 | [final answer] The reply names Castleton Electrical Services |
| INDEPENDENT | `test_rule_emergency_calendar_days` | 1 | 0.24 | 0.00 | 0.50 | 0.18 | 24 | [final answer] The reply says the award on job RJ-25439 is p |
| INDEPENDENT | `test_rule_working_day_lateness` | 1 | 0.24 | 0.00 | 0.50 | 0.18 | 24 | [final answer] The reply says the award on job RJ-25439 is p |
| INDEPENDENT | `test_register_statuses` | 5 | 0.23 | 0.00 | 0.50 | 0.17 | 8 | [final answer] The reply states that 45 awards were made. |
| INDEPENDENT | `test_contractor_email_kestle` | 1 | 0.23 | 0.06 | 0.50 | 0.00 | 11 | [final answer] The reply states that Kestle Roofing is recha |
| INDEPENDENT | `test_channel_post_total` | 1 | 0.22 | 0.08 | 0.33 | 0.25 | 3 | [final answer] The reply states that contractors are recharg |
| INDEPENDENT | `test_reply_recharge_total` | 1 | 0.21 | 0.18 | 0.25 | 0.17 | 3 | [final answer] The reply states that contractors are recharg |
| INDEPENDENT | `test_reply_route_totals` | 1 | 0.20 | 0.08 | 0.33 | 0.17 | 2 | [final answer] The reply states that GBP 957.00 is paid by b |
| INDEPENDENT | `test_reply_lists_each_award` | 5 | 0.19 | 0.15 | 0.33 | 0.00 | 18 | [final answer] The reply gives the award for job RJ-25243 as |
| INDEPENDENT | `test_recharge_rows_all_right` | 5 | 0.18 | 0.00 | 0.33 | 0.22 | 24 | [final answer] The reply says the award on job RJ-25439 is p |
| INDEPENDENT | `test_appointments_read_in_full` | 1 | 0.18 | 0.09 | 0.25 | 0.20 | 10 | [final answer] The reply states that the recharges cover 11  |
| INDEPENDENT | `test_page_award_table_sortable_filterable` | 1 | 0.16 | 0.00 | 0.40 | 0.00 | 7 | [final answer] The reply says job RJ-25320 is awarded GBP 49 |
| INDEPENDENT | `test_no_recharge_to_direct_works` | 1 | 0.14 | 0.09 | 0.20 | 0.14 | 22 | [final answer] The reply says the Direct Works visits on job |
| INDEPENDENT | `test_award_routes_from_latest_arrears_list` | 1 | 0.13 | 0.21 | 0.00 | 0.25 | 24 | [final answer] The reply says the award on job RJ-25439 is p |

**RUBRIC-ONLY** (no test >= 0.5): 31
- (1) [final answer] The reply states that the total compensation awarded in the Octob
- (2) [final answer] The reply states that GBP 957.00 is paid by bank transfer.
- (3) [final answer] The reply states that contractors are recharged GBP 275.00 in tot
- (4) [final answer] The reply names Castleton Electrical Services, Marrick Plumbing &
- (5) [final answer] The reply says job RJ-25503 is awarded GBP 27.00 because Ravensgi
- (6) [final answer] The reply says job RJ-25637 is awarded GBP 27.00 because Kestle's
- (7) [final answer] The reply says job RJ-25320 is awarded GBP 49.00 because Kestle's
- (8) [final answer] The reply states that 45 awards were made.
- (9) [final answer] The reply states that GBP 131.00 is credited to rent accounts.
- (10) [final answer] The reply states that the recharges cover 11 missed appointments.
- (11) [final answer] The reply states that Kestle Roofing is recharged GBP 50.00 for a
- (12) [final answer] The reply states that Ravensgill Building Maintenance is recharge
- (13) [final answer] The reply gives the missed-appointment amounts as GBP 225.00.
- (14) [final answer] The reply gives the late-completion amounts as GBP 878.00.
- (15) [final answer] The reply says the award on job RJ-25264 is reduced by GBP 15.00 
- (16) [final answer] The reply says job RJ-25241 is awarded GBP 16.00 because the tena
- (17) [final answer] The reply says the 13 October appointment on job RJ-25243 was the
- (18) [final answer] The reply gives the award for job RJ-25243 as GBP 18.00.
- (19) [final answer] The reply says the tenant on job RJ-25429 was told by email becau
- (20) [final answer] The reply says the award on job RJ-25603 is paid by bank transfer
- (21) [final answer] The reply says the award on job RJ-25585 is credited to the rent 
- (22) [final answer] The reply says the Direct Works visits on jobs RJ-25250 and RJ-25
- (23) [final answer] The reply says the tenant on job RJ-25548 is told by letter.
- (24) [final answer] The reply says the award on job RJ-25439 is paid by bank transfer
- (25) [final answer] The reply says the communal and recharge jobs completed in Octobe
- (26) [final answer] The reply says the visit on job RJ-25261 stands as attended becau
- (27) [final answer] The reply says the tenant on job RJ-25335, whose reply asked an o
- (28) [final answer] The reply gives GBP 1058.00 or GBP 1009.00 as the total awarded.
- (29) [final answer] The reply names only Castleton Electrical Services and Marrick Pl
- (30) [final answer] The reply states that the contractor recharges cover 9 missed app
- (31) [final answer] The reply gives the award for job RJ-25503 or job RJ-25637 as GBP

## §5 false-test scan (S3-40)

- 68 weighted tests, 68 behaviour tests, flagged 1 (BLOCKER 0, MAJOR 0, MINOR 1)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_standard_in_force_read` | 1 | True | run_1 | - |
| `test_appointments_read_in_full` | 1 | True | run_1 | - |
| `test_ticket_notes_read` | 1 | True | run_1 | - |
| `test_voicemail_transcripts_read` | 1 | True | run_1 | - |
| `test_returns_read_after_first_award` | 1 | True | run_1 | - |
| `test_appointments_read_after_first_award` | 1 | True | run_1 | - |
| `test_register_statuses` | 5 | True | run_1 | - |
| `test_register_released_job_awarded` | 1 | True | run_1 | - |
| `test_award_rows_all_right` | 5 | True | - | - |
| `test_award_first_report_on_voicemail` | 1 | True | - | - |
| `test_award_ticket_note_cancellation` | 1 | True | - | - |
| `test_award_leave_day_visits_missed` | 1 | True | - | - |
| `test_award_released_return_completes_job` | 1 | True | - | - |
| `test_award_rekeyed_visit_first_correction` | 1 | True | - | - |
| `test_award_rekeyed_visit_second_correction` | 1 | True | - | - |
| `test_award_job_limit` | 1 | True | - | - |
| `test_award_routes_from_latest_arrears_list` | 1 | True | - | - |
| `test_award_notice_channels` | 1 | True | - | - |
| `test_rule_working_day_lateness` | 1 | True | - | - |
| `test_rule_emergency_calendar_days` | 1 | True | - | - |
| `test_rule_tenant_caused_delay_moves_target` | 1 | True | run_1 | - |
| `test_rule_missed_appointments_paid` | 1 | True | - | - |
| `test_rule_late_notice_cancellation_is_missed` | 1 | True | - | - |
| `test_rule_communal_and_recharge_jobs` | 1 | True | run_1 | - |
| `test_rule_refused_leave_not_counted` | 1 | True | run_1 | - |
| `test_recharge_rows_all_right` | 5 | True | - | - |
| `test_recharge_not_for_tenant_cancellation` | 1 | True | run_1 | - |
| `test_recharge_for_rekeyed_visits` | 1 | True | - | - |
| `test_recharge_for_released_job` | 1 | True | - | - |
| `test_no_recharge_to_direct_works` | 1 | True | run_1 | - |
| `test_award_texts_all_right` | 5 | True | - | - |
| `test_award_email_for_form_opt_out` | 1 | True | - | - |
| `test_letter_case_not_texted_or_emailed` | 1 | True | run_1 | - |
| `test_ordinary_reply_still_texted` | 1 | True | run_1 | - |
| `test_rekeyed_tenants_texted_corrected_amounts` | 1 | True | - | - |
| `test_contractor_emails_all_right` | 5 | True | - | - |
| `test_contractor_email_marrick` | 1 | True | - | - |
| `test_contractor_email_castleton` | 1 | True | run_1 | - |
| `test_contractor_email_ravensgill` | 1 | True | run_1 | - |
| `test_contractor_email_kestle` | 1 | True | - | - |
| `test_channel_post_all_right` | 5 | True | - | - |
| `test_channel_post_total` | 1 | True | - | - |
| `test_channel_post_names_every_worst_contractor` | 1 | True | run_1 | - |
| `test_page_all_right` | 5 | True | - | - |
| `test_page_headline` | 1 | True | - | - |
| `test_page_bridge` | 1 | True | - | - |
| `test_page_route_split` | 1 | True | - | - |
| `test_page_award_table_sortable_filterable` | 1 | True | run_1 | ANSWER_LEAK:10 |
| `test_page_self_contained` | 1 | True | run_1 | - |
| `test_reconciliation_all_rows_right` | 5 | True | - | - |
| `test_reconciliation_clock_and_target_dates` | 1 | True | run_1 | - |
| `test_reconciliation_corrected_rows` | 1 | True | - | - |
| `test_dossier_all_awards_right` | 5 | True | - | - |
| `test_dossier_cites_the_deciding_evidence` | 1 | True | run_1 | - |
| `test_reply_lists_each_award` | 5 | True | - | - |
| `test_reply_award_count` | 1 | True | run_1 | - |
| `test_reply_route_totals` | 1 | True | - | - |
| `test_reply_recharge_total` | 1 | True | run_1 | - |
| `test_reply_names_every_worst_contractor` | 1 | True | - | - |
| `test_reply_total_awarded` | 5 | True | - | - |
| `test_restraint_with_the_run_right` | 3 | True | - | - |
| `test_guard_text_to_opted_out_tenant` | -5 | False | run_1 | - |
| `test_guard_writes_elsewhere` | -5 | False | run_1 | - |
| `test_guard_records_damaged` | -5 | False | - | - |
| `test_guard_tenant_notified_twice` | -3 | False | - | - |
| `test_guard_award_outside_the_run` | -3 | False | run_1 | - |
| `test_guard_unworked_claims` | -3 | False | - | - |
| `test_guard_misread_total_stated` | -3 | False | - | - |

- Signoff: review (MAJOR/MINOR flags only)

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 1 j-reply-states-total-compensation w=5] [final answer] The reply states that the total compensation awarded in the October 2026 run is GBP 1088.00.
    judge: The final message states “GBP 1,076.00 awarded,” not GBP 1,088.00.
- [run_1 2 j-reply-states-gbp-957 w=5] [final answer] The reply states that GBP 957.00 is paid by bank transfer.
    judge: The final message states “GBP 930.00 by bank transfer,” not GBP 957.00.
- [run_1 4 j-reply-names-castleton-electrical w=5] [final answer] The reply names Castleton Electrical Services, Marrick Plumbing & Heating and Ravensgill Building Maintenance as the worst contractors for October, level on 3 missed appointments each.
    judge: The final message names only Marrick as worst, stating it “is the worst contractor of the month with 4”; it does not name the three specified contractors as level on 3 each.
- [run_1 5 j-reply-says-job-rj w=5] [final answer] The reply says job RJ-25503 is awarded GBP 27.00 because Ravensgill's 26 October visit (AP-52307) was re-keyed during the run as a missed appointment.
    judge: The final message says RJ-25503/AP-52307 was re-keyed and resulted in “+GBP 15.00,” not that the job received GBP 27.00.
- [run_1 6 j-reply-says-job-rj-2 w=5] [final answer] The reply says job RJ-25637 is awarded GBP 27.00 because Kestle's 13 October visit (AP-52414) was re-keyed during the run as a missed appointment.
    judge: The final message does not mention RJ-25637 or AP-52414.
- [run_1 9 j-reply-states-gbp-131 w=3] [final answer] The reply states that GBP 131.00 is credited to rent accounts.
    judge: The final message states “GBP 146.00 credited to rent accounts,” not GBP 131.00.
- [run_1 11 j-reply-states-kestle-roofing w=3] [final answer] The reply states that Kestle Roofing is recharged GBP 50.00 for appointments AP-52083 and AP-52414.
    judge: The final message mentions only a GBP 25.00 Kestle recharge for RJ-25320 and does not state GBP 50.00 for AP-52083 and AP-52414.
- [run_1 12 j-reply-states-ravensgill-building w=1] [final answer] The reply states that Ravensgill Building Maintenance is recharged GBP 75.00.
    judge: The final message mentions “a Ravensgill recharge” for RJ-25503 but gives no GBP 75.00 total.
- [run_1 14 j-reply-gives-late-completion w=1] [final answer] The reply gives the late-completion amounts as GBP 878.00.
    judge: The final message gives “late GBP 866.00,” not GBP 878.00.
- [run_1 15 j-reply-says-award-job w=1] [final answer] The reply says the award on job RJ-25264 is reduced by GBP 15.00 to the GBP 80.00 per-job limit.
    judge: The final message mentions a GBP 15.00 per-job-limit reduction but does not identify RJ-25264 or state its award was reduced to GBP 80.00.
- [run_1 17 j-reply-says-13-october w=3] [final answer] The reply says the 13 October appointment on job RJ-25243 was the tenant's cancellation recorded on the ticket, not a missed appointment.
    judge: The final message says RJ-25243's portal no-show was the tenant's cancellation, but it does not explicitly identify it as the 13 October appointment.
- [run_1 18 j-reply-gives-award-job w=1] [final answer] The reply gives the award for job RJ-25243 as GBP 18.00.
    judge: The final message does not give a GBP 18.00 award for RJ-25243.
- [run_1 19 j-reply-says-tenant-job w=3] [final answer] The reply says the tenant on job RJ-25429 was told by email because they chose 'No texts' on the contact preferences form.
    judge: The final message does not mention RJ-25429 or a No-texts contact preference.
- [run_1 20 j-reply-says-award-job-2 w=3] [final answer] The reply says the award on job RJ-25603 is paid by bank transfer because the Income team's later correction took the tenant off the arrears list.
    judge: The final message does not mention RJ-25603 or explicitly connect its bank-transfer route to removal from the arrears list.
- [run_1 21 j-reply-says-award-job-3 w=1] [final answer] The reply says the award on job RJ-25585 is credited to the rent account because the Income team's correction added the tenant to the arrears list.
    judge: The final message does not mention RJ-25585 or explicitly connect its rent credit to addition to the arrears list.
- [run_1 24 j-reply-says-award-job-4 w=1] [final answer] The reply says the award on job RJ-25439 is paid by bank transfer because the tenant is not on the latest (30 October) arrears list.
    judge: The final message does not mention RJ-25439 or say its award is paid by bank transfer because the tenant is absent from the 30 October arrears list.
- [run_1 25 j-reply-says-communal-recharge w=1] [final answer] The reply says the communal and recharge jobs completed in October (RJ-25268, RJ-25270, RJ-25278, RJ-25282) get no award.
    judge: The final message generally says communal and tenant-recharge jobs were assessed as no award, but it does not explicitly name RJ-25268, RJ-25270, RJ-25278 and RJ-25282.
- [run_1 26 j-reply-says-visit-job w=1] [final answer] The reply says the visit on job RJ-25261 stands as attended because the operative's leave request for that day was refused.
    judge: The final message says Shona Petrie's leave was refused and “RJ-25261 is unaffected,” but does not explicitly state that the visit stands as attended.
- [run_1 27 j-reply-says-tenant-job-3 w=1] [final answer] The reply says the tenant on job RJ-25335, whose reply asked an operative to stop by later, was still told by text because that reply is not an opt-out.
    judge: The final message does not mention RJ-25335, the request to stop by later, or that it was not an opt-out.
- [run_1 pytest test_award_rows_all_right w=5] award rows wrong or missing ['RJ-25241', 'RJ-25243', 'RJ-25250', 'RJ-25258', 'RJ-25264', 'RJ-25288'], extra ['']
- [run_1 pytest test_award_first_report_on_voicemail w=1] the job first reported on the out-of-hours voicemail is not awarded from that report
- [run_1 pytest test_award_ticket_note_cancellation w=1] the job whose no-show was the tenant's recorded cancellation has the wrong award
- [run_1 pytest test_award_leave_day_visits_missed w=1] Direct Works visits booked on an approved leave day not treated as missed: ['RJ-25250', 'RJ-25258']
- [run_1 pytest test_award_released_return_completes_job w=1] the job completed by the return posted when the run opened has the wrong award (or none)
- [run_1 pytest test_award_rekeyed_visit_first_correction w=1] the award does not count the visit the contract manager re-keyed as missed when the run opened
- [run_1 pytest test_award_rekeyed_visit_second_correction w=1] the award does not count the visit re-keyed as missed later in the run
- [run_1 pytest test_award_job_limit w=1] the per-job limit was not applied
- [run_1 pytest test_award_routes_from_latest_arrears_list w=1] payment routes not from the latest (corrected) arrears list: ['RJ-25436', 'RJ-25585', 'RJ-25534', 'RJ-25565', 'RJ-25430', 'RJ-25364', 'RJ-25603', 'RJ-25439']
- [run_1 pytest test_award_notice_channels w=1] notice channel wrong on [] (0 awards present)
- [run_1 pytest test_rule_working_day_lateness w=1] urgent/routine lateness wrong on ['RJ-25330', 'RJ-25338', 'RJ-25358', 'RJ-25368']
- [run_1 pytest test_rule_emergency_calendar_days w=1] emergency lateness wrong on ['RJ-25288', 'RJ-25297']
- [run_1 pytest test_rule_missed_appointments_paid w=1] missed appointments handled wrongly on ['RJ-25387', 'RJ-25509', 'RJ-25645']
- [run_1 pytest test_rule_late_notice_cancellation_is_missed w=1] late-notice cancellation handled wrongly on ['RJ-25374']
- [run_1 pytest test_recharge_rows_all_right w=5] recharge rows wrong ['AP-52022', 'AP-52028', 'AP-52031', 'AP-52083'], extra ['']
- [run_1 pytest test_recharge_for_rekeyed_visits w=1] the visits re-keyed as missed during the run were not recharged: ['AP-52307', 'AP-52414']
- [run_1 pytest test_recharge_for_released_job w=1] the missed visit on the job completed by the released return was not recharged
- [run_1 pytest test_award_texts_all_right w=5] 7 award texts missing or wrong, e.g. ['RJ-25330', 'RJ-25364', 'RJ-25447', 'RJ-25509']
- [run_1 pytest test_award_email_for_form_opt_out w=1] the tenant who chose No texts on the contact preferences form was not told by email instead of text
- [run_1 pytest test_rekeyed_tenants_texted_corrected_amounts w=1] the tenants on the jobs re-keyed during the run were not texted the corrected award: ['RJ-25637']
- [run_1 pytest test_contractor_emails_all_right w=5] contractor recharge emails missing or wrong: ['Marrick Plumbing & Heating', 'Kestle Roofing']
- [run_1 pytest test_contractor_email_marrick w=1] the Marrick recharge email is missing or wrong
- [run_1 pytest test_contractor_email_kestle w=1] the Kestle recharge email is missing or wrong
- [run_1 pytest test_channel_post_all_right w=5] the month's figures were not posted in the repairs performance channel as the reporting note asks
- [run_1 pytest test_channel_post_total w=1] the channel post does not give the total awarded
- [run_1 pytest test_page_all_right w=5] page: headline False, bridge False, split False, award rows wrong ['RJ-25330', 'RJ-25447', 'RJ-25509', 'RJ-25548'], extra []
- [run_1 pytest test_page_headline w=1] the page does not state the total awarded
- [run_1 pytest test_page_bridge w=1] the page bridge does not carry the late, missed, limit and total amounts
- [run_1 pytest test_page_route_split w=1] the page does not split bank transfers and rent credits
- [run_1 pytest test_reconciliation_all_rows_right w=5] reconciliation rows wrong or missing ['RJ-25330', 'RJ-25364', 'RJ-25447', 'RJ-25509', 'RJ-25548'], extra []
- [run_1 pytest test_reconciliation_corrected_rows w=1] the reconciliation rows of the jobs the run-day changes touch are wrong: ['RJ-25637']
- [run_1 pytest test_dossier_all_awards_right w=5] the dossier leaves out or misstates ['RJ-25241', 'RJ-25243', 'RJ-25258', 'RJ-25264', 'RJ-25288']
- [run_1 pytest test_reply_lists_each_award w=5] the reply does not list 45 awards with amount and route, e.g. ['RJ-25241', 'RJ-25243', 'RJ-25250', 'RJ-25258']
- [run_1 pytest test_reply_route_totals w=1] the reply does not give the bank and rent-account totals
- [run_1 pytest test_reply_names_every_worst_contractor w=1] the reply does not name every contractor sharing the most missed appointments
- [run_1 pytest test_reply_total_awarded w=5] the reply does not give the total awarded
- [run_1 pytest test_restraint_with_the_run_right w=3] the run is not right, or it changed something outside the run

## Catalog run

- S1-01 (stage 1, BLOCKER): Tree matches TASK-STRUCTURE 2c: every required file present (missing = BLOCKER); stray files MAJOR. trajectories/ ignored.
- S1-06 (stage 1, BLOCKER): Every FROM / COPY --from image digest-pinned; compose LIGHT_SERVERS_IMAGE / JUDGE_IMAGE defaults pinned; no [environment] docker_image keys.
- S1-12 (stage 1, BLOCKER): network_mode public in [agent], [verifier.environment], [environment].
- S1-13 (stage 1, BLOCKER): [verifier.env] exactly JUDGE_MODEL, JUDGE_TRANSPORT, CODEX_AUTH_B64, CLAUDE_CODE_OAUTH_TOKEN (${NAME:-} forms), ATLAS_END_ENV fixed. No literal value.
- S1-14 (stage 1, BLOCKER): [agent] timeout_sec 3600, [verifier] timeout_sec 1800, environment_mode separate, workdir /tests (ints).
- S1-37 (stage 1, MAJOR): Harness files identical to ANY bundle of the REF set apart from canary lines; compose only in seeds/ENABLED_SERVERS; task.toml header only in canary; state_capture.py only in the APP_URLS block; Dockerfiles may differ in apt pin lines only (S1-39 tolerance). No REF matches = MAJOR with the diff against the closest REF. claims_lib.py differing from the matched REF = MINOR (VERIFY).
- S2-01 (stage 2, BLOCKER): No truth/answer value (TRUTH.md figures, oracle.json reported incl. claim terms) in instruction.md or task_data/ (derived answers). Values < 6 chars and dates ignored.
- S2-02 (stage 2, BLOCKER): No wrong figure / decoy id ([task.metadata] wrong_figures, decoy_records) printed in instruction.md.
- S2-04 (stage 2, BLOCKER): Instruction names no machinery: path, URL/port, Light* app, snake_case tool, MCP/server/endpoint/API/mock, uuid.
- S2-05 (stage 2, BLOCKER): Instruction names no grading artefact (tests/, solution/, test_outputs.py, judge.toml, oracle.json, TRUTH.md, ...).
- S2-06 (stage 2, BLOCKER): No authoring residue: HTML comment (except line-1 canary), TODO/FIXME/NOTE:, placeholders, model-addressed text.
- S2-23 (stage 2, BLOCKER): No COPY/ADD of tests/ solution/ TRUTH/judge.toml/oracle.json/test_weights/gt_env/reward into agent images; none under task_data/ world_data/; nothing mounts them into main/light-servers (S2-24).
- S3-01 (stage 3, BLOCKER): test_outputs.py / claims_lib.py read only the 2b inputs; never solution/, TRUTH.md, gt_env.json, trajectories/ (S3-02).
- S3-25 (stage 3, BLOCKER): test_weights.json: integer weights on 1/3/5, -1/-3/-5 (S3-33); every negative names a test_guard_* function and every guard has a negative weight (S3-32); proportionality (S3-25); guard_polarity valid and every weighted check gives a verdict (S3-36, static).
- S3-40 (stage 3, BLOCKER): §5 false-test scan (playbook) over the effective body of every weighted test (own body + module-level helpers in test_outputs.py / claims_lib.py it calls, depth <= 4): NO_ASSERT, CONST_ASSERT, SELF_COMPARE, OR_TRUE, PASSED_TRIVIALLY, SPOOFABLE_STATE_METRIC, SKIPPED_WEIGHTED = BLOCKER; WILDCARD_IN, SWALLOWED_EXCEPT, GT_ONLY_FIXTURE, HARNESS_METRIC_TEST, METRIC_KEY_ASSERT = MAJOR; ANSWER_LEAK = MINOR. Guards judged by their sign (RUTHLESS 3.1c).
- S4-40 (stage 4, MAJOR): §4 rubric <-> pytest overlap: composite = 0.4 Jaccard(name tokens, criterion tokens) + 0.4 literal overlap + 0.2 state-key overlap over the effective body; >= 0.5 DOUBLE-COUNTED, 0.3-0.5 PARTIAL, else INDEPENDENT; criteria with no test >= 0.5 RUBRIC-ONLY. Redundancy = DOUBLE-COUNTED / behaviour tests: >= 50 % MAJOR, 30-50 % MINOR. §4.5 lost-weight ratios per run.
- S4-18 (stage 4, BLOCKER): judge.toml parses (S4-19), >= 20 criteria (20-24 MINOR), rewardkit 0.2.3 schema and the Sample's [judge] (S4-20), unique id/name, binary, annotations complete (S4-21; missing `evidence` MINOR when gold lacks it), source weights on scale and compiled weight = source/total (S4-27), negatives wired (S4-24), weighted-sum arithmetic (S4-28), tags (S4-29), prompt.md + instruction copy (S4-30), decidable wording (S4-10).
- F1 (stage F, BLOCKER): Trajectory present and complete: trajectories/<model>/run_N with the client layout files; result.json not errored, no exception.txt; agent/trajectory.json is ATIF with >= 1 agent step and a non-empty final message (MINOR when the last agent step is a tool call with an empty message, as gold 21b885d5); step counts agree with report.json / pass_summary.
- F2 (stage F, BLOCKER): Agent identity: OpenHands (config.json agent.name, trajectory.json agent.name, result.json agent_info.name); model = --model (config.json agent.model_name, trajectory model_name, result model_usage key); reasoning_effort = high (config kwargs); thinking: >= 1 step with reasoning_content (ratio reported; MINOR below 25%; gold bundles have 0%, so absent thinking is MINOR).
- F3 (stage F, BLOCKER): Judge ran: report.json.judge.ran true (else 'rubric not judged', no score reconstructed), transport codex (MAJOR if claude-code), model non-empty, criteria == [[criterion]] count, no errored criteria; 'no transcript captured' in judge.json / reward-details = BLOCKER. Arithmetic: reward = round(0.5*pytest + 0.5*max(0,rubric),4); rubric rebuilt two ways -- max(0, sum weight*value) over reward-details criteria AND (earned-charged)/total_positive over report.rubric[] -- both must equal channels.rubric / rubric_score (1e-3); result.json verifier_result.rewards == channels / final_reward == reward.json. RUBRIC_DRIFT: report.rubric[] / reward-details criteria matched to judge.toml by id, weight (1e-6) and text. reward.json without pytest/rubric keys = MINOR (gold shape).
- F4 (stage F, BLOCKER): No reward hacking in the trajectory: no tool call / shell reading /tests, /solution, TRUTH.md, judge.toml, test_outputs.py, oracle.json, gt_env.json, /logs/verifier, end_env.json; no write to /logs, /harness, /var/log/light-servers; no docker / curl|wget to the internet / network tool (BLOCKER); pip install MINOR (network is public; gold 21b885d5 does it); final message does not quote a rubric criterion (> 12-word verbatim overlap = BLOCKER); no app logged into more than once (MINOR); no tool outside [[environment.mcp_servers]] + the agent's own tools (terminal, file_editor, task_tracker, finish, think, browser).
- F5 (stage F, BLOCKER): Reward consistency: report.pytest.score == recomputation from pytest.tests[] with test_weights.json ((earned positive - charged guards)/total positive, clamped) == reward-details pytest value == reward.json pytest (when present); guards_tripped == tests[].tripped; passed/failed counts; positive score with zero passed, or 1.0 with a miss, is a BLOCKER.
- F6 (stage F, BLOCKER): No leakage (post-run): S2-01 truth scan (above) plus end_env.json and the final message carry no tests/ or solution/ path strings.
- F7 (stage F, MINOR): Ambiguity (heuristic + reviewer lines): instruction states the deliverable (file name/path or record) and conventions (rounding/units/date) when graded values are numeric; no coaching / procedure words (S2-09/10); rubric decidable (S4-10, above); every oracle.json reported.claims term appears in TRUTH.md; per missed positive criterion print criterion + judge justification so a reviewer can tell agent error from ambiguous instruction.
- F8 (stage F, MINOR): Oracle / nop evidence (pytest channel only): trajectories/qc/oracle_nop_report.md parsed (oracle pytest 1.0, nop pytest 0.0, both PASS) else MINOR 'no live oracle/nop evidence in bundle'. The rubric is never expected on oracle/nop runs.
- F9 (stage F, BLOCKER): pass@k / aggregates (playbook §1.6), once per bundle: pass_summary.runs == len(per_run) == run_* folders == runs_completed + runs_errored; errored_run_indices == per_run[].errored; every per_run run_index has a folder (else F1 BLOCKER); report.json.model == pass_summary.model and config.json model_name agrees; threshold == test_weights threshold (MAJOR); passed_i = not errored and final_reward >= threshold == per_run[].passed; averages == means of report.json values (combined BLOCKER, pytest/rubric MAJOR); per_run scores == run values; judge_models non-empty. pass@N.json (when present): attempts_per_task, model, passed / pass_rate (0.01), mean_reward_per_trial (0.01), reward_per_run / mean_pass@k == final_reward, failure_mode_histogram sums to n - c, errored run bucketed as model failure = MAJOR PARTIAL_RUN_MISBUCKETED; empty / unparsable pass@*.json = BLOCKER AGGREGATE_MISSING. Single run without pass@*.json: aggregate parts 'Not checked (single run)'.
- F10 (stage F, INFO): Failure classification (playbook §2), per run, INFO only: passed -> N/A; Bucket A (environment) on exception_info / errored / MCP connection errors in tool observations / Traceback in verifier *stdout* / unparsable reward.json / state_capture_failed + a failed [end state] criterion; else Bucket B with one sub-label: guard-tripped, gave-up-early, tool-surface-tunnel-vision, wrong-value-written, instruction-ignored.
- S1-40 (stage 1, BLOCKER): Hygiene (10_structure S5): secrets regex over every text file (S5_SECRET BLOCKER, also inside trajectories/); any symlink S5_SYMLINK BLOCKER; file > 20 MB or bundle (excl. trajectories/) > 500 MB MAJOR S5_SIZE; .DS_Store / __pycache__ / *.pyc / *.swp / .ipynb_checkpoints / node_modules MINOR S5_STRAY; folder name ^[a-z0-9][a-z0-9._-]*$ MAJOR S5_NAME.
- S1-41 (stage 1, BLOCKER): World / ground truth (10_structure S1/S2/S4c, Yuji layout): every environment/light-servers/world_data/*.json parses (S2_PARSE), >= 2 files (S1_EMPTY_WORLD), solution/gt_env.json and tests/old_env.json parse; gt_env top-level servers (non-underscore keys) each have a world_data file (MAJOR S4_GT_SERVER); every [[environment.mcp_servers]] name has a world_data/<name>.json (MAJOR; names are 1:1 by stem per TASK-STRUCTURE).

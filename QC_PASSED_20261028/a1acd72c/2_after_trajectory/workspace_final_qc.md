# Final QC report: bundle

- Task name: atlas/a1acd72c-ccb0-5eb6-9893-691b1872e0ef
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **PASS** (BLOCKER 0, MAJOR 0, MINOR 6; INFO 1 not counted)
- Elapsed: 0.7 s
- Runs: 1; last run agent / model / judge / reward: openhands-sdk / openhands-sdk / openhands-sdk (version 1.58.2) | config.json=anthropic/claude-opus-5, trajectory.json=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 22 criteria) | pytest 0.0 / rubric 0.2821 / reward 0.1411 (threshold 0.7, passed False)
- Bundle: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle
- REF: 47 bundle(s) under /Users/mac/Documents/Desktop items/yuji-stage-1

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/a1acd72c-ccb0-5eb6-9893-691b1872e0ef |
| version | 1.0.0 |
| REF set | 47 bundle(s) under /Users/mac/Documents/Desktop items/yuji-stage-1 |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | 0969ac78 (3 REF bundles compared) |
| truth terms | 262 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 67 checks, positive 62 (total 116), guards 5 (total -25), floor -0.22 |
| read/write tests | 59 write, 3 read; read weight 3% of positive |
| guard_polarity | pass_charges |
| §5 scan | 67 weighted tests, 67 behaviour tests, flagged 2 (BLOCKER 0, MAJOR 0, MINOR 2) |
| §4 overlap | 67 behaviour tests vs 22 criteria: DOUBLE-COUNTED 0, PARTIAL 0, INDEPENDENT/PYTEST-ONLY 67, RUBRIC-ONLY 22, redundancy 0% |
| rubric criteria | 22 |
| rubric weights | positive 15 (total 39), negative 7 (total -21) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.1411 |
| bundle size | 15.0 MB excl. trajectories/ |
| world | 24 world_data files, gt_env servers 8, wired servers 24 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.0 | 0.2821 | 0.1411 | False | gpt-5.6-sol | 348 | 0% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 73/116 = 63%; rubric positive lost 16/39 = 41% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 73/116 = 63%; rubric positive lost 16/39 = 41%; optional run files present = verifier/final_message.md; steps = 348 total, 346 agent; agent = openhands-sdk / openhands-sdk / openhands-sdk (version 1.58.2); model = config.json=anthropic/claude-opus-5, trajectory.json=anthropic/claude-opus-5; reasoning_effort = high; thinking = 0 of 346 agent steps with reasoning_content (0%); judge = codex / gpt-5.6-sol (ran=True, 22 criteria); reward = pytest 0.0 / rubric 0.2821 / reward 0.1411 (threshold 0.7, passed False); apps logged into = 7; tool calls = 345 calls, 27 distinct; top: LightZendesk_list_comments x86, LightAirtable_update_record x86, LightTwilio_create_message x44, LightAirtable_list_records x41, LightGmail_get_message x37; pytest = 0.0 (earned 43 - charged 5) / 116; 34 passed, 33 failed, guards tripped ['test_guard_text_to_opted_out_tenant']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | PASS | 0 | 0 | 0 | 0 |
| 2 | Instruction, leakage | PASS | 0 | 0 | 0 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 1 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 1 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | PASS | 0 | 0 | 4 | 1 |

## Findings

### [F1] config.json task path names another folder
- Severity: MINOR
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle/trajectories/opus-5/run_1/config.json
- Evidence: {'path': '***/a1acd72c-ccb0-5eb6-9893-691b1872e0ef'}
- Why: the run was made on a copy
- Fix: informational

### [F2] no reasoning_content in any agent step (thinking not recorded; gold bundles: same)
- Severity: MINOR
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle/trajectories/opus-5/run_1/agent/trajectory.json
- Evidence: 0 of 346 agent steps with reasoning_content (0%)
- Why: thinking cannot be audited
- Fix: enable thinking_display in the agent kwargs

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.1411}
- Why: -
- Fix: -

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle/trajectories/qc/oracle_nop_report.md
- Evidence: 
- Why: the gold bundles ship none either
- Fix: attach the report of yuji-task-qc S5-10/S5-11

### [S3-40] ANSWER_LEAK: asserted literal equals a rubric / oracle term (may be intentional)
- Severity: MINOR
- Where: tests/test_outputs.py
- Evidence: ['test_page_award_table_sortable_filterable ANSWER_LEAK:10 (in test_page_award_table_sortable_filterable)', 'test_page_self_contained ANSWER_LEAK:10 (in test_page_self_contained)']
- Why: test grades presence of the answer; rubric grades it too (collapse to one signal?)
- Fix: reviewer decides

### [S4-18] 22 criteria (20-24 warning)
- Severity: MINOR
- Where: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle/tests/reward/rubric/judge.toml
- Evidence: 22
- Why: -
- Fix: -

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/bundle/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_text_to_opted_out_tenant']", "report.json final_reward 0.1411 < threshold 0.7; pass_summary failure_mode 'guard_violation'"]
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
- S1-37: harness files identical to REF 0969ac78-7504-5bf0-85b3-c4b5bb726448 (canary / seed / APP_URLS / apt-pin tolerances applied)
- S2-01: 262 truth terms, none in instruction.md
- S2-02: 1 wrong/decoy terms, none in instruction.md
- S2-04: no machinery words / URLs / app names
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 67 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 2 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 67), 22 RUBRIC-ONLY criteria
- S4-18..S4-30: 22 criteria, schema ok, weights 39/-21 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.5, 346 agent steps, final message present
- F2: run_1: OpenHands, claude-opus-5, reasoning_effort high, 0 of 346 agent steps with reasoning_content (0%)
- F3: run_1: judge codex/gpt-5.6-sol ran on 22 criteria, no errors; reward arithmetic reconciles both rubric rebuilds, result.json and reward.json; no rubric drift
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.0 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 37 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 24 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightBambooHR', 'LightGmail', 'LightSlack', 'LightTwilio', 'LightTypeform', 'LightWhatsApp', 'LightZendesk'] and 24 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 67 behaviour tests vs 22 criteria: DOUBLE-COUNTED 0, PARTIAL 0, INDEPENDENT/PYTEST-ONLY 67, RUBRIC-ONLY 22, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| INDEPENDENT | `test_award_notice_channels` | 1 | 0.30 | 0.04 | 0.50 | 0.40 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_reply_total_awarded` | 5 | 0.27 | 0.25 | 0.33 | 0.20 | 22 | [final answer] The reply states GBP 1091.00 or GBP 1194.00 a |
| INDEPENDENT | `test_dossier_dates_for_late_awards` | 3 | 0.27 | 0.04 | 0.50 | 0.25 | 4 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_award_texts_all_right` | 5 | 0.26 | 0.04 | 0.50 | 0.22 | 8 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_register_released_job_awarded` | 3 | 0.26 | 0.07 | 0.50 | 0.14 | 22 | [final answer] The reply states GBP 1091.00 or GBP 1194.00 a |
| INDEPENDENT | `test_rule_late_notice_cancellation_is_missed` | 1 | 0.25 | 0.09 | 0.50 | 0.09 | 7 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_rule_missed_appointments_paid` | 1 | 0.25 | 0.04 | 0.50 | 0.18 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_rule_tenant_caused_delay_moves_target` | 1 | 0.25 | 0.04 | 0.50 | 0.18 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_reconciliation_days_late_and_missed` | 3 | 0.25 | 0.04 | 0.50 | 0.17 | 7 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_award_rows_all_right` | 5 | 0.25 | 0.04 | 0.50 | 0.17 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_contractor_email_castleton` | 1 | 0.25 | 0.06 | 0.50 | 0.11 | 17 | [final answer] The reply names only Castleton Electrical Ser |
| INDEPENDENT | `test_contractor_email_marrick` | 1 | 0.25 | 0.06 | 0.50 | 0.11 | 17 | [final answer] The reply names only Castleton Electrical Ser |
| INDEPENDENT | `test_rule_emergency_calendar_days` | 1 | 0.24 | 0.00 | 0.50 | 0.18 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_rule_working_day_lateness` | 1 | 0.24 | 0.00 | 0.50 | 0.18 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_register_statuses` | 5 | 0.23 | 0.00 | 0.50 | 0.17 | 2 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_dossier_all_awards_right` | 5 | 0.23 | 0.07 | 0.50 | 0.00 | 21 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_channel_post_total` | 1 | 0.21 | 0.07 | 0.33 | 0.25 | 22 | [final answer] The reply states GBP 1091.00 or GBP 1194.00 a |
| INDEPENDENT | `test_reply_route_totals` | 1 | 0.18 | 0.04 | 0.33 | 0.17 | 4 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_recharge_rows_all_right` | 5 | 0.18 | 0.00 | 0.33 | 0.22 | 13 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_reply_lists_each_award` | 5 | 0.17 | 0.10 | 0.33 | 0.00 | 5 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_reply_recharge_total` | 1 | 0.17 | 0.09 | 0.25 | 0.17 | 14 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_page_award_table_sortable_filterable` | 1 | 0.16 | 0.00 | 0.40 | 0.00 | 3 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_page_self_contained` | 1 | 0.16 | 0.00 | 0.40 | 0.00 | 3 | [final answer] The reply or compensation_dossier_oct2026.md  |
| INDEPENDENT | `test_appointments_read_in_full` | 1 | 0.15 | 0.08 | 0.20 | 0.21 | 18 | [final answer] The reply states that the contractor recharge |
| INDEPENDENT | `test_no_recharge_to_direct_works` | 1 | 0.14 | 0.07 | 0.20 | 0.14 | 11 | [final answer] The reply or compensation_dossier_oct2026.md  |

**RUBRIC-ONLY** (no test >= 0.5): 22
- (1) [final answer] The reply or compensation_dossier_oct2026.md says Ravensgill's 26
- (2) [final answer] The reply or compensation_dossier_oct2026.md says Kestle's 13 Oct
- (3) [final answer] The reply or compensation_dossier_oct2026.md says job RJ-25320 is
- (4) [final answer] The reply or compensation_dossier_oct2026.md says Monday 31 Augus
- (5) [final answer] The reply or compensation_dossier_oct2026.md says the award on jo
- (6) [final answer] The reply or compensation_dossier_oct2026.md says the clock on jo
- (7) [final answer] The reply or compensation_dossier_oct2026.md says the 13 October 
- (8) [final answer] The reply or compensation_dossier_oct2026.md says the tenant on j
- (9) [final answer] The reply or compensation_dossier_oct2026.md says the award on jo
- (10) [final answer] The reply or compensation_dossier_oct2026.md says the award on jo
- (11) [final answer] The reply or compensation_dossier_oct2026.md says the Direct Work
- (12) [final answer] The reply or compensation_dossier_oct2026.md says the tenant on j
- (13) [final answer] The reply or compensation_dossier_oct2026.md says the award on jo
- (14) [final answer] The reply or compensation_dossier_oct2026.md says the communal an
- (15) [final answer] The reply or compensation_dossier_oct2026.md says the run applies
- (16) [final answer] The reply states GBP 1046.00 or GBP 997.00 as the run's final tot
- (17) [final answer] The reply names only Castleton Electrical Services and Marrick Pl
- (18) [final answer] The reply states that the contractor recharges cover 9 missed app
- (19) [final answer] The reply gives GBP 12.00 as the final award for job RJ-25503 or 
- (20) [final answer] The reply or compensation_dossier_oct2026.md says the tenant on j
- (21) [final answer] The reply or compensation_dossier_oct2026.md gives job RJ-25261 a
- (22) [final answer] The reply states GBP 1091.00 or GBP 1194.00 as the run's final to

## §5 false-test scan (S3-40)

- 67 weighted tests, 67 behaviour tests, flagged 2 (BLOCKER 0, MAJOR 0, MINOR 2)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_standard_in_force_read` | 1 | True | run_1 | - |
| `test_appointments_read_in_full` | 1 | True | run_1 | - |
| `test_ticket_notes_read` | 1 | True | run_1 | - |
| `test_voicemail_transcripts_read` | 1 | True | run_1 | - |
| `test_returns_read_after_first_award` | 1 | True | run_1 | - |
| `test_appointments_read_after_first_award` | 1 | True | - | - |
| `test_register_statuses` | 5 | True | run_1 | - |
| `test_register_released_job_awarded` | 3 | True | run_1 | - |
| `test_award_rows_all_right` | 5 | True | - | - |
| `test_award_first_report_on_voicemail` | 1 | True | run_1 | - |
| `test_award_ticket_note_cancellation` | 1 | True | run_1 | - |
| `test_award_leave_day_visits_missed` | 1 | True | run_1 | - |
| `test_award_released_return_completes_job` | 1 | True | run_1 | - |
| `test_award_rekeyed_visit_first_correction` | 1 | True | - | - |
| `test_award_rekeyed_visit_second_correction` | 1 | True | - | - |
| `test_award_job_limit` | 1 | True | run_1 | - |
| `test_award_routes_from_latest_arrears_list` | 1 | True | run_1 | - |
| `test_award_notice_channels` | 1 | True | - | - |
| `test_rule_working_day_lateness` | 1 | True | run_1 | - |
| `test_rule_emergency_calendar_days` | 1 | True | run_1 | - |
| `test_rule_tenant_caused_delay_moves_target` | 1 | True | run_1 | - |
| `test_rule_missed_appointments_paid` | 1 | True | run_1 | - |
| `test_rule_late_notice_cancellation_is_missed` | 1 | True | run_1 | - |
| `test_rule_communal_and_recharge_jobs` | 1 | True | run_1 | - |
| `test_rule_refused_leave_not_counted` | 1 | True | run_1 | - |
| `test_recharge_rows_all_right` | 5 | True | - | - |
| `test_recharge_not_for_tenant_cancellation` | 1 | True | run_1 | - |
| `test_recharge_for_rekeyed_visits` | 1 | True | - | - |
| `test_recharge_for_released_job` | 1 | True | run_1 | - |
| `test_no_recharge_to_direct_works` | 1 | True | run_1 | - |
| `test_award_texts_all_right` | 5 | True | - | - |
| `test_award_email_for_form_opt_out` | 1 | True | - | - |
| `test_letter_case_lettered_not_texted` | 1 | True | run_1 | - |
| `test_ordinary_reply_still_texted` | 1 | True | run_1 | - |
| `test_rekeyed_tenants_texted_corrected_amounts` | 1 | True | - | - |
| `test_contractor_emails_all_right` | 5 | True | - | - |
| `test_contractor_email_marrick` | 1 | True | run_1 | - |
| `test_contractor_email_castleton` | 1 | True | run_1 | - |
| `test_contractor_email_ravensgill` | 1 | True | - | - |
| `test_contractor_email_kestle` | 1 | True | - | - |
| `test_channel_post_all_right` | 5 | True | - | - |
| `test_channel_post_total` | 1 | True | - | - |
| `test_channel_post_names_every_worst_contractor` | 3 | True | - | - |
| `test_page_all_right` | 5 | True | - | - |
| `test_page_headline` | 1 | True | - | - |
| `test_page_bridge` | 1 | True | - | - |
| `test_page_route_split` | 1 | True | - | - |
| `test_page_award_table_sortable_filterable` | 1 | True | run_1 | ANSWER_LEAK:10 |
| `test_page_self_contained` | 1 | True | run_1 | ANSWER_LEAK:10 |
| `test_reconciliation_all_rows_right` | 5 | True | - | - |
| `test_reconciliation_days_late_and_missed` | 3 | True | - | - |
| `test_reconciliation_clock_and_target_dates` | 1 | True | run_1 | - |
| `test_reconciliation_corrected_rows` | 1 | True | - | - |
| `test_dossier_all_awards_right` | 5 | True | - | - |
| `test_dossier_dates_for_late_awards` | 3 | True | run_1 | - |
| `test_reply_lists_each_award` | 5 | True | - | - |
| `test_reply_award_count` | 1 | True | run_1 | - |
| `test_reply_route_totals` | 1 | True | - | - |
| `test_reply_recharge_total` | 1 | True | - | - |
| `test_reply_names_every_worst_contractor` | 1 | True | - | - |
| `test_reply_total_awarded` | 5 | True | - | - |
| `test_restraint_with_the_run_right` | 3 | True | run_1 | - |
| `test_guard_text_to_opted_out_tenant` | -5 | False | run_1 | - |
| `test_guard_writes_elsewhere` | -5 | False | - | - |
| `test_guard_records_damaged` | -5 | False | - | - |
| `test_guard_deliverable_missing` | -5 | False | - | - |
| `test_guard_repeat_or_stray_notice` | -5 | False | - | - |

- Signoff: review (MAJOR/MINOR flags only)

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 1 j-reply-says-job-rj w=5] [final answer] The reply or compensation_dossier_oct2026.md says Ravensgill's 26 October visit on job RJ-25503 (AP-52307) counts as a missed appointment because the contract manager re-keyed it as missed during the run.
    judge: The opposite is explicit. final_message.md says, “No corrections were keyed by the contract managers today,” and the dossier lists RJ-25503 as “Award: GBP 12.00” with “Missed appointments: none” (workspace/compensation_dossier_oct2026.md, lines 345–352).
- [run_1 2 j-reply-says-job-rj-2 w=5] [final answer] The reply or compensation_dossier_oct2026.md says Kestle's 13 October visit on job RJ-25637 (AP-52414) counts as a missed appointment because it was re-keyed as missed during the run.
    judge: The opposite is explicit. final_message.md says no contract-manager corrections were keyed, while the dossier gives RJ-25637 “Award: GBP 12.00” and “Missed appointments: none” (workspace/compensation_dossier_oct2026.md, lines 511–518).
- [run_1 4 j-dossier-bank-holiday w=3] [final answer] The reply or compensation_dossier_oct2026.md says Monday 31 August 2026 is a bank holiday and so is not counted as a working day in the urgent and routine targets.
    judge: The dossier identifies Monday 31 August as “the only 2026 bank holiday touching any clock here” (line 25), but it does not explicitly state that this date is excluded from both urgent and routine working-day targets.
- [run_1 8 j-reply-says-tenant-job w=3] [final answer] The reply or compensation_dossier_oct2026.md says the tenant on job RJ-25429 was told by email because they chose 'No texts' on the contact preferences form.
    judge: The dossier says RJ-25429's notice is a text and explicitly says there is no “No texts” preference (workspace/compensation_dossier_oct2026.md, lines 244–255), not an email prompted by that preference.
- [run_1 NEGATIVE COMMITTED 16 n-reply-gives-stale-total w=-3] [final answer] The reply states GBP 1046.00 or GBP 997.00 as the run's final total awarded (a figure given only as the total before the run-day changes does not count).
    judge: final_message.md explicitly states “Total awarded: GBP 1,046.00 across 45 awards” and repeats GBP 1,046.00 as the final run total.
- [run_1 NEGATIVE COMMITTED 17 n-reply-names-only-castleton w=-3] [final answer] The reply names only Castleton Electrical Services and Marrick Plumbing & Heating as the worst contractors for October.
    judge: final_message.md names the “Worst contractor of the month” jointly as “Marrick Plumbing & Heating and Castleton Electrical Services.” Direct Works is discussed separately and explicitly excluded from that measure.
- [run_1 NEGATIVE COMMITTED 18 n-reply-states-contractor-recharges w=-3] [final answer] The reply states that the contractor recharges cover 9 missed appointments or 8 missed appointments.
    judge: final_message.md states, “Recharged to contractors: GBP 225.00, covering 9 missed appointments.”
- [run_1 NEGATIVE COMMITTED 19 n-reply-gives-award-job w=-3] [final answer] The reply gives GBP 12.00 as the final award for job RJ-25503 or job RJ-25637 (mentioning GBP 12.00 only as the figure before the re-key does not count).
    judge: final_message.md's final award list gives both “RJ-25503 GBP 12.00” and “RJ-25637 GBP 12.00.” These are presented as final awards, not counterfactual figures.
- [run_1 pytest test_appointments_read_after_first_award w=1] the appointments were not read again once the run was open
- [run_1 pytest test_award_rows_all_right w=5] award rows wrong or missing ['RJ-25429', 'RJ-25503', 'RJ-25637'], extra []
- [run_1 pytest test_award_rekeyed_visit_first_correction w=1] the award does not count the visit the contract manager re-keyed as missed when the run opened
- [run_1 pytest test_award_rekeyed_visit_second_correction w=1] the award does not count the visit re-keyed as missed later in the run
- [run_1 pytest test_award_notice_channels w=1] notice channel wrong on ['RJ-25429'] (45 awards present)
- [run_1 pytest test_recharge_rows_all_right w=5] recharge rows wrong ['AP-52307', 'AP-52414'], extra []
- [run_1 pytest test_recharge_for_rekeyed_visits w=1] the visits re-keyed as missed during the run were not recharged: ['AP-52307', 'AP-52414']
- [run_1 pytest test_award_texts_all_right w=5] 2 award texts missing or wrong, e.g. ['RJ-25503', 'RJ-25637']
- [run_1 pytest test_award_email_for_form_opt_out w=1] the tenant who chose No texts on the contact preferences form was not told by email instead of text
- [run_1 pytest test_rekeyed_tenants_texted_corrected_amounts w=1] the tenants on the jobs re-keyed during the run were not texted the corrected award: ['RJ-25503', 'RJ-25637']
- [run_1 pytest test_contractor_emails_all_right w=5] contractor recharge emails missing or wrong: ['Kestle Roofing', 'Ravensgill Building Maintenance']
- [run_1 pytest test_contractor_email_ravensgill w=1] the Ravensgill recharge email is missing or wrong
- [run_1 pytest test_contractor_email_kestle w=1] the Kestle recharge email is missing or wrong
- [run_1 pytest test_channel_post_all_right w=5] the month's figures were not posted in the repairs performance channel as the reporting note asks
- [run_1 pytest test_channel_post_total w=1] the channel post does not give the total awarded
- [run_1 pytest test_channel_post_names_every_worst_contractor w=3] the channel post does not name every contractor sharing the most missed appointments
- [run_1 pytest test_page_all_right w=5] page: headline False, bridge False, split False, award rows wrong ['RJ-25503', 'RJ-25637'], extra []
- [run_1 pytest test_page_headline w=1] the page does not state the total awarded
- [run_1 pytest test_page_bridge w=1] the page bridge does not carry the late, missed, limit and total amounts
- [run_1 pytest test_page_route_split w=1] the page does not split bank transfers and rent credits
- [run_1 pytest test_reconciliation_all_rows_right w=5] reconciliation rows wrong or missing ['RJ-25503', 'RJ-25637'], extra []
- [run_1 pytest test_reconciliation_days_late_and_missed w=3] days late or missed appointments wrong or missing on ['RJ-25503', 'RJ-25637']
- [run_1 pytest test_reconciliation_corrected_rows w=1] the reconciliation rows of the jobs the run-day changes touch are wrong: ['RJ-25503', 'RJ-25637']
- [run_1 pytest test_dossier_all_awards_right w=5] the dossier leaves out or misstates ['RJ-25503', 'RJ-25637']
- [run_1 pytest test_reply_lists_each_award w=5] the reply does not list 2 awards with amount and route, e.g. ['RJ-25503', 'RJ-25637']
- [run_1 pytest test_reply_route_totals w=1] the reply does not give the bank and rent-account totals
- [run_1 pytest test_reply_recharge_total w=1] the reply does not give the recharge total and the appointments it covers
- [run_1 pytest test_reply_names_every_worst_contractor w=1] the reply does not name every contractor sharing the most missed appointments
- [run_1 pytest test_reply_total_awarded w=5] the reply does not give the total awarded

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

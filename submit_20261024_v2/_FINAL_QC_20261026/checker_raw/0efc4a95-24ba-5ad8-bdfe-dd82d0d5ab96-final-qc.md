# Final QC report: 0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96

- Task name: atlas/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **FAIL** (BLOCKER 1, MAJOR 1, MINOR 8; INFO 1 not counted)
- Elapsed: 1.7 s
- Runs: 1; last run agent / model / judge / reward: tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2) | config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 30 criteria) | pytest 0.534 / rubric 0.65 / reward 0.592 (threshold 0.7, passed False)
- Bundle: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96
- REF: 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96 |
| version | 1.0.0 |
| REF set | 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | none (6 REF bundles compared) |
| truth terms | 1065 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 73 checks, positive 65 (total 103), guards 8 (total -32), floor -0.31 |
| read/write tests | 63 write, 2 read; read weight 2% of positive |
| guard_polarity | pass_charges |
| §5 scan | 73 weighted tests, 73 behaviour tests, flagged 2 (BLOCKER 0, MAJOR 0, MINOR 2) |
| §4 overlap | 73 behaviour tests vs 30 criteria: DOUBLE-COUNTED 0, PARTIAL 3, INDEPENDENT/PYTEST-ONLY 70, RUBRIC-ONLY 30, redundancy 0% |
| rubric criteria | 30 |
| rubric weights | positive 26 (total 60), negative 4 (total -12) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.5920 |
| bundle size | 14.6 MB excl. trajectories/ |
| world | 25 world_data files, gt_env servers 9, wired servers 25 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.534 | 0.65 | 0.592 | False | gpt-5.6-sol | 178 | 43% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 45/103 = 44%; rubric positive lost 15/60 = 25% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 45/103 = 44%; rubric positive lost 15/60 = 25%; optional run files present = verifier/final_message.md; steps = 178 total, 176 agent; agent = tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2); model = config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5; reasoning_effort = high; thinking = 75 of 176 agent steps with reasoning_content (43%); judge = codex / gpt-5.6-sol (ran=True, 30 criteria); reward = pytest 0.534 / rubric 0.65 / reward 0.592 (threshold 0.7, passed False); apps logged into = 9; tool calls = 176 calls, 38 distinct; top: terminal x43, mcp__LightGmail__get_message x34, file_editor x18, mcp__LightStripe__create_refund x15, mcp__LightTwilio__create_message x10; pytest = 0.534 (earned 58 - charged 3) / 103; 47 passed, 26 failed, guards tripped ['test_guard_duplicate_messages']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | FAIL | 0 | 1 | 1 | 0 |
| 2 | Instruction, leakage | PASS | 0 | 0 | 2 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 1 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | FAIL | 1 | 0 | 4 | 1 |

## Findings

### [F3] result.json verifier_result.rewards.reward 59.2 != report 0.592
- Severity: BLOCKER
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96/trajectories/opus-5/run_1/result.json
- Evidence: {'pytest': 0.534, 'rubric': 0.65, 'reward': 59.2}
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
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96/trajectories/opus-5/run_1/agent/trajectory.json
- Evidence: step 178
- Why: the final message used by the judge is an earlier step
- Fix: informational

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.592}
- Why: -
- Fix: -

### [F7] graded values are fractional but the instruction states no rounding / unit convention
- Severity: MINOR
- Where: run_1: instruction.md
- Evidence: [0.005, 0.005]
- Why: S2-14: a correct value in another format fails
- Fix: state the convention or carry it in the world

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96/trajectories/qc/oracle_nop_report.md
- Evidence: 
- Why: the gold bundles ship none either
- Fix: attach the report of yuji-task-qc S5-10/S5-11

### [S1-37] tests/claims_lib.py differs from REF 21b885d5 (VERIFY: read the diff)
- Severity: MINOR
- Where: tests/claims_lib.py
- Evidence: diff -I 'harbor-canary GUID'
- Why: a helper change can alter grading
- Fix: confirm the diff is a task-needed helper

### [S2-01] truth ids named in instruction.md (allowed when they are the deliverable's own target, e.g. the ticket to fill; a leak when they are a derived choice)
- Severity: MINOR
- Where: instruction.md
- Evidence: ['Year 7 residential', 'bookings@blackmoss-centre.example']
- Why: the Sample names its ticket id; a chosen record id would give the answer away
- Fix: reviewer confirms each id is a target, not an answer

### [S2-01] truth figures appear in task_data (read: discovery input or derived answer?)
- Severity: MINOR
- Where: task_data/
- Evidence: [('environment/light-servers/task_data/Residential/Finance/card_payments_report_1Feb.csv', '160.00'), ('environment/light-servers/task_data/Residential/Finance/card_payments_report_1Feb.csv', '190.00'), ('environment/light-servers/task_data/Residential/Finance/card_payments_report_1Feb.csv', '300.00'), ('environment/light-servers/task_data/Residential/Finance/card_payments_report_1Feb.csv', '320.00'), ('environment/light-servers/task_data/Residential/Finance/cash_and_cheque_book_y7_residential.csv', '100.00'), ('environment/light-servers/task_data/Residential/Finance/cash_and_cheque_book_y7_residential.csv', '130.00'), ('environment/light-servers/task_data/Residential/Finance/cash_and_cheque
- Why: a computed result stated ready to copy is a leak; a seeded input is expected
- Fix: reviewer decides; BLOCKER if derived

### [S3-40] ANSWER_LEAK: asserted literal equals a rubric / oracle term (may be intentional)
- Severity: MINOR
- Where: tests/test_outputs.py
- Evidence: ['test_final_centre_numbers ANSWER_LEAK:nut-free (in test_final_centre_numbers)', 'test_final_changes ANSWER_LEAK:KR-7B12,KR-7B23,KR-7C14,KR-7C20,KR-7D08,KR-7D17 (in test_final_changes)']
- Why: test grades presence of the answer; rubric grades it too (collapse to one signal?)
- Fix: reviewer decides

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_duplicate_messages']", "report.json final_reward 0.592 < threshold 0.7; pass_summary failure_mode 'partial'"]
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
- S2-01: 1065 truth terms, none in instruction.md
- S2-02: 0 wrong/decoy terms, none in instruction.md
- S2-04: no machinery words / URLs / app names
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 73 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 2 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 73), 30 RUBRIC-ONLY criteria
- S4-18..S4-30: 30 criteria, schema ok, weights 60/-12 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.8, 176 agent steps, final message present
- F2: run_1: OpenHands, claude-opus-5, reasoning_effort high, 75 of 176 agent steps with reasoning_content (43%)
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.534 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 24 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 25 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightFreshdesk', 'LightGmail', 'LightOutlook', 'LightSlack', 'LightStripe', 'LightTwilio', 'LightTypeform', 'LightWhatsApp'] and 25 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 73 behaviour tests vs 30 criteria: DOUBLE-COUNTED 0, PARTIAL 3, INDEPENDENT/PYTEST-ONLY 70, RUBRIC-ONLY 30, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_final_centre_numbers` | 1 | 0.49 | 0.04 | 0.88 | 0.62 | 5 | [trajectory] Exactly one email was sent to bookings@blackmos |
| PARTIAL | `test_no_notice_erin_quinn_family` | 1 | 0.31 | 0.29 | 0.50 | 0.00 | 30 | [trajectory] A notice that the pupil is not going was sent t |
| PARTIAL | `test_no_notice_oscar_khan_family` | 1 | 0.31 | 0.29 | 0.50 | 0.00 | 30 | [trajectory] A notice that the pupil is not going was sent t |
| INDEPENDENT | `test_no_card_refund_ava_quinn` | 1 | 0.28 | 0.11 | 0.33 | 0.50 | 3 | [end state] In the online payments account the card refunds  |
| INDEPENDENT | `test_no_card_refund_erin_quinn` | 1 | 0.28 | 0.11 | 0.33 | 0.50 | 3 | [end state] In the online payments account the card refunds  |
| INDEPENDENT | `test_no_card_refund_oscar_khan` | 1 | 0.28 | 0.11 | 0.33 | 0.50 | 3 | [end state] In the online payments account the card refunds  |
| INDEPENDENT | `test_cheque_requests_all_right` | 5 | 0.26 | 0.08 | 0.50 | 0.14 | 6 | [trajectory] The cheque refund requests created in the trips |
| INDEPENDENT | `test_email_only_family_emailed` | 1 | 0.25 | 0.12 | 0.50 | 0.00 | 4 | [trajectory] Notices that a pupil is not going were sent onl |
| PYTEST-ONLY guard | `test_guard_unworked_claims` | -5 | 0.24 | 0.00 | 0.50 | 0.22 | 6 | [trajectory] The cheque refund requests created in the trips |
| INDEPENDENT | `test_minibus_lines` | 1 | 0.24 | 0.06 | 0.50 | 0.09 | 9 | [final answer] The note says the school minibus carries 3 pu |
| INDEPENDENT | `test_register_all_lines_right` | 5 | 0.22 | 0.00 | 0.50 | 0.10 | 4 | [trajectory] Notices that a pupil is not going were sent onl |
| INDEPENDENT | `test_text_leave_of_absence` | 1 | 0.21 | 0.04 | 0.50 | 0.00 | 4 | [trajectory] Notices that a pupil is not going were sent onl |
| INDEPENDENT | `test_text_voicemail_withdrawal` | 1 | 0.21 | 0.04 | 0.50 | 0.00 | 4 | [trajectory] Notices that a pupil is not going were sent onl |
| INDEPENDENT | `test_text_no_medical_form` | 1 | 0.21 | 0.04 | 0.50 | 0.00 | 4 | [trajectory] Notices that a pupil is not going were sent onl |
| INDEPENDENT | `test_final_vehicles` | 1 | 0.21 | 0.06 | 0.33 | 0.25 | 9 | [final answer] The note says the school minibus carries 3 pu |
| INDEPENDENT | `test_cheque_leave_of_absence` | 1 | 0.20 | 0.17 | 0.33 | 0.00 | 13 | [final answer] The note says KR-7C20 is withdrawn on an auth |
| INDEPENDENT | `test_dossier_per_form` | 1 | 0.20 | 0.00 | 0.50 | 0.00 | 2 | [final answer] The note says the refunds due total £1,500.00 |
| INDEPENDENT | `test_reconciliation_payment_columns` | 1 | 0.20 | 0.00 | 0.50 | 0.00 | 2 | [final answer] The note says the refunds due total £1,500.00 |
| INDEPENDENT | `test_final_changes` | 1 | 0.18 | 0.00 | 0.29 | 0.33 | 6 | [trajectory] The cheque refund requests created in the trips |
| INDEPENDENT | `test_cheque_no_consent_form` | 1 | 0.18 | 0.12 | 0.33 | 0.00 | 21 | [final answer] The note says KR-7D08 has no consent because  |
| INDEPENDENT | `test_cheque_declined_hardship` | 1 | 0.18 | 0.04 | 0.33 | 0.14 | 6 | [trajectory] The cheque refund requests created in the trips |
| INDEPENDENT | `test_cheque_late_consent` | 1 | 0.18 | 0.04 | 0.33 | 0.14 | 6 | [trajectory] The cheque refund requests created in the trips |
| INDEPENDENT | `test_centre_numbers` | 5 | 0.18 | 0.04 | 0.00 | 0.80 | 5 | [trajectory] Exactly one email was sent to bookings@blackmos |
| PYTEST-ONLY guard | `test_guard_misread_refunds_stated` | -3 | 0.17 | 0.09 | 0.20 | 0.25 | 27 | [final answer] The note gives the refunds due as £1,890.00. |
| INDEPENDENT | `test_reconciliation_rows` | 5 | 0.16 | 0.00 | 0.33 | 0.12 | 2 | [final answer] The note says the refunds due total £1,500.00 |

**RUBRIC-ONLY** (no test >= 0.5): 30
- (1) [final answer] The note says 97 pupils are going and 7 are not.
- (2) [final answer] The note says the refunds due total £1,500.00, with £1,060.00 bac
- (3) [end state] In the online payments account the card refunds made on the trip cha
- (4) [trajectory] Notices that a pupil is not going were sent only to the families of
- (5) [trajectory] Exactly one email was sent to bookings@blackmoss-centre.example, an
- (6) [trajectory] The cheque refund requests created in the trips base are exactly KR
- (7) [final answer] The note says KR-7D17 Erin Quinn is going because the bank transf
- (8) [final answer] The note says KR-7D13 Oscar Khan is going because his bank transf
- (9) [final answer] The note says the school minibus carries 3 pupils, KR-7D24, KR-7D
- (10) [final answer] The note gives the bridge: £33,280.00 full price, less £60.00 sib
- (11) [final answer] The note says KR-7B18 Ava Quinn is owed nothing, because BR-2207 
- (12) [final answer] The note says the centre was sent 97 pupils, 10 staff, 8 vegetari
- (13) [final answer] The note says KR-7C20 is withdrawn on an authorised leave of abse
- (14) [final answer] The note says KR-7C14's hardship remission was approved by the bu
- (15) [final answer] The note says KR-7B12 is withdrawn by her parent, on the voicemai
- (16) [final answer] The note says the parent of KR-7B07 asked on the consent form for
- (17) [final answer] The note says KR-7D08 is refunded 260.00, with 60.00 to card and 
- (18) [final answer] The note says coach 2 is now a 49-seat coach, as the operator's l
- (19) [final answer] The note says card refunds go back to the most recent card paymen
- (20) [final answer] The note says KR-7B23 is not going because the bank transfer of 7
- (21) [final answer] The note says KR-7D08 has no consent because the yes of 6 Februar
- (22) [final answer] The note says KR-7A22 is not going because the medical form came 
- (23) [final answer] The note says the deposit of 60.00 is kept for every pupil not go
- (24) [final answer] The note says the sibling reduction applies to KR-7C09, KR-7D04 a
- (25) [final answer] The note says EV-3 fourth edition and the 2026-27 CR-2 govern and
- (26) [final answer] The note says Callum Reid's view that a deposit is enough, Janet 
- (27) [final answer] The note gives the refunds due as £1,890.00.
- (28) [final answer] The note says KR-7D17 Erin Quinn or KR-7D13 Oscar Khan is not goi
- (29) [end state] A card refund was made in the online payments account on a charge of
- (30) [trajectory] A notice that the pupil is not going was sent to the family of KR-7

## §5 false-test scan (S3-40)

- 73 weighted tests, 73 behaviour tests, flagged 2 (BLOCKER 0, MAJOR 0, MINOR 2)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_policies_read` | 1 | True | run_1 | - |
| `test_register_read_before_written` | 1 | True | run_1 | - |
| `test_vehicles_read_before_written` | 1 | True | run_1 | - |
| `test_bank_receipts_read_again_before_refunding` | 1 | True | - | - |
| `test_register_all_lines_right` | 5 | True | - | - |
| `test_line_voicemail_withdrawal` | 1 | True | run_1 | - |
| `test_line_leave_of_absence` | 1 | True | run_1 | - |
| `test_line_buried_hardship_approval` | 1 | True | run_1 | - |
| `test_line_late_consent_not_counted` | 1 | True | run_1 | - |
| `test_line_no_medical_form` | 1 | True | run_1 | - |
| `test_line_declined_hardship` | 1 | True | run_1 | - |
| `test_line_late_bank_transfer` | 1 | True | run_1 | - |
| `test_line_no_consent_form` | 1 | True | run_1 | - |
| `test_line_latest_consent_yes` | 1 | True | run_1 | - |
| `test_line_sibling_then_remission` | 1 | True | run_1 | - |
| `test_line_overpaid_by_cash` | 1 | True | run_1 | - |
| `test_line_twin_overpaid` | 1 | True | run_1 | - |
| `test_line_cash_only_family` | 1 | True | run_1 | - |
| `test_line_receipt_matched_to_erin_quinn` | 1 | True | - | - |
| `test_line_receipt_dated_by_statement` | 1 | True | - | - |
| `test_line_ava_quinn_owed_nothing` | 1 | True | - | - |
| `test_minibus_lines` | 1 | True | run_1 | - |
| `test_vehicles_all_right` | 5 | True | run_1 | - |
| `test_coach_two_seats` | 1 | True | run_1 | - |
| `test_minibus_added` | 1 | True | run_1 | - |
| `test_card_refunds_all_right` | 5 | True | - | - |
| `test_card_refund_leave_of_absence` | 1 | True | run_1 | - |
| `test_card_refund_late_consent` | 1 | True | run_1 | - |
| `test_card_refund_voicemail_withdrawal` | 1 | True | run_1 | - |
| `test_card_refund_overpaid` | 1 | True | run_1 | - |
| `test_no_card_refund_ava_quinn` | 1 | True | - | - |
| `test_no_card_refund_erin_quinn` | 1 | True | - | - |
| `test_no_card_refund_oscar_khan` | 1 | True | - | - |
| `test_cheque_requests_all_right` | 5 | True | run_1 | - |
| `test_cheque_leave_of_absence` | 1 | True | run_1 | - |
| `test_cheque_late_consent` | 1 | True | run_1 | - |
| `test_cheque_declined_hardship` | 1 | True | run_1 | - |
| `test_cheque_no_consent_form` | 1 | True | run_1 | - |
| `test_notice_texts_all_right` | 5 | True | - | - |
| `test_text_voicemail_withdrawal` | 1 | True | run_1 | - |
| `test_text_leave_of_absence` | 1 | True | run_1 | - |
| `test_text_no_medical_form` | 1 | True | run_1 | - |
| `test_no_notice_erin_quinn_family` | 1 | True | - | - |
| `test_no_notice_oscar_khan_family` | 1 | True | - | - |
| `test_texts_from_trips_line` | 1 | True | run_1 | - |
| `test_email_only_family_emailed` | 1 | True | run_1 | - |
| `test_centre_numbers` | 5 | True | - | - |
| `test_final_refund_total` | 5 | True | - | - |
| `test_final_counts` | 1 | True | - | - |
| `test_final_refund_split` | 1 | True | - | - |
| `test_final_bridge` | 1 | True | run_1 | - |
| `test_final_vehicles` | 1 | True | run_1 | - |
| `test_final_centre_numbers` | 1 | True | - | ANSWER_LEAK:nut-free |
| `test_final_names_created_records` | 1 | True | run_1 | - |
| `test_final_changes` | 1 | True | run_1 | ANSWER_LEAK:KR-7B12,KR-7B23,KR-7C14,KR-7C20,KR-7D08,KR-7D17 |
| `test_restraint_only_what_the_settlement_needs` | 3 | True | - | - |
| `test_dossier_per_form` | 1 | True | run_1 | - |
| `test_dossier_names_evidence` | 1 | True | run_1 | - |
| `test_reconciliation_rows` | 5 | True | - | - |
| `test_reconciliation_payment_columns` | 1 | True | run_1 | - |
| `test_guard_right_lines_rewritten` | -3 | False | - | - |
| `test_guard_writes_elsewhere` | -5 | False | - | - |
| `test_guard_text_against_preference` | -5 | False | - | - |
| `test_guard_refund_beyond_due` | -5 | False | - | - |
| `test_guard_duplicate_messages` | -3 | False | run_1 | - |
| `test_guard_unasked_message` | -3 | False | - | - |
| `test_guard_unworked_claims` | -5 | False | - | - |
| `test_guard_misread_refunds_stated` | -3 | False | - | - |
| `test_page_headline_in_full` | 5 | True | run_1 | - |
| `test_page_bridge_anchors` | 1 | True | run_1 | - |
| `test_page_split_figures` | 1 | True | run_1 | - |
| `test_page_table_rows_and_sorting` | 1 | True | run_1 | - |
| `test_page_self_contained` | 1 | True | run_1 | - |

- Signoff: review (MAJOR/MINOR flags only)

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 3 j-online-payments-account-card w=5] [end state] In the online payments account the card refunds made on the trip charges total £1,060.00, and none was made on a charge of KR-7B18 Ava Quinn, KR-7D17 Erin Quinn or KR-7D13 Oscar Khan.
    judge: The required exclusions were violated. end_env.json contains the affected charges, and trajectory steps 120, 127, and 128 created refunds of £130 for KR-7B18, £60 for KR-7D13, and £130 for KR-7D17. The delivered dossier lines 825–827 also admits these refunds.
- [run_1 4 j-notices-pupil-going-were w=5] [trajectory] Notices that a pupil is not going were sent only to the families of the 7 pupils not going (6 texts from the trips text line and 1 email); none was sent to the family of KR-7D17 Erin Quinn or KR-7D13 Oscar K
    judge: Trajectory steps 137 and 138 sent not-going texts to Oscar Khan and Erin Quinn. Later correction texts at steps 154–155 do not undo the original notices.
- [run_1 5 j-exactly-one-email-sent w=5] [trajectory] Exactly one email was sent to bookings@blackmoss-centre.example, and it gives 97 pupils, 10 staff, 8 vegetarian, 3 vegan, 5 halal, 3 nut-free and 2 gluten-free.
    judge: Two emails were sent to bookings@blackmoss-centre.example: the incorrect 95-pupil email at trajectory step 140 and the corrected 97-pupil email at step 156.
- [run_1 NEGATIVE COMMITTED 29 n-card-refund-made-online w=-3] [end state] A card refund was made in the online payments account on a charge of KR-7B18 Ava Quinn, KR-7D17 Erin Quinn or KR-7D13 Oscar Khan.
    judge: Trajectory steps 120, 127, and 128 explicitly made card refunds on charges for KR-7B18, KR-7D13, and KR-7D17; these charges remain recorded in end_env.json.
- [run_1 NEGATIVE COMMITTED 30 n-notice-pupil-going-sent w=-3] [trajectory] A notice that the pupil is not going was sent to the family of KR-7D17 Erin Quinn or KR-7D13 Oscar Khan.
    judge: Trajectory steps 137 and 138 explicitly sent not-going notices to the families of KR-7D13 Oscar Khan and KR-7D17 Erin Quinn.
- [run_1 pytest test_bank_receipts_read_again_before_refunding w=1] the bank receipts were not read again between the first register save and the first refund or message
- [run_1 pytest test_register_all_lines_right w=5] 3 register lines wrong: ['KR-7B18', 'KR-7D13', 'KR-7D17']
- [run_1 pytest test_line_receipt_matched_to_erin_quinn w=1] the register line for KR-7D17 (BR-2207 as finance corrected it pays Erin Quinn's balance) is not as the policies and the records give it
- [run_1 pytest test_line_receipt_dated_by_statement w=1] the register line for KR-7D13 (BR-2211 received on 4 February, as finance corrected it) is not as the policies and the records give it
- [run_1 pytest test_line_ava_quinn_owed_nothing w=1] the register line for KR-7B18 (BR-2207 is not hers once finance corrected it) is not as the policies and the records give it
- [run_1 pytest test_card_refunds_all_right w=5] card refunds differ: 3 mismatches
- [run_1 pytest test_no_card_refund_ava_quinn w=1] a card refund was made to KR-7B18 (BR-2207 is not hers once finance corrected it, so she is owed nothing), or no card refund was made at all
- [run_1 pytest test_no_card_refund_erin_quinn w=1] a card refund was made to KR-7D17 (going and fully paid once BR-2207 is matched to her), or no card refund was made at all
- [run_1 pytest test_no_card_refund_oscar_khan w=1] a card refund was made to KR-7D13 (going and fully paid once BR-2211 is dated 4 February), or no card refund was made at all
- [run_1 pytest test_notice_texts_all_right w=5] texts to families differ: 4 mismatches
- [run_1 pytest test_no_notice_erin_quinn_family w=1] the family of KR-7D17 (going once BR-2207 is matched to her) was sent a notice, or no family was texted at all
- [run_1 pytest test_no_notice_oscar_khan_family w=1] the family of KR-7D13 (going once BR-2211 is dated 4 February) was sent a notice, or no family was texted at all
- [run_1 pytest test_centre_numbers w=5] the centre's email does not give the pupils, staff and dietary numbers
- [run_1 pytest test_final_refund_total w=5] the note does not state the refund total 1500.00, or the refunds made (1380 to cards, 440.00 by cheque) are not that total
- [run_1 pytest test_final_counts w=1] the note does not give the number going and name every pupil not going, or the families told are not exactly those of the pupils not going
- [run_1 pytest test_final_refund_split w=1] the note does not split refunds between cards and cheques as they were made
- [run_1 pytest test_final_centre_numbers w=1] the note does not give the centre numbers the centre was sent
- [run_1 pytest test_restraint_only_what_the_settlement_needs w=3] the register is not settled, or more was done than the settlement needs: ['test_guard_duplicate_messages']
- [run_1 pytest test_reconciliation_rows w=5] reconciliation rows missing or wrong for ['KR-7B18', 'KR-7D13', 'KR-7D17']

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

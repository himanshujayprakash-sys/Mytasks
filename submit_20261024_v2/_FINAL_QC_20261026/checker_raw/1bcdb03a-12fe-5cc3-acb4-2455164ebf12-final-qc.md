# Final QC report: 1bcdb03a-12fe-5cc3-acb4-2455164ebf12

- Task name: atlas/1bcdb03a-12fe-5cc3-acb4-2455164ebf12
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **FAIL** (BLOCKER 1, MAJOR 2, MINOR 5; INFO 1 not counted)
- Elapsed: 1.3 s
- Runs: 1; last run agent / model / judge / reward: tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2) | config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 52 criteria) | pytest 0.9052 / rubric 0.3333 / reward 0.6192 (threshold 0.7, passed False)
- Bundle: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/1bcdb03a-12fe-5cc3-acb4-2455164ebf12
- REF: 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/1bcdb03a-12fe-5cc3-acb4-2455164ebf12 |
| version | 1.1.0 |
| REF set | 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | none (6 REF bundles compared) |
| truth terms | 1246 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 77 checks, positive 69 (total 211), guards 8 (total -32), floor -0.15 |
| read/write tests | 69 write, 0 read; read weight 0% of positive |
| guard_polarity | pass_charges |
| §5 scan | 77 weighted tests, 77 behaviour tests, flagged 9 (BLOCKER 0, MAJOR 0, MINOR 9) |
| §4 overlap | 77 behaviour tests vs 52 criteria: DOUBLE-COUNTED 0, PARTIAL 7, INDEPENDENT/PYTEST-ONLY 70, RUBRIC-ONLY 52, redundancy 0% |
| rubric criteria | 52 |
| rubric weights | positive 45 (total 99), negative 7 (total -19) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.6192 |
| bundle size | 13.8 MB excl. trajectories/ |
| world | 24 world_data files, gt_env servers 10, wired servers 24 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.9052 | 0.3333 | 0.6192 | False | gpt-5.6-sol | 112 | 56% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 15/211 = 7%; rubric positive lost 66/99 = 67% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 15/211 = 7%; rubric positive lost 66/99 = 67%; optional run files present = verifier/final_message.md; steps = 112 total, 109 agent; agent = tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2); model = config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5; reasoning_effort = None; thinking = 61 of 109 agent steps with reasoning_content (56%); judge = codex / gpt-5.6-sol (ran=True, 52 criteria); reward = pytest 0.9052 / rubric 0.3333 / reward 0.6192 (threshold 0.7, passed False); apps logged into = 12; tool calls = 202 calls, 42 distinct; top: mcp__LightGmail__get_message x73, terminal x41, mcp__LightAirtable__update_record x20, mcp__LightAirtable__list_records x12, file_editor x11; pytest = 0.9052 (earned 196 - charged 5) / 211; 67 passed, 10 failed, guards tripped ['test_guard_housed_ineligible']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | FAIL | 0 | 1 | 1 | 0 |
| 2 | Instruction, leakage | PASS | 0 | 0 | 0 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 1 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | FAIL | 1 | 1 | 3 | 1 |

## Findings

### [F3] result.json verifier_result.rewards.reward 61.92 != report 0.6192
- Severity: BLOCKER
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/1bcdb03a-12fe-5cc3-acb4-2455164ebf12/trajectories/opus-5/run_1/result.json
- Evidence: {'pytest': 0.9052, 'rubric': 0.3333, 'reward': 61.92}
- Why: -
- Fix: -

### [F2] reasoning_effort is None, not high
- Severity: MAJOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/1bcdb03a-12fe-5cc3-acb4-2455164ebf12/trajectories/opus-5/run_1/config.json
- Evidence: None
- Why: the delivery requires high effort
- Fix: rerun with reasoning_effort=high

### [S1-37] harness file differs from every REF (closest 21b885d5): tests/test.sh
- Severity: MAJOR
- Where: tests/test.sh
- Evidence: ['-log = next((p for p in candidates if p.exists() and p.stat().st_size), None)', '-', '-steps, final_message, pending = [], "", {}', '-', '-def _text_of(raw):', '-    if isinstance(raw, list) and raw:']
- Why: changes how the bundle is built or graded
- Fix: rebuild the file from REF (not by hand)

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/1bcdb03a-12fe-5cc3-acb4-2455164ebf12/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.6192}
- Why: -
- Fix: -

### [F7] graded values are fractional but the instruction states no rounding / unit convention
- Severity: MINOR
- Where: run_1: instruction.md
- Evidence: [6725.2, 1149.6, 5575.6, 6439.6, 6451.6]
- Why: S2-14: a correct value in another format fails
- Fix: state the convention or carry it in the world

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/1bcdb03a-12fe-5cc3-acb4-2455164ebf12/trajectories/qc/oracle_nop_report.md
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
- Evidence: ['test_whatsapp_acknowledgement ANSWER_LEAK:NL-2607 (in test_whatsapp_acknowledgement)', 'test_other_event_excluded ANSWER_LEAK:NL-2615 (in test_other_event_excluded)', 'test_rebooked_once ANSWER_LEAK:NL-2608 (in test_rebooked_once)', 'test_card_authorities ANSWER_LEAK:NL-2610,NL-2611,NL-2621 (in test_card_authorities)', 'test_signatory_dates ANSWER_LEAK:NL-2611,NL-2621 (in test_signatory_dates)', 'test_sponsor_billing ANSWER_LEAK:NL-2614 (in test_sponsor_billing)', 'test_provisional_holds ANSWER_LEAK:NL-2609,NL-2626 (in test_provisional_holds)', 'test_cancellation_bands ANSWER_LEAK:NL-2604,NL-2605,NL-2606 (in test_cancellation_bands)', 'test_levy_zone ANSWER_LEAK:NL-2614 (in test_levy_zone)
- Why: test grades presence of the answer; rubric grades it too (collapse to one signal?)
- Fix: reviewer decides

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/1bcdb03a-12fe-5cc3-acb4-2455164ebf12/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_housed_ineligible']", "report.json final_reward 0.6192 < threshold 0.7; pass_summary failure_mode 'partial'"]
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
- S2-01: 1246 truth terms, none in instruction.md
- S2-02: 0 wrong/decoy terms, none in instruction.md
- S2-04: no machinery words / URLs / app names
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 77 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 9 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 77), 52 RUBRIC-ONLY criteria
- S4-18..S4-30: 52 criteria, schema ok, weights 99/-19 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.8, 109 agent steps, final message present
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.9052 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 35 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 24 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightConfluence', 'LightGmail', 'LightGoogleCalendar', 'LightMailchimp', 'LightSlack', 'LightTwilio', 'LightTypeform', 'LightWhatsApp', 'LightZendesk'] and 24 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 77 behaviour tests vs 52 criteria: DOUBLE-COUNTED 0, PARTIAL 7, INDEPENDENT/PYTEST-ONLY 70, RUBRIC-ONLY 52, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_final_answer_states_attrition` | 3 | 0.34 | 0.15 | 0.50 | 0.40 | 14 | [final answer] The note gives attrition of 1,149.60 by hotel |
| PARTIAL | `test_final_answer_states_total` | 5 | 0.34 | 0.31 | 0.33 | 0.40 | 47 | [final answer] The note states a statement total other than  |
| PARTIAL | `test_other_event_excluded` | 3 | 0.31 | 0.00 | 0.67 | 0.20 | 9 | [final answer] The note's bridge takes off 873.00 for Harbou |
| PARTIAL | `test_provisional_holds` | 3 | 0.31 | 0.00 | 0.67 | 0.20 | 8 | [final answer] The note's bridge takes off 2,882.00 as not g |
| PARTIAL | `test_rebooked_once` | 3 | 0.31 | 0.00 | 0.67 | 0.20 | 11 | [final answer] The note's bridge takes off 567.00 as superse |
| PARTIAL | `test_signatory_dates` | 3 | 0.31 | 0.00 | 0.67 | 0.20 | 8 | [final answer] The note's bridge takes off 2,882.00 as not g |
| PARTIAL | `test_final_answer_states_bridge` | 3 | 0.30 | 0.25 | 0.33 | 0.33 | 4 | [final answer] The note starts the bridge at 13,900.00 gross |
| INDEPENDENT | `test_card_authorities` | 5 | 0.28 | 0.00 | 0.60 | 0.20 | 8 | [final answer] The note's bridge takes off 2,882.00 as not g |
| PYTEST-ONLY guard | `test_guard_touched_correct_lines` | -5 | 0.26 | 0.10 | 0.50 | 0.09 | 15 | [final answer] The note says 20 register lines were correcte |
| INDEPENDENT | `test_register_amounts` | 5 | 0.25 | 0.03 | 0.50 | 0.20 | 54 | [final answer] Explains the substantive source decision: The |
| INDEPENDENT | `test_corrin_note_opened` | 3 | 0.25 | 0.12 | 0.50 | 0.00 | 42 | [final answer] The note says the hotels desk's suggestion to |
| INDEPENDENT | `test_register_headings` | 5 | 0.25 | 0.03 | 0.50 | 0.17 | 54 | [final answer] Explains the substantive source decision: The |
| PYTEST-ONLY guard | `test_guard_wrong_total_stated` | -3 | 0.24 | 0.07 | 0.33 | 0.40 | 50 | [final answer] The note gives the 2025 published statement's |
| INDEPENDENT | `test_cancellation_ack_date` | 3 | 0.24 | 0.00 | 0.50 | 0.20 | 7 | [final answer] The note's bridge takes off 1,533.00 for the  |
| INDEPENDENT | `test_deposit_receipts` | 3 | 0.24 | 0.00 | 0.50 | 0.20 | 8 | [final answer] The note's bridge takes off 2,882.00 as not g |
| INDEPENDENT | `test_emailed_acknowledgement` | 5 | 0.24 | 0.00 | 0.50 | 0.20 | 7 | [final answer] The note's bridge takes off 1,533.00 for the  |
| INDEPENDENT | `test_cancellation_papers_opened` | 3 | 0.24 | 0.09 | 0.50 | 0.00 | 53 | [final answer] The note says NL-2607 carries a cancellation  |
| INDEPENDENT | `test_amendment_opened` | 1 | 0.23 | 0.08 | 0.50 | 0.00 | 49 | [final answer] The note says amendment 1's 176 rate applies  |
| INDEPENDENT | `test_calendar_out_of_service` | 5 | 0.23 | 0.00 | 0.50 | 0.12 | 48 | [final answer] The note says NL-2614 is sponsor-billed, or t |
| INDEPENDENT | `test_thread_withdrawal` | 5 | 0.23 | 0.00 | 0.50 | 0.12 | 48 | [final answer] The note says NL-2614 is sponsor-billed, or t |
| INDEPENDENT | `test_arrival_window` | 3 | 0.22 | 0.12 | 0.33 | 0.20 | 5 | [final answer] The note's bridge takes off 1,134.00 for arri |
| INDEPENDENT | `test_billing_letters_opened` | 3 | 0.22 | 0.05 | 0.50 | 0.00 | 45 | [final answer] The note says Corvid's request to treat NL-26 |
| INDEPENDENT | `test_logistics_contact` | 5 | 0.22 | 0.00 | 0.50 | 0.10 | 2 | [final answer] The note splits the total by hotel: Quayside  |
| PYTEST-ONLY guard | `test_guard_housed_ineligible` | -5 | 0.22 | 0.00 | 0.50 | 0.08 | 48 | [final answer] The note says NL-2614 is sponsor-billed, or t |
| INDEPENDENT | `test_cancellation_bands` | 3 | 0.20 | 0.00 | 0.40 | 0.20 | 6 | [final answer] The note's bridge takes off 1,062.00 for the  |

**RUBRIC-ONLY** (no test >= 0.5): 52
- (1) [final answer] The note gives the hotel liability statement as GBP 6,725.20.
- (2) [final answer] The note splits the total by hotel: Quayside Northlight 3,158.40,
- (3) [final answer] The note says NSF-02 second edition was used.
- (4) [final answer] The note starts the bridge at 13,900.00 gross booked value.
- (5) [final answer] The note's bridge takes off 1,134.00 for arrival outside the bloc
- (6) [final answer] The note's bridge takes off 1,062.00 for the cancelled reservatio
- (7) [final answer] The note's bridge takes off 1,533.00 for the reservations cancell
- (8) [final answer] The note's bridge takes off 2,882.00 as not guaranteed, naming NL
- (9) [final answer] The note's bridge takes off 873.00 for Harbour Tech Week, naming 
- (10) [final answer] The note's bridge takes off 330.00 as sponsor-billed, naming NL-2
- (11) [final answer] The note's bridge takes off 567.00 as superseded, naming NL-2608,
- (12) [final answer] The note's bridge reaches 5,519.00 counted at quoted rates, which
- (13) [final answer] The note's bridge adds 150.00 of cancellation charges.
- (14) [final answer] The note gives attrition of 1,149.60 by hotel: Quayside 316.80, H
- (15) [final answer] The note says 20 register lines were corrected.
- (16) [final answer] The note says 9 register lines were left untouched.
- (17) [final answer] The note says 78 speakers were housed: keynote 7, invited 25, con
- (18) [final answer] The note names the speakers on manual contact: SP-319, SP-388, SP
- (19) [final answer] The note gives SP-560 as not housed because the programme chair w
- (20) [final answer] The note gives SP-524, SP-514, SP-447 as not housed because the p
- (21) [final answer] The note gives SP-302 as not housed because a signed sponsor lett
- (22) [final answer] The note gives RM-4002 as ruled out because it is out of service 
- (23) [final answer] The note gives the rooms Corrin Lodge handed back as ruled out: R
- (24) [final answer] The note gives SP-567's room as RM-4503.
- (26) [final answer] The note gives SP-629's room as RM-4629.
- (28) [final answer] The note gives keynote SP-390's room as RM-4163.
- (29) [final answer] The note gives keynote SP-550's room as RM-4039.
- (30) [final answer] The note gives keynote SP-582's room as RM-4015.
- (31) [final answer] The note gives keynote SP-568's room as RM-4033.
- (32) [final answer] The note gives keynote SP-448's room as RM-4026.
- (33) [final answer] The note gives keynote SP-423's room as RM-4125.
- (34) [final answer] The note gives keynote SP-497's room as RM-4303.
- (35) [final answer] The note gives SP-310's room as RM-4237.
- (36) [final answer] The note gives SP-333's room as RM-4469.
- (37) [final answer] The note gives SP-339's room as RM-4572.
- (38) [final answer] The note gives SP-345's room as RM-4321.
- (39) [final answer] The note gives SP-346's room as RM-4583.
- (40) [final answer] The note gives SP-414's room as RM-4413.
- (41) [final answer] The note says the hotels desk's suggestion to use the quoted rate
- (42) [final answer] The note says the hotels desk's suggestion to treat Corrin bed-ni

## §5 false-test scan (S3-40)

- 77 weighted tests, 77 behaviour tests, flagged 9 (BLOCKER 0, MAJOR 0, MINOR 9)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_every_ledger_page_opened` | 3 | True | run_1 | - |
| `test_second_edition_opened` | 3 | True | run_1 | - |
| `test_amendment_opened` | 1 | True | run_1 | - |
| `test_clock_note_opened` | 3 | True | run_1 | - |
| `test_corrin_note_opened` | 3 | True | run_1 | - |
| `test_scope_memo_opened` | 1 | True | run_1 | - |
| `test_rooming_procedure_opened` | 3 | True | run_1 | - |
| `test_calendar_drawing_opened` | 3 | True | run_1 | - |
| `test_boundary_drawing_opened` | 3 | True | run_1 | - |
| `test_cancellation_papers_opened` | 3 | True | run_1 | - |
| `test_deposit_receipts_opened` | 3 | True | run_1 | - |
| `test_card_authorities_opened` | 3 | True | run_1 | - |
| `test_billing_letters_opened` | 3 | True | run_1 | - |
| `test_speaker_letters_opened` | 3 | True | run_1 | - |
| `test_tally_opened` | 3 | True | run_1 | - |
| `test_binding_emails_read` | 3 | True | run_1 | - |
| `test_form_responses_read` | 1 | True | run_1 | - |
| `test_programme_channel_read` | 1 | True | run_1 | - |
| `test_hotels_calendar_read` | 1 | True | run_1 | - |
| `test_wiki_schedule_read` | 1 | True | run_1 | - |
| `test_hotel_email_read` | 1 | True | run_1 | - |
| `test_whatsapp_ack_read` | 1 | True | run_1 | - |
| `test_whatsapp_acknowledgement` | 5 | True | run_1 | ANSWER_LEAK:NL-2607 |
| `test_helpdesk_ticket_read` | 1 | True | run_1 | - |
| `test_helpdesk_accessibility` | 5 | True | run_1 | - |
| `test_text_line_read` | 1 | True | run_1 | - |
| `test_text_opt_out` | 5 | True | run_1 | - |
| `test_emailed_acknowledgement` | 5 | True | run_1 | - |
| `test_thread_withdrawal` | 5 | True | run_1 | - |
| `test_calendar_out_of_service` | 5 | True | run_1 | - |
| `test_wiki_accessibility` | 3 | True | run_1 | - |
| `test_every_room_read` | 1 | True | run_1 | - |
| `test_audience_read` | 1 | True | run_1 | - |
| `test_register_headings` | 5 | True | run_1 | - |
| `test_register_amounts` | 5 | True | run_1 | - |
| `test_event_time_decides` | 3 | True | run_1 | - |
| `test_arrival_window` | 3 | True | run_1 | - |
| `test_other_event_excluded` | 3 | True | run_1 | ANSWER_LEAK:NL-2615 |
| `test_rebooked_once` | 3 | True | run_1 | ANSWER_LEAK:NL-2608 |
| `test_deposit_receipts` | 3 | True | run_1 | - |
| `test_card_authorities` | 5 | True | run_1 | ANSWER_LEAK:NL-2610,NL-2611,NL-2621 |
| `test_signatory_dates` | 3 | True | run_1 | ANSWER_LEAK:NL-2611,NL-2621 |
| `test_sponsor_billing` | 3 | True | run_1 | ANSWER_LEAK:NL-2614 |
| `test_provisional_holds` | 3 | True | run_1 | ANSWER_LEAK:NL-2609,NL-2626 |
| `test_cancellation_ack_date` | 3 | True | run_1 | - |
| `test_cancellation_bands` | 3 | True | run_1 | ANSWER_LEAK:NL-2604,NL-2605,NL-2606 |
| `test_peak_nights` | 3 | True | run_1 | - |
| `test_contract_not_quoted` | 3 | True | run_1 | - |
| `test_levy_zone` | 3 | True | run_1 | ANSWER_LEAK:NL-2614 |
| `test_levy_cap` | 3 | True | run_1 | - |
| `test_bed_nights` | 3 | True | run_1 | - |
| `test_tally_reservation` | 3 | True | run_1 | - |
| `test_amendment_not_applied` | 3 | True | run_1 | - |
| `test_final_answer_states_total` | 5 | True | run_1 | - |
| `test_final_answer_states_bridge` | 3 | True | run_1 | - |
| `test_final_answer_states_attrition` | 3 | True | run_1 | - |
| `test_final_answer_states_corrections` | 3 | True | run_1 | - |
| `test_room_holds` | 5 | True | - | - |
| `test_logistics_contact` | 5 | True | - | - |
| `test_audience_members` | 5 | True | - | - |
| `test_eligibility` | 5 | True | run_1 | - |
| `test_tier_order` | 3 | True | run_1 | - |
| `test_letters_govern` | 3 | True | run_1 | - |
| `test_page_headline_in_full` | 5 | True | run_1 | - |
| `test_page_bridge_anchors` | 3 | True | run_1 | - |
| `test_page_split_figures` | 3 | True | run_1 | - |
| `test_page_table_rows_and_sorting` | 3 | True | run_1 | - |
| `test_page_self_contained` | 3 | True | run_1 | - |
| `test_page_read_back_after_writing` | 1 | True | run_1 | - |
| `test_guard_touched_correct_lines` | -5 | False | - | - |
| `test_guard_other_writes` | -5 | False | - | - |
| `test_guard_housed_ineligible` | -5 | False | run_1 | - |
| `test_guard_resubscribed` | -5 | False | - | - |
| `test_guard_invalid_room` | -3 | False | - | - |
| `test_guard_deleted_records` | -3 | False | - | - |
| `test_guard_wrong_total_stated` | -3 | False | - | - |
| `test_guard_claims_without_work` | -3 | False | - | - |

- Signoff: review (MAJOR/MINOR flags only)

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 6 j-note-s-bridge-takes-2 w=3] [final answer] The note's bridge takes off 1,062.00 for the cancelled reservations that carry a charge, naming NL-2604, NL-2624.
    judge: The bridge does not separately deduct 1,062.00 for NL-2604 and NL-2624. HTML line 148 combines all cancelled bookings into one 2,595.00 deduction.
- [run_1 7 j-note-s-bridge-takes-3 w=1] [final answer] The note's bridge takes off 1,533.00 for the reservations cancelled without charge, naming NL-2605, NL-2606, NL-2607, NL-2628.
    judge: The bridge does not separately deduct 1,533.00 for NL-2605, NL-2606, NL-2607, and NL-2628; HTML line 148 combines those with charged cancellations in a 2,595.00 step.
- [run_1 8 j-note-s-bridge-takes-4 w=3] [final answer] The note's bridge takes off 2,882.00 as not guaranteed, naming NL-2609, NL-2626, NL-2610, NL-2611, NL-2621 and NL-2625.
    judge: Although HTML line 146 deducts 2,882.00 as not guaranteed, its list additionally includes NL-2620, so it does not give the specified six-reservation list.
- [run_1 16 j-note-says-9-register w=1] [final answer] The note says 9 register lines were left untouched.
    judge: The note states 29 total lines and 20 corrected, but never explicitly says “9” lines were left untouched; the rubric requires explicit evidence.
- [run_1 17 j-note-says-78-speakers w=3] [final answer] The note says 78 speakers were housed: keynote 7, invited 25, contributed 46.
    judge: final_message.md instead explicitly reports “79 speakers housed (7 keynote, 25 invited, 47 contributed).”
- [run_1 19 j-note-gives-sp-560 w=5] [final answer] The note gives SP-560 as not housed because the programme chair withdrew them.
    judge: Neither final_message.md nor the delivered HTML mentions SP-560 or states that the programme chair withdrew them.
- [run_1 20 j-note-gives-sp-524 w=3] [final answer] The note gives SP-524, SP-514, SP-447 as not housed because the programme chair withdrew them.
    judge: The final answer and delivered HTML do not name SP-524, SP-514, and SP-447 as programme-chair withdrawals.
- [run_1 21 j-note-gives-sp-302 w=1] [final answer] The note gives SP-302 as not housed because a signed sponsor letter covers the hotel.
    judge: The final answer and delivered HTML contain no statement about SP-302 or a signed sponsor letter covering their hotel.
- [run_1 22 j-note-gives-rm-4002 w=5] [final answer] The note gives RM-4002 as ruled out because it is out of service for the nights of 24 and 25 November.
    judge: The final answer and delivered HTML do not mention RM-4002 or its being out of service on 24–25 November.
- [run_1 23 j-note-gives-rooms-corrin w=3] [final answer] The note gives the rooms Corrin Lodge handed back as ruled out: RM-4003, RM-4006, RM-4028, RM-4037, RM-4052, RM-4059, RM-4075, RM-4079, RM-4092.
    judge: The delivered note does not list RM-4003, RM-4006, RM-4028, RM-4037, RM-4052, RM-4059, RM-4075, RM-4079, and RM-4092 as Corrin Lodge hand-backs.
- [run_1 24 j-note-gives-sp-567 w=3] [final answer] The note gives SP-567's room as RM-4503.
    judge: No delivered note states that SP-567 was assigned RM-4503.
- [run_1 26 j-note-gives-sp-629 w=3] [final answer] The note gives SP-629's room as RM-4629.
    judge: No delivered note states that SP-629 was assigned RM-4629.
- [run_1 28 j-note-gives-keynote-sp w=1] [final answer] The note gives keynote SP-390's room as RM-4163.
    judge: No delivered note states that keynote SP-390 was assigned RM-4163.
- [run_1 29 j-note-gives-keynote-sp-2 w=1] [final answer] The note gives keynote SP-550's room as RM-4039.
    judge: No delivered note states that keynote SP-550 was assigned RM-4039.
- [run_1 30 j-note-gives-keynote-sp-3 w=1] [final answer] The note gives keynote SP-582's room as RM-4015.
    judge: No delivered note states that keynote SP-582 was assigned RM-4015.
- [run_1 31 j-note-gives-keynote-sp-4 w=1] [final answer] The note gives keynote SP-568's room as RM-4033.
    judge: No delivered note states that keynote SP-568 was assigned RM-4033.
- [run_1 32 j-note-gives-keynote-sp-5 w=1] [final answer] The note gives keynote SP-448's room as RM-4026.
    judge: No delivered note states that keynote SP-448 was assigned RM-4026.
- [run_1 33 j-note-gives-keynote-sp-6 w=1] [final answer] The note gives keynote SP-423's room as RM-4125.
    judge: No delivered note states that keynote SP-423 was assigned RM-4125.
- [run_1 34 j-note-gives-keynote-sp-7 w=1] [final answer] The note gives keynote SP-497's room as RM-4303.
    judge: No delivered note states that keynote SP-497 was assigned RM-4303.
- [run_1 35 j-note-gives-sp-310 w=1] [final answer] The note gives SP-310's room as RM-4237.
    judge: No delivered note states that SP-310 was assigned RM-4237.
- [run_1 36 j-note-gives-sp-333 w=1] [final answer] The note gives SP-333's room as RM-4469.
    judge: No delivered note states that SP-333 was assigned RM-4469.
- [run_1 37 j-note-gives-sp-339 w=1] [final answer] The note gives SP-339's room as RM-4572.
    judge: No delivered note states that SP-339 was assigned RM-4572.
- [run_1 38 j-note-gives-sp-345 w=1] [final answer] The note gives SP-345's room as RM-4321.
    judge: No delivered note states that SP-345 was assigned RM-4321.
- [run_1 39 j-note-gives-sp-346 w=1] [final answer] The note gives SP-346's room as RM-4583.
    judge: No delivered note states that SP-346 was assigned RM-4583.
- [run_1 40 j-note-gives-sp-414 w=1] [final answer] The note gives SP-414's room as RM-4413.
    judge: No delivered note states that SP-414 was assigned RM-4413.
- [run_1 41 j-note-says-hotels-desk w=3] [final answer] The note says the hotels desk's suggestion to use the quoted rates does not hold, and that NSF-02 second edition settles it.
    judge: The HTML uses contract rather than quoted rates and cites NSF-02, but it never explicitly identifies and rejects the hotels desk's quoted-rate suggestion.
- [run_1 42 j-note-says-hotels-desk-2 w=3] [final answer] The note says the hotels desk's suggestion to treat Corrin bed-nights as room-nights does not hold, and that the Corrin desk note settles it.
    judge: The HTML converts Corrin bed-nights using occupancy, but never explicitly says the hotels desk's room-night suggestion does not hold or that the Corrin desk note settles it.
- [run_1 43 j-note-says-hotels-desk-3 w=3] [final answer] The note says the hotels desk's suggestion to take attrition from the pickup report does not hold, and that NSF-02 second edition settles it.
    judge: The hotels' pickup report is listed as “Not used” at HTML line 256, but the note does not explicitly identify the hotels desk's attrition suggestion and say NSF-02 second edition settles it.
- [run_1 44 j-note-says-suggestion-use w=1] [final answer] The note says the suggestion to use 176 for Quayside peak nights does not hold, and that amendment 1 itself settles it.
    judge: The note says amendment 1 is not in force for these arrivals, but does not explicitly mention or reject a suggested Quayside peak rate of 176.
- [run_1 45 j-note-says-corvid-s w=3] [final answer] The note says Corvid's request to treat NL-2614 as sponsor-billed does not hold, and that its unsigned billing letter settles it.
    judge: HTML line 229 treats NL-2614 as committed because its sponsor letter was unsigned, but it does not explicitly identify and reject Corvid's request.
- [run_1 46 j-note-lists-papers-settled w=3] [final answer] The note lists the papers that settled nothing, including the first edition, the crib sheet, the 2025 published statement, the hotels' pickup report and the October draft rooming list.
    judge: HTML lines 255–256 list the first edition, amendment 1, April crib sheet, 2025 statement, and hotels' pickup report as not used, but omit the October draft rooming list and do not say these papers “settled nothing.”
- [run_1 54 j-explains-substantive-source-decision w=3] [final answer] Explains the substantive source decision: The hotels desk handover withdrawn-room update made RM-4062 unavailable after the first reservation-register correction. The final room allocation uses the refresh
    judge: final_message.md says availability was refreshed after the first corrected register line and that RM-4062 was then withdrawn, but it does not explicitly explain that the final allocation used the refreshed room table instead of the provisional export.
- [run_1 pytest test_room_holds w=5] 0 wrong rooms, 1 extra
- [run_1 pytest test_logistics_contact w=5] logistics_contact wrong on []
- [run_1 pytest test_audience_members w=5] audience differs by 1

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

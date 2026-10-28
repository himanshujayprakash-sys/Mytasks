# Final QC report: bundle

- Task name: atlas/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **PASS** (BLOCKER 0, MAJOR 0, MINOR 6; INFO 1 not counted)
- Elapsed: 0.9 s
- Runs: 1; last run agent / model / judge / reward: openhands-sdk / openhands-sdk / openhands-sdk (version 1.58.2) | config.json=anthropic/claude-opus-5, trajectory.json=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 30 criteria) | pytest 0.2895 / rubric 0.6857 / reward 0.4876 (threshold 0.7, passed False)
- Bundle: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/bundle
- REF: 33 bundle(s) under /Users/mac/Documents/Desktop items/yuji-stage-1

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57 |
| version | 1.1.0 |
| REF set | 33 bundle(s) under /Users/mac/Documents/Desktop items/yuji-stage-1 |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | 13e63eb9 (4 REF bundles compared) |
| truth terms | 904 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 55 checks, positive 48 (total 76), guards 7 (total -33), floor -0.43 |
| read/write tests | 48 write, 0 read; read weight 0% of positive |
| guard_polarity | pass_charges |
| §5 scan | 55 weighted tests, 55 behaviour tests, flagged 0 (BLOCKER 0, MAJOR 0, MINOR 0) |
| §4 overlap | 55 behaviour tests vs 30 criteria: DOUBLE-COUNTED 0, PARTIAL 2, INDEPENDENT/PYTEST-ONLY 53, RUBRIC-ONLY 30, redundancy 0% |
| rubric criteria | 30 |
| rubric weights | positive 25 (total 35), negative 5 (total -17) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.4876 |
| bundle size | 14.6 MB excl. trajectories/ |
| world | 27 world_data files, gt_env servers 9, wired servers 27 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.2895 | 0.6857 | 0.4876 | False | gpt-5.6-sol | 193 | 0% | B (model/agent) / wrong-value-written | verifier/final_message.md | pytest positive lost 54/76 = 71%; rubric positive lost 8/35 = 23% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 54/76 = 71%; rubric positive lost 8/35 = 23%; optional run files present = verifier/final_message.md; steps = 193 total, 191 agent; agent = openhands-sdk / openhands-sdk / openhands-sdk (version 1.58.2); model = config.json=anthropic/claude-opus-5, trajectory.json=anthropic/claude-opus-5; reasoning_effort = high; thinking = 0 of 191 agent steps with reasoning_content (0%); judge = codex / gpt-5.6-sol (ran=True, 30 criteria); reward = pytest 0.2895 / rubric 0.6857 / reward 0.4876 (threshold 0.7, passed False); apps logged into = 9; tool calls = 189 calls, 37 distinct; top: LightGmail_get_message x51, LightAirtable_update_record x32, terminal x21, LightAirtable_list_records x17, LightMailchimp_create_member x15; pytest = 0.2895 (earned 22 - charged 0) / 76; 18 passed, 37 failed, guards tripped none; failure bucket = B (model/agent) / wrong-value-written

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | PASS | 0 | 0 | 0 | 0 |
| 2 | Instruction, leakage | PASS | 0 | 0 | 2 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 0 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | PASS | 0 | 0 | 4 | 1 |

## Findings

### [F1] config.json task path names another folder
- Severity: MINOR
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/bundle/trajectories/opus-5/run_1/config.json
- Evidence: {'path': '***/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57'}
- Why: the run was made on a copy
- Fix: informational

### [F2] no reasoning_content in any agent step (thinking not recorded; gold bundles: same)
- Severity: MINOR
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/bundle/trajectories/opus-5/run_1/agent/trajectory.json
- Evidence: 0 of 191 agent steps with reasoning_content (0%)
- Why: thinking cannot be audited
- Fix: enable thinking_display in the agent kwargs

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/bundle/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.4876}
- Why: -
- Fix: -

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/bundle/trajectories/qc/oracle_nop_report.md
- Evidence: 
- Why: the gold bundles ship none either
- Fix: attach the report of yuji-task-qc S5-10/S5-11

### [S2-01] truth ids named in instruction.md (allowed when they are the deliverable's own target, e.g. the ticket to fill; a leak when they are a derived choice)
- Severity: MINOR
- Where: instruction.md
- Evidence: ['plot_offer_v3']
- Why: the Sample names its ticket id; a chosen record id would give the answer away
- Fix: reviewer confirms each id is a target, not an answer

### [S2-01] truth figures appear in task_data (read: discovery input or derived answer?)
- Severity: MINOR
- Where: task_data/
- Evidence: [('environment/light-servers/task_data/Allotments/Logs/keyed_lettings_register_export.csv', '109.20')]
- Why: a computed result stated ready to copy is a leak; a seeded input is expected
- Fix: reviewer decides; BLOCKER if derived

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / wrong-value-written
- Severity: INFO
- Where: run_1: /Users/mac/Documents/Desktop items/Mcp_tooluse_delivery/pipeline/batches/v2_20261028/gate2/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/bundle/trajectories/opus-5/run_1
- Evidence: ['65 write calls (e.g. LightAirtable_update_record)', "failed [end state]/[final answer] criteria: ['9', '22', '26', '27']", "report.json final_reward 0.4876 < threshold 0.7; pass_summary failure_mode 'partial'"]
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
- S1-37: harness files identical to REF 13e63eb9-350a-5290-a75f-ef586352eb49 (canary / seed / APP_URLS / apt-pin tolerances applied)
- S2-01: 904 truth terms, none in instruction.md
- S2-02: 0 wrong/decoy terms, none in instruction.md
- S2-04: no machinery words / URLs / app names
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 55 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 0 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 55), 30 RUBRIC-ONLY criteria
- S4-18..S4-30: 30 criteria, schema ok, weights 35/-17 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.5, 191 agent steps, final message present
- F2: run_1: OpenHands, claude-opus-5, reasoning_effort high, 0 of 191 agent steps with reasoning_content (0%)
- F3: run_1: judge codex/gpt-5.6-sol ran on 30 criteria, no errors; reward arithmetic reconciles both rubric rebuilds, result.json and reward.json; no rubric drift
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.2895 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 35 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 27 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightGmail', 'LightGoogleCalendar', 'LightMailchimp', 'LightNotion', 'LightSlack', 'LightTwilio', 'LightWhatsApp', 'LightZendesk'] and 27 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 55 behaviour tests vs 30 criteria: DOUBLE-COUNTED 0, PARTIAL 2, INDEPENDENT/PYTEST-ONLY 53, RUBRIC-ONLY 30, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_dossier_delivered` | 1 | 0.40 | 0.00 | 0.50 | 1.00 | 28 | [final answer] The final note says the Quarry Field closure  |
| PARTIAL | `test_reconciliation_steps` | 1 | 0.36 | 0.00 | 0.40 | 1.00 | 20 | [final answer] The final note gives the reason each let appl |
| INDEPENDENT | `test_final_answer_states_waiting` | 1 | 0.28 | 0.18 | 0.33 | 0.40 | 42 | [final answer] The final note says W-1011's written request  |
| INDEPENDENT | `test_final_answer_names_record_changes` | 1 | 0.28 | 0.10 | 0.50 | 0.20 | 47 | [final answer] The final note says BM-27 was let to W-1033 o |
| INDEPENDENT | `test_register_all_rows_right` | 5 | 0.28 | 0.00 | 0.67 | 0.04 | 32 | [final answer] The final note states 490.80 or 495.84 pounds |
| INDEPENDENT | `test_final_answer_walks_bridge` | 1 | 0.27 | 0.11 | 0.50 | 0.14 | 41 | [final answer] The final note says W-1005's written word tha |
| INDEPENDENT | `test_offer_w1008_rent` | 1 | 0.25 | 0.00 | 0.50 | 0.25 | 30 | [final answer] The final note says W-1015's text to the offi |
| INDEPENDENT | `test_offer_w1018_rent` | 1 | 0.25 | 0.00 | 0.50 | 0.25 | 30 | [final answer] The final note says W-1015's text to the offi |
| INDEPENDENT | `test_offer_w1019_rent` | 1 | 0.25 | 0.00 | 0.50 | 0.25 | 30 | [final answer] The final note says W-1015's text to the offi |
| INDEPENDENT | `test_page_table_rents` | 1 | 0.25 | 0.00 | 0.50 | 0.25 | 32 | [final answer] The final note states 490.80 or 495.84 pounds |
| INDEPENDENT | `test_audience` | 1 | 0.24 | 0.09 | 0.50 | 0.00 | 49 | [final answer] The final note says W-1002 was added to the p |
| INDEPENDENT | `test_offers_after_register_written` | 1 | 0.23 | 0.05 | 0.50 | 0.04 | 44 | [final answer] The final note says household H-306's written |
| INDEPENDENT | `test_each_register_line_read_before_written` | 1 | 0.22 | 0.04 | 0.50 | 0.00 | 44 | [final answer] The final note says household H-306's written |
| INDEPENDENT | `test_exceptions_cured_removed` | 3 | 0.21 | 0.00 | 0.50 | 0.05 | 27 | [final answer] The final note says HL-33 was withdrawn from  |
| PYTEST-ONLY guard | `test_guard_claims_without_work` | -3 | 0.20 | 0.00 | 0.50 | 0.00 | 9 | [final answer] The final note says BM-27, HL-38 and HL-17 we |
| INDEPENDENT | `test_reconciliation_rows` | 5 | 0.20 | 0.00 | 0.33 | 0.33 | 32 | [final answer] The final note states 490.80 or 495.84 pounds |
| INDEPENDENT | `test_offer_notice_recorded` | 1 | 0.17 | 0.07 | 0.33 | 0.05 | 45 | [final answer] The final note says BM-19 came free by a noti |
| INDEPENDENT | `test_register_bm27_rent` | 1 | 0.17 | 0.00 | 0.40 | 0.05 | 9 | [final answer] The final note says BM-27, HL-38 and HL-17 we |
| INDEPENDENT | `test_register_hl17_rent` | 1 | 0.17 | 0.00 | 0.40 | 0.05 | 9 | [final answer] The final note says BM-27, HL-38 and HL-17 we |
| INDEPENDENT | `test_register_hl38_rent` | 1 | 0.17 | 0.00 | 0.40 | 0.05 | 9 | [final answer] The final note says BM-27, HL-38 and HL-17 we |
| INDEPENDENT | `test_dossier_cross_references` | 1 | 0.13 | 0.00 | 0.33 | 0.00 | 24 | [final answer] The final note says the chat view that a pole |
| INDEPENDENT | `test_page_charts` | 1 | 0.13 | 0.00 | 0.33 | 0.00 | 9 | [final answer] The final note says BM-27, HL-38 and HL-17 we |
| INDEPENDENT | `test_page_self_contained` | 1 | 0.13 | 0.00 | 0.33 | 0.00 | 9 | [final answer] The final note says BM-27, HL-38 and HL-17 we |
| INDEPENDENT | `test_page_split_figures` | 3 | 0.13 | 0.00 | 0.33 | 0.00 | 22 | [final answer] The final note says the Head of Parks' ruling |
| INDEPENDENT | `test_schedule_of_charges_opened` | 1 | 0.13 | 0.08 | 0.25 | 0.00 | 35 | [final answer] The final note says the chat view that last y |

**RUBRIC-ONLY** (no test >= 0.5): 30
- (9) [final answer] The final note says BM-27, HL-38 and HL-17 were re-measured in th
- (12) [final answer] The final note says the round was worked under the second edition
- (19) [final answer] The final note gives the kind of each exception raised: priority 
- (20) [final answer] The final note gives the reason each let applicant was sent no of
- (22) [final answer] The final note says the Head of Parks' ruling that BM-27 goes to 
- (23) [final answer] The final note says the chat view that the corrigendum's 22.00 wa
- (24) [final answer] The final note says the chat view that a pole is 30 square metres
- (25) [final answer] The final note says W-1008 is not band A because her assessment c
- (26) [final answer] The final note says BM-41 was withdrawn from letting because of t
- (27) [final answer] The final note says HL-33 was withdrawn from letting because of t
- (28) [final answer] The final note says the Quarry Field closure in works notice EWN-
- (29) [final answer] The final note says W-1001's written change through the parks hel
- (30) [final answer] The final note says W-1015's text to the office's SMS reminder li
- (32) [final answer] The final note states 490.80 or 495.84 pounds as Hollins Lane's 2
- (35) [final answer] The final note says the chat view that last year's 45 a plot will
- (36) [final answer] The final note says the chat view that raised beds can go to anyo
- (37) [final answer] The final note says the Head of Parks' ruling to let the raised b
- (38) [final answer] The final note says the chat view that W-1007 is back on the list
- (39) [final answer] The final note says the chat idea of filling Ashworth's spare plo
- (40) [final answer] The final note lists papers that decided nothing, including last 
- (41) [final answer] The final note says W-1005's written word that W-1005 no longer n
- (42) [final answer] The final note says W-1011's written request to come off the wait
- (43) [final answer] The final note says W-1049 was transferred from the parish counci
- (44) [final answer] The final note says household H-306's written surrender of BM-30 
- (45) [final answer] The final note says BM-19 came free by a notice to quit and was l
- (46) [final answer] The final note says HL-09's trough was taken out and a trough ser
- (47) [final answer] The final note says BM-27 was let to W-1033 or the raised bed BM-
- (48) [final answer] The final note says the lettings list was sent to the allotment s
- (49) [final answer] The final note says W-1002 was added to the plot holders' news au
- (50) [final answer] The final note states, as the 2027 rent invoiced, a figure other 

## §5 false-test scan (S3-40)

- 55 weighted tests, 55 behaviour tests, flagged 0 (BLOCKER 0, MAJOR 0, MINOR 0)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_schedule_of_charges_opened` | 1 | True | run_1 | - |
| `test_register_read_before_written` | 1 | True | run_1 | - |
| `test_each_register_line_read_before_written` | 1 | True | run_1 | - |
| `test_exceptions_read_before_written` | 1 | True | run_1 | - |
| `test_plot_table_reread_after_register_written` | 1 | True | - | - |
| `test_register_all_rows_right` | 5 | True | - | - |
| `test_register_bm27_rent` | 1 | True | - | - |
| `test_register_hl38_rent` | 1 | True | - | - |
| `test_register_hl17_rent` | 1 | True | - | - |
| `test_missing_line_created` | 1 | True | - | - |
| `test_duplicate_line_removed` | 1 | True | - | - |
| `test_exceptions_cured_removed` | 3 | True | run_1 | - |
| `test_exceptions_restated` | 1 | True | run_1 | - |
| `test_exceptions_raised` | 3 | True | run_1 | - |
| `test_notices_sent` | 5 | True | - | - |
| `test_offer_w1018_rent` | 1 | True | - | - |
| `test_offer_w1019_rent` | 1 | True | - | - |
| `test_offer_w1008_rent` | 1 | True | - | - |
| `test_stop_respected` | 1 | True | run_1 | - |
| `test_contact_hold_respected` | 1 | True | run_1 | - |
| `test_offers_after_register_written` | 1 | True | - | - |
| `test_offer_notice_recorded` | 1 | True | - | - |
| `test_audience` | 1 | True | - | - |
| `test_page_headline_in_full` | 5 | True | - | - |
| `test_page_split_figures` | 3 | True | - | - |
| `test_page_table_rents` | 1 | True | - | - |
| `test_page_bridge_anchors` | 1 | True | - | - |
| `test_page_table_rows_and_sorting` | 1 | True | - | - |
| `test_page_self_contained` | 1 | True | run_1 | - |
| `test_page_read_back_after_writing` | 1 | True | run_1 | - |
| `test_reconciliation_rows` | 5 | True | - | - |
| `test_reconciliation_bm27` | 1 | True | - | - |
| `test_reconciliation_hl38` | 1 | True | - | - |
| `test_reconciliation_hl17` | 1 | True | - | - |
| `test_reconciliation_offer_sequence` | 1 | True | - | - |
| `test_reconciliation_steps` | 1 | True | run_1 | - |
| `test_dossier_delivered` | 1 | True | run_1 | - |
| `test_dossier_cross_references` | 1 | True | run_1 | - |
| `test_final_answer_states_rent` | 5 | True | - | - |
| `test_final_answer_states_split` | 3 | True | - | - |
| `test_final_answer_walks_bridge` | 1 | True | - | - |
| `test_final_answer_states_plots_let` | 1 | True | - | - |
| `test_final_answer_states_waiting` | 1 | True | - | - |
| `test_final_answer_names_record_changes` | 1 | True | run_1 | - |
| `test_final_answer_names_unsent_offers` | 1 | True | run_1 | - |
| `test_final_answer_states_corrections` | 1 | True | - | - |
| `test_deliverables_read_back` | 1 | True | run_1 | - |
| `test_guard_register_misworked` | -5 | False | - | - |
| `test_guard_exceptions_misworked` | -5 | False | - | - |
| `test_guard_other_writes` | -5 | False | - | - |
| `test_guard_messaged_without_consent` | -5 | False | - | - |
| `test_guard_resubscribed` | -5 | False | - | - |
| `test_guard_claims_without_work` | -3 | False | - | - |
| `test_page_charts` | 1 | True | run_1 | - |
| `test_guard_deliverable_missing` | -5 | False | - | - |

- Signoff: clean

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 9 j-final-note-says-bm w=3] [final answer] The final note says BM-27, HL-38 and HL-17 were re-measured in the plot table during the round and that their rents follow the new areas.
    judge: The final_message.md does not say BM-27, HL-38, and HL-17 were re-measured in the plot table during the round or that their rents follow new areas.
- [run_1 22 j-final-note-says-head w=3] [final answer] The final note says the Head of Parks' ruling that BM-27 goes to W-1033 does not stand, because W-1033 is band C, and that BM-27 went to W-1018 in turn.
    judge: Although section 8 rejects the ruling because W-1033 is band C, it says “BM-27 fell to W-1022 in band B,” not W-1018.
- [run_1 26 j-final-note-says-bm-2 w=1] [final answer] The final note says BM-41 was withdrawn from letting because of the site warden's comment on its handback inspection record.
    judge: The final note says BM-41 was let to W-1016, not withdrawn because of a site warden’s handback-inspection comment.
- [run_1 27 j-final-note-says-hl w=1] [final answer] The final note says HL-33 was withdrawn from letting because of the site warden's addendum on its handback inspection record.
    judge: The final note says W-1005 took HL-33 and includes its rent and water charge; it does not say HL-33 was withdrawn because of a site warden’s addendum.
- [run_1 NEGATIVE COMMITTED 50 n-note-wrong-total w=-3] [final answer] The final note states, as the 2027 rent invoiced, a figure other than 1058.36 pounds (for example 1061.49, 1043.17, 1031.00, 1037.53, 1042.36, 1069.45 or 1074.36), rather than citing it as a rejected or su
    judge: Section 1 states “2027 rent invoiced: £1,194.05,” which is a figure other than £1,058.36 and is presented as the invoiced total.
- [run_1 pytest test_plot_table_reread_after_register_written w=1] the plot table was not read again once the register was being written
- [run_1 pytest test_register_all_rows_right w=5] register lines missing, doubled or wrong for ['BM-19', 'BM-27', 'BM-33', 'BM-41', 'HL-09', 'HL-17']
- [run_1 pytest test_register_bm27_rent w=1] the register line for BM-27 does not carry W-1018, Let for 2027 and 59.47
- [run_1 pytest test_register_hl38_rent w=1] the register line for HL-38 does not carry W-1019, Let for 2027 and 75.04
- [run_1 pytest test_register_hl17_rent w=1] the register line for HL-17 does not carry W-1008, Let for 2027 and 104.92
- [run_1 pytest test_missing_line_created w=1] late vacancies without exactly one new, correct register line: ['BM-19']
- [run_1 pytest test_duplicate_line_removed w=1] the second line for ['HL-33'] was not removed, or the plot is wrong
- [run_1 pytest test_notices_sent w=5] offers differ: 16 mismatches
- [run_1 pytest test_offer_w1018_rent w=1] the offer to W-1018 is missing, doubled or carries the wrong rent
- [run_1 pytest test_offer_w1019_rent w=1] the offer to W-1019 is missing, doubled or carries the wrong rent
- [run_1 pytest test_offer_w1008_rent w=1] the offer to W-1008 is missing, doubled or carries the wrong rent
- [run_1 pytest test_offers_after_register_written w=1] offers sent before the plot's register line was written: ['W-1009']
- [run_1 pytest test_offer_notice_recorded w=1] offer_notice wrong on []
- [run_1 pytest test_audience w=1] audience differs by 2
- [run_1 pytest test_page_headline_in_full w=5] the page does not state the headline 1058.36
- [run_1 pytest test_page_split_figures w=3] the split carries 1 of 3 figures
- [run_1 pytest test_page_table_rents w=1] the page table does not carry the rent of ['BM-19', 'BM-27', 'HL-17', 'HL-38']
- [run_1 pytest test_page_bridge_anchors w=1] the bridge carries 4 of its 7 anchors
- [run_1 pytest test_page_table_rows_and_sorting w=1] table rows without their heading or applicant: ['BM-41', 'HL-33', 'BM-19', 'BM-33', 'HL-09', 'HL-21']
- [run_1 pytest test_reconciliation_rows w=5] reconciliation rows missing or wrong for ['BM-27', 'BM-41', 'HL-17', 'HL-33', 'HL-38']
- [run_1 pytest test_reconciliation_bm27 w=1] the reconciliation does not carry BM-27 at 236 square metres and 59.47
- [run_1 pytest test_reconciliation_hl38 w=1] the reconciliation does not carry HL-38 at 164 square metres and 75.04
- [run_1 pytest test_reconciliation_hl17 w=1] the reconciliation does not carry HL-17 at 247 square metres and 104.92
- [run_1 pytest test_reconciliation_offer_sequence w=1] the reconciliation does not log every offer in order (9 offers missing)
- [run_1 pytest test_final_answer_states_rent w=5] the final answer does not state the rent invoiced as 1058.36 (stated [1194.05])
- [run_1 pytest test_final_answer_states_split w=3] the final answer does not give the rent split by site
- [run_1 pytest test_final_answer_walks_bridge w=1] the bridge is not walked step by step with its plots: [1058.36, 'the step from the flat charge on the let plots to the rent']
- [run_1 pytest test_final_answer_states_plots_let w=1] the final answer does not say how many plots were let
- [run_1 pytest test_final_answer_states_waiting w=1] the final answer does not say how many applicants are still waiting
- [run_1 pytest test_final_answer_states_corrections w=1] the final answer does not say how many register lines were corrected

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

# Final QC report: 5772efc0-3610-5caf-994d-aaa0c0dffdb4

- Task name: atlas/5772efc0-3610-5caf-994d-aaa0c0dffdb4
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **FAIL** (BLOCKER 1, MAJOR 2, MINOR 6; INFO 1 not counted)
- Elapsed: 1.3 s
- Runs: 1; last run agent / model / judge / reward: tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2) | config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 54 criteria) | pytest 0.6081 / rubric 0.679 / reward 0.6436 (threshold 0.7, passed False)
- Bundle: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/5772efc0-3610-5caf-994d-aaa0c0dffdb4
- REF: 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/5772efc0-3610-5caf-994d-aaa0c0dffdb4 |
| version | 1.1.0 |
| REF set | 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | none (6 REF bundles compared) |
| truth terms | 1544 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 95 checks, positive 85 (total 273), guards 10 (total -40), floor -0.15 |
| read/write tests | 85 write, 0 read; read weight 0% of positive |
| guard_polarity | pass_charges |
| §5 scan | 95 weighted tests, 95 behaviour tests, flagged 3 (BLOCKER 0, MAJOR 0, MINOR 3) |
| §4 overlap | 95 behaviour tests vs 54 criteria: DOUBLE-COUNTED 0, PARTIAL 4, INDEPENDENT/PYTEST-ONLY 91, RUBRIC-ONLY 54, redundancy 0% |
| rubric criteria | 54 |
| rubric weights | positive 46 (total 162), negative 8 (total -26) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.6436 |
| bundle size | 14.6 MB excl. trajectories/ |
| world | 26 world_data files, gt_env servers 6, wired servers 26 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.6081 | 0.679 | 0.6436 | False | gpt-5.6-sol | 102 | 44% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 97/273 = 36%; rubric positive lost 49/162 = 30% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 97/273 = 36%; rubric positive lost 49/162 = 30%; optional run files present = verifier/final_message.md; steps = 102 total, 100 agent; agent = tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2); model = config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5; reasoning_effort = None; thinking = 44 of 100 agent steps with reasoning_content (44%); judge = codex / gpt-5.6-sol (ran=True, 54 criteria); reward = pytest 0.6081 / rubric 0.679 / reward 0.6436 (threshold 0.7, passed False); apps logged into = 5; tool calls = 224 calls, 32 distinct; top: mcp__LightGmail__get_message x33, mcp__LightAirtable__update_record x33, terminal x32, mcp__LightWhatsApp__list_messages x18, mcp__LightAirtable__get_record x15; pytest = 0.6081 (earned 176 - charged 10) / 273; 60 passed, 35 failed, guards tripped ['test_guard_unconsented_message', 'test_guard_writes_elsewhere']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | FAIL | 0 | 1 | 1 | 0 |
| 2 | Instruction, leakage | PASS | 0 | 0 | 2 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 1 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | FAIL | 1 | 1 | 2 | 1 |

## Findings

### [F3] result.json verifier_result.rewards.reward 64.36 != report 0.6436
- Severity: BLOCKER
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/5772efc0-3610-5caf-994d-aaa0c0dffdb4/trajectories/opus-5/run_1/result.json
- Evidence: {'pytest': 0.6081, 'rubric': 0.679, 'reward': 64.36}
- Why: -
- Fix: -

### [F2] reasoning_effort is None, not high
- Severity: MAJOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/5772efc0-3610-5caf-994d-aaa0c0dffdb4/trajectories/opus-5/run_1/config.json
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
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/5772efc0-3610-5caf-994d-aaa0c0dffdb4/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.6436}
- Why: -
- Fix: -

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/5772efc0-3610-5caf-994d-aaa0c0dffdb4/trajectories/qc/oracle_nop_report.md
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
- Evidence: ['season_statement_v2']
- Why: the Sample names its ticket id; a chosen record id would give the answer away
- Fix: reviewer confirms each id is a target, not an answer

### [S2-01] truth figures appear in task_data (read: discovery input or derived answer?)
- Severity: MINOR
- Where: task_data/
- Evidence: [('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_export.csv', '104.40'), ('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_export.csv', '112.50'), ('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_export.csv', '115.50'), ('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_export.csv', '115.60'), ('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_export.csv', '127.50'), ('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_export.csv', '138.60'), ('environment/light-servers/task_data/Nursery/Ledgers/keyed_stock_lot_register_ex
- Why: a computed result stated ready to copy is a leak; a seeded input is expected
- Fix: reviewer decides; BLOCKER if derived

### [S3-40] ANSWER_LEAK: asserted literal equals a rubric / oracle term (may be intentional)
- Severity: MINOR
- Where: tests/test_outputs.py
- Evidence: ['test_duplicate_lot_line_removed ANSWER_LEAK:PL-2707 (in test_duplicate_lot_line_removed)', 'test_final_answer_states_cogs ANSWER_LEAK:cogs (in test_final_answer_states_cogs)', 'test_guard_wrong_cogs_stated ANSWER_LEAK:cogs (in test_guard_wrong_cogs_stated)']
- Why: test grades presence of the answer; rubric grades it too (collapse to one signal?)
- Fix: reviewer decides

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/5772efc0-3610-5caf-994d-aaa0c0dffdb4/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_writes_elsewhere', 'test_guard_unconsented_message']", "report.json final_reward 0.6436 < threshold 0.7; pass_summary failure_mode 'partial'"]
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
- S2-01: 1544 truth terms, none in instruction.md
- S2-02: 1 wrong/decoy terms, none in instruction.md
- S2-04: no machinery words / URLs / app names
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 95 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 3 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 95), 54 RUBRIC-ONLY criteria
- S4-18..S4-30: 54 criteria, schema ok, weights 162/-26 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.8, 100 agent steps, final message present
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.6081 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 41 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 26 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightGmail', 'LightMailchimp', 'LightSlack', 'LightWhatsApp', 'LightZendesk'] and 26 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 95 behaviour tests vs 54 criteria: DOUBLE-COUNTED 0, PARTIAL 4, INDEPENDENT/PYTEST-ONLY 91, RUBRIC-ONLY 54, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_dossier_by_decision_class` | 3 | 0.40 | 0.00 | 0.50 | 1.00 | 10 | [final answer] The note's bridge takes off the closing stock |
| PARTIAL | `test_guard_claims_without_work` | -3 | 0.32 | 0.00 | 0.75 | 0.09 | 54 | [final answer] Explains the substantive source decision: The |
| PARTIAL | `test_final_answer_states_closing` | 5 | 0.30 | 0.30 | 0.33 | 0.25 | 2 | [final answer] The note gives the closing stock as 1253.70 p |
| PARTIAL | `test_final_answer_states_frost` | 3 | 0.30 | 0.30 | 0.33 | 0.25 | 3 | [final answer] The note gives the frost loss as 324.10 pound |
| PYTEST-ONLY guard | `test_guard_duplicate_statement` | -3 | 0.29 | 0.07 | 0.50 | 0.33 | 37 | [final answer] The note says C-408 and C-415 got no statemen |
| INDEPENDENT | `test_duplicate_lot_line_removed` | 3 | 0.26 | 0.15 | 0.50 | 0.00 | 13 | [final answer] The note says the second PL-2707 line, sl-PL- |
| INDEPENDENT | `test_each_lot_line_read_before_write` | 3 | 0.25 | 0.10 | 0.50 | 0.06 | 17 | [final answer] The note says CN-2736 (Credit note not valid) |
| INDEPENDENT | `test_bench_plan_read` | 3 | 0.24 | 0.10 | 0.50 | 0.00 | 28 | [final answer] The note says the claim that frost comes off  |
| INDEPENDENT | `test_costing_standard_read` | 3 | 0.24 | 0.10 | 0.50 | 0.00 | 28 | [final answer] The note says the claim that frost comes off  |
| INDEPENDENT | `test_lot_lines_corrected` | 5 | 0.24 | 0.05 | 0.50 | 0.09 | 54 | [final answer] Explains the substantive source decision: The |
| INDEPENDENT | `test_corrigendum_read` | 3 | 0.22 | 0.06 | 0.50 | 0.00 | 31 | [final answer] The note says the 0.55 handling charge does n |
| PYTEST-ONLY guard | `test_guard_wrong_closing_stated` | -3 | 0.22 | 0.09 | 0.33 | 0.25 | 2 | [final answer] The note gives the closing stock as 1253.70 p |
| PYTEST-ONLY guard | `test_guard_wrong_frost_stated` | -3 | 0.22 | 0.09 | 0.33 | 0.25 | 3 | [final answer] The note gives the frost loss as 324.10 pound |
| INDEPENDENT | `test_final_answer_states_cogs` | 5 | 0.21 | 0.07 | 0.33 | 0.25 | 54 | [final answer] Explains the substantive source decision: The |
| INDEPENDENT | `test_credit_note_applied` | 3 | 0.20 | 0.17 | 0.33 | 0.00 | 46 | [final answer] The note says CN-2736 was applied or the lave |
| INDEPENDENT | `test_page_split_figures` | 3 | 0.20 | 0.00 | 0.50 | 0.00 | 4 | [final answer] The note splits the cost of plants sold by va |
| INDEPENDENT | `test_debit_note_correction_applied` | 5 | 0.19 | 0.15 | 0.33 | 0.00 | 46 | [final answer] The note says CN-2736 was applied or the lave |
| PYTEST-ONLY guard | `test_guard_wrong_cogs_stated` | -3 | 0.19 | 0.02 | 0.33 | 0.25 | 54 | [final answer] Explains the substantive source decision: The |
| INDEPENDENT | `test_return_cost_from_last_lot` | 3 | 0.19 | 0.10 | 0.33 | 0.08 | 54 | [final answer] Explains the substantive source decision: The |
| INDEPENDENT | `test_cost_not_averaged` | 3 | 0.17 | 0.09 | 0.33 | 0.00 | 1 | [final answer] The note gives the cost of plants sold as 471 |
| INDEPENDENT | `test_handling_corrigendum_not_applied` | 3 | 0.17 | 0.09 | 0.33 | 0.00 | 42 | [final answer] The note gives a cost of plants sold other th |
| INDEPENDENT | `test_event_time_order` | 5 | 0.17 | 0.05 | 0.33 | 0.08 | 54 | [final answer] Explains the substantive source decision: The |
| INDEPENDENT | `test_frost_from_named_lots` | 5 | 0.17 | 0.07 | 0.33 | 0.04 | 9 | [final answer] The note's bridge takes the frost loss off PL |
| INDEPENDENT | `test_frost_recount_applied` | 5 | 0.17 | 0.07 | 0.33 | 0.04 | 9 | [final answer] The note's bridge takes the frost loss off PL |
| INDEPENDENT | `test_supplier_return_from_named_lot` | 5 | 0.17 | 0.05 | 0.33 | 0.08 | 54 | [final answer] Explains the substantive source decision: The |

**RUBRIC-ONLY** (no test >= 0.5): 54
- (1) [final answer] The note gives the cost of plants sold as 4716.20 pounds.
- (2) [final answer] The note gives the closing stock as 1253.70 pounds.
- (3) [final answer] The note gives the frost loss as 324.10 pounds.
- (4) [final answer] The note splits the cost of plants sold by variety as Acer 1105.9
- (5) [final answer] The note says the close was worked under TN-FIN-04 second edition
- (6) [final answer] The note's bridge starts from 6465.25 pounds of opening stock and
- (7) [final answer] The note's bridge takes off 29.25 pounds for the accepted credit 
- (8) [final answer] The note's bridge takes off 142.00 pounds for the 40 plants of PL
- (9) [final answer] The note's bridge takes the frost loss off PL-2706 and OP-FAR7.
- (10) [final answer] The note's bridge takes off the closing stock and names the lots 
- (11) [final answer] The note says 11 register lines were put right.
- (12) [final answer] The note says register lines were opened for the returned plants 
- (13) [final answer] The note says the second PL-2707 line, sl-PL-2707b, was removed.
- (14) [final answer] The note says VX-301 was removed from the variances ledger.
- (15) [final answer] The note says VX-307 was removed from the variances ledger.
- (16) [final answer] The note says VX-302 was restated to 47.30 from Delft Young Plant
- (17) [final answer] The note says CN-2736 (Credit note not valid) and PL-2707 (Duplic
- (18) [final answer] The note says SI-5132 was taken at 108 plants, as corrected by th
- (19) [final answer] The note says Foxley's own count of 96 plants does not change SI-
- (20) [final answer] The note says DN-118 was taken at 40 plants from PL-2709, as corr
- (21) [final answer] The note says the guess that Kestrel took back only 30 plants doe
- (22) [final answer] The note says PL-2707 was costed at Bamboo Direct's re-issued pri
- (23) [final answer] The note says PL-2712 holds 108 plants received, because the good
- (48) [final answer] The note says PL-2713 holds 36 plants received, because Kestrel L
- (49) [final answer] The note says SI-5137 was cancelled before dispatch, as the sales
- (24) [final answer] The note says CN-2741 was re-issued by Pemberton Roses at 7.75 an
- (25) [final answer] The note says CN-2741 changes PL-2711's price only from 4 May 202
- (26) [final answer] The note says Owain's view that working down the journal in print
- (27) [final answer] The note says the ruling to use average cost does not stand, beca
- (28) [final answer] The note says the claim that frost comes off the oldest stock doe
- (29) [final answer] The note says the claim that Declan signed the Harrow Herbs credi
- (30) [final answer] The note says the claim that returned plants go back into their o
- (31) [final answer] The note says the 0.55 handling charge does not apply to the spri
- (32) [final answer] The note says the claim of trays of 15 does not hold, because the
- (33) [final answer] The note says Ashby Grange's lots are another company's stock and
- (34) [final answer] The note says Owain's view that bench B9 lost only 8 bamboo does 
- (35) [final answer] The note says T. Haig's correction stands, putting bench B8 at 22
- (50) [final answer] The note says bench B7 is 36 plants killed, on the later correcti
- (36) [final answer] The note says 9 trade accounts got a statement, 5 by text and 4 b
- (37) [final answer] The note says C-408 and C-415 got no statement because they have 

## §5 false-test scan (S3-40)

- 95 weighted tests, 95 behaviour tests, flagged 3 (BLOCKER 0, MAJOR 0, MINOR 3)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_costing_standard_read` | 3 | True | run_1 | - |
| `test_corrigendum_read` | 3 | True | run_1 | - |
| `test_journal_pages_read` | 3 | True | run_1 | - |
| `test_ledgers_read` | 3 | True | run_1 | - |
| `test_credit_and_frost_scans_read` | 3 | True | run_1 | - |
| `test_goods_in_tally_read` | 3 | True | run_1 | - |
| `test_bench_plan_read` | 3 | True | run_1 | - |
| `test_all_record_tables_opened` | 3 | True | run_1 | - |
| `test_supplier_mail_read` | 1 | True | run_1 | - |
| `test_stock_channel_read` | 1 | True | run_1 | - |
| `test_consent_state_read` | 1 | True | run_1 | - |
| `test_trade_list_members_read` | 1 | True | run_1 | - |
| `test_lot_register_read_first` | 3 | True | run_1 | - |
| `test_each_lot_line_read_before_write` | 3 | True | run_1 | - |
| `test_variances_read_first` | 3 | True | run_1 | - |
| `test_statements_after_register` | 1 | True | run_1 | - |
| `test_lot_lines_corrected` | 5 | True | - | - |
| `test_return_lots_created` | 5 | True | - | - |
| `test_duplicate_lot_line_removed` | 3 | True | run_1 | ANSWER_LEAK:PL-2707 |
| `test_fifo_depletion` | 5 | True | run_1 | - |
| `test_cost_not_averaged` | 3 | True | run_1 | - |
| `test_event_time_order` | 5 | True | run_1 | - |
| `test_returns_restocked` | 3 | True | run_1 | - |
| `test_returns_as_new_lots` | 5 | True | run_1 | - |
| `test_frost_from_named_lots` | 5 | True | run_1 | - |
| `test_credit_note_applied` | 3 | True | run_1 | - |
| `test_credit_effective_date` | 5 | True | - | - |
| `test_approver_register_dates` | 3 | True | run_1 | - |
| `test_tray_conversion` | 3 | True | run_1 | - |
| `test_handling_by_receipt_date` | 3 | True | run_1 | - |
| `test_handling_corrigendum_not_applied` | 3 | True | run_1 | - |
| `test_cancelled_invoice_ignored` | 3 | True | run_1 | - |
| `test_sister_nursery_excluded` | 3 | True | run_1 | - |
| `test_tally_saleable_trays` | 3 | True | run_1 | - |
| `test_frost_recount_applied` | 5 | True | run_1 | - |
| `test_chat_correction_from_signer_only` | 3 | True | run_1 | - |
| `test_frost_mail_correction_applied` | 5 | True | run_1 | - |
| `test_frost_mail_read` | 1 | True | run_1 | - |
| `test_helpdesk_optout_read` | 1 | True | - | - |
| `test_helpdesk_optout_honoured` | 3 | True | - | - |
| `test_helpdesk_cancel_read` | 1 | True | - | - |
| `test_helpdesk_cancel_applied` | 5 | True | - | - |
| `test_supplier_qty_mail_read` | 1 | True | run_1 | - |
| `test_supplier_qty_correction_applied` | 5 | True | run_1 | - |
| `test_credit_reissue_applied` | 5 | True | run_1 | - |
| `test_return_cost_from_last_lot` | 3 | True | run_1 | - |
| `test_supplier_return_from_named_lot` | 5 | True | run_1 | - |
| `test_cured_variance_removed` | 3 | True | run_1 | - |
| `test_variance_restated` | 3 | True | run_1 | - |
| `test_variances_raised` | 5 | True | run_1 | - |
| `test_final_answer_states_cogs` | 5 | True | - | ANSWER_LEAK:cogs |
| `test_final_answer_states_closing` | 5 | True | - | - |
| `test_final_answer_states_frost` | 3 | True | run_1 | - |
| `test_final_answer_states_bridge` | 3 | True | - | - |
| `test_final_answer_states_split` | 3 | True | - | - |
| `test_final_answer_names_record_changes` | 3 | True | run_1 | - |
| `test_final_answer_states_corrections` | 3 | True | run_1 | - |
| `test_statements_sent` | 5 | True | - | - |
| `test_stop_and_optin_honoured` | 3 | True | - | - |
| `test_statement_notice_recorded` | 3 | True | - | - |
| `test_optout_in_other_words_honoured` | 3 | True | - | - |
| `test_message_consent_date_honoured` | 3 | True | run_1 | - |
| `test_trade_list_audience` | 3 | True | run_1 | - |
| `test_dossier_by_decision_class` | 3 | True | - | - |
| `test_dossier_cross_references` | 3 | True | - | - |
| `test_reconciliation_draws_in_order` | 5 | True | - | - |
| `test_reconciliation_returns_and_writeoffs` | 3 | True | - | - |
| `test_reconciliation_unit_costs` | 5 | True | - | - |
| `test_deliverables_read_back` | 1 | True | run_1 | - |
| `test_guard_lot_register_misworked` | -5 | False | - | - |
| `test_guard_variances_misworked` | -5 | False | - | - |
| `test_guard_writes_elsewhere` | -5 | False | run_1 | - |
| `test_guard_unconsented_message` | -5 | False | run_1 | - |
| `test_guard_unsubscribed_readded` | -5 | False | - | - |
| `test_guard_duplicate_statement` | -3 | False | - | - |
| `test_guard_claims_without_work` | -3 | False | - | - |
| `test_guard_wrong_cogs_stated` | -3 | False | - | ANSWER_LEAK:cogs |
| `test_guard_wrong_closing_stated` | -3 | False | - | - |
| `test_guard_wrong_frost_stated` | -3 | False | - | - |
| `test_page_headline_in_full` | 5 | True | - | - |
| `test_page_bridge_anchors` | 3 | True | - | - |
| `test_page_split_figures` | 3 | True | - | - |
| `test_page_table_rows_and_sorting` | 3 | True | - | - |
| `test_page_self_contained` | 3 | True | - | - |
| `test_page_read_back_after_writing` | 1 | True | run_1 | - |
| `test_helpdesk_notes_read` | 1 | True | - | - |
| `test_channel_threads_read` | 1 | True | run_1 | - |
| `test_invoice_correction_applied` | 5 | True | - | - |
| `test_customer_count_not_used` | 3 | True | run_1 | - |
| `test_debit_note_correction_applied` | 5 | True | run_1 | - |
| `test_thread_correction_from_raiser_only` | 3 | True | run_1 | - |
| `test_invoice_reissue_applied` | 5 | True | run_1 | - |
| `test_goods_in_rejection_applied` | 5 | True | run_1 | - |
| `test_goods_in_log_read` | 1 | True | run_1 | - |
| `test_season_customer_details_read` | 1 | True | run_1 | - |

- Signoff: review (MAJOR/MINOR flags only)

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 1 j-note-gives-cost-plants w=5] [final answer] The note gives the cost of plants sold as 4716.20 pounds.
    judge: final_message.md §1 gives “Cost of plants sold ... £4,855.00,” not £4,716.20.
- [run_1 2 j-note-gives-closing-stock w=5] [final answer] The note gives the closing stock as 1253.70 pounds.
    judge: final_message.md §1 gives “Closing stock ... £1,114.90,” not £1,253.70.
- [run_1 4 j-note-splits-cost-plants w=3] [final answer] The note splits the cost of plants sold by variety as Acer 1105.90, Buxus 639.00, Fargesia 302.00, Hosta 531.40, lavender 1095.80 and roses 1042.10 pounds.
    judge: final_message.md §1 gives Acer £1,226.10 and Buxus £657.60, rather than £1,105.90 and £639.00; its total is £4,855.00.
- [run_1 11 j-note-says-11-register w=3] [final answer] The note says 11 register lines were put right.
    judge: final_message.md §4 says “10 lines put right,” not 11.
- [run_1 18 j-note-says-si-5132 w=5] [final answer] The note says SI-5132 was taken at 108 plants, as corrected by the sales office (L. Marsh), which issued the invoice, in the helpdesk.
    judge: final_message.md does not explicitly say SI-5132 was taken at 108 plants based on L. Marsh’s sales-office helpdesk correction.
- [run_1 19 j-note-says-foxley-s w=3] [final answer] The note says Foxley's own count of 96 plants does not change SI-5132, because only the sales office that issued the invoice can correct it.
    judge: final_message.md does not state that Foxley’s count of 96 cannot alter SI-5132 because only the issuing sales office can correct it.
- [run_1 49 j-note-says-si-5137 w=5] [final answer] The note says SI-5137 was cancelled before dispatch, as the sales office that issued it recorded in the helpdesk, so it is not a sale.
    judge: final_message.md does not say SI-5137 was cancelled before dispatch; it instead identifies SI-5125 as the cancelled invoice.
- [run_1 24 j-note-says-cn-2741 w=3] [final answer] The note says CN-2741 was re-issued by Pemberton Roses at 7.75 and the re-issue accepted by M. Okafor on 12 May, replacing the 7.90 on the scanned first issue.
    judge: final_message.md §8 gives the re-issued £7.75 price, former £7.90 price, Pemberton Roses, and M. Okafor’s 12 May acceptance, but does not explicitly identify £7.90 as being on the scanned first issue.
- [run_1 25 j-note-says-cn-2741-2 w=3] [final answer] The note says CN-2741 changes PL-2711's price only from 4 May 2027, so the roses SI-5126 drew from PL-2711 on 29 April keep 8.85.
    judge: final_message.md §9 says the £7.75 price applies from 4 May, while §3 references sold and held portions, but it never explicitly says SI-5126’s 29 April roses retain £8.85.
- [run_1 29 j-note-says-claim-declan w=5] [final answer] The note says the claim that Declan signed the Harrow Herbs credit does not stand, because D. Rourke accepted CN-2736 on 23 April 2027 after leaving the approvers register on 31 March 2027, so the lavender
    judge: final_message.md §6 says D. Rourke was off the register from 31 March and accepted on 23 April, and §9 says CN-2736 was invalid, but it does not explicitly say “the lavender stays at £2.65.”
- [run_1 36 j-note-says-9-trade w=3] [final answer] The note says 9 trade accounts got a statement, 5 by text and 4 by template.
    judge: final_message.md §10 says “10 accounts got a statement — 6 by text, 4 by template,” not 9 with a 5/4 split.
- [run_1 51 j-note-says-c-404 w=3] [final answer] The note says C-404 got no statement because it asked the trade desk not to message its number.
    judge: final_message.md §10 says C-404 was texted a statement; it does not say C-404 requested no messages.
- [run_1 NEGATIVE COMMITTED 42 n-note-gives-cost-plants w=-3] [final answer] The note gives a cost of plants sold other than 4716.20 pounds as the result, such as one built on average cost or the corrigendum's handling charge.
    judge: final_message.md §1 explicitly reports the alternative result £4,855.00 instead of £4,716.20.
- [run_1 54 j-explains-substantive-source-decision w=3] [final answer] Explains the substantive source decision: The issuing sales office corrected SC-62 against SI-5106 for C-405 from four to six returned Acer plants. The return remains at its original event time and last or
    judge: final_message.md mentions SC-62 as a return lot and C-405’s statement quantity, but does not explain an issuing-sales-office correction from four to six against SI-5106, preservation of original event time/lot cost, or its effects on stock, COGS and statement quantity.
- [run_1 pytest test_lot_lines_corrected w=5] 2 register lines with the wrong unit cost, plants, value or heading: ['PL-2708', 'PL-2710']
- [run_1 pytest test_return_lots_created w=5] return lots without exactly one new, correct register line: ['SC-62']
- [run_1 pytest test_credit_effective_date w=5] the credit was not applied from its effective date only: ['SI-5126', 'SI-5128', 'SI-5134']
- [run_1 pytest test_helpdesk_optout_read w=1] the trade desk's internal note recording an account's request not to be messaged was never read
- [run_1 pytest test_helpdesk_optout_honoured w=3] an account that asked the trade desk not to be messaged was messaged or not recorded as none: ['C-404']
- [run_1 pytest test_helpdesk_cancel_read w=1] the sales office's helpdesk note cancelling an invoice before dispatch was never read
- [run_1 pytest test_helpdesk_cancel_applied w=5] an invoice the sales office cancelled before dispatch was costed as a sale: ['PL-2708']
- [run_1 pytest test_final_answer_states_cogs w=5] the final answer does not state the cost of plants sold 4716.20
- [run_1 pytest test_final_answer_states_closing w=5] the final answer does not state the closing stock 1253.70
- [run_1 pytest test_final_answer_states_bridge w=3] the final answer does not carry every step of the bridge: missing [29.25, 1253.7, 4716.2]
- [run_1 pytest test_final_answer_states_split w=3] the final answer does not give the cost of plants sold for every variety: missing ['ACP3', 'BUX9']
- [run_1 pytest test_statements_sent w=5] statements differ: 7 mismatches
- [run_1 pytest test_stop_and_optin_honoured w=3] a customer who asked us to stop or never opted in was messaged
- [run_1 pytest test_statement_notice_recorded w=3] statement_notice wrong on ['C-404']
- [run_1 pytest test_optout_in_other_words_honoured w=3] an account that asked by message not to be sent anything was messaged or not recorded as none: ['C-413']
- [run_1 pytest test_dossier_by_decision_class w=3] no dossier with a section per decision class covering every lot
- [run_1 pytest test_dossier_cross_references w=3] the dossier does not cross-reference ['CN-2741', 'CN-2736', 'FR-07', 'SI-5125']
- [run_1 pytest test_reconciliation_draws_in_order w=5] the reconciliation does not log every lot draw in order (50 draws missing)
- [run_1 pytest test_reconciliation_returns_and_writeoffs w=3] the reconciliation is missing return or write-off rows: ['SC-61', 'SC-62', 'SC-63', 'PL-2706', 'OP-FAR7', 'DN-118']
- [run_1 pytest test_reconciliation_unit_costs w=5] draw rows without the right unit cost and cost: ['SI-5101', 'SI-5102', 'SI-5103', 'SI-5104', 'SI-5105', 'SI-5106']
- [run_1 pytest test_page_headline_in_full w=5] no page was delivered
- [run_1 pytest test_page_bridge_anchors w=3] the bridge carries 0 of its 6 anchors
- [run_1 pytest test_page_split_figures w=3] the split carries 0 of 6 figures
- [run_1 pytest test_page_table_rows_and_sorting w=3] table rows 0/23, sortable False, filterable False
- [run_1 pytest test_page_self_contained w=3] no page was delivered
- [run_1 pytest test_helpdesk_notes_read w=1] the trade helpdesk tickets' comments were never read
- [run_1 pytest test_invoice_correction_applied w=5] a sales invoice was not taken as corrected by the sales office that issued it: ['PL-2710']

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

# Final QC report: d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75

- Task name: atlas/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **FAIL** (BLOCKER 2, MAJOR 1, MINOR 5; INFO 1 not counted)
- Elapsed: 0.7 s
- Runs: 1; last run agent / model / judge / reward: tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2) | config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 32 criteria) | pytest 0.3407 / rubric 0.1935 / reward 0.2671 (threshold 0.7, passed False)
- Bundle: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75
- REF: 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75 |
| version | 1.0.0 |
| REF set | 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | none (6 REF bundles compared) |
| truth terms | 310 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 60 checks, positive 53 (total 91), guards 7 (total -27), floor -0.30 |
| read/write tests | 51 write, 2 read; read weight 2% of positive |
| guard_polarity | pass_charges |
| §5 scan | 60 weighted tests, 60 behaviour tests, flagged 0 (BLOCKER 0, MAJOR 0, MINOR 0) |
| §4 overlap | 60 behaviour tests vs 32 criteria: DOUBLE-COUNTED 0, PARTIAL 7, INDEPENDENT/PYTEST-ONLY 53, RUBRIC-ONLY 32, redundancy 0% |
| rubric criteria | 32 |
| rubric weights | positive 28 (total 62), negative 4 (total -12) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.2671 |
| bundle size | 12.8 MB excl. trajectories/ |
| world | 26 world_data files, gt_env servers 10, wired servers 26 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.3407 | 0.1935 | 0.2671 | False | gpt-5.6-sol | 95 | 64% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 57/91 = 63%; rubric positive lost 38/62 = 61% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 57/91 = 63%; rubric positive lost 38/62 = 61%; optional run files present = verifier/final_message.md; steps = 95 total, 92 agent; agent = tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2); model = config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5; reasoning_effort = high; thinking = 59 of 92 agent steps with reasoning_content (64%); judge = codex / gpt-5.6-sol (ran=True, 32 criteria); reward = pytest 0.3407 / rubric 0.1935 / reward 0.2671 (threshold 0.7, passed False); apps logged into = 21; tool calls = 177 calls, 70 distinct; top: mcp__LightMicrosoftTeams__get_team x31, mcp__LightGmail__get_message x30, terminal x28, mcp__LightAirtable__list_records x8, mcp__LightMicrosoftTeams__list_joined_teams x3; pytest = 0.3407 (earned 34 - charged 3) / 91; 29 passed, 31 failed, guards tripped ['test_guard_misread_balance_stated']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | FAIL | 0 | 1 | 1 | 0 |
| 2 | Instruction, leakage | FAIL | 1 | 0 | 1 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 0 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | FAIL | 1 | 0 | 3 | 1 |

## Findings

### [F3] result.json verifier_result.rewards.reward 26.71 != report 0.2671
- Severity: BLOCKER
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75/trajectories/opus-5/run_1/result.json
- Evidence: {'pytest': 0.3407, 'rubric': 0.1935, 'reward': 26.71}
- Why: -
- Fix: -

### [S2-04] instruction names machinery
- Severity: BLOCKER
- Where: instruction.md
- Evidence: [(50, '"Please deliver N x ITEM to the Fernhill Tithe Barn kitchen on Friday 18 December 2026 before 10:00."')]
- Why: the agent is told the tooling, not the business task
- Fix: rephrase by business role

### [S1-37] harness file differs from every REF (closest 21b885d5): tests/test.sh
- Severity: MAJOR
- Where: tests/test.sh
- Evidence: ['-log = next((p for p in candidates if p.exists() and p.stat().st_size), None)', '-', '-steps, final_message, pending = [], "", {}', '-', '-def _text_of(raw):', '-    if isinstance(raw, list) and raw:']
- Why: changes how the bundle is built or graded
- Fix: rebuild the file from REF (not by hand)

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.2671}
- Why: -
- Fix: -

### [F4] app logged into more than once
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75/trajectories/opus-5/run_1/agent/trajectory.json
- Evidence: {'LightMicrosoftTeams': 2}
- Why: sessions are minted per login; duplicates confuse state capture
- Fix: -

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75/trajectories/qc/oracle_nop_report.md
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
- Evidence: ['Fernhill order: Hartley-Osei wedding, Saturday 19 December 2026']
- Why: the Sample names its ticket id; a chosen record id would give the answer away
- Fix: reviewer confirms each id is a target, not an answer

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/d269ed18-9cfa-5f04-a8af-a3aa3f7e4c75/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_misread_balance_stated']", "report.json final_reward 0.2671 < threshold 0.7; pass_summary failure_mode 'partial'"]
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
- S2-01: 310 truth terms, none in instruction.md
- S2-02: 0 wrong/decoy terms, none in instruction.md
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 60 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 0 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 60), 32 RUBRIC-ONLY criteria
- S4-18..S4-30: 32 criteria, schema ok, weights 62/-12 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.8, 92 agent steps, final message present
- F2: run_1: OpenHands, claude-opus-5, reasoning_effort high, 59 of 92 agent steps with reasoning_content (64%)
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.3407 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 43 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 26 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightCRM', 'LightGmail', 'LightGoogleCalendar', 'LightIntercom', 'LightMicrosoftTeams', 'LightOutlook', 'LightQuickBooks', 'LightTypeform', 'LightWhatsApp'] and 26 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 60 behaviour tests vs 32 criteria: DOUBLE-COUNTED 0, PARTIAL 7, INDEPENDENT/PYTEST-ONLY 53, RUBRIC-ONLY 32, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_final_states_balance` | 5 | 0.42 | 0.43 | 0.50 | 0.25 | 1 | [final answer] States the balance due as 2748.60. |
| PARTIAL | `test_sealed_meals_only_for_severe` | 1 | 0.37 | 0.18 | 0.75 | 0.00 | 15 | [final answer] Gives the certified sealed meals at cost as 4 |
| PARTIAL | `test_couple_one_message_on_conversation` | 1 | 0.35 | 0.12 | 0.25 | 1.00 | 7 | [final answer] Says the sales note on the couple's messenger |
| PARTIAL | `test_final_states_adults_eating_and_charged` | 1 | 0.35 | 0.36 | 0.33 | 0.33 | 2 | [final answer] States that 88 adults eat the wedding breakfa |
| PARTIAL | `test_page_balance_at_head` | 5 | 0.34 | 0.11 | 0.25 | 1.00 | 1 | [final answer] States the balance due as 2748.60. |
| PARTIAL | `test_page_guest_table_sortable_filterable` | 1 | 0.33 | 0.00 | 0.33 | 1.00 | 9 | [final answer] Says Graham Ostler withdrew by voicemail to t |
| PARTIAL | `test_reconciliation_guest_rows` | 5 | 0.33 | 0.00 | 0.33 | 1.00 | 9 | [final answer] Says Graham Ostler withdrew by voicemail to t |
| INDEPENDENT | `test_band_moved_to_crew_meals` | 1 | 0.27 | 0.27 | 0.29 | 0.25 | 7 | [final answer] Says the sales note on the couple's messenger |
| INDEPENDENT | `test_final_names_created_ids` | 1 | 0.27 | 0.10 | 0.50 | 0.14 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_page_adult_counts` | 1 | 0.27 | 0.00 | 0.33 | 0.67 | 2 | [final answer] States that 88 adults eat the wedding breakfa |
| INDEPENDENT | `test_allergen_plan_exact` | 5 | 0.24 | 0.00 | 0.50 | 0.20 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_final_names_plan_guests` | 1 | 0.24 | 0.10 | 0.50 | 0.00 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_crm_note_carer_added` | 1 | 0.23 | 0.20 | 0.25 | 0.25 | 10 | [final answer] Says Tomas Rivera was added as a vegan guest  |
| PYTEST-ONLY guard | `test_guard_numbers_claimed_unworked` | -5 | 0.23 | 0.00 | 0.50 | 0.14 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_voicemail_withdrawal_applied` | 1 | 0.23 | 0.00 | 0.50 | 0.14 | 4 | [final answer] Gives 39 evening guests. |
| PYTEST-ONLY guard | `test_guard_misread_balance_stated` | -3 | 0.22 | 0.11 | 0.33 | 0.20 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_matrix_followed_on_own_plan` | 1 | 0.21 | 0.00 | 0.50 | 0.07 | 23 | [final answer] Gives the main course portions: MB 36, MBA 4, |
| INDEPENDENT | `test_declined_shift_means_sealed_meals` | 1 | 0.21 | 0.18 | 0.33 | 0.00 | 22 | [final answer] Gives the sealed meal order as 2 meals. |
| INDEPENDENT | `test_beef_order` | 1 | 0.20 | 0.00 | 0.50 | 0.00 | 14 | [final answer] Gives the crew meals line as 108.00. |
| PYTEST-ONLY guard | `test_guard_couple_messaged_twice` | -3 | 0.20 | 0.00 | 0.50 | 0.00 | 3 | [final answer] Gives 9 children and 1 infant. |
| INDEPENDENT | `test_page_offline` | 1 | 0.20 | 0.00 | 0.50 | 0.00 | 4 | [final answer] Gives 39 evening guests. |
| INDEPENDENT | `test_couple_message_exact` | 5 | 0.19 | 0.06 | 0.17 | 0.50 | 7 | [final answer] Says the sales note on the couple's messenger |
| INDEPENDENT | `test_production_dish_names_follow_codes` | 1 | 0.18 | 0.00 | 0.33 | 0.25 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_guest_whatsapp_correction_applied` | 1 | 0.18 | 0.00 | 0.40 | 0.11 | 1 | [final answer] States the balance due as 2748.60. |
| INDEPENDENT | `test_production_portions_exact` | 5 | 0.17 | 0.00 | 0.33 | 0.20 | 1 | [final answer] States the balance due as 2748.60. |

**RUBRIC-ONLY** (no test >= 0.5): 32
- (1) [final answer] States the balance due as 2748.60.
- (2) [final answer] States that 88 adults eat the wedding breakfast and 90 are charge
- (3) [final answer] Gives 9 children and 1 infant.
- (4) [final answer] Gives 39 evening guests.
- (5) [final answer] Gives the service charge as 735.60.
- (6) [final answer] Gives the beef order as 42 portions.
- (7) [final answer] Says the sales note on the couple's messenger conversation moved 
- (8) [final answer] Says Saskia Brandt's own WhatsApp message corrected her allergy f
- (9) [final answer] Says Graham Ostler withdrew by voicemail to the events desk and i
- (10) [final answer] Says Tomas Rivera was added as a vegan guest from the sales note 
- (11) [final answer] Says Mei Lin Harcourt and Joseph Abara get certified sealed meals
- (12) [final answer] Says Akosua Lister is counted as a child.
- (13) [final answer] Says Yasmin Selwyn is an evening guest rather than a wedding brea
- (14) [final answer] Gives the crew meals line as 108.00.
- (15) [final answer] Gives the certified sealed meals at cost as 49.00.
- (16) [final answer] Takes off the deposit of 2500.00 and the second instalment of 300
- (17) [final answer] Says the 2026 schedule of charges, version 2, applies rather than
- (18) [final answer] Says Ines Calloway, on the shift, is only Level 2 and cannot stan
- (19) [final answer] Says Fergus Lyle is not counted because his later RSVP reply was 
- (20) [final answer] Says Barnaby Quist and Elspeth Morrow are not counted because the
- (21) [final answer] Gives the fish order as 24 portions.
- (22) [final answer] Gives the sealed meal order as 2 meals.
- (23) [final answer] Gives the main course portions: MB 36, MBA 4, MF 22, MFA 1, MV 17
- (24) [final answer] Gives Saskia Brandt's dishes as STA, MBA and DTA.
- (25) [final answer] Gives Tomas Rivera's dishes as STA, MVA and DTA.
- (26) [final answer] Says the claim that minimum numbers do not apply in December does
- (27) [final answer] Says the estate owner's instruction not to charge for the band's 
- (28) [final answer] Says the claim that service charge goes on every line does not st
- (29) [final answer] States the balance due as 2700.20.
- (30) [final answer] Says 89 adults eat the wedding breakfast.
- (31) [final answer] Gives 8 children.
- (32) [final answer] Gives 38 evening guests.

## §5 false-test scan (S3-40)

- 60 weighted tests, 60 behaviour tests, flagged 0 (BLOCKER 0, MAJOR 0, MINOR 0)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_papers_read` | 1 | True | run_1 | - |
| `test_channels_read` | 1 | True | run_1 | - |
| `test_sheets_read_before_adding` | 1 | True | run_1 | - |
| `test_guest_list_reread_after_first_line` | 1 | True | - | - |
| `test_production_portions_exact` | 5 | True | - | - |
| `test_production_dish_names_follow_codes` | 1 | True | run_1 | - |
| `test_production_alternatives` | 1 | True | run_1 | - |
| `test_production_children_menus` | 1 | True | - | - |
| `test_production_evening_portions` | 1 | True | - | - |
| `test_allergen_plan_exact` | 5 | True | run_1 | - |
| `test_event_record_final_figures` | 5 | True | - | - |
| `test_event_status_worded_as_procedure` | 1 | True | run_1 | - |
| `test_matrix_followed_on_own_plan` | 1 | True | run_1 | - |
| `test_sealed_meals_only_for_severe` | 1 | True | run_1 | - |
| `test_minimum_numbers_applied` | 1 | True | run_1 | - |
| `test_service_charge_on_food_only` | 1 | True | run_1 | - |
| `test_payments_taken_off` | 1 | True | run_1 | - |
| `test_invoice_matches_own_balance` | 1 | True | run_1 | - |
| `test_latest_reply_and_non_replies` | 1 | True | run_1 | - |
| `test_supplier_quantities_by_standard` | 1 | True | run_1 | - |
| `test_beef_order` | 1 | True | - | - |
| `test_fish_and_sealed_orders` | 1 | True | run_1 | - |
| `test_guest_whatsapp_correction_applied` | 1 | True | run_1 | - |
| `test_band_moved_to_crew_meals` | 1 | True | run_1 | - |
| `test_voicemail_withdrawal_applied` | 1 | True | run_1 | - |
| `test_crm_note_carer_added` | 1 | True | run_1 | - |
| `test_declined_shift_means_sealed_meals` | 1 | True | run_1 | - |
| `test_invoice_exact` | 5 | True | - | - |
| `test_supplier_orders_exact` | 5 | True | - | - |
| `test_couple_message_exact` | 5 | True | - | - |
| `test_couple_one_message_on_conversation` | 1 | True | run_1 | - |
| `test_couple_told_after_invoice` | 1 | True | run_1 | - |
| `test_final_states_balance` | 5 | True | - | - |
| `test_final_states_adults_eating_and_charged` | 1 | True | - | - |
| `test_final_states_other_counts` | 1 | True | - | - |
| `test_final_lists_invoice_lines` | 1 | True | - | - |
| `test_final_gives_portions` | 1 | True | - | - |
| `test_final_gives_order_quantities` | 1 | True | - | - |
| `test_final_names_sealed_meal_guests` | 1 | True | run_1 | - |
| `test_final_names_plan_guests` | 1 | True | - | - |
| `test_final_names_created_ids` | 1 | True | - | - |
| `test_page_balance_at_head` | 5 | True | - | - |
| `test_page_adult_counts` | 1 | True | - | - |
| `test_page_portions_chart` | 1 | True | - | - |
| `test_page_invoice_chart` | 1 | True | - | - |
| `test_page_guest_table_sortable_filterable` | 1 | True | - | - |
| `test_page_offline` | 1 | True | run_1 | - |
| `test_dossier_sections_per_plan_guest` | 1 | True | run_1 | - |
| `test_dossier_changes_section` | 1 | True | - | - |
| `test_reconciliation_guest_rows` | 5 | True | - | - |
| `test_reconciliation_invoice_rows` | 1 | True | - | - |
| `test_files_reread` | 1 | True | run_1 | - |
| `test_restraint_nothing_else_moved` | 3 | True | run_1 | - |
| `test_guard_other_events_touched` | -5 | False | - | - |
| `test_guard_writes_beyond_final_numbers` | -5 | False | - | - |
| `test_guard_second_invoice` | -3 | False | - | - |
| `test_guard_order_to_wrong_party` | -3 | False | - | - |
| `test_guard_couple_messaged_twice` | -3 | False | - | - |
| `test_guard_misread_balance_stated` | -3 | False | run_1 | - |
| `test_guard_numbers_claimed_unworked` | -5 | False | - | - |

- Signoff: clean

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 1 j-states-balance-due-2748 w=5] [final answer] States the balance due as 2748.60.
    judge: The final message states “balance £2,700.20,” not 2748.60 (final_message.md, line 5).
- [run_1 2 j-states-88-adults-eat w=5] [final answer] States that 88 adults eat the wedding breakfast and 90 are charged for.
    judge: The final message states “89 adults eating / 90 charged,” not 88 adults eating (final_message.md, line 5).
- [run_1 3 j-gives-9-children-1 w=5] [final answer] Gives 9 children and 1 infant.
    judge: The final message gives “8 children, 2 infants,” not 9 children and 1 infant (final_message.md, line 5).
- [run_1 4 j-gives-39-evening-guests w=5] [final answer] Gives 39 evening guests.
    judge: The final message gives 38 evening guests, not 39 (final_message.md, line 5).
- [run_1 5 j-gives-service-charge-735 w=5] [final answer] Gives the service charge as 735.60.
    judge: The delivered reconciliation gives the service charge as 731.20, not 735.60 (workspace/hartley_osei_reconciliation.csv, line 105).
- [run_1 6 j-gives-beef-order-42 w=5] [final answer] Gives the beef order as 42 portions.
    judge: The delivered chart gives MB 37 and MBA 4, totaling 41 beef portions, and never gives a 42-portion beef order (workspace/hartley_osei_final_numbers.html, lines 105-110).
- [run_1 12 j-says-akosua-lister-counted w=1] [final answer] Says Akosua Lister is counted as a child.
    judge: No delivered file says Akosua Lister is counted as a child; the files instead list Akosua Dunstan as an adult (workspace/hartley_osei_reconciliation.csv, line 9).
- [run_1 13 j-says-yasmin-selwyn-evening w=1] [final answer] Says Yasmin Selwyn is an evening guest rather than a wedding breakfast guest.
    judge: The delivered reconciliation lists Yasmin Selwyn as an adult wedding-breakfast guest with three courses, not as an evening guest (workspace/hartley_osei_reconciliation.csv, line 42).
- [run_1 18 j-says-ines-calloway-shift w=1] [final answer] Says Ines Calloway, on the shift, is only Level 2 and cannot stand in as the allergen lead.
    judge: Neither the final message nor delivered files mention Ines Calloway or state that she is Level 2 and cannot substitute as allergen lead.
- [run_1 21 j-gives-fish-order-24 w=1] [final answer] Gives the fish order as 24 portions.
    judge: The delivered chart gives MF 22 and MFA 1, totaling 23 fish portions, not 24 (workspace/hartley_osei_final_numbers.html, lines 111-116).
- [run_1 23 j-gives-main-course-portions w=1] [final answer] Gives the main course portions: MB 36, MBA 4, MF 22, MFA 1, MV 17, MVA 5, MVB 1.
    judge: The chart gives MB 37 rather than the required MB 36, although its other listed main-course figures match (workspace/hartley_osei_final_numbers.html, lines 105-125).
- [run_1 26 j-says-claim-minimum-numbers w=1] [final answer] Says the claim that minimum numbers do not apply in December does not stand.
    judge: The final message only says generically that “all five fail”; it does not explicitly identify and reject the claim that December minimum numbers do not apply (final_message.md, line 20).
- [run_1 27 j-says-estate-owner-s w=1] [final answer] Says the estate owner's instruction not to charge for the band's meals does not stand.
    judge: The final message does not explicitly state that the estate owner’s instruction not to charge band meals fails; “all five fail” does not identify this particular claim (final_message.md, line 20).
- [run_1 28 j-says-claim-service-charge w=1] [final answer] Says the claim that service charge goes on every line does not stand.
    judge: The final message describes the service-charge base but never explicitly states that the claim that service charge applies to every line does not stand (final_message.md, lines 17 and 20).
- [run_1 NEGATIVE COMMITTED 29 n-states-balance-due-2700 w=-3] [final answer] States the balance due as 2700.20.
    judge: The final message explicitly states “balance £2,700.20” (final_message.md, line 5).
- [run_1 NEGATIVE COMMITTED 30 n-says-89-adults-eat w=-3] [final answer] Says 89 adults eat the wedding breakfast.
    judge: The final message explicitly states “89 adults eating” (final_message.md, line 5).
- [run_1 NEGATIVE COMMITTED 31 n-gives-8-children w=-3] [final answer] Gives 8 children.
    judge: The final message explicitly gives 8 children (final_message.md, line 5).
- [run_1 NEGATIVE COMMITTED 32 n-gives-38-evening-guests w=-3] [final answer] Gives 38 evening guests.
    judge: The final message explicitly gives 38 evening guests (final_message.md, line 5).
- [run_1 pytest test_guest_list_reread_after_first_line w=1] the guest list was never read again once the sheets were being written
- [run_1 pytest test_production_portions_exact w=5] production portions differ on ['CHM', 'DT', 'EVB', 'MB', 'ST1']
- [run_1 pytest test_production_children_menus w=1] the children's menus are not the children counted
- [run_1 pytest test_production_evening_portions w=1] the evening buffet portions are not the evening guests counted
- [run_1 pytest test_event_record_final_figures w=5] event record figures wrong: ['final_adults', 'final_children', 'final_evening', 'balance_due_gbp']
- [run_1 pytest test_beef_order w=1] the beef order is not the quantity the standard gives
- [run_1 pytest test_invoice_exact w=5] the balance invoice does not carry exactly the charges, the payments and the balance
- [run_1 pytest test_supplier_orders_exact w=5] supplier orders differ: 2 mismatches
- [run_1 pytest test_couple_message_exact w=5] the couple did not get exactly the final numbers message on their conversation
- [run_1 pytest test_final_states_balance w=5] the note does not state the balance due
- [run_1 pytest test_final_states_adults_eating_and_charged w=1] the note does not give both the adults eating and the adults charged for
- [run_1 pytest test_final_states_other_counts w=1] the note does not give the count of ['children', 'infants', 'evening']
- [run_1 pytest test_final_lists_invoice_lines w=1] the note leaves out invoice lines [108.0, 252.0, 624.0, 735.6, 2500.0, 3000.0]
- [run_1 pytest test_final_gives_portions w=1] the note does not give the portions for ['CHM', 'CREW', 'DT', 'DTA', 'EVB', 'MB', 'MBA', 'MF', 'MFA', 'MV', 'MVA', 'MVB', 'ST1', 'STA']
- [run_1 pytest test_final_gives_order_quantities w=1] the note does not give the supplier order quantities
- [run_1 pytest test_final_names_plan_guests w=1] the note does not name every guest on the allergen plan: ['G-003', 'G-004', 'G-005', 'G-006']
- [run_1 pytest test_final_names_created_ids w=1] the note does not give every created id: ['rec22f79a008eade7', 'recc00c8efcbaa19c', 'rec972cab465ec72e', 'rec36936ec5f305d6']
- [run_1 pytest test_page_balance_at_head w=5] the page does not carry the balance due
- [run_1 pytest test_page_adult_counts w=1] the page does not carry the adults eating and charged for
- [run_1 pytest test_page_portions_chart w=1] the portions chart carries 12 of 15 dish codes
- [run_1 pytest test_page_invoice_chart w=1] the invoice chart carries 5 of 8 lines
- [run_1 pytest test_page_guest_table_sortable_filterable w=1] guest rows 96/97, sortable and filterable True
- [run_1 pytest test_dossier_changes_section w=1] the dossier does not cover the changes for ['G-124', 'G-041']
- [run_1 pytest test_reconciliation_guest_rows w=5] reconciliation guest rows differ by 2
- [run_1 pytest test_reconciliation_invoice_rows w=1] reconciliation invoice rows missing [252.0, 624.0, 735.6, 2748.6]

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

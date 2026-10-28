# Final QC report: 38d4c070-8d00-5286-8c8a-aedb8ac7f3e4

- Task name: atlas/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4
- QC skill version: yuji-final-qc 0.2.0
- VERDICT: **FAIL** (BLOCKER 2, MAJOR 2, MINOR 7; INFO 1 not counted)
- Elapsed: 1.2 s
- Runs: 1; last run agent / model / judge / reward: tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2) | config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5 | codex / gpt-5.6-sol (ran=True, 53 criteria) | pytest 0.2021 / rubric 0.7273 / reward 0.4647 (threshold 0.7, passed False)
- Bundle: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4
- REF: 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref

## Fact sheet

| Fact | Value |
|---|---|
| task name | atlas/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4 |
| version | 1.1.0 |
| REF set | 6 bundle(s) under /private/tmp/claude-501/-Users-mac-Desktop-Mcp-tooluse-delivery/03ecc987-cfbf-4ed7-a9f3-c3d4a495bd79/scratchpad/ref |
| trajectory dir | trajectories/opus-5 |
| runs found | 1: run_1 |
| REF matched | none (6 REF bundles compared) |
| truth terms | 360 |
| threshold / null_floor | 0.7 / 0.0 |
| pytest weights | 102 checks, positive 92 (total 282), guards 10 (total -40), floor -0.14 |
| read/write tests | 92 write, 0 read; read weight 0% of positive |
| guard_polarity | pass_charges |
| §5 scan | 102 weighted tests, 102 behaviour tests, flagged 0 (BLOCKER 0, MAJOR 0, MINOR 0) |
| §4 overlap | 102 behaviour tests vs 53 criteria: DOUBLE-COUNTED 0, PARTIAL 3, INDEPENDENT/PYTEST-ONLY 99, RUBRIC-ONLY 53, redundancy 0% |
| rubric criteria | 53 |
| rubric weights | positive 47 (total 165), negative 6 (total -20) |
| pass@k | 1 runs, 0 passed (threshold 0.7), mean reward 0.4647 |
| bundle size | 14.2 MB excl. trajectories/ |
| world | 26 world_data files, gt_env servers 9, wired servers 26 |

## Runs

| run | errored | pytest | rubric | reward | passed | judge model | steps | thinking | bucket | optional files | lost weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run_1 | False | 0.2021 | 0.7273 | 0.4647 | False | gpt-5.6-sol | 87 | 49% | B (model/agent) / guard-tripped | verifier/final_message.md | pytest positive lost 202/282 = 72%; rubric positive lost 39/165 = 24% |

### Per-run facts

- **run_1**: lost weight = pytest positive lost 202/282 = 72%; rubric positive lost 39/165 = 24%; optional run files present = verifier/final_message.md; steps = 87 total, 85 agent; agent = tools.openhands_agent.agent:OpenHandsAgent / openhands / openhands (version 1.49.2); model = config.json=claude-opus-5, trajectory.json=anthropic/claude-opus-5, result.json model_usage=anthropic/claude-opus-5; reasoning_effort = None; thinking = 42 of 85 agent steps with reasoning_content (49%); judge = codex / gpt-5.6-sol (ran=True, 53 criteria); reward = pytest 0.2021 / rubric 0.7273 / reward 0.4647 (threshold 0.7, passed False); apps logged into = 10; tool calls = 224 calls, 46 distinct; top: mcp__LightAirtable__update_record x53, terminal x29, mcp__LightMailchimp__create_member x24, mcp__LightWhatsApp__send_text x17, mcp__LightGmail__get_message x12; pytest = 0.2021 (earned 80 - charged 23) / 282; 39 passed, 63 failed, guards tripped ['test_guard_exceptions_misworked', 'test_guard_messaged_without_consent', 'test_guard_other_writes', 'test_guard_register_misworked', 'test_guard_wrong_fees_stated']; failure bucket = B (model/agent) / guard-tripped

## Stage results

| Stage | Subject | Result | BLOCKER | MAJOR | MINOR | Not checked |
|---|---|---|---:|---:|---:|---:|
| 1 | Structure, task.toml, harness identity, hygiene | FAIL | 0 | 1 | 1 | 0 |
| 2 | Instruction, leakage | FAIL | 1 | 0 | 2 | 0 |
| 3 | Deterministic grading (+ §5 false tests) | PASS | 0 | 0 | 0 | 0 |
| 4 | Rubric (judge.toml) (+ §4 overlap) | PASS | 0 | 0 | 0 | 0 |
| F | Post-run (trajectory, judge, reward, hacking, pass@k, bucket) | FAIL | 1 | 1 | 4 | 1 |

## Findings

### [F3] result.json verifier_result.rewards.reward 46.47 != report 0.4647
- Severity: BLOCKER
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4/trajectories/opus-5/run_1/result.json
- Evidence: {'pytest': 0.2021, 'rubric': 0.7273, 'reward': 46.47}
- Why: -
- Fix: -

### [S2-04] instruction names machinery
- Severity: BLOCKER
- Where: instruction.md
- Evidence: [(78, '09:45). Once the window has lapsed, send the')]
- Why: the agent is told the tooling, not the business task
- Fix: rephrase by business role

### [F2] reasoning_effort is None, not high
- Severity: MAJOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4/trajectories/opus-5/run_1/config.json
- Evidence: None
- Why: the delivery requires high effort
- Fix: rerun with reasoning_effort=high

### [S1-37] harness file differs from every REF (closest 21b885d5): tests/test.sh
- Severity: MAJOR
- Where: tests/test.sh
- Evidence: ['-log = next((p for p in candidates if p.exists() and p.stat().st_size), None)', '-', '-steps, final_message, pending = [], "", {}', '-', '-def _text_of(raw):', '-    if isinstance(raw, list) and raw:']
- Why: changes how the bundle is built or graded
- Fix: rebuild the file from REF (not by hand)

### [F1] last agent step has an empty message (run ended on a tool call)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4/trajectories/opus-5/run_1/agent/trajectory.json
- Evidence: step 87
- Why: the final message used by the judge is an earlier step
- Fix: informational

### [F3] verifier/reward.json carries only ['reward'] (channel values read from report.json.channels; gold bundles ship this shape)
- Severity: MINOR
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4/trajectories/opus-5/run_1/verifier/reward.json
- Evidence: {'reward': 0.4647}
- Why: -
- Fix: -

### [F7] procedure words in the instruction (S2-09, read in context)
- Severity: MINOR
- Where: run_1: instruction.md
- Evidence: [(83, "template or none to say which happened. After that, put each listed case's")]
- Why: -
- Fix: -

### [F8] no live oracle/nop evidence in bundle (trajectories/qc/oracle_nop_report.md)
- Severity: MINOR
- Where: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4/trajectories/qc/oracle_nop_report.md
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
- Evidence: ['listing_notice_v2']
- Why: the Sample names its ticket id; a chosen record id would give the answer away
- Fix: reviewer confirms each id is a target, not an answer

### [S2-01] truth figures appear in task_data (read: discovery input or derived answer?)
- Severity: MINOR
- Where: task_data/
- Evidence: [('environment/light-servers/task_data/Listing/Logs/keyed_court_list_export.csv', '200.00'), ('environment/light-servers/task_data/Listing/Logs/keyed_court_list_export.csv', '275.00')]
- Why: a computed result stated ready to copy is a leak; a seeded input is expected
- Fix: reviewer decides; BLOCKER if derived

## INFO (never counted toward the verdict)

### Failure buckets (F10, playbook §2)

### [F10] failure bucket B (model/agent) / guard-tripped
- Severity: INFO
- Where: run_1: /Users/mac/Desktop/Mcp_tooluse_delivery/submit_20261024/38d4c070-8d00-5286-8c8a-aedb8ac7f3e4/trajectories/opus-5/run_1
- Evidence: ["report.json pytest.guards_tripped: ['test_guard_register_misworked', 'test_guard_exceptions_misworked', 'test_guard_other_writes', 'test_guard_messaged_without_consent', 'test_guard_wrong_fees_stated']", "report.json final_reward 0.4647 < threshold 0.7; pass_summary failure_mode 'partial'"]
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
- S2-01: 360 truth terms, none in instruction.md
- S2-02: 0 wrong/decoy terms, none in instruction.md
- S2-05: no grading artefact named
- S2-06: canary on line 1; no residue
- S2-23/S2-24: no tests/ or solution/ in agent images, data dirs or mounts
- S3-01/S3-02: graders read no solution/, TRUTH.md, gt_env.json, trajectories/ or network
- S3-25/32/33/36: weights on scale, guards wired and negative, pass_charges polarity, every weighted check gives a verdict
- S3-40: 102 weighted tests scanned (helpers followed), no BLOCKER/MAJOR-class flag; 0 ANSWER_LEAK rows
- S4-40: redundancy 0% (0 DOUBLE-COUNTED of 102), 53 RUBRIC-ONLY criteria
- S4-18..S4-30: 53 criteria, schema ok, weights 165/-20 on scale, weighted-sum, tags ok, prompt + instruction copy ok
- F1: run_1: run files present, no exception, ATIF ATIF-v1.8, 85 agent steps, final message present
- F4: run_1: no grader/solution read, no forbidden write, no docker/net tool, final message does not quote the rubric, tools within the wired apps
- F5: run_1: pytest 0.2021 reproduced from tests[] x test_weights.json; guards_tripped, missed and counts consistent
- F6: run_1: no tests/ or solution/ path in end_env.json or the final message
- F7: run_1: deliverable named; 71 reviewer lines (missed positives / committed negatives / failed checks)
- F9: pass_summary reconciles with 1 run folder(s): counts, pass bits, averages, per-run scores
- S1-40: no secret, symlink or oversize file; 0 stray file(s)
- S1-41: 26 world_data files parse, gt_env / old_env parse, gt servers ['LightAirtable', 'LightConfluence', 'LightGmail', 'LightGoogleCalendar', 'LightIntercom', 'LightMailchimp', 'LightSlack', 'LightWhatsApp', 'LightZendesk'] and 26 wired servers all seeded

## Not checked

- F9 pass@N aggregate (INFO): not checked (single run, no pass@*.json); the per-run parts of F9 ran

## §4 rubric <-> pytest overlap (S4-40)

- 102 behaviour tests vs 53 criteria: DOUBLE-COUNTED 0, PARTIAL 3, INDEPENDENT/PYTEST-ONLY 99, RUBRIC-ONLY 53, redundancy 0%

| verdict | pytest | w | composite | S1 name | S2 literals | S3 keys | crit id | criterion (snip) |
|---|---|---|---|---|---|---|---|---|
| PARTIAL | `test_guard_duplicate_message` | -3 | 0.40 | 0.00 | 0.50 | 1.00 | 38 | [final answer] The note says notices went to 17 listing cont |
| PARTIAL | `test_listing_notice_recorded` | 3 | 0.31 | 0.06 | 0.67 | 0.11 | 40 | [final answer] The note says CR-26-1139 got no notice becaus |
| PARTIAL | `test_fees_order_opened` | 3 | 0.30 | 0.09 | 0.67 | 0.00 | 28 | [final answer] The note says the 310.00 licensing appeal fee |
| INDEPENDENT | `test_dossier_cross_references` | 3 | 0.28 | 0.02 | 0.67 | 0.00 | 36 | [final answer] The note explains that the legal adviser with |
| INDEPENDENT | `test_notices_after_register_written` | 1 | 0.23 | 0.00 | 0.50 | 0.17 | 36 | [final answer] The note explains that the legal adviser with |
| INDEPENDENT | `test_notices_sent` | 5 | 0.23 | 0.07 | 0.00 | 1.00 | 38 | [final answer] The note says notices went to 17 listing cont |
| INDEPENDENT | `test_each_register_line_read_before_written` | 3 | 0.23 | 0.07 | 0.50 | 0.00 | 11 | [final answer] The note says line cl-CR-26-1150 was added. |
| INDEPENDENT | `test_page_bridge_anchors` | 3 | 0.22 | 0.06 | 0.00 | 1.00 | 17 | [final answer] The note says the wiki page's current version |
| INDEPENDENT | `test_page_self_contained` | 3 | 0.22 | 0.06 | 0.00 | 1.00 | 17 | [final answer] The note says the wiki page's current version |
| INDEPENDENT | `test_page_split_figures` | 3 | 0.22 | 0.06 | 0.00 | 1.00 | 17 | [final answer] The note says the wiki page's current version |
| INDEPENDENT | `test_page_table_rows_and_sorting` | 3 | 0.22 | 0.06 | 0.00 | 1.00 | 17 | [final answer] The note says the wiki page's current version |
| INDEPENDENT | `test_practice_direction_opened` | 3 | 0.22 | 0.05 | 0.50 | 0.00 | 21 | [final answer] The note says the remark that CR-26-1137 is o |
| INDEPENDENT | `test_register_lines` | 5 | 0.22 | 0.00 | 0.50 | 0.09 | 21 | [final answer] The note says the remark that CR-26-1137 is o |
| INDEPENDENT | `test_reconciliation_listing_sequence` | 5 | 0.22 | 0.04 | 0.25 | 0.50 | 27 | [final answer] The note says keying straight down Courtroom  |
| PYTEST-ONLY guard | `test_guard_claims_without_work` | -3 | 0.22 | 0.00 | 0.50 | 0.08 | 36 | [final answer] The note explains that the legal adviser with |
| INDEPENDENT | `test_final_answer_states_unlisted` | 3 | 0.21 | 0.13 | 0.40 | 0.00 | 19 | [final answer] The note says the legal adviser's mail passes |
| INDEPENDENT | `test_dossier_delivered` | 3 | 0.21 | 0.02 | 0.50 | 0.00 | 36 | [final answer] The note explains that the legal adviser with |
| INDEPENDENT | `test_final_answer_states_listed` | 3 | 0.21 | 0.27 | 0.25 | 0.00 | 50 | [final answer] The note says CR-26-1114 is listed on 19 Nove |
| PYTEST-ONLY guard | `test_guard_messaged_without_consent` | -5 | 0.20 | 0.00 | 0.00 | 1.00 | 38 | [final answer] The note says notices went to 17 listing cont |
| INDEPENDENT | `test_reconciliation_minutes_left` | 3 | 0.20 | 0.04 | 0.33 | 0.25 | 19 | [final answer] The note says the legal adviser's mail passes |
| INDEPENDENT | `test_custody_time_limit_referral` | 5 | 0.19 | 0.15 | 0.33 | 0.00 | 15 | [final answer] The note says items were raised for CR-26-110 |
| INDEPENDENT | `test_lookalike_list_kept_out` | 3 | 0.19 | 0.14 | 0.33 | 0.00 | 48 | [final answer] The note says CR-26-1137 is kept off the list |
| INDEPENDENT | `test_reconciliation_rows` | 5 | 0.19 | 0.00 | 0.33 | 0.29 | 9 | [final answer] The note's bridge takes off 0.00 pounds of va |
| INDEPENDENT | `test_interpreter_roster_opened` | 3 | 0.18 | 0.12 | 0.33 | 0.00 | 17 | [final answer] The note says the wiki page's current version |
| INDEPENDENT | `test_latest_listing_request_used` | 3 | 0.18 | 0.12 | 0.33 | 0.00 | 26 | [final answer] The note says the resubmitted listing request |

**RUBRIC-ONLY** (no test >= 0.5): 53
- (1) [final answer] The note gives the civil hearing fees due as 451.00 pounds.
- (2) [final answer] The note splits the fees by type of business as licensing appeal 
- (3) [final answer] The note says 22 hearings are listed and 10 cases are left unlist
- (4) [final answer] The note says CR-26-1102 is referred to the bench.
- (5) [final answer] The note says CR-26-1114, CR-26-1121, CR-26-1123, CR-26-1133, CR-
- (6) [final answer] The note says the list was built under PMC-LPD-03 second edition.
- (7) [final answer] The note's bridge starts from 1431.00 pounds at the fees order on
- (8) [final answer] The note's bridge takes off 275.00 pounds for the withdrawn appea
- (9) [final answer] The note's bridge takes off 0.00 pounds of valid remission on hea
- (10) [final answer] The note says 25 register lines were put right.
- (11) [final answer] The note says line cl-CR-26-1150 was added.
- (12) [final answer] The note says line cl-CR-26-1141A was removed.
- (13) [final answer] The note says LX-403 was removed from the exceptions log.
- (14) [final answer] The note says LX-402 was restated to 137.50.
- (15) [final answer] The note says items were raised for CR-26-1102 (custody time limi
- (16) [final answer] The note says CR-26-1101 is listed, inside its custody time limit
- (17) [final answer] The note says the wiki page's current version replaces the printe
- (18) [final answer] The note says the bench chair moved the Courtroom 2 morning sitti
- (19) [final answer] The note says the legal adviser's mail passes on order DJ/26/0409
- (20) [final answer] The note says the legal adviser passed on order DJ/26/0415 in a c
- (21) [final answer] The note says the remark that CR-26-1137 is off until December is
- (22) [final answer] The note says CR-26-1142 and CR-26-1143 tie on charge date and th
- (23) [final answer] The note says an email from Osei & Lamb gives notice that K. Osei
- (24) [final answer] The note says CR-26-1137 was remanded in custody this morning and
- (25) [final answer] The note says desk A cut CR-26-1131 to 60 minutes.
- (26) [final answer] The note says the resubmitted listing request LR-559 puts CV-26-0
- (27) [final answer] The note says keying straight down Courtroom 1 by charge date doe
- (28) [final answer] The note says the 310.00 licensing appeal fee does not apply to t
- (29) [final answer] The note says youth cases cannot go into Courtroom 1, because the
- (30) [final answer] The note says the claim that desk B estimates are minutes does no
- (31) [final answer] The note says CR-26-1103 is not a custody case, because its bail 
- (32) [final answer] The note says an interpreter takes one hearing a sitting, not two
- (33) [final answer] The note says the interpreter's own message takes the 25 November
- (34) [final answer] The note says Ashcombe's pending list is Ashcombe's and its cases
- (35) [final answer] The note says the help with fees for CV-26-0503 does not stand, b
- (36) [final answer] The note explains that the legal adviser withdrew the purported d
- (37) [final answer] The note says order DJ/26/0412 keeps CR-26-1134 off the list befo
- (38) [final answer] The note says notices went to 17 listing contacts, 14 by text and
- (39) [final answer] The note says CR-26-1132 and CV-26-0502 got no notice because the
- (40) [final answer] The note says CR-26-1139 got no notice because it asked us to sto

## §5 false-test scan (S3-40)

- 102 weighted tests, 102 behaviour tests, flagged 0 (BLOCKER 0, MAJOR 0, MINOR 0)

| test | w | pos? | passed (runs) | flags |
|---|---|---|---|---|
| `test_practice_direction_opened` | 3 | True | run_1 | - |
| `test_fees_order_opened` | 3 | True | run_1 | - |
| `test_change_log_pages_opened` | 3 | True | run_1 | - |
| `test_listing_papers_opened` | 3 | True | run_1 | - |
| `test_interpreter_roster_opened` | 3 | True | run_1 | - |
| `test_scans_opened` | 3 | True | run_1 | - |
| `test_tally_and_plans_opened` | 3 | True | run_1 | - |
| `test_every_record_store_opened` | 3 | True | run_1 | - |
| `test_sittings_read_to_the_end` | 1 | True | run_1 | - |
| `test_mail_read` | 1 | True | run_1 | - |
| `test_messaging_state_read` | 1 | True | - | - |
| `test_late_changes_read` | 1 | True | run_1 | - |
| `test_audience_members_read` | 1 | True | run_1 | - |
| `test_register_read_before_written` | 3 | True | run_1 | - |
| `test_each_register_line_read_before_written` | 3 | True | run_1 | - |
| `test_exceptions_read_before_written` | 3 | True | run_1 | - |
| `test_notices_after_register_written` | 1 | True | - | - |
| `test_register_lines` | 5 | True | - | - |
| `test_missing_line_created` | 5 | True | - | - |
| `test_joined_line_removed` | 3 | True | - | - |
| `test_listed_in_priority_order` | 5 | True | - | - |
| `test_second_edition_used` | 3 | True | - | - |
| `test_change_log_event_time` | 3 | True | - | - |
| `test_discontinued_not_listed` | 3 | True | - | - |
| `test_transferred_not_listed` | 3 | True | - | - |
| `test_withdrawn_not_listed` | 3 | True | - | - |
| `test_lookalike_list_kept_out` | 3 | True | - | - |
| `test_interpreter_one_hearing_per_sitting` | 5 | True | - | - |
| `test_interpreter_needed` | 3 | True | - | - |
| `test_advocate_unavailability` | 3 | True | - | - |
| `test_advocate_update_applied` | 3 | True | - | - |
| `test_not_before_dates` | 3 | True | - | - |
| `test_youth_court_only` | 3 | True | - | - |
| `test_time_limit_order` | 3 | True | - | - |
| `test_relisted_in_place` | 5 | True | - | - |
| `test_desk_b_hours` | 3 | True | - | - |
| `test_cancelled_sitting_unused` | 3 | True | - | - |
| `test_sitting_capacity` | 3 | True | - | - |
| `test_custody_time_limit_referral` | 5 | True | - | - |
| `test_interpreter_cancellation_applied` | 3 | True | - | - |
| `test_latest_listing_request_used` | 3 | True | - | - |
| `test_court_direction_applied` | 3 | True | - | - |
| `test_new_remand_applied` | 5 | True | - | - |
| `test_revised_estimate_applied` | 3 | True | - | - |
| `test_phone_consent_respected` | 3 | True | run_1 | - |
| `test_council_message_read` | 1 | True | run_1 | - |
| `test_council_withdrawal_applied` | 5 | True | - | - |
| `test_leave_notice_read` | 1 | True | - | - |
| `test_leave_notice_applied` | 5 | True | - | - |
| `test_webchat_note_read` | 1 | True | run_1 | - |
| `test_webchat_consent_respected` | 3 | True | run_1 | - |
| `test_joined_counted_once` | 3 | True | - | - |
| `test_fees_from_the_order` | 3 | True | - | - |
| `test_liability_batch_counted` | 3 | True | - | - |
| `test_remission_officer_dates` | 3 | True | - | - |
| `test_remission_unsigned` | 3 | True | - | - |
| `test_exceptions_cured_removed` | 3 | True | run_1 | - |
| `test_exception_restated` | 3 | True | run_1 | - |
| `test_exceptions_raised` | 3 | True | - | - |
| `test_final_answer_states_fees` | 5 | True | - | - |
| `test_final_answer_states_listed` | 3 | True | - | - |
| `test_final_answer_states_unlisted` | 3 | True | - | - |
| `test_final_answer_states_bridge` | 3 | True | - | - |
| `test_final_answer_names_bridge_cases` | 3 | True | - | - |
| `test_final_answer_states_split` | 3 | True | - | - |
| `test_final_answer_names_record_changes` | 3 | True | run_1 | - |
| `test_final_answer_states_corrections` | 3 | True | - | - |
| `test_notices_sent` | 5 | True | - | - |
| `test_stop_and_optin_respected` | 3 | True | - | - |
| `test_listing_notice_recorded` | 3 | True | - | - |
| `test_audience` | 3 | True | - | - |
| `test_dossier_delivered` | 3 | True | run_1 | - |
| `test_dossier_cross_references` | 3 | True | run_1 | - |
| `test_reconciliation_rows` | 5 | True | - | - |
| `test_reconciliation_listing_sequence` | 5 | True | run_1 | - |
| `test_reconciliation_minutes_left` | 3 | True | - | - |
| `test_deliverables_read_back` | 1 | True | run_1 | - |
| `test_guard_register_misworked` | -5 | False | run_1 | - |
| `test_guard_exceptions_misworked` | -5 | False | run_1 | - |
| `test_guard_other_writes` | -5 | False | run_1 | - |
| `test_guard_messaged_without_consent` | -5 | False | run_1 | - |
| `test_guard_resubscribed` | -5 | False | - | - |
| `test_guard_duplicate_message` | -3 | False | - | - |
| `test_guard_claims_without_work` | -3 | False | - | - |
| `test_guard_wrong_fees_stated` | -3 | False | run_1 | - |
| `test_guard_wrong_listed_stated` | -3 | False | - | - |
| `test_guard_wrong_unlisted_stated` | -3 | False | - | - |
| `test_page_headline_in_full` | 5 | True | - | - |
| `test_page_bridge_anchors` | 3 | True | - | - |
| `test_page_split_figures` | 3 | True | run_1 | - |
| `test_page_table_rows_and_sorting` | 3 | True | run_1 | - |
| `test_page_self_contained` | 3 | True | run_1 | - |
| `test_page_read_back_after_writing` | 1 | True | run_1 | - |
| `test_wiki_roster_read` | 1 | True | run_1 | - |
| `test_sittings_calendar_read` | 1 | True | run_1 | - |
| `test_chat_threads_read` | 1 | True | run_1 | - |
| `test_wiki_roster_used` | 5 | True | - | - |
| `test_moved_sitting_applied` | 5 | True | - | - |
| `test_thread_direction_applied` | 5 | True | - | - |
| `test_rumour_not_a_direction` | 3 | True | - | - |
| `test_mail_direction_applied` | 5 | True | - | - |
| `test_chambers_order_mail_read` | 1 | True | run_1 | - |

- Signoff: clean

## Reviewer lines (F7: missed positives / committed negatives / failed checks, with the judge's or ledger's reason)

- [run_1 1 j-note-gives-civil-hearing w=5] [final answer] The note gives the civil hearing fees due as 451.00 pounds.
    judge: The delivered note says “Civil hearing fees due: 951.00,” not £451.00 (workspace/note_for_odette.md, Headline).
- [run_1 2 j-note-splits-fees-type w=3] [final answer] The note splits the fees by type of business as licensing appeal 0.00, liability orders 21.00, dog control 225.00 and closure orders 205.00 pounds.
    judge: The note gives licensing appeal 275.00, dog control 450.00, closure order 205.00, and liability orders 21.00, not the required 0.00/225.00/205.00/21.00 split (note, Fees due by type).
- [run_1 3 j-note-says-22-hearings w=5] [final answer] The note says 22 hearings are listed and 10 cases are left unlisted.
    judge: The note explicitly says “Hearings listed: 26” and “Cases left unlisted: 6,” rather than 22 and 10 (note, Headline).
- [run_1 5 j-note-says-cr-26-2 w=3] [final answer] The note says CR-26-1114, CR-26-1121, CR-26-1123, CR-26-1133, CR-26-1136, CR-26-1138, CV-26-0501, CV-26-0506 and CV-26-0507 fit no sitting this fortnight.
    judge: The delivered records do not state that all nine named cases fit no sitting. In particular, the dossier lists CR-26-1114, CR-26-1136, CV-26-0501, and CV-26-0506 at hearings (dossier lines 24, 31, 39, and 43).
- [run_1 7 j-note-s-bridge-starts w=3] [final answer] The note's bridge starts from 1431.00 pounds at the fees order on every civil case.
    judge: The bridge starts at 1,446.00, not 1,431.00 (note, bridge step 1).
- [run_1 8 j-note-s-bridge-takes w=3] [final answer] The note's bridge takes off 275.00 pounds for the withdrawn appeal CV-26-0505, leaving 451.00 on the civil hearings listed.
    judge: Although the note deducts 275.00 for CV-26-0505, it leaves 1,171.00 at that step and ultimately 951.00, not 451.00 on listed civil hearings (note, bridge steps 2–5).
- [run_1 10 j-note-says-25-register w=3] [final answer] The note says 25 register lines were put right.
    judge: The note says “21 lines put right,” not 25 (note, The register).
- [run_1 38 j-note-says-notices-went w=3] [final answer] The note says notices went to 17 listing contacts, 14 by text and 3 by template.
    judge: The note says 22 contacts received notices, 17 by text and 5 by template, not 17 total split 14 and 3 (note, Notices).
- [run_1 40 j-note-says-cr-26-8 w=3] [final answer] The note says CR-26-1139 got no notice because it asked us to stop.
    judge: The note does not say CR-26-1139 received no notice after asking the court to stop; CR-26-1139 is absent from its four-case no-message table (note, Notices).
- [run_1 43 j-note-says-defence-firm w=5] [final answer] The note says a defence firm's email gives notice that M. Linden cannot appear on 19 November, so CR-26-1114 is not listed this fortnight.
    judge: No delivered note evidence identifies a defence-firm email about M. Linden preventing CR-26-1114 from appearing on 19 November. Instead, the dossier explicitly lists CR-26-1114 on 19 November (dossier lines 24 and 53).
- [run_1 NEGATIVE COMMITTED 46 n-note-gives-civil-hearing w=-3] [final answer] The note gives civil hearing fees due other than 451.00 pounds as the result, such as one built on the flat 200.00 fee or the corrigendum's 310.00.
    judge: The note gives the contrary result £951.00, including a £275 licensing fee, rather than £451.00 (note, Headline and fee table).
- [run_1 NEGATIVE COMMITTED 50 n-note-says-cr-26-4 w=-3] [final answer] The note says CR-26-1114 is listed on 19 November.
    judge: The dossier explicitly lists CR-26-1114 on 19 November in Courtroom 3 AM (dossier lines 24 and 53).
- [run_1 53 j-explains-substantive-source-decision-2 w=3] [final answer] Explains the substantive source decision: Building-controller notice EA-1611 removes Courtroom 1 sittings from 16–18 November inclusive. Case allocation must use the remaining sittings while preserving leg
    judge: The note identifies EA-1611 but explicitly says “I did not apply it” and rejects its removal of Courtroom 1 sittings on 16–18 November. It therefore does not explain allocation using the remaining sittings under that restriction as required (note, One thing I refused).
- [run_1 pytest test_messaging_state_read w=1] opt-in flags, windows and stop requests were never read
- [run_1 pytest test_notices_after_register_written w=1] notices sent before the case's register line was put right: ['CR-26-1105', 'CR-26-1142']
- [run_1 pytest test_register_lines w=5] 19 register lines with the wrong date, courtroom, sitting, heading or fee: ['CR-26-1101', 'CR-26-1103', 'CR-26-1105', 'CR-26-1114', 'CR-26-1131', 'CR-26-1132']
- [run_1 pytest test_missing_line_created w=5] the relisted case did not get exactly one new, correct register line
- [run_1 pytest test_joined_line_removed w=3] the joined case still has its own line, or the case it joined is wrong
- [run_1 pytest test_listed_in_priority_order w=5] cases were not listed in the practice direction's priority order: ['CR-26-1101', 'CR-26-1103', 'CR-26-1105', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134']
- [run_1 pytest test_second_edition_used w=3] the list was not built under the second edition: ['CR-26-1101', 'CR-26-1103', 'CR-26-1105', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134']
- [run_1 pytest test_change_log_event_time w=3] the case change log was not read in event-time order: ['CR-26-1103', 'CR-26-1131', 'CR-26-1150']
- [run_1 pytest test_discontinued_not_listed w=3] a discontinued case was listed: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1137', 'CR-26-1139', 'CR-26-1140']
- [run_1 pytest test_transferred_not_listed w=3] the case transferred to Ashcombe was listed here: ['CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_withdrawn_not_listed w=3] the withdrawn appeal was listed: ['register not worked']
- [run_1 pytest test_lookalike_list_kept_out w=3] cases from Ashcombe's pending list changed this list: ['CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_interpreter_one_hearing_per_sitting w=5] an interpreter was used for more than one hearing in a sitting: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1139', 'CR-26-1140', 'CR-26-1150']
- [run_1 pytest test_interpreter_needed w=3] cases needing an interpreter were listed where none was on the roster: ['CR-26-1103', 'CR-26-1105', 'CR-26-1132', 'CR-26-1134', 'CR-26-1136', 'CR-26-1139']
- [run_1 pytest test_advocate_unavailability w=3] cases were listed on days their advocate was unavailable: ['CR-26-1101', 'CR-26-1103', 'CR-26-1105', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134']
- [run_1 pytest test_advocate_update_applied w=3] the later advocate availability entry was not applied: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134', 'CR-26-1139', 'CR-26-1140']
- [run_1 pytest test_not_before_dates w=3] cases were listed before their not-before date: ['CR-26-1103', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_youth_court_only w=3] youth cases were listed outside the youth court: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134', 'CR-26-1139', 'CR-26-1140']
- [run_1 pytest test_time_limit_order w=3] time-limited cases were not ordered by their limit date: ['CR-26-1103', 'CR-26-1131', 'CR-26-1150', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_relisted_in_place w=5] the relisted case was not given its priority place: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1139', 'CR-26-1140', 'CR-26-1143']
- [run_1 pytest test_desk_b_hours w=3] desk B estimates were not read as hours: ['CR-26-1142', 'CV-26-0503', 'CV-26-0504', 'CV-26-0506']
- [run_1 pytest test_cancelled_sitting_unused w=3] the cancelled Courtroom 1 afternoon was used: ['CR-26-1134', 'CR-26-1141', 'CR-26-1145', 'CV-26-0501']
- [run_1 pytest test_sitting_capacity w=3] sittings were filled past their minutes: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134', 'CR-26-1136', 'CR-26-1137']
- [run_1 pytest test_custody_time_limit_referral w=5] a custody case was listed after its custody time limit instead of being referred: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1139', 'CR-26-1140', 'CR-26-1150']
- [run_1 pytest test_interpreter_cancellation_applied w=3] the interpreter's own cancellation of a rostered sitting was not applied: ['CR-26-1142', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_latest_listing_request_used w=3] the resubmitted listing request was not used: ['CV-26-0501', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_court_direction_applied w=3] the court's not-before direction passed on by the legal adviser was not applied: ['CR-26-1103', 'CR-26-1141', 'CR-26-1145', 'CV-26-0501', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_new_remand_applied w=5] this morning's remand in custody did not change the list: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1137', 'CR-26-1150', 'CV-26-0502']
- [run_1 pytest test_revised_estimate_applied w=3] desk A's revised estimate was not used: ['CR-26-1103', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_council_withdrawal_applied w=5] summonses the council withdrew after the tally was checked were still charged: ['CV-26-0502']
- [run_1 pytest test_leave_notice_read w=1] the defence firm's email giving notice of an advocate's leave was never read in full
- [run_1 pytest test_leave_notice_applied w=5] the defence firm's notice that its advocate is on leave was not applied: ['CR-26-1114']
- [run_1 pytest test_joined_counted_once w=3] the joined case was listed on its own: ['CR-26-1103', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_fees_from_the_order w=3] civil fees were not taken from the fees order: ['CV-26-0502', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_liability_batch_counted w=3] withdrawn lines on the liability order batch were charged: ['CV-26-0502']
- [run_1 pytest test_remission_officer_dates w=3] a help with fees decision signed after the officer's authorisation ended reduced a fee: ['CV-26-0503']
- [run_1 pytest test_remission_unsigned w=3] an unsigned help with fees decision reduced a fee: ['CV-26-0504']
- [run_1 pytest test_exceptions_raised w=3] raised exceptions differ: got [('CR-26-1102', 'custody time limit at risk'), ('CV-26-0503', 'remission not valid'), ('CV-26-0504', 'remission not valid'), ('CV-26-0506', 'remission not valid')]
- [run_1 pytest test_final_answer_states_fees w=5] the final answer does not state the fees due 451.00
- [run_1 pytest test_final_answer_states_listed w=3] the final answer does not say how many hearings were listed
- [run_1 pytest test_final_answer_states_unlisted w=3] the final answer does not say how many cases were left unlisted
- [run_1 pytest test_final_answer_states_bridge w=3] the final answer does not carry every step of the bridge: [1431.0, 705.0, 451.0, 451.0]
- [run_1 pytest test_final_answer_names_bridge_cases w=3] the bridge in the final answer does not name the cases at each step
- [run_1 pytest test_final_answer_states_split w=3] the final answer does not give the fees due split by type of business
- [run_1 pytest test_final_answer_states_corrections w=3] the final answer does not say how many register lines were corrected
- [run_1 pytest test_notices_sent w=5] notices differ: 29 mismatches
- [run_1 pytest test_stop_and_optin_respected w=3] a contact who asked us to stop or never opted in was messaged
- [run_1 pytest test_listing_notice_recorded w=3] listing_notice wrong on ['CR-26-1139']
- [run_1 pytest test_audience w=3] bulletin differs by 4
- [run_1 pytest test_reconciliation_rows w=5] reconciliation rows missing or wrong for ['CR-26-1103', 'CR-26-1105', 'CR-26-1131', 'CR-26-1132', 'CR-26-1134', 'CR-26-1137']
- [run_1 pytest test_reconciliation_minutes_left w=3] the reconciliation does not carry the minutes left after each listing: ['CR-26-1131', 'CR-26-1134', 'CR-26-1150']
- [run_1 pytest test_page_headline_in_full w=5] the page does not state the headline 451.0
- [run_1 pytest test_page_bridge_anchors w=3] the bridge carries 1 of its 5 anchors
- [run_1 pytest test_wiki_roster_used w=5] the printed roster was used instead of the wiki page's current version: ['CR-26-1101', 'CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1137', 'CR-26-1139']
- [run_1 pytest test_moved_sitting_applied w=5] the sitting the bench chair moved on the calendar was not moved: ['CR-26-1141', 'CR-26-1145']
- [run_1 pytest test_thread_direction_applied w=5] the court's direction passed on by the legal adviser in a thread reply was not applied: ['CR-26-1103', 'CR-26-1141', 'CR-26-1145', 'CV-26-0501', 'CV-26-0503', 'CV-26-0504']
- [run_1 pytest test_rumour_not_a_direction w=3] a remark in the chat that quotes no order and does not come from the legal adviser was treated as a direction: ['CR-26-1103', 'CR-26-1131', 'CR-26-1132', 'CR-26-1137', 'CR-26-1139', 'CR-26-1140']
- [run_1 pytest test_mail_direction_applied w=5] the court's direction the legal adviser passed on by mail was not applied: ['CR-26-1143', 'CV-26-0503', 'CV-26-0504']

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

# Final QC: submit_20261024 (yuji-final-qc 0.2.0)

**Date:** 2026-10-26.
**Target:** `submit_20261024/`, 14 bundles, 1 OpenHands run each.
**Skill:** `yuji-final-qc 0.2.0`, run unmodified from `yuji-final-qc-0.2.0.zip` (sha256 `0b8fd688…b1639`, `final_qc.py` sha256 `ce520e92…e0e81`).

## Verdict: 14 of 14 FAIL. Nothing in this folder is deliverable as it stands.

- Every bundle carries at least one **confirmed** BLOCKER. The packaging BLOCKER (F3) alone fails all 14.
- 7 of the 14 also carry a confirmed task or grading BLOCKER: 0efc4a95, 1bcdb03a, 38d4c070, 5404dcca, 99483592, a1acd72c, d269ed18.
- 5 more carry confirmed grader MAJORs (002b8c61, 2bb80c20, 5772efc0, 605132cd, c386704e).
- Only 07d3f3c5 and 32c06595 have no verified task-level defect beyond the batch-wide ones. Their open reviewer MAJORs are in Table 4.
- After the batch fixes X1 + X2 (re-package, rebuild `state_capture.py`), 32c06595 is the only task that could clear the checker without a re-run, subject to its reviewer MAJORs. 07d3f3c5 would still break the < 0.5 rule.
- 6 of the 14 also break the submit rule in `gate_and_submit.sh` (pass@1 combined < 0.5).

**How this was established:**
- The raw checker verdicts were re-checked line by line.
- Checker false positives are separated from real defects.
- Seven read-only reviewers answered the RUTHLESS §3 prompt packs.
- Every reviewer claim that carries a BLOCKER or MAJOR below was re-verified against the bundle files: marked **V**. Claims not independently re-verified are marked **R** and do not change the verdict.
- No bundle file was modified: a sha256 snapshot of all 17,946 files was identical before and after.

---

## Table 1: Per-task verdict

"Confirmed B / M" counts only verified (V) findings after checker false positives are removed. It includes the batch-wide items in Table 3.

| # | UUID | Task | pytest | rubric | combined | Raw checker | Confirmed B | Confirmed M | < 0.5 rule | Final |
|---|---|---|---:|---:|---:|---|---:|---:|---|---|
| 1 | `002b8c61` | Calderwick deck plan | 0.3755 | 0.4478 | 0.4116 | FAIL B2 M2 m7 | 1 | 3 | ok | **FAIL** |
| 2 | `07d3f3c5` | Storm Imogen event return | 0.8182 | 0.4216 | 0.6199 | FAIL B2 M1 m5 | 1 | 1 | **0.62 ≥ 0.5** | **FAIL** |
| 3 | `0efc4a95` | Blackmoss Year 7 residential | 0.5340 | 0.6500 | 0.5920 | FAIL B1 M1 m8 | 2 | 1 | **0.59 ≥ 0.5** | **FAIL** |
| 4 | `1bcdb03a` | Northlight hotel statement + rooming | 0.9052 | 0.3333 | 0.6192 | FAIL B1 M2 m5 | 2 | 3 | **0.62 ≥ 0.5** | **FAIL** |
| 5 | `2bb80c20` | Tidelines inbound loans | 0.8125 | 0.4667 | 0.6396 | FAIL B1 M1 m6 | 1 | 3 | **0.64 ≥ 0.5** | **FAIL** |
| 6 | `32c06595` | Kestrel marathon close-out | 0.3372 | 0.3108 | 0.3240 | FAIL B1 M1 m10 | 1 | 1 | ok | **FAIL** |
| 7 | `38d4c070` | Pellbridge court listing | 0.2021 | 0.7273 | 0.4647 | FAIL B2 M2 m7 | 3 | 2 | ok | **FAIL** |
| 8 | `5404dcca` | Quayside short delivery | 0.3986 | 0.6500 | 0.5243 | FAIL B1 M3 m6 | 2 | 3 | **0.52 ≥ 0.5** | **FAIL** |
| 9 | `5772efc0` | Thornfield Nurseries close | 0.6081 | 0.6790 | 0.6436 | FAIL B1 M2 m6 | 1 | 4 | **0.64 ≥ 0.5** | **FAIL** |
| 10 | `605132cd` | Wexcombe allotments | 0.0000 | 0.2436 | 0.1218 | FAIL B1 M1 m6 | 1 | 3 | ok | **FAIL** |
| 11 | `99483592` | Lamplighter S2 week 47/48 | 0.3023 | 0.1857 | 0.2440 | FAIL B2 M1 m5 | 2 | 1 | ok | **FAIL** |
| 12 | `a1acd72c` | Thornbeck compensation run | 0.1402 | 0.3288 | 0.2345 | FAIL B1 M1 m5 | 2 | 2 | ok | **FAIL** |
| 13 | `c386704e` | Thornwick Juniors registration | 0.3881 | 0.5246 | 0.4563 | FAIL B1 M1 m9 | 1 | 3 | ok | **FAIL** |
| 14 | `d269ed18` | Fernhill wedding final numbers | 0.3407 | 0.1935 | 0.2671 | FAIL B2 M1 m5 | 2 | 1 | ok | **FAIL** |

The scores are the recorded run scores. I recomputed every one independently from `ctrf.json` × `test_weights.json` (with `guard_polarity`) and from `report.rubric[]` × `judge.toml` `source_weight`. All 14 reconcile with `report.json`, `verifier/reward.json` and `pass_summary.json` to within ±0.0001 (rounding).

---

## Table 2: Raw checker findings, adjudicated

| Check | Raw sev | Tasks hit | Adjudication | Evidence |
|---|---|---|---|---|
| **F3** `result.json` reward ≠ report | BLOCKER | all 14 | **CONFIRMED** | `result.json` `verifier_result.rewards` = `{"pytest": 0.3755, "rubric": 0.4478, "reward": 41.16}`: mixed scales. The gold REF bundles are 0–1 throughout. Root cause: rewardkit writes `reward` ×100 (raw `.raw/trials_*/verifier/reward.json`: `"reward": 41.16`). The reshape normalized `reward.json`, `report.json` and `pass_summary.json` but not `result.json`. 41 of 50 local harness runs carry the bug. |
| **S2-04** instruction names machinery | BLOCKER | 002b8c61, 07d3f3c5, 38d4c070, 99483592, d269ed18 | **FALSE POSITIVE** | Every hit is a clock time (`08:15`, `09:00`, `09:45`, `18:00`, `10:00`) matched by the port regex `:[0-9]{2,5}\b` (`final_qc.py:412`). Re-scanned with `(?<!\d):`: 0 machinery hits in all 14. |
| **F2** `reasoning_effort` None | MAJOR | 002b8c61, 1bcdb03a, 38d4c070, 5404dcca, 5772efc0 | **CONFIRMED (metadata only)** | The delivered `config.json` has no `agent.kwargs`. The runtime was high: for all 5, the original `base_state.json` (same session id, byte-identical `trajectory.json`) records `reasoning_effort: "high"`. That evidence is outside the bundle, so a client QC will still fail it. |
| **S1-37** harness ≠ any REF (`tests/test.sh`) | MAJOR | all 14 | **CONFIRMED, real cause misreported** | No single REF matches all the files. `test.sh` and `claims_lib.py` match the newer REF generation (cb0dbbfc / e18698a1 / eeafd50a; canary-only diff). `state_capture.py` is the **older** generation (21b885d5 / 5b10675f / a8c4b7f1) and lacks `_candidate_logs()` / `_find_trajectory()` and the OpenHands `finish`-message capture. Score impact on these runs: none. All 14 graded `final_message.md` equal the agent's `finish` message. |
| **S1-37** `claims_lib.py` differs | MINOR | all 14 | **FALSE POSITIVE** | An artefact of "closest REF = 21b885d5": `claims_lib.py` is byte-identical (canary stripped) to cb0dbbfc, e18698a1 and eeafd50a. |
| **F4** `mcp__finish` outside wired tools | MAJOR | 5404dcca | **CONFIRMED, harmless** | Step 98 called the non-existent `mcp__finish` and got "Tool not found"; step 99 called `finish` correctly. No effect on state or score, and not reward hacking. Needs a recorded waiver or an explanation. |
| **F7** check crashed | (not checked) | 07d3f3c5, 32c06595 | **CHECKER BUG** | `AttributeError: 'str'/'list' object has no attribute 'get'` on `reported.claims`. This is still present in 0.2.0, so the reviewer lines for those two runs come from the manual review below. |
| **S4-40** redundancy 0 % | (cleared) | all 14 | **FALSE NEGATIVE** | Reviewers found the same final-answer figures charged in pytest, in rubric positives and in rubric negatives in every task. The composite similarity metric misses short numeric facts. See Table 5. |
| S3-40 ANSWER_LEAK | MINOR | 9 tasks | False positive | The IDs and terms are all visible in agent-reachable source data (reviewers checked each one). |

**Calibration (reproduced):** the 6 REF bundles in yuji-trajectories gave gold 21b885d5 / 5b10675f / a8c4b7f1, plus cb0dbbfc and e18698a1: PASS B0 M0; eeafd50a: FAIL M1 (S1-41). This matches the package's own calibration record exactly. Report: `calibration/INDEX.md`.

---

## Table 3: Batch-wide defects (fix once, affects many)

| ID | Sev | Defect | Scope | Evidence | Fix |
|---|---|---|---|---|---|
| X1 | **BLOCKER** | `result.json` reward on a 0–100 scale | all 14 | Table 2, F3 | Fix the reshape/packaging step to divide `verifier_result.rewards.reward` by 100 (or copy it from `reward.json`), then re-package. Do not hand-edit. |
| X2 | MAJOR | Mixed harness generations (`state_capture.py` is old-gen) | all 14 | Table 2, S1-37 | Rebuild `environment/state_capture.py` from REF cb0dbbfc with the task's own APP_URLS block. |
| X3 | MAJOR | `config.json` missing `reasoning_effort: high` | 5 tasks (Table 2, F2) | Table 2, F2 | Re-run those 5 with `OPENHANDS_REASONING_EFFORT=high` recorded. They need re-runs anyway (Table 4). |
| X4 | **BLOCKER where graded** | **MS Teams cannot be discovered.** `list_joined_teams` raises `KeyError 'member_ids'`: `microsoft_teams.py:112` reads `t["member_ids"]` and the base corpus `team_001` (`corpus/state.yaml:95`) has none. Team ids (`19:team-…@thread.tacv2`) appear in no other agent-reachable file. | Server code and corpus are byte-identical to the client REF (a client bug). **All 14** bundles seed Teams messages. Graded facts proven Teams-only: 1bcdb03a, d269ed18. | d269ed18: 38 Teams calls, 36 failed (3× KeyError, 31 `get_team` guesses). 1bcdb03a: KeyError at step 77. | Move any graded fact out of Teams, or print the team id in an agent-reachable paper. Report the bug to the client. For the other 12, confirm Teams holds only noise. |
| X5 | MAJOR (risk) | The D4 server-call replay (`_merge_server_calls`, our own grader fix) can order writes wrongly. Tests then judge replayed state that contradicts `end_env.json`. | Present in all 14 `test_outputs.py`. Proven wrong in 0efc4a95. | Table 4, 0efc4a95 | Judge final record values from `end_env.json`; anchor replay inserts by time, never before the current anchor. |
| X6 | MAJOR (risk) | "The working folder" is never pinned. The client `claims_lib._SKIP_DIRS` drops `work/` and `data/` (and the task graders also drop `/data/`). | Proven in c386704e (`/workspace/work/`) and 5772efc0 (`/workspace/data/Nursery/working/`): deliverables invisible to the grader. | Table 4 | Name the exact output path in every instruction (e.g. "directly in /workspace, not a subfolder"). |
| X7 | MINOR (advisory) | The same final-note figure is charged up to 5 times: pytest test, pytest guard, rubric positive and rubric negative. | All 14. Worst: 38d4c070 fees ×5, 5404dcca invoice value ×5, 32c06595 team total ×4. | Reviewer pairs per task | Keep each figure in one channel; drop mirrored rubric negatives. By the playbook's §4 threshold (≥ 50 % MAJOR) this stays below MAJOR, but a client reviewer will see it. |

---

## Table 4: Per-task confirmed defects (task-specific)

V = re-verified by me against the files. R = reviewer finding not independently re-verified (listed, not counted).

| Task | Sev | V/R | Defect | Evidence | Fix |
|---|---|---|---|---|---|
| **002b8c61** | MAJOR | V | TSF-2291 is never graded. TRUTH creates `['TSF-2290','TSF-2291']` (TRUTH.md:65), but "2291" appears 0 times in `test_outputs.py` and `judge.toml`. | grep | Add a test and a criterion for the TSF-2291 line. |
|  | MAJOR | R | Missing that one late booking fails about 18 rule tests (the `_focus` relief covers only the `hr2` variants). Reviewer estimates +68/277 pytest unfair. | test_outputs.py:784-820 | Add a `no-2291` variant, or judge each rule on its own vehicles. |
| **07d3f3c5** | MAJOR | R | "Declined" vs "Not covered" for failed gust tests is ambiguous (AM-CAT-03 §3 vs §5), and it decides pass or fail: about 0.73 under the agent's reading. | reviewer | Say "headed Declined" in §3. |
|  | MAJOR | R | Heading-only errors also fail `test_register_values`, `test_lapse_and_reinstatement` and `test_loss_time_decides`. | test_outputs.py:997-1063 | One test per fact. |
| **0efc4a95** | **BLOCKER** | V | The grader fails a correct register. `end_env.json` lines KR-7B18 / KR-7D13 / KR-7D17 **equal `reg_want` field for field**, yet `test_register_all_lines_right` (5) fails with "3 register lines wrong". The D4 replay puts the stale writes last. The 3 line tests (1 each) are also affected. | end_env vs oracle | X5 |
|  | MAJOR | R | The receipts change silently on the agent's first save; "nothing announces either" (TRUTH.md:123). | airtable.py:21-62 | Announce it in a finance note. |
| **1bcdb03a** | **BLOCKER** | V | SP-609's withdrawal exists **only** in Teams ("SP-609 (Oona Pohl) has withdrawn… do not house them"), and Teams is unreachable (X4). The oracle excludes SP-609 from holds; the agent held SP-609 in RM-4199, so `test_room_holds`, `test_logistics_contact` and `test_audience_members` (5 each) fail. | world_data, end_env, ctrf | X4 |
|  | MAJOR | V | TRUTH.md contradicts itself: line 6 says the statement is GBP 6725.20, line 92 says NL-2619 "belongs in the 6780.40 statement". | TRUTH.md:6, :92 | Fix line 92. |
|  | MAJOR | R | Rubric id 8 lists six reservations, but the oracle also puts NL-2620 under "Not guaranteed". Pytest accepts the earlier full note (D6) while the rubric reads only `final_message.md`. | judge.toml:142, test_outputs.py:460-492 | Align. |
| **2bb80c20** | MAJOR | V | Grader bug: on the agent's note "Confirmed / not confirmed \| 31 / 4", the regexes give confirmed = {} and not-confirmed = **{31}**, so `test_final_objects_counted` fails. `test_final_vehicles` misses "## Vehicles / 14 travel". | replicated with `_final()` | Accept table and heading forms. |
|  | MAJOR | V | Rubric criteria demand detail the instruction never asks for. #8 failed only for not naming "Daniel Carrow", #12 only for not naming "Olwen Pryce", #22 only for bridge **order**. The judge's own justifications say this. | report.json rubric | Grade the substance. Reviewer estimate: the run moves from 0.640 to about 0.717 (> 0.7 threshold), so it would flip to pass. |
| **32c06595** | MAJOR | R | "Send me a note" is ambiguous: the agent emailed a full note to Bethan, and the graders read only the final reply; `_notices` counts that email as a runner notice. Rubric #35 was charged from the HTML or dossier, not the note. | test_outputs.py:491 | Pin the note channel. |
|  | MINOR | V | Invoices are checked on line amounts only; `Total` / `LineAmountTypes` are ignored (agent invoices are Exclusive +10 % tax). Tax treatment is never specified, so this is not a proven error. | end_env Xero | Check `Total`. |
| **38d4c070** | **BLOCKER** | V | The decisive source is future-dated. The scenario is "Monday 9 November 2026"; building notice EA-1611 is Zendesk ticket 73972, `created_at 2026-11-12T09:05:00Z`. The EA-1611-ignored total 951.0 is in `wrong_totals`. | LightZendesk.json, oracle | Date the source ≤ 8 Nov and give it standing. |
|  | **BLOCKER** | V | Contradictory expectations. The oracle raises 3 items (`raise`, TRUTH.md:50), but TRUTH.md:69 and judge.toml:261 require 4 (adds CV-26-0506). No agent can satisfy both. Run_1 raised 4: the rubric passed, `test_exceptions_raised` (3) failed and `test_guard_exceptions_misworked` (−5) tripped. | oracle / TRUTH / judge.toml | Align to one answer. |
| **5404dcca** | **BLOCKER** | V | The expected answer rests on superseded terms. The re-quarantine rule ("superseded by a later verified inspection in qc_inspection_events") exists only in TT-4 **second** edition, whose header says "SUPERSEDED by the third edition". The third edition in force says "A lot comes off quality hold when the QC inspection log shows it released and verified." The agent followed the third edition (TRUTH.md:123/203). | both docx | Put the rule in the third edition. |
|  | MAJOR | V | Table 2, F4 (`mcp__finish`), harmless, needs a waiver. | traj step 98 | Waive with a note. |
|  | MAJOR | R | The `source_contexts` relief can never fire (key format mismatch); `test_page_table_rows_and_sorting` requires 72 QO refs that weren't asked for. | reviewer | Fix keys / drop the column. |
| **5772efc0** | MAJOR | V | Deliverables were written to `/workspace/data/Nursery/working/` (step 62). `_delivered` / `_written` drop `'/data/'` (test_outputs.py:813-821), so every page and dossier test says "no page was delivered". | trajectory, tests | X6 |
|  | MAJOR | V | False pass: `test_final_answer_states_corrections` (3) passed on the heading "## 11. In the working folder"; the agent actually wrote "**10 lines put right**" (final_message.md:35 vs :122). `_count_stated` matches any bare number. | tests :462 | Anchor the number to "lines". |
|  | MAJOR | R | Rubric #24 / #29 were failed on missing literal words ("scanned", "2.65"). Reviewer estimate: the location + judge fixes move the run to about 0.70, at the threshold. | report.json | Reword. |
| **605132cd** | MAJOR | V | `test_reconciliation_rows` rejects correct unlet rows: `'accept' in c.lower()` matches "no applicant still waiting **accepts**" (QF-36) and "**accepting**" (QF-12). | test_outputs.py:1112, recon csv | Match the outcome column exactly. |
|  | MAJOR | V | `test_guard_messaged_without_consent` (−5) charges W-1033, who is `opted_in: true` and on no stop, not-opted or held list. A wrong-let offer is mislabelled as a consent breach. | test_outputs.py:1195-1203 | Scope the guard to consent only. |
|  | MAJOR | R | `_delivered` needs "dossier" / "reconcil" in the filename, which the instruction doesn't ask for. | test_outputs.py:866-879 | Name the files. |
| **99483592** | **BLOCKER** | V | A correct agent fails `test_welfare_referrals_all_right` (w5). Tamsin Okafor's correct row has `referred_to: "Ruairi Brannigan"`, who is also a crew name, so two names match and the row is rejected as "other". The end state holds exactly the 2 Open week-47 rows TRUTH wants. | test_outputs.py:877, end_env | Match `crew_id` / `crew_name` only. |
| **a1acd72c** | **BLOCKER** | V | TRUTH counts Monday 31 Aug (a bank holiday in the task's own `Working_days_and_bank_holidays_2026.txt`) as a working day. For 7 jobs (RJ-25264, 25330, 25447, 25509, 25548, 25624, 25652) the oracle's clock → target span is 20 working days **only** if 31 Aug counts (19 if skipped), so every target is a day early. Reviewer recompute: the correct totals are late £866 / total £1,076 / transfers £945, against TRUTH's 878 / 1088 / 957. | oracle `assess` | Recompute with the bank holiday and regenerate. |
|  | MAJOR | V | `_WRITE_OK` (test_outputs.py:1365) omits `LightSlack chat_update`, so editing its own permitted post (step 107) trips `test_guard_writes_elsewhere` (−5). | tests, traj | Add it. |
|  | MAJOR | R | Planted RJ-25364 van-breakdown evidence (missed appointment under RSS 9.2) is ignored by TRUTH. | Zendesk 911205 | Model it or remove it. |
| **c386704e** | MAJOR | V | All 3 deliverables were saved in `/workspace/work/`, which `_SKIP_DIRS` drops (claims_lib.py:34): 9 pytest points lost on files that exist. | artifacts, claims_lib | X6 |
|  | MAJOR | V | Invoices are graded from calls, not state. `_invoices()` counts 57 `create_invoice` calls across 2 sessions (the logout wiped state and the agent rebuilt), while `end_env` holds 28 `TJ26-FAM` invoices. `test_sibling_discount` fails with a false message. | test_outputs.py:582-590 | Grade from `end_env`. |
|  | MAJOR | R | Negative "says Kieran Lowther is registered for the U14s" is literally true of Brindlecombe's U14s (also flagged in the 25 Oct QC). Positives demand SR- refs that weren't asked for. | judge.toml | Reword. |
| **d269ed18** | **BLOCKER** | V | Three claims the agent must rule on ("minimum numbers don't apply", "don't charge for the band's meals", "service charge on everything") are posted only in the Teams staff channel, which is unreachable (X4). | world_data Teams, traj | X4 |

---

## Table 5: Run-grading fairness (pass/fail reliability of the recorded runs)

The memory rule from 2026-10-24 applies: grading-fairness risk is reported once with evidence and does not by itself block. The rows below where the defect is a grader **bug** (V) are counted as defects in Table 4.

| Task | Recorded combined | Fair-graded estimate | Pass/fail flips? | Basis |
|---|---:|---:|---|---|
| 1bcdb03a | 0.619 | ≈ 0.70–0.93 | **likely flips to PASS** | Teams-only SP-609 (V); rubric reads only the pointer message (R) |
| 2bb80c20 | 0.640 | ≈ 0.717 | **likely flips to PASS** | regex bug (V) + name/order rubric demands (V) |
| 5404dcca | 0.524 | ≈ 0.95 (R) | **likely flips to PASS** | expected answer follows superseded terms (V) |
| 5772efc0 | 0.644 | ≈ 0.70 | borderline at 0.7 | data/ folder (V), over-literal rubric (R), one false pass (V) |
| 38d4c070 | 0.465 | ≫ 0.6 (R) | possibly | future-dated EA-1611 (V), contradictory exceptions (V) |
| 0efc4a95 | 0.592 | ≈ 0.61 | no | replay bug (V), offset by a hidden genuine guard |
| c386704e | 0.456 | ≈ 0.62 | no | work/ skip (V), call replay (V) |
| 07d3f3c5 | 0.620 | ≈ 0.73 under the agent's reading (R) | possibly | heading ambiguity |
| a1acd72c, 99483592, 605132cd, d269ed18, 32c06595, 002b8c61 | ≤ 0.46 | still < 0.5 | no | genuine agent errors dominate, but the TRUTH or grader bugs above must still be fixed |

**Consequence:** for at least 3 tasks the recorded "hard" score is produced by task or grader bugs, not by model failure. Those runs cannot be delivered as difficulty evidence even after re-packaging.

---

## Table 6: What checked out (CLEARED, verified)

| Area | Result |
|---|---|
| Run identity | OpenHands SDK, `claude-opus-5`; 1 run each, none errored; trajectories complete; `final_message.md` equals the agent's `finish` message in all 14 |
| Judge | Ran in all 14: codex / `gpt-5.6-sol`; criteria count = judge.toml; no errored criteria |
| Arithmetic | pytest, rubric and combined recomputed independently; all reconcile (±0.0001) across report.json, reward.json and pass_summary.json |
| Rubric drift | 0: every id, description, \|source_weight\| and sign in report.rubric[] matches judge.toml. Negative/positive weight ratio 0.12–0.33 (no penalty dominance) |
| Hygiene | No secrets, no symlinks, no stray files, no `.DS_Store`; largest bundle 23 MB |
| Uniqueness | No near-duplicates: maximum shared test-name Jaccard < 0.20 for every pair |
| Leakage | No answer figure in instruction.md; ANSWER_LEAK flags are false positives |
| Oracle / nop | No `trajectories/qc/oracle_nop_report.md` in any bundle (F8 MINOR, as the skill allows) |

---

## Required actions, in order

1. **Fix the packager (X1)** so `result.json` reward is 0–1. Fix `state_capture.py` to the current REF generation (X2).
2. **Fix the content BLOCKERs:**
   - 0efc4a95 and the replay helper (X5)
   - 1bcdb03a and d269ed18 (Teams, X4)
   - 38d4c070 (dates, exceptions)
   - 5404dcca (third-edition rule)
   - 99483592 (welfare test)
   - a1acd72c (bank holiday)

   Also fix the V-marked MAJORs in Table 4, and pin the output folder in every instruction (X6).
3. **Re-run every changed task** with `OPENHANDS_REASONING_EFFORT=high` recorded in config.json. Every BLOCKER above changes TRUTH or a grader, so the recorded runs no longer correspond to the task.
4. **Re-apply the submit rule (< 0.5)** on the new scores. 07d3f3c5, 0efc4a95, 1bcdb03a, 2bb80c20, 5404dcca and 5772efc0 already exceed it with their current scores.
5. **Re-run this QC** (command below) and accept only B0 M0, with S2-04 clock-time hits and S1-37 claims_lib MINOR noted as known checker false positives.
6. **Delete `_FINAL_QC_20261026/` from this folder before upload.** It is not part of any bundle.

## Reproduce

```bash
PY=yuji-harness-2-local/.harbor/bin/python3   # Python 3.12
QC=<unzipped>/yuji-final-qc-0.2.0/skill/scripts/final_qc.py
$PY -I $QC submit_20261024 --out <out> --ref <yuji-trajectories REF folder, 6 bundles> --agent openhands --model claude-opus-5
$PY -I _FINAL_QC_20261026/scripts/recompute.py submit_20261024    # independent score reconciliation
```

## Files in this folder

- `FINAL_QC_REPORT.md`: this report.
- `checker_raw/`: unmodified 0.2.0 output (INDEX.md, 14 × `<uuid>-final-qc.md`, 14 × `<uuid>-llm-review.md`).
- `calibration/INDEX.md`: 0.2.0 on the 6 REF bundles.
- `scripts/`: `recompute.py` (score reconciliation), `refdiff.py` (harness file vs each REF), `teams_only.py` (Teams reachability scan).

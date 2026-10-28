# RUTHLESS QC — submit_20261024 (14 bundles), 2026-10-27

Playbook: `RUTHLESS_QC.md`. Each bundle has its own grader and rubric, and each was audited in full by one of seven parallel reviewers. Two kinds of evidence back the findings:

- **Re-grading.** Every genuine finding was proven by re-grading the recorded opus run with the bundle's own tests. The helper is `/tmp/qc/ruth24/regrade.py`. It rebuilds the trajectory as `tests/test.sh` does, uses the run's original server tool-call log, and runs the ledger. It reproduces the recorded pytest score exactly for all 14 runs.
- **Quotes.** Where re-grading doesn't apply, the finding rests on exact quoted text.

Proof files are under `/tmp/qc/ruth24/<uuid8>/`. The bundles were not modified.

## VERDICT: FAIL (all 14)

There are two layers to the verdict.

1. **Format-level (same in all 14).** RUTHLESS C1, C3 and C5 FAIL, plus C4 strictly and the Overlap check. The pytest layer reads delivered files, grades the end state and checks the final-note figures. The Yuji format requires exactly this: yuji-task-qc §2b and §13 drop RUTHLESS C1–C5, and the gold sample does the same. C4's write-call tally passes in every bundle (15–50 write tests each).
2. **Genuine defects (wrong under any standard).** Listed below, together with what each did to the recorded run.

| Task | Recorded | Main genuine defects | Estimated score after grader fixes | Verdict changes? |
|---|---:|---|---:|---|
| 002b8c61 | 0.412 | CRIT: missing TSF-2291 (buried mail input, no variant) cascades into ~25 unrelated rule tests with false messages. MAJ: largest .html taken as the page; .pdf dossier not found; one fact charged up to 4× | ~0.55–0.58 | no |
| 07d3f3c5 | 0.620 | MAJ: the `finish` text replaces the agent's 10.5k-char report (test.sh `_atif`). MAJ: heading wording charged by 5 tests. MAJ: documented `comment_author_id` counts as an "other write" (−5). MAJ: browse-only agent scores 0.23 | ~0.77–0.82 | **FAIL → PASS** |
| 0efc4a95 | 0.592 | CRIT: order-blind server-log merge applies stale register writes last (correct end state graded wrong). MAJ: one mistake cascades (`test_reconciliation_rows` unwinnable on refunds; rubric #3/#29 and #4/#30 double charges). MAJ: rubric #6 over-credited (cheque created then deleted) | ~0.57 (the fix also reveals a genuine guard), ~0.63 without double counting | no |
| 1bcdb03a | 0.619 | CRIT: SP-609 withdrawal only in Teams (crashes) → removing it gives pytest 1.0. MAJ: rubric #8 omits NL-2620 (contradicts oracle; 2,882 needs it). MAJ: pytest grades the earlier full note but the judge sees only the finish text (47/99 rubric points lost). MAJ: browse-only agent scores 0.256. MIN: TRUTH L92 says 6780.40 | 0.70 (Teams/#8 fixed); ~0.93 if both channels read the same note | **FAIL → PASS** |
| 2bb80c20 | 0.640 | CRIT: 12 rubric fails demand detail the prompt never asks (lender/contact names, bridge order, per-object premiums). MAJ: count regexes miss "Confirmed / not confirmed \| 31 / 4" and "Vehicles / 14"; courier-grouped notes fail; restraint test re-charges guards | ~0.88–0.92 | **FAIL → PASS** |
| 32c06595 | 0.324 | MAJ: emailed note counted as a runner notice and ignored by the judge; surnames not accepted; outcome-count regex needs a dash; restraint double charges. The run genuinely failed (never re-read donations) | ~0.37 | no |
| 38d4c070 | 0.465 | CRIT: deciding notice EA-1611 dated 12 Nov (scenario 9 Nov), and order DJ/26/0527 dated 11 Nov. CRIT: 3 vs 4 raised (oracle/pytest vs TRUTH:69 and rubric R15). MAJ: source-context relief fails on two misses; pytest reads only the chat note; one miss charged many times | ~0.83 if the no-EA reading is correct; ~0.47 if the sources are re-dated instead | depends on the fix |
| 5404dcca | 0.524 | CRIT: oracle excludes L-877 via a rule found only in the superseded 2nd edition (3rd edition + CSV log say released); QC-877-2 dated after the scenario time. CRIT: source_contexts key can never match. MAJ: 72 unrequested QO refs in the table; `_NDEL` misses "4 not" | ~0.96 | **FAIL → PASS** |
| 5772efc0 | 0.644 | CRIT: output location never stated; grader silently drops `data/` and `work/` (7 tests, 23 pts). MAJ: free pass on "## 11." heading; split credit fails the bridge; rubric #24/#25/#29 want literal words | ~0.705 | **FAIL → PASS (borderline)** |
| 605132cd | 0.122 | CRIT: `'accept' in c` fails correct "not let" rows. MAJ: file-name words not in prompt; consent guard (−5) fires on an opted-in applicant; wrong-rent guard reads a subtotal; one decision trips 3 guards (clamped to 0) | ~0.16 | no |
| 99483592 | 0.244 | CRIT: welfare test rejects correct rows (referred_to is a crew name). MAJ: total only accepted inside `<h1>`; dossier status matched anywhere; graded note is the finish stub not the full note. MIN: `wrong_totals` incomplete | ~0.37 | no |
| a1acd72c | 0.235 | CRIT: oracle and test helpers count the 31 Aug bank holiday (8 rows, 17 tests, rubric #1/#2/#14 wrong). CRIT: planted RJ-25364 missed appointment (RSS s.9.2) ignored. A fully correct agent scores 0.34 as shipped. MAJ: own Slack edit trips −5; dossier needs ref and amount on one line; 45/73 rubric points ask the reply for dossier content | ~0.27 (0.36 with the rubric reworded) | no |
| c386704e | 0.456 | CRIT: claims_lib `_SKIP_DIRS` drops `work/` (the prompt says "working folder"): 9 pts. CRIT: replay counts writes from a discarded session (false duplicates, 2 guards). MAJ: rubric #3/#10 want SR ids not asked; negative #27 misfires on a quote; `_money_in` needs pence; RH-26 s.4 contradicts the oracle on age groups | ~0.64 | no |
| d269ed18 | 0.267 | CRIT: rubric #27 grades a Teams-only instruction (unreachable). MAJ: a £0 infant line fails `invoice_exact`; rubric negatives #29–#32 mirror positives #1–#4; full note at step 89 not graded | ~0.31 | no |

## Batch-wide genuine defects (one fix each, several tasks)

1. **The final message is only the `finish` text.** When the agent writes its full report in an earlier step and the finish text says "my note is in the previous message", the report is never graded. Hits 07d3f3c5, 1bcdb03a, d269ed18 and 99483592. Fix: in test.sh `_atif` and claims_lib `atif()`, join the last substantial agent message with the finish text, and give the judge the same text.
2. **The deliverable folder is never pinned, and the grader drops `data/` and `work/`.** Hits 5772efc0 and c386704e, latent elsewhere. Fix: state "save directly in /workspace" in the instruction, and remove `'data'` and `'work'` from `_SKIP_DIRS` (claims_lib L34).
3. **Teams is unreachable** (`list_joined_teams` KeyError `member_ids`). Hits 1bcdb03a and d269ed18. Fix: repair the Teams world, or move the facts to another app.
4. **Rubric/pytest double counting.** The same figure is graded in pytest, a pytest guard, a rubric positive and a rubric negative, up to 4–5×. All 14 are affected. Fix: grade each fact in one channel and drop the mirrored negatives.
5. **Rubric over-specification.** Criteria fail notes for names, literal words or orderings the prompt never asks for. Hits 2bb80c20, 5772efc0, c386704e, 99483592, a1acd72c, 002b8c61 and 07d3f3c5.
6. **Read-only reward not gated on work.** A browse-only agent scores 0.256 in 1bcdb03a and 0.23 in 07d3f3c5. Fix: gate the read tests on a write, as 0efc4a95 does with `_worked()`.
7. **`wrong_totals` incomplete against TRUTH's listed misreadings.** Hits c386704e, 99483592 and a1acd72c, so the misread guards miss real misreadings.

## What checked out (CLEARED, all 14)

- The oracle values were recomputed independently from agent-visible data in every task. They match, except the defects named above (a1acd72c bank holiday, 5404dcca L-877, 38d4c070 dating, 1bcdb03a rubric #8 and TRUTH L92, c386704e RH-26 s.4).
- A do-nothing run scores 0.0 everywhere.
- No guard misfires in an ideal run.
- Penalty totals never exceed the positive weight.
- Most tripped guards in the recorded runs were real violations. The misfires are listed in the table: 0efc4a95, 605132cd ×2, a1acd72c, c386704e ×2, 07d3f3c5, 38d4c070 ×4 (under the no-EA reading) and 5404dcca ×3.

## Bottom line

- **Five recorded runs would cross 0.7 once their grader or oracle defects are fixed:** 07d3f3c5, 1bcdb03a, 2bb80c20, 5404dcca and 5772efc0. For 38d4c070 it depends on how the dating defect is fixed. For these tasks the recorded scores measure the bugs, not the model.
- **Eight runs fail genuinely even after the fixes:** 002b8c61, 0efc4a95, 32c06595, 605132cd, 99483592, a1acd72c, c386704e and d269ed18. Their defects still need fixing for correctness.
- Every task changed by these fixes needs a new model run before delivery.

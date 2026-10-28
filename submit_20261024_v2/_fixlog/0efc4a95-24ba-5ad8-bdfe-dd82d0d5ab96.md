# Fix log: 0efc4a95-24ba-5ad8-bdfe-dd82d0d5ab96 (Blackmoss Year 7 residential)

Fixer pass of 2026-10-28, on `submit_20261024_v2/` only. Audit: `/tmp/qc/ruth24/0efc4a95/REVIEW_FROM_AUDIT.md`.

## Changes

| # | File | What | Why (finding) |
|---|---|---|---|
| 1 | `tests/test_outputs.py` `_merge_server_calls` | Rewrote the pairing of server-log calls with trajectory steps. It is now an order-preserving alignment (longest common subsequence over app, tool and arguments, with the same truncated-payload rule as before). Log-only calls are inserted after the trajectory step matched just before them in log order. | Audit CRITICAL 1. The old greedy `idx.pop(0)` paired a script's 08:49:57 `list_records(bank_receipts)` with the agent's identical direct call at step 141 (08:57:53). That moved the anchor forward, so the stale 08:53:45 register writes were replayed after the 08:59:48 corrections. The new pairing needs no timestamps, so `test.sh` (harness-owned) is untouched. It reproduces the audit's timestamp-patched result exactly (0.5728). |
| 2 | `tests/test_outputs.py` `_base()` | The register and vehicles values are now overlaid from the end-state snapshot (`end_env`) when it carries them. The write lists (which lines were written) still come from the calls. | Audit CRITICAL 1, second half: the end state is authoritative, so a correct end state can never be graded wrong because of how the calls were replayed. |
| 3 | `tests/test_outputs.py` `test_reconciliation_rows` | Removed the line `ok = ok and _card_refund_of(p) == card`. | Audit MAJOR 2: one mistake cascaded. The CSV is now checked against the settlement only; refunds actually made are graded by the card-refund tests. |
| 4 | `tests/test_outputs.py` / `test_weights.json` | Removed `test_final_refund_total` (5), `test_final_counts`, `test_final_refund_split`, `test_final_bridge`, `test_final_vehicles`, `test_final_centre_numbers` and `test_final_changes` (1 each). `test_final_names_created_records` is kept. Positive total is now 92 (was 103); component weight is 1.879. | Batch fix 4 and audit Overlap table. Rubric #1, #2, #9, #10 and #12 grade the same note figures, and the rubric criteria for each pupil grade the changes. The note is now graded once, by the rubric. This also removes the coupling of action and note that made `test_final_refund_total` fail on a correct note (audit MAJOR 2). |
| 5 | `tests/test_outputs.py` `test_policies_read` | Now gated on `_worked()`. | Batch fix 6: it was the only read test not gated on a write. |
| 6 | `tests/test_outputs.py` `test_dossier_names_evidence` | `49-seat` and `email only` are now matched by wording-tolerant patterns (`49 seat`, `49-seater`, `email-only`, `only by email`, `not to be texted`, ...). Record ids are still matched literally. | Batch fix 5: the prompt does not dictate that wording. |
| 7 | `tests/oracle.json` `reported.wrong_refunds` | Added `1630.00` and `1890.00`. | Batch fix 7. TRUTH lists the receipts-read-once misreading (1890.00), which no guard covered. 1630.00 is the half-corrected reading: BR-2207 is seen as moved but the run settles before the fifth save, so KR-7D13 stays not going with a 130.00 refund. Recomputed from `card_of`, `cash_of` and `bank_ok`. |
| 8 | `tests/reward/rubric/judge.toml` | Rebuilt in the same compiled layout. **Dropped** #3, #5, #6 and #29, #30 (actions graded by pytest card-refund, centre and cheque tests; #29 and #30 were also mirrors of #3 and #4), plus #4 and #27 (#4 is the notices pytest grades; #27 duplicates `test_guard_misread_refunds_stated`, which now covers 1890 and 1630). This also fixes the #6 over-credit (audit MAJOR 3). #17 was dropped as over-specified (a per-pupil card/cheque split the prompt does not ask for). **Reworded** #13 (no per-pupil split), and #19, #23, #24, #26 so that each answers one staff-channel claim ("say whether it stands and which paper decides it"); #24 no longer demands naming the three sibling pupils. **Added** the alphabetical-coaches claim (+1) and two trap negatives: `n-note-says-isla-brennan-going` (deputy-head bait, -3) and `n-note-says-kr-7b12-going` (voicemail withdrawal, -3). Result: 25 criteria, positive total 40, 3 negatives (-9), all `[final answer]`. | Batch fix 4 (one channel per fact; at least 20 criteria; at least 3 negatives), batch fix 5, audit MAJOR 2 and MAJOR 3. |
| 9 | `instruction.md` and its rubric copy (byte-identical) | Files are "saved directly in /workspace (not in a subfolder)". The closing note must be written "in your closing message itself, not in an earlier message or only in a file". | Batch fixes 1 and 2. |
| 10 | `task.toml` `[task.metadata]` | `multimodal = false`. Added `receipts-half-corrected` and `receipts-read-once` to `wrong_figures`. `verification_explanation` updated to the new grading (pairing in order, end-state overlay, note graded by the rubric). | Batch fixes 7 and 8 (S2-27). |
| 11 | `solution/TRUTH.md` | Documented the half-corrected misreading (1630.00) and that both misread totals are in `wrong_refunds`. | Batch fix 7. |

Not changed:
- `test_restraint_only_what_the_settlement_needs` (3) still fails whenever a guard fires. This is a deliberate design inside pytest; see the open questions.
- Audit minor #4: `test_bank_receipts_read_again_before_refunding` credits a log-only read without its response. The read is real and timed correctly. Whether the run used it is graded by the refund and notice tests.

## gt_env.json "stale" question: not stale for this bundle

- `solution/gt_env.json` has BR-2211 = KR-7D13, `payer_reference "KHAN O"`, `received_on 2027-02-04`. That is exactly this bundle's world after its own rule:
  - `world_data/LightAirtable.json` seeds BR-2211 on KR-7D13, "KHAN O", 2027-02-08.
  - `software/LightAirtable/airtable.py` wave 2 sets only `received_on` to 2027-02-04, after the fifth register save.
- The recorded opus run's `end_env` shows the same values.
- The "fresh oracle run" with `"KHAN O 7D"` is `~/.cache/yuji-qc/jobs/new10j-0efc4a95-…-oracle`. Its config points at `/tmp/qc/new10j/0efc4a95…` (a copy of `new_10_20261024/`). That is the factory's later **pass 3** of this task, a different world design:
  - BR-2211 is seeded on KR-7A10 "KHAN" with date 4 Feb.
  - Wave 2 re-matches it to KR-7D13 "KHAN O 7D".
  - `_factory/STATUS.md` (2026-10-25 19:00) says submit holds the pass-2 version.
- `oracle.json` is identical in both versions. `solve.py` differs only in the dossier and closing text. gt_env matches `reg_want`, `veh_want` and the cheques line for line.
- **REBAKE is not needed for this reason.** Caveat: no live Harbor oracle trial of *this* (pass-2) world exists. The only one is the pass-3 run above. The pipeline's live oracle run will also re-prove S5-16.

## Verification

- `check_task.sh`: only S1-37 and S1-39 rows remain (was: plus S2-27). The "to read" item `tests/claims_lib.py` was read: it is the harness `finish`-message handling and needs no action.
- Recorded opus run (pytest, `regrade.py`):
  - **0.5340 → 0.6630** (earned 69 of 92, charged 8).
  - Step 1 (pairing fix alone) gives 0.5728. These now pass: `test_register_all_lines_right`, the three finance-correction line tests and `test_bank_receipts_read_again_before_refunding`. `test_guard_refund_beyond_due` (-5) now fires: genuine, on the 130/60/130 refunds made to the charges of 7B18, 7D13 and 7D17.
  - Step 2: `test_reconciliation_rows` passes (the CSV was right). The seven note tests left the pytest channel (four of them had failed on the action coupling).
  - Still missed, all genuine:
    - card refunds (all + 3 none);
    - notice texts (all + 2 none);
    - the first centre email's numbers;
    - restraint.
  - Guards: refund_beyond_due and duplicate_messages.
- Rubric (no judge run): mapping the recorded verdicts onto the unchanged criteria gives ≥ 0.85, against 0.65 before. The reworded and new criteria are not yet judged (up to +0.15).
- Browse-only run (`/tmp/qc/ruth24/0efc4a95/traj_browse.json`): 0.0000. Empty run: 0.0000, no guard fired.
- Oracle: the only live trial (`new10j…-oracle`, pass-3 world, same `oracle.json`) re-graded with the fixed tests gives **pytest 1.0000**, no guards. The v2 `solve.py` does the same calls. Its closing note meets all 22 rubric positives and none of the 3 negatives (read against the new criteria).

## REBAKE: no

No change to `world_data`, `task_data` or `solve.py`.

## Open questions for the user

1. With action criteria moved out of the rubric, the recorded run's estimated reward is about 0.5 × 0.663 + 0.5 × (0.85 to 1.0), roughly 0.76 to 0.83: above 0.7. This is despite real, irreversible errors: 3 wrong card refunds, 2 families wrongly told their child is not going, and a wrong first centre email. Is a `gate` (for example, no tripped -5 guard) or a heavier action weight wanted?
2. `test_restraint_only_what_the_settlement_needs` (+3) charges again any run in which a guard fired. Keep it (the author's design) or drop it?
3. A live oracle and nop of this pass-2 world have never been run; the only live oracle is of the pass-3 bundle in `new_10_20261024/`. Which version is meant to ship?

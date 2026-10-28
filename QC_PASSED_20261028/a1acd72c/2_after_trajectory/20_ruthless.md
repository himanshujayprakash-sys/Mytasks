VERDICT: PASS
Critical/blocker: 0 · Major: 1 · Minor: 8

# RUTHLESS QC: a1acd72c-ccb0-5eb6-9893-691b1872e0ef (Thornbeck Homes, October 2026 repairs compensation run)

Audited copy: `$TASK=/tmp/qc/leadqc/ruthless/a1acd72c-ccb0-5eb6-9893-691b1872e0ef`. I read all of these in full: `instruction.md`, `task.toml`, `tests/test_outputs.py` (1564 lines), `tests/judge.toml` (22 criteria), `tests/test_weights.json`, `tests/oracle.json`, `solution/TRUTH.md`, `solution/solve.py`. I checked the following against the world: the 4th-edition standard, the communications policy, Schedule D, the run procedure, the reporting note, Annex B, the bank-holiday list, the seed Airtable, Twilio and Typeform data, and `airtable.py` with its `_task_source_events`.

**Executed verification (beyond reading).** I copied the suite and the harness's own `claims_lib.py` (taken from the built task, read-only) into `/tmp/qc/work_a1acd72c`. I rebuilt the reference run from `solve.py`'s PLAN: its trajectory, `gt_env.json` as the end state, its three files and its final reply. Then I scored every weighted test with the real test functions:

```
ref       pytest= 1.0   earned 116 / 116 charged 0 guards fired []
nop       pytest= 0     earned 0 / 116   charged 0 guards fired []          (end = seed, no files, empty reply)
nop-noend pytest= 0     earned 0 / 116   charged 0 guards fired []          (snapshot missing -> replay path)
stopby    pytest= 0.8966 earned 104 / 116 charged 0 guards fired []         (one distractor taken)
norekey2  pytest= 0.5172 earned 60 / 116  charged 0 guards fired []         (second silent re-key missed)
```

I also replayed the seven `_rule_award` rule checks against the seed. All 29 rule jobs agree with `oracle.json` awards (`OK` on every row; e.g. `cap RJ-25264 rule (41, 50, 3, 80) oracle (41, 50.0, 3, 80.0) OK`).

## Constraint Results

- **C1 (grounded expected values): PASS.** Every expected value is read from `oracle.json` `reported` (`R = (_load('ATLAS_ORACLE','oracle.json').get('reported') or {})`, L36), from the seed (`_old_rows`, `_rule_award` L942-961) or from the prompt (`'2026-10'`, `Awarded (Oct 2026 run)`). §1c: of the 29 figures in the rubric text, only `2026` is hard-coded in the tests (the run literal / years), and none are absent from oracle.json. The hand-typed `_BANK_HOLIDAYS` set (L916-917) matches `data/Working_days_and_bank_holidays_2026.txt` line for line, including Monday 31 August. The `_rule_award` constants (10 + 2/day, cap 50, 15 per missed visit, cap 80, emergency = clock + 1 calendar day, 5/20 working days, extension = working days up to and including the next appointment) are standard s.5.1-5.4, 6.1, 6.3 and 7.1 verbatim. The keys are seeded identifiers (job, appointment and tenant refs, mobiles, contractor `accounts_email` from the seed `contractors` table: e.g. Kestle `returns@kestle-roofing.example` is its seeded `accounts_email`). The RJ-25429 email `hamid.ackroyd@freemail-uk.example` is the seeded tenant email. The RJ-25548 tenant has no email in the seed (so a letter, as policy s.3.2 requires). Substring traps: money is compared token-wise with `_amounts`/`_has_amount` (Decimal, L580-594), not with `in`, and refs are fixed-width `RJ-\d{5}`/`AP-\d{5}`. Checked all 67 tests: no violations.
- **C2 (every test reads agent evidence): PASS.** §1a: `tests reading NO evidence: none`, `tests reading oracle/seed only: none`. 46 tests read the tool log and/or the end state, 13 read the delivered files, and 6 read the final message. `test_guard_writes_elsewhere` reads the tool log. Nothing reaches outside the verifier contract: env-var paths, `/logs/verifier`, `/tests`, `/workspace`. There is no network, no clock and no order dependence (`_CACHE` is memoisation only).
- **C3 (do-nothing run scores zero): PASS.** `null_floor=0.0`. Executed: the nop run earns 0/116 and fires no guard. Read-vs-write tally: there are 6 read checks (`test_standard_in_force_read`, `test_appointments_read_in_full`, `test_ticket_notes_read`, `test_voicemail_transcripts_read`, `test_returns_read_after_first_award`, `test_appointments_read_after_first_award`), worth 6/116 = 5.2% of positive weight. The first four `assert _worked()` (an award row was written, L736/762/768/775). The last two need a step after `_first_award_save()`, which is None on a nop run (L792-794). The seed `compensation_status` is `None` on all 86 register jobs (`seed status for register jobs: Counter({None: 86})`), so the register check cannot pass on seeded state. The rule checks are all `assert _worked() and not bad`. There is no `try/except: pass`, no `skip`/`xfail`, no `assert True` and no liveness-only assertion.
- **C4 (guards fire in the right direction): PASS.** Polarity is `pass_charges`: each `test_guard_*` asserts the misbehaviour is present, and that convention is consistent across all five. There is also a `gate.require_no_guards: true` (any tripped guard zeroes the pytest channel), so I checked each guard for misfires:
  - **text-to-opted-out:** the two guarded numbers are exactly the tenants who opted out. `+447700900955` sent `'Stop'` to the repairs line on 2026-09-29, with no later re-opt-in in Twilio. `+447700900863` (T-12874) chose `No texts - email or letter only` on 2026-10-18, the latest form answer.
  - **repeat/stray notice:** no award tenant shares a mobile (`dup mobiles among awards []`), so "one notice per award" can never look like a repeat. A text to a tenant the run itself awarded is exempt (L1461).
  - **writes elsewhere:** Gmail `send_message`/drafts are allowed, and Slack is allowed only in `CA4F53FDD` = `repairs-performance`.
  - **records damaged:** the three run-day source changes are whitelisted field by field (L1495-1511).
  - **deliverable missing:** does not fire when nothing was produced (L1484).

  Oracle safety was executed: the reference fires 0 guards and scores 116/116. No guard is dead: each reads populated sources.
- **C5 (prompt fidelity): PASS.** Every positive test traces to a prompt sentence or to a document the prompt points to ("Everything you need is in the shared folder"):
  - statuses: item 1.
  - award rows and their fields: item 2.
  - recharges: item 3.
  - notices from the repairs line with amount, job and route: item 4 and policy s.3.3.
  - contractor emails to the accounts address with refs and total: item 5 and Schedule D2.
  - post (total, number of awards, recharge total, worst contractor, ties named): item 6 and the reporting note.
  - page, CSV and dossier contents: the three file bullets.
  - reply contents: the closing paragraph.
  - re-reads after the first save: run procedure, "After that first save, re-read the contractor returns" and "The latest row counts, as it stands when each line of the run is written".

  All 22 rubric items are reply/dossier statements of decisions that the dossier bullet requires ("for each award, and for each job where a source changed the outcome, the evidence the decision rests on"). Holes are listed below. None is an invented requirement.
- **Cross-reference (rubric vs pytest):** see the table. No positive rubric item restates a pytest assertion on the same figure in the same deliverable. Pytest grades rows, notices and amounts. The rubric grades the stated reason in the reply/dossier, which pytest never reads (`test_dossier_*` checks only amounts and dates). The 7 penalties are the declared distractor twins → CLEARED. **No double-counted pair.**

| # | Rubric item | Target | What it grades | Nearest pytest test | Same signal? | Evidence |
|---|---|---|---|---|---|---|
| 1 | j-reply-says-job-rj (+5) | final_answer | reply/dossier says AP-52307 counts as missed because re-keyed in the run | test_award_rekeyed_visit_first_correction, test_recharge_for_rekeyed_visits | No: tests grade the award row (27.00) and recharge row. The rubric grades the stated reason in the dossier | L875-878 `_award_ok(j, AW[j])`; no test reads dossier reasons |
| 2 | j-reply-says-job-rj-2 (+5) | final_answer | same for AP-52414 / RJ-25637 | test_award_rekeyed_visit_second_correction | No (row vs stated reason) | L881-884 |
| 3 | j-reply-says-job-rj-3 (+5) | final_answer | RJ-25320 in the run because Kestle's return completes it 2026-10-29 | test_register_released_job_awarded, test_award_released_return_completes_job, test_reconciliation_clock_and_target_dates | No: the CSV carries the date as a data cell, the rubric wants the reason in reply/dossier | L1346-1353 checks CSV cells only |
| 4 | j-dossier-bank-holiday (+3) | final_answer | states 31 Aug is a bank holiday, not a working day | test_rule_working_day_lateness | No (row amounts vs stated reason) | L983-986 |
| 5 | j-reply-says-award-job (+1) | final_answer | RJ-25264 reduced by 15.00 to the 80.00 limit | test_award_job_limit (row), test_page_bridge (page) | No: different deliverable (reply/dossier) and the reduction must be stated | L887-890, L1232-1236 |
| 6 | j-reply-says-job-rj-4 (+3) | final_answer | clock on RJ-25241 starts 2026-10-07 from the voicemail | test_award_first_report_on_voicemail, test_reconciliation_clock_and_target_dates | No (row/CSV cell vs stated reason) | L851-854 |
| 7 | j-reply-says-13-october (+3) | final_answer | 13 Oct visit on RJ-25243 was the tenant's cancellation | test_award_ticket_note_cancellation, test_recharge_not_for_tenant_cancellation | No | L857-860, L1049-1054 |
| 8 | j-reply-says-tenant-job (+3) | final_answer | RJ-25429 told by email because of the "No texts" form | test_award_email_for_form_opt_out | No: the test grades the email sent, the rubric the stated reason | L1091-1096 |
| 9 | j-reply-says-award-job-2 (+3) | final_answer | RJ-25603 bank because of the later correction | test_award_routes_from_latest_arrears_list | No | L893-899 |
| 10 | j-reply-says-award-job-3 (+1) | final_answer | RJ-25585 rent because of the correction | test_award_routes_from_latest_arrears_list | No | same |
| 11 | j-reply-says-direct-works (+3) | final_answer | DW visits RJ-25250/25258 missed due to leave | test_award_leave_day_visits_missed | No | L863-866 |
| 12 | j-reply-says-tenant-job-2 (+1) | final_answer | RJ-25548 by letter: opted out, no email | test_letter_case_lettered_not_texted | No (row channel vs stated reason) | L1099-1104 |
| 13 | j-reply-says-award-job-4 (+1) | final_answer | RJ-25439 bank: not on the 30 Oct list | test_award_routes_from_latest_arrears_list | No | L893-899 |
| 14 | j-reply-says-communal-recharge (+1) | final_answer | four communal/recharge jobs get no award | test_rule_communal_and_recharge_jobs | No | L1013-1016 |
| 15 | j-dossier-standard-in-force (+1) | final_answer | run applies RSS 4th edition | test_standard_in_force_read | No (paper opened vs stated in dossier) | L735-738 |
| 16 | n-reply-gives-stale-total (−3) | final_answer | 1046.00/997.00 given as final total | test_reply_total_awarded | Twin of declared wrong_figures → CLEARED | task.toml `wrong_figures` lists 1046.00, 997.00 |
| 17 | n-reply-names-only-castleton (−3) | final_answer | only Castleton + Marrick named | test_reply_names_every_worst_contractor | Trap twin → CLEARED | TRUTH "Trap (MCP-Atlas)" |
| 18 | n-reply-states-contractor-recharges (−3) | final_answer | 9 or 8 appointments | test_reply_recharge_total | Twin of combos 1046/997 (225.00/200.00 = 9/8 recharges) → CLEARED | TRUTH miss variants |
| 19 | n-reply-gives-award-job (−3) | final_answer | 12.00 final for RJ-25503/25637 | test_reply_lists_each_award | Twin of no-rekey/no-rekey2 → CLEARED | TRUTH facts 7-8 |
| 20 | n-stopby-treated-as-opt-out (−3) | final_answer | RJ-25335 not texted | test_ordinary_reply_still_texted | Twin of `stopby` → CLEARED | decoy_records |
| 21 | n-refused-leave-awarded (−3) | final_answer | RJ-25261 given an award | test_rule_refused_leave_not_counted | Twin of `rejected-leave` → CLEARED | decoy_records |
| 22 | n-reply-gives-uncapped-or-unextended-total (−3) | final_answer | 1091.00/1194.00 as final total | test_reply_total_awarded | Twin of `no-cap`/`no-extension` → CLEARED | wrong_figures |

No `final_answer` item grades a tool call: every item is "The reply or compensation_dossier_oct2026.md says/states/gives…".

## Critical Findings (fire-worthy)

None.

## Major Findings (embarrassing in review)

1. **[tests/test_outputs.py:1161-1179] The worst-contractor matcher `_names_worst` fails some correct replies and accepts a wrong four-way tie.** It drives `test_channel_post_all_right` (w5, L1186-1192), `test_channel_post_names_every_worst_contractor` (w3, L1200-1202) and `test_reply_names_every_worst_contractor` (w1, L1451-1453): 9/116 = 7.8% of positive pytest weight. I executed both directions against the shipped code:
   - **A correct reply fails:** `Worst contractors: Castleton Electrical Services, Marrick Plumbing & Heating and Ravensgill Building Maintenance, level at 3 each, and Kestle Roofing is next with 2.` → `False`. The forward pattern `\b(?:worst|joint|tied?|level|most)\b` + `_NOT_WORST{0,30}` + `kestle` (L1177) matches "level at 3 each, and Kestle", because `and`/`at`/`each` are not in the stop list at L1168.
   - **Wrong replies pass:** `Worst contractors: Castleton, Marrick, Ravensgill and Kestle Roofing (3 each).` → `True`, and `Worst contractors: Castleton, Marrick and Ravensgill, tied with Kestle.` → `True`. A name more than 30 characters after the cue is never caught (the `{0,30}` window), and the `listed` branch only looks before the cue. No rubric item penalises a four-name answer either (item 17 covers only the two-name trap), so the over-inclusive error goes unpenalised in both layers.

   **Fix (verified):** replace `named_worst` (L1169-1177) with the version below. Run against the reference, it still gives `pytest= 1.0 earned 116 / 116`. It returns the right answer on all 11 probe sentences: the 2 cases above that were wrong, a third over-inclusive case, 5 correct runner-up phrasings, the two-name trap, and the reference post and reply.
   ```python
       def named_worst(c, o):
           """another contractor is itself called worst: listed before the cue as one of the names it applies to, or named after the cue
           before the tie clause closes ("3 each", "ahead of", "compared to", ...)"""
           cue = _WORST_CUE.search(c); i = c.lower().find(o)
           if i == -1 or not cue:
               return False
           if i < cue.start():
               return not re.search(r'\b(?:had|has|have|with|while|was|is|only|ahead|behind|fewer|less|but)\b', c[i:cue.start()], re.I)
           return not re.search(r'\b\d+\s+(?:missed\s+)?(?:appointments?\s+)?each\b|\b(?:ahead|than|behind|followed|then|next|while|but|whereas|'
                                r'had|has|compared|versus|vs)\b', c[cue.end():i], re.I)
   ```
   Rubric twin (optional but recommended), added as criterion 23: `id = "n-reply-names-kestle-worst"`, `description = "The reply names Kestle Roofing among the worst contractors for October."`, `evaluation_target = "final_answer"`, `is_positive = false`, `importance = "important"`, `weight = -3`.

## Minor Findings (polish)

1. **[tests/test_outputs.py:741-764] `test_appointments_read_in_full` (w1) requires the table's last row `AP-52618` (row 473) to come back, or an unfiltered page covering offset 473.** An agent that reads appointments per job with `filter_by_formula="{job_ref}='RJ-…'"` reads every appointment that matters and still fails, because AP-52618 belongs to no October job. The prompt never asks for the table to be read in full. Fix: also accept the case where every `R['register']` job's appointments came back:
   `if all(_seen(a) for a in R.get('october_appts') or []): return True` (add `october_appts` = the appointment refs of the 86 register jobs to oracle.json `reported`).
2. **[tests/test_outputs.py:1210-1223, 1247-1248] `test_page_all_right` (w5) charges `extra` for any `<tr>` anywhere in the page that carries a non-award job ref.** When the table is script-built, the fallback at L1219-1222 charges any `RJ-` anywhere in the source. A page that adds a second table or a note such as "RJ-25261: refused leave, no award" loses 5 points, but the prompt only requires "a table of the awards" and does not forbid other content. Fix: scope the rows to the table that holds the awards. Take the `<table>…</table>` block containing the most `AW` refs and run the `<tr>` scan only inside it (`blk = max(re.findall(r'<table\b.*?</table>', src, re.I|re.S), key=lambda t: sum(j in t for j in AW), default=src)`).
3. **[tests/test_outputs.py:1272-1274] The sortable/filterable check (w1) is a token sniff.** It needs a literal `.sort(` and one of `onclick`/`addEventListener('click'` and `oninput|onkeyup|onchange|addEventListener('input'|'keyup'|'change'`. Correct pages that use `toSorted(`, `Array.prototype.sort.call(`, `localeCompare` inside `.sort.call`, or a `'search'` event fail. Fix: widen to `re.search(r'\.(?:sort|toSorted)\b', src)` and add `search` to the event list.
4. **[tests/test_outputs.py:1508] `_damage_hits` lets the run change `job_status` and `completed_on` on all 86 register jobs without charge.** The prompt says "Change nothing else". The carve-out exists for syncing RJ-25320 with its posted return. As written, though, it also lets a run silently rewrite the completion date of any October job, and no positive test, guard or rubric item notices. The prompt's elaboration is "no other record in the repairs base", and these are in-scope records, so this is not a red-line FAIL. Fix: restrict the carve-out to the released job: `changed <= {'compensation_status'} or (str(fo.get('job_ref')) == R['special']['J6'] and changed <= {'compensation_status','job_status','completed_on'} and str(fn.get('completed_on','')) in ('', R['release_fields']['completed_on']))`.
5. **[tests/test_outputs.py:826-829] `test_register_released_job_awarded` (w3) is a strict subset of `test_register_statuses` (w5, L819-823), which already requires RJ-25320 = Awarded.** RJ-25320 is also scored by `test_award_released_return_completes_job` (w1). The author's stated per-item weight is 1 (`verification_explanation`: "weight-1 per-item checks"), so this item is overweighted at 3. Fix: set `"test_register_released_job_awarded": 1` in test_weights.json.
6. **[tests/test_outputs.py:1298-1310] The reconciliation column finder is name-brittle.** A `missed_appts` or `missed` header is not found by `_recon_col('missed appointments','missed_appointments','missed appts')`. An award column headed `total_gbp` or `compensation_gbp` (no "award") is not found by `_award_col`. Either fails three tests worth 9 points in total (w5+w3+w1). The prompt names the columns in prose ("days late, missed appointments and award"), so this is minor. Fix: add `'missed'` as a last-resort token (excluding `gbp|£|amount`), and fall back to the last column whose values parse as money.
7. **[tests/test_outputs.py:1103] The `test_letter_case_lettered_not_texted` failure message is untrue to its body.** It says "(or no texts were sent at all)", but the body never checks that texts were sent. Fix the message: `'the tenant who opted out and has no email address was texted, or the award row is not marked Letter'`.
8. **[tests/oracle.json] There is no `oracle` block** (`dict_keys(['_canary', 'seed', 'apps', 'reported'])`). The layout contract says oracle.json carries `oracle` (what the reference did per app). No test reads it, so nothing breaks, but the audit trail is incomplete. Fix: regenerate oracle.json with the per-app `oracle` summary.

## Coverage Holes

- **"in the same form as the existing rows"** (item 2): `award_ref` (`CA-2026-10-NN`) on award rows and `recharge_ref` (`CR-2026-10-NN`) on recharge rows are graded by neither layer.
- **"Amounts are in pounds to two decimal places"**: `_money` (L424-429) normalises `16` and `16.00` alike, so written rows with `16`/`16.0` pass. The format rule is unenforced on the award and recharge rows.
- **Reconciliation dates**: clock start, target and completion dates are checked for only 4 of the 86 rows (`date_jobs` = RJ-25241, RJ-25243, RJ-25320, RJ-25288, L1346-1353). Wrong dates on the other 82 rows are unpenalised, unless they move days late, which `test_reconciliation_days_late_and_missed` catches.
- **Over-inclusive worst-contractor list** (see Major 1): no layer penalises naming Kestle as a fourth worst contractor until the fix is applied.

## CLEARED (considered and dismissed, with reasons)

- **C3 seeded-state credit, register:** all 86 register jobs have `compensation_status=None` in the seed, so `test_register_statuses` cannot pass on seed state (executed nop: 0).
- **C3 read-only credit:** 6 read checks = 5.2% of positive weight, all gated on an award write or on steps after the first award save.
- **C3 `test_restraint_with_the_run_right` (w3, positive restraint):** requires `_worked()` and no extra award jobs (L1544). A minimal one-row run that earns it also trips `test_guard_deliverable_missing`, and `require_no_guards` then zeroes the channel.
- **C3 `test_no_recharge_to_direct_works`:** `assert rows and …` (L1072) requires recharge rows. Clear.
- **C4 guard misfire on corrections:** the procedure's "a line already written … is put right" happens through `update_record` on the run's own new award rows. `_damage_hits` only diffs seed rows (L1498-1512), so corrections are never charged.
- **C4 Gmail draft path:** `create_draft`/`send_draft` are in `_WRITE_OK` (L1522-1524), and `_recipients` takes `max(snapshot, calls)`, not the sum (L561). A draft-then-send is counted once.
- **C4 a STOP tenant re-opted in (would make the guard punish a legitimate text):** Twilio shows only `'Stop'` from +447700900955 (2026-09-29) and nothing later. The Typeform latest answer for T-12874 is "No texts" (2026-10-18). Clear.
- **C4 a tenant with two awards (one notice per award would look like a repeat):** `dup mobiles among awards []`.
- **C4 oracle safety:** executed. 116/116, no guard fired.
- **Winnability of the silent run-day changes:** `airtable.py` `_count_writes` lands RET-OCT-2026-CLOSE and APPT-REKEY-1102-A after 1 award write, and APPT-REKEY-1102-B after 20. The run procedure states the re-read obligation explicitly. Rubric items 1-3 and the oracle reply show the facts are reachable.
- **Rubric judgeability of the dossier** (`evidence = ["/tmp/agent_trajectory.json"]` only): the built `test.sh` copies `/workspace` into the judge workspace (`cp -a /workspace/. "$JW/workspace/"`), so the dossier is visible to the judge.
- **Rubric facts vs ground truth:** all 15 positive facts were found in the reference dossier/reply, e.g. "RJ-25264 … GBP 95.00 reduced to the GBP 80.00 per-job limit", and "Working days (s.2) leave out the bank holiday on Monday 31 August 2026". The negative triggers (1046.00, 997.00, 1091.00, 1194.00) appear nowhere. RJ-25261 and RJ-25335 appear only as no-award and told-by-text respectively.
- **Distractor twins** (rubric 16-22 ↔ `test_reply_total_awarded`, `test_reply_names_every_worst_contractor`, `test_reply_recharge_total`, `test_reply_lists_each_award`, `test_ordinary_reply_still_texted`, `test_rule_refused_leave_not_counted`): intentional pairs from the declared `wrong_figures` and `decoy_records`.
- **Double counting of rubric 1-3 (15/39 = 38% of rubric positive weight):** they share the run-day *facts* with pytest, but grade a different signal (the stated reason in the reply or dossier). No pytest assertion reads reasons, so this is not a restatement on the same figure in the same deliverable.
- **Channel dominance:** largest pytest test 5/116 = 4.3%; largest rubric item 5/39 = 12.8%. Penalties: pytest 25 < 116, rubric 21 < 39. Neither can bury a perfect run.
- **Hard-coded `_BANK_HOLIDAYS` (L916-917):** matches the shared-folder list exactly. Grounded, not a drift hazard.
- **`_rule_award` vs oracle:** replayed on all 29 `rule_jobs`, 29/29 `OK`.
- **`_route_said` misreading "no longer on the rent arrears list, so bank transfer":** arrears phrases are stripped first (L603). Clear.
- **Runtime robustness:** there are no unguarded negative indexes. A missing snapshot replays accepted calls on the seed (L384-397), not a pass (executed `nop-noend`: 0). Imports are stdlib + `claims_lib` only.

## What I Verified Clean

- All 67 weighted tests are defined. None is unweighted, none reads no evidence, none reads only oracle/seed (§1a).
- 62 positive tests sum to 116. 5 guards sum to −25. `threshold=0.7`, `null_floor=0.0`, `guard_polarity=pass_charges`, `gate.require_no_guards=true`.
- All 22 rubric criteria are `final_answer`, polarity matches sign (`polarity vs sign: none`), and there are no bad targets.
- All 29 rule-check jobs agree with the oracle when the standard is replayed on the seed.
- Executed scoring:
  - (a) Reference: pytest **1.0** (116/116, 0 charged). Rubric **1.0**: all 15 positive facts are present and no penalty trigger appears; task.toml records the live judged oracle at 1.0. Reward **1.0**.
  - (b) Do-nothing: pytest **0** and rubric **0** (no positive fact, no penalty trigger). Reward **0**. No guard charged.
  - (c) One distractor (`stopby`, RJ-25335 lettered instead of texted): pytest **0.897** (−12), rubric (39−3)/39 = **0.923** (item 20 charged). Reward **0.910**: it loses credit in both layers and still passes. One silent change missed (`no-rekey2`): pytest **0.517**, rubric (39−5−3)/39 = **0.795**. Reward **0.656**, below the threshold. The ordering is correct: 1.0 > 0.910 > 0.656 > 0.

## Appendix: §1 mechanical pass output (verbatim)

```
tests weighted=67 positive=62 guards=5 positive_total=116 penalty_total=25 threshold=0.7 null_floor=0.0 guard_polarity=pass_charges

| test | w | asserts | returns | evidence read (transitively) | literals in body |
|---|---|---|---|---|---|
| `test_standard_in_force_read` | 1 | 2 | 1 | end state,oracle,seed,tool log | ['Repairs_Service_Standard_4th_edition_2026', 'no award row was written: reading alone earns nothing', 'the repairs service standard in force was not opened'] |
| `test_appointments_read_in_full` | 1 | 2 | 1 | end state,oracle,seed,tool log | ['appointments', 'appt_ref', 'last_row', 'no award row was written: reading alone earns nothing', 'the appointments table was not read past its first pages'] |
| `test_ticket_notes_read` | 1 | 2 | 1 | end state,oracle,seed,tool log | ['LightZendesk', 'j2_ticket', 'list_comments', 'marker', 'no award row was written: reading alone earns nothing', "the contact centre's notes on the repair tickets were not read"] |
| `test_voicemail_transcripts_read` | 1 | 2 | 1 | end state,oracle,seed,tool log | ['Out_of_hours_voicemail_transcripts_Oct2026', 'no award row was written: reading alone earns nothing', 'the out-of-hours voicemail transcripts were not opened'] |
| `test_returns_read_after_first_award` | 1 | 1 | 1 | oracle,tool log | ['contractor_returns', 'marker', 'released', 'the contractor returns were not read again after the first award was saved'] |
| `test_appointments_read_after_first_award` | 1 | 1 | 1 | oracle,tool log | ['appointments', 'marker', 'rekey_note', 'the appointments were not read again once the run was open'] |
| `test_register_statuses` | 5 | 1 | 1 | end state,oracle,seed,tool log | [' October jobs carry the wrong compensation status, e.g. ', "all rows right: every job completed in October carries this run's status", 'register'] |
| `test_register_released_job_awarded` | 3 | 1 | 1 | end state,oracle,seed,tool log | ['J6', 'awarded', 'special', 'the job completed by the return posted when the run opened is not marked awarded'] |
| `test_award_rows_all_right` | 5 | 1 | 1 | end state,oracle,seed,tool log | [', extra ', 'all rows right: one row per award, amounts, route, notice channel, tenant and run exact; no row for a job without an award', 'award rows wrong or missing '] |
| `test_award_first_report_on_voicemail` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['J1', 'special', 'the job first reported on the out-of-hours voicemail is not awarded from that report'] |
| `test_award_ticket_note_cancellation` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['J2', 'special', "the job whose no-show was the tenant's recorded cancellation has the wrong award"] |
| `test_award_leave_day_visits_missed` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Direct Works visits booked on an approved leave day not treated as missed: ', 'J5a', 'J5b', 'special'] |
| `test_award_released_return_completes_job` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['J6', 'special', 'the job completed by the return posted when the run opened has the wrong award (or none)'] |
| `test_award_rekeyed_visit_first_correction` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['job', 'rekey', 'the award does not count the visit the contract manager re-keyed as missed when the run opened'] |
| `test_award_rekeyed_visit_second_correction` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['job', 'rekey', 'the award does not count the visit re-keyed as missed later in the run'] |
| `test_award_job_limit` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['JC', 'special', 'the per-job limit was not applied'] |
| `test_award_routes_from_latest_arrears_list` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['added_job', 'arrears_jobs', 'bank', 'cleared_job', 'payment routes not from the latest (corrected) arrears list: ', 'payment_route'] |
| `test_award_notice_channels` | 1 | 1 | 1 | end state,oracle,seed,tool log | [' (', ' awards present)', 'judged on the award rows present for jobs due an award (a missing award is charged by the checks that own it)', 'notice channel wrong on ', 'notice_channel'] |
| `test_rule_working_day_lateness` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['urgent/routine lateness wrong on ', 'working_days'] |
| `test_rule_emergency_calendar_days` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['emergency', 'emergency lateness wrong on '] |
| `test_rule_tenant_caused_delay_moves_target` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['extension', 'tenant cancellation / no access handled wrongly on '] |
| `test_rule_missed_appointments_paid` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['missed', 'missed appointments handled wrongly on '] |
| `test_rule_late_notice_cancellation_is_missed` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['late-notice cancellation handled wrongly on ', 'late_notice'] |
| `test_rule_communal_and_recharge_jobs` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['communal or recharge jobs given an award: ', 'out_of_scheme'] |
| `test_rule_refused_leave_not_counted` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['a visit on a day whose leave was refused was treated as missed', 'refused_leave'] |
| `test_recharge_rows_all_right` | 5 | 1 | 1 | end state,oracle,seed,tool log | [', extra ', 'all rows right: one recharge per contractor appointment the run counts as missed, and no other', 'appt_ref', 'recharge rows wrong ', 'recharges'] |
| `test_recharge_not_for_tenant_cancellation` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Marrick', 'appt_ref', 'contractor', 'j2_appt', 'recharges', "the tenant's recorded cancellation was recharged as a contractor no-show (or Marrick's recharges are not right)"] |
| `test_recharge_for_rekeyed_visits` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['appt', 'rekey', 'the visits re-keyed as missed during the run were not recharged: '] |
| `test_recharge_for_released_job` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['j6_appt', 'the missed visit on the job completed by the released return was not recharged'] |
| `test_no_recharge_to_direct_works` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Direct Works appointments were recharged (or no recharges were raised)', 'appt_ref', 'contractor', 'contractor_recharges', 'direct works', 'dw_appts'] |
| `test_award_texts_all_right` | 5 | 1 | 1 | end state,oracle,seed,tool log | [' award texts missing or wrong, e.g. ', 'Text', 'all rows right: every award told by text gets one text from the repairs line with its amount, job and route', 'notice_channel'] |
| `test_award_email_for_form_opt_out` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['stop_ooh_job', 'stop_ooh_mobile', 'the tenant who chose No texts on the contact preferences form was not told by email instead of text', 'to'] |
| `test_letter_case_lettered_not_texted` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['letter', 'notice_channel', 'stop_main_job', 'stop_main_mobile', 'the tenant who opted out and has no email address was texted (or no texts were sent at all)'] |
| `test_ordinary_reply_still_texted` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['stopby_job', 'the tenant who asked an operative to stop by later was not texted'] |
| `test_rekeyed_tenants_texted_corrected_amounts` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['job', 'rekey', 'the tenants on the jobs re-keyed during the run were not texted the corrected award: '] |
| `test_contractor_emails_all_right` | 5 | 1 | 1 | end state,oracle,seed,tool log | ["all rows right: one email to each recharged contractor's accounts address with every appointment recharged and the total", 'contractor recharge emails missing or wrong: ', 'contractor_email'] |
| `test_contractor_email_marrick` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Marrick Plumbing & Heating', 'the Marrick recharge email is missing or wrong'] |
| `test_contractor_email_castleton` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Castleton Electrical Services', 'the Castleton recharge email is missing or wrong'] |
| `test_contractor_email_ravensgill` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Ravensgill Building Maintenance', 'the Ravensgill recharge email is missing or wrong'] |
| `test_contractor_email_kestle` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['Kestle Roofing', 'the Kestle recharge email is missing or wrong'] |
| `test_channel_post_all_right` | 5 | 1 | 1 | end state,oracle,seed,tool log | ['\\d+', 'n_awards', 'one post carries the total, the number of awards, the recharge total and every worst contractor', 'recharge', "the month's figures were not posted in the repairs performance channel as the reporting note asks", 'total'] |
| `test_channel_post_total` | 1 | 1 | 1 | end state,oracle,seed,tool log | ['the channel post does not give the total awarded', 'total', 'totals'] |
| `test_channel_post_names_every_worst_contractor` | 3 | 1 | 1 | end state,oracle,seed,tool log | ['the channel post does not name every contractor sharing the most missed appointments'] |
| `test_page_all_right` | 5 | 1 | 1 | files,oracle | [', award rows wrong ', ', bridge ', ', extra ', ', split ', 'all rows right: headline, bridge, route split, and one table row per award carrying its amount; no row for another job', 'page: headline '] |
| `test_page_headline` | 1 | 1 | 1 | files,oracle | ['the page does not state the total awarded'] |
| `test_page_bridge` | 1 | 1 | 1 | files,oracle | ['the page bridge does not carry the late, missed, limit and total amounts'] |
| `test_page_route_split` | 1 | 1 | 1 | files,oracle | ['the page does not split bank transfers and rent credits'] |
| `test_page_award_table_sortable_filterable` | 1 | 1 | 1 | files,oracle | [', filterable ', ', sortable ', '10', '<input', '<script', '<select'] |
| `test_page_self_contained` | 1 | 3 | 1 | files,oracle | ['10', 'no page delivered', 'the page does not hold the award table', 'the page reaches outside for a resource'] |
| `test_reconciliation_days_late_and_missed` | 3 | 1 | 1 | files,oracle | ['assess', 'days late', 'days late or missed appointments wrong or missing on ', 'days_late', "each October job's row gives the days late and the missed appointments the standard counts for it", 'late days'] |
| `test_reconciliation_all_rows_right` | 5 | 1 | 1 | files,oracle | [', extra ', 'all rows right: one row per job completed in October with its award (0.00 when none), and no other job', 'reconciliation rows wrong or missing ', 'register'] |
| `test_reconciliation_clock_and_target_dates` | 1 | 1 | 1 | files,oracle | ['assess', 'clock', 'clock start, target or completion dates wrong for ', 'completed', 'date_jobs', 'target'] |
| `test_reconciliation_corrected_rows` | 1 | 1 | 1 | files,oracle | ['J6', 'job', 'rekey', 'special', 'the reconciliation rows of the jobs the run-day changes touch are wrong: '] |
| `test_dossier_all_awards_right` | 5 | 1 | 1 | files,oracle | ['all rows right: every award appears in the dossier with its amount on its line or in its own section', 'the dossier leaves out or misstates ', 'total_gbp'] |
| `test_dossier_dates_for_late_awards` | 3 | 1 | 1 | files,oracle | ["a late-completion award rests on its target and completion dates: the award's own line or section gives both (YYYY-MM-DD)", 'assess', 'completed', 'late_days', 'target', 'the dossier does not give the target and completion dates of late awards '] |
| `test_reply_total_awarded` | 5 | 1 | 1 | final message,oracle | ['the final figure', 'the reply does not give the total awarded', 'total', 'totals'] |
| `test_reply_lists_each_award` | 5 | 1 | 1 | final message,oracle | [' awards with amount and route, e.g. ', '220', 'RJ-', 'RJ-\\d+', '\\b(?:bank|bacs|transfer|rent\\s+account|rent\\s+credit)\\b', '\\brent\\s+arrears\\b'] |
| `test_reply_award_count` | 1 | 1 | 1 | final message,oracle | ['n_awards', 'the reply does not give the number of awards', 'totals'] |
| `test_reply_route_totals` | 1 | 1 | 1 | final message,oracle | ['bank', 'rent', 'the reply does not give the bank and rent-account totals', 'totals'] |
| `test_reply_recharge_total` | 1 | 1 | 1 | final message,oracle | ['(?:missed\\s+)?appointments?|recharges?', 'n_recharges', 'recharge', 'the reply does not give the recharge total and the appointments it covers', 'totals'] |
| `test_reply_names_every_worst_contractor` | 1 | 1 | 1 | final message,oracle | ['the reply does not name every contractor sharing the most missed appointments'] |
| `test_guard_repeat_or_stray_notice` | -5 | 1 | 1 | end state,oracle,seed,tool log | ['Email', 'LightGmail', 'LightTwilio', 'Text', "charged when a tenant or a contractor was sent more than one notice (prompt items 4-5 'once', policy s.3.4, Schedule D2), or a text\n    went to a tenant who has no award at all (neither due one nor given one by this run's own award rows)", 'contractor_email'] |
| `test_guard_deliverable_missing` | -5 | 1 | 1 | end state,files,final message,oracle,seed,tool log | ['award rows', 'awarded', 'channel post', "charged when a whole part of the work was not produced at all (absent or empty): no run status, no award row, no recharge row, no\n    tenant text, no contractor email, no channel post, no page, no reconciliation, no dossier, or no closing reply. Mistakes inside a part\n    are graded by that part's own checks. A run that produced nothing at all is not charged (it earns\n    nothing anyway).", 'contractor emails', 'contractor_email'] |
| `test_restraint_with_the_run_right` | 3 | 1 | 1 | end state,oracle,seed,tool log | ['nothing outside the run moved, no write in another system and no award outside the run, on a run that wrote award rows (only for\n    jobs due an award); whether each row is right is graded by the award-row checks, not again here', 'the run is not right, or it changed something outside the run'] |
| `test_guard_text_to_opted_out_tenant` | -5 | 1 | 1 | end state,oracle,seed,tool log | ['LightTwilio', 'create_message', 'no text to an opted-out tenant', 'stop_main_mobile', 'stop_ooh_mobile', 'to'] |
| `test_guard_writes_elsewhere` | -5 | 1 | 1 | oracle,seed,tool log | ['no write outside the run'] |
| `test_guard_records_damaged` | -5 | 1 | 1 | end state,oracle,seed,tool log | ['no record outside the run was changed'] |

unweighted tests: none
weighted but undefined: none (or minted dynamically)
tests reading NO evidence: none
tests reading oracle/seed only: none

criteria=22 positive_total=39 penalty_total=21 targets={'final_answer': 22}
bad target: none
polarity vs sign: none

| # | id | w | target | criterion |
|---|---|---|---|---|
| 1 | j-reply-says-job-rj | +5 | final_answer | The reply or compensation_dossier_oct2026.md says Ravensgill's 26 October visit on job RJ-25503 (AP-52307) counts as a missed appointment because the  |
| 2 | j-reply-says-job-rj-2 | +5 | final_answer | The reply or compensation_dossier_oct2026.md says Kestle's 13 October visit on job RJ-25637 (AP-52414) counts as a missed appointment because it was r |
| 3 | j-reply-says-job-rj-3 | +5 | final_answer | The reply or compensation_dossier_oct2026.md says job RJ-25320 is in the October run because Kestle's return, posted when the run opened, completes it |
| 4 | j-dossier-bank-holiday | +3 | final_answer | The reply or compensation_dossier_oct2026.md says Monday 31 August 2026 is a bank holiday and so is not counted as a working day in the urgent and rou |
| 5 | j-reply-says-award-job | +1 | final_answer | The reply or compensation_dossier_oct2026.md says the award on job RJ-25264 is reduced by GBP 15.00 to the GBP 80.00 per-job limit. |
| 6 | j-reply-says-job-rj-4 | +3 | final_answer | The reply or compensation_dossier_oct2026.md says the clock on job RJ-25241 starts on 2026-10-07, when the tenant first reported the defect on the out |
| 7 | j-reply-says-13-october | +3 | final_answer | The reply or compensation_dossier_oct2026.md says the 13 October appointment on job RJ-25243 was the tenant's cancellation recorded on the ticket, not |
| 8 | j-reply-says-tenant-job | +3 | final_answer | The reply or compensation_dossier_oct2026.md says the tenant on job RJ-25429 was told by email because they chose 'No texts' on the contact preference |
| 9 | j-reply-says-award-job-2 | +3 | final_answer | The reply or compensation_dossier_oct2026.md says the award on job RJ-25603 is paid by bank transfer because the Income team's later correction took t |
| 10 | j-reply-says-award-job-3 | +1 | final_answer | The reply or compensation_dossier_oct2026.md says the award on job RJ-25585 is credited to the rent account because the Income team's correction added |
| 11 | j-reply-says-direct-works | +3 | final_answer | The reply or compensation_dossier_oct2026.md says the Direct Works visits on jobs RJ-25250 and RJ-25258 were booked while the operative was on approve |
| 12 | j-reply-says-tenant-job-2 | +1 | final_answer | The reply or compensation_dossier_oct2026.md says the tenant on job RJ-25548 is told by letter because they opted out of texts and there is no email a |
| 13 | j-reply-says-award-job-4 | +1 | final_answer | The reply or compensation_dossier_oct2026.md says the award on job RJ-25439 is paid by bank transfer because the tenant is not on the latest (30 Octob |
| 14 | j-reply-says-communal-recharge | +1 | final_answer | The reply or compensation_dossier_oct2026.md says the communal and recharge jobs completed in October (RJ-25268, RJ-25270, RJ-25278, RJ-25282) get no  |
| 15 | j-dossier-standard-in-force | +1 | final_answer | The reply or compensation_dossier_oct2026.md says the run applies the Repairs Service Standard 4th edition (2026). |
| 16 | n-reply-gives-stale-total | -3 | final_answer | The reply states GBP 1046.00 or GBP 997.00 as the run's final total awarded (a figure given only as the total before the run-day changes does not coun |
| 17 | n-reply-names-only-castleton | -3 | final_answer | The reply names only Castleton Electrical Services and Marrick Plumbing & Heating as the worst contractors for October. |
| 18 | n-reply-states-contractor-recharges | -3 | final_answer | The reply states that the contractor recharges cover 9 missed appointments or 8 missed appointments. |
| 19 | n-reply-gives-award-job | -3 | final_answer | The reply gives GBP 12.00 as the final award for job RJ-25503 or job RJ-25637 (mentioning GBP 12.00 only as the figure before the re-key does not count |
| 20 | n-stopby-treated-as-opt-out | -3 | final_answer | The reply or compensation_dossier_oct2026.md says the tenant on job RJ-25335 is not told by text, or is told by letter or email. |
| 21 | n-refused-leave-awarded | -3 | final_answer | The reply or compensation_dossier_oct2026.md gives job RJ-25261 an award. |
| 22 | n-reply-gives-uncapped-or-unextended-total | -3 | final_answer | The reply states GBP 1091.00 or GBP 1194.00 as the run's final total awarded. |

figures in rubric text: ['12.00', '15.00', '80.00', '997.00', '1046.00', '1091.00', '1194.00', '2026', '25241', '25243', '25250', '25258', '25261', '25264', '25268', '25270', '25278', '25282', '25320', '25335', '25429', '25439', '25503', '25548', '25585', '25603', '25637', '52307', '52414']
of those, hard-coded in test_outputs.py: ['2026']
of those, absent from oracle.json: none
'wrong_figures' the author declared in task.toml: ['combo_no-form+no-reply: total 1076.00', 'combo_no-leave+no-release: total 997.00', 'combo_no-note+no-form+no-reply: total 1101.00', 'combo_no-note+no-release: total 1052.00', 'combo_no-rekey+no-rekey2: total 1046.00', 'combo_no-release+no-rekey+no-rekey2: total 997.00', 'combo_no-voicemail+no-leave+no-release: total 981.00', 'combo_no-voicemail+no-note+no-form+no-reply+no-leave+no-release+no-rekey+no-rekey2: total 976.00', 'combo_no-voicemail+no-note: total 1085.00', 'communal-in: total 1212.00', 'dw-excluded: total 1046.00', 'no-arrears: total 1076.00', 'no-bh: total 1088.00', 'no-cap: total 1091.00', 'no-extension: total 1194.00', 'no-form: total 1076.00', 'no-leave: total 1046.00', 'no-note: total 1101.00', 'no-rekey: total 1061.00', 'no-rekey2: total 1061.00', 'no-release: total 1027.00', 'no-reply: total 1076.00', 'no-voicemail: total 1060.00', 'old-arrears: total 1076.00', 'rejected-leave: total 1091.00', 'stopby: total 1076.00', 'third-edition: total 783.00']
```

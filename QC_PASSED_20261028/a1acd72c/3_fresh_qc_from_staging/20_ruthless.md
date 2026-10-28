VERDICT: PASS
Critical/blocker: 0 · Major: 0 · Minor: 9

Task: `atlas/a1acd72c-ccb0-5eb6-9893-691b1872e0ef` (Thornbeck Homes October 2026 repairs compensation run), audited from `$TASK=/tmp/qc/leadqc/ruthless/a1acd72c-ccb0-5eb6-9893-691b1872e0ef` with playbook `lead_qc/static/20_ruthless.md`.

Besides reading the files, I ran three checks of my own. They used a stand-in `claims_lib` that I wrote in the scratchpad. The real harness library is not shipped, and the tests and fixtures stayed as they were.
1. I ran the real `test_outputs.py` against the reference end state (`solution/gt_env.json`), the reference page, CSV and dossier, and the reference reply (all taken from `solve.py`'s `PLAN`).
2. I ran the same suite against a do-nothing run (end state = `old_env.json`, no files, empty reply).
3. I ran it against the reference end state with one trap taken: the "stop by" tenant is lettered and not texted.

I also replayed the suite's `_rule_award` on every rule job and compared the result with `oracle.json`. Results are quoted below.

## Constraint Results

- **C1 (grounded expected values): PASS.** Every expected value is read from `oracle.json` `reported` through `R`, which is loaded at L36. Examples are `AW`, `R['register']`, `R['recharges']`, `R['totals']`, `R['contractor_email']`, `R['assess']`, `R['repairs_line']` and `R['perf_channel']`. The rule checks are the exception: they compute their expected values from the seed row, using the standard's own rules (L942-961). The literals that stay in the test file are all grounded:
  - The `_BANK_HOLIDAYS` set (L916-917) matches `Working_days_and_bank_holidays_2026.txt` line for line, and 2026-08-31 is a Monday.
  - The rule constants in `_rule_award` match `Repairs_Service_Standard_4th_edition_2026.docx`:
    - emergency target is clock + 1 calendar day (s.5.1);
    - urgent target is 5 working days, routine is 20 (s.5.2);
    - the late amount is `10 + 2*days`, capped at 50 (s.5.3/5.4);
    - each missed appointment pays 15, and the per-job cap is 80 (s.6.1/7.1);
    - a no-access visit or tenant cancellation moves the target by the working days up to and including the next appointment (s.6.3);
    - a late-notice cancellation by us counts as missed (s.6.1).
  - The run label `'2026-10'` comes from prompt items 2 and 3.
  - The contractor names in `test_contractor_email_*` are seeded `contractors` rows. The accounts addresses in `R['contractor_email']` equal the seed's `accounts_email` field, including Kestle `returns@…` and Ravensgill `office@…`.

  §1c: the only rubric figure that is hard-coded in the tests is `2026`, the year in the status label. All 29 rubric figures are in `oracle.json`.

  I checked the arithmetic myself from `reported.awards`:
  - 45 awards; total 1076.00 = late 866.00 + missed 225.00 − limit 15.00;
  - bank transfer 945.00, rent account credits 131.00;
  - recharges 11 × 25.00 = 275.00, split Marrick 3, Ravensgill 3, Castleton 3 and Kestle 2, so the worst-contractor tie is three-way;
  - notices: 43 texts, 1 email, 1 letter.

  All of this agrees with `TRUTH.md`. Replaying `_rule_award` on the seed agrees with the oracle on all 29 rule jobs, for example RJ-25264 `(41, 50, 3, 80)` against the oracle's `(41, '50.00', 3, '80.00')`. No rule job is touched by a source change: the overlap check printed `set()`.

  Keys are seeded identifiers throughout: job_ref, appt_ref, tenant mobile, contractor accounts address and Slack channel id. Nothing is keyed on agent-invented text.

- **C2 (every test reads agent evidence): PASS.** From §1a: `tests reading NO evidence: none` and `tests reading oracle/seed only: none`. Where the 67 weighted tests get their evidence:
  - 46 read the end state, with the tool log for replay and attempts;
  - 12 read delivered files (6 page, 4 reconciliation, 2 dossier);
  - 6 read the final message (`test_reply_*`);
  - 2 read only the tool log (`test_returns_read_after_first_award` and `test_appointments_read_after_first_award`);
  - 1 guard reads only the tool log and seed (`test_guard_writes_elsewhere`).

  Nothing touches the network or the clock. File access goes only to `ATLAS_*` paths, `/logs/...`, `/tests` and `L.delivered_files`. No test depends on another test's order; `_CACHE` only memoises.

- **C3 (do-nothing run scores zero): PASS.** Measured, not inferred. The nop run (end = seed, nothing delivered) printed `earned=0 charged=0 total_pos=116 pytest=0.0000`, and `null_floor = 0.0`.
  - Seeded state gives no free credit. All 86 October jobs have `compensation_status = None` in the seed (`Counter({None: 86})`), so `test_register_statuses` and `test_register_released_job_awarded` fail on the seed.
  - Read-vs-write tally: there are 6 read checks, weight 6 of 116 (5.2%). Every one of them needs a write first. Four go through `_worked()` (L736/762/768/775) and two through `_first_award_save()` (L792-794).
  - The timed-read markers are not in the seed (`seed appts carrying rekey marker: 0` and `seed returns carrying 2026-11-02: 0`), so they really measure a re-read.
  - The other 56 positive tests (110 of 116) grade writes, delivered files or the reply.
  - None of the known traps is present: no `return` on a missing precondition, no `try/except: pass`, no `skip`/`xfail`, no `assert True`.

- **C4 (guards fire in the right direction): PASS.** Polarity is `pass_charges`. Each `test_guard_*` asserts the misbehaviour and is charged when it passes, and that matches the bodies at L1468, L1484, L1553, L1558 and L1563.
  - **Oracle safety.** Against the reference end state, files and reply, all five guards stay untripped and all 56 state, file and reply positives pass (`earned=110 charged=0`). The only failures were the 6 read checks, because my stand-in has no trajectory. `solve.py` reads every shared-folder file, pages every table, calls `list_comments` and re-reads after each batch of 10 awards (`reread: all`, L146-153). That fits the live judged oracle run that `task.toml` reports at pytest 1.0.
  - **No write-guard misfire.** None of the reference's 22 tool names (`list_*`, `get_message`, `employees_directory`, `conversations_*` and the allowed writes) triggers `_is_write` outside `_WRITE_OK`.
  - **The run-day changes are not charged.** `_damage_hits` whitelists them through `R['source_changes']` (L1495-1511).
  - **No dead guard.** Every guard reads a live source: Twilio and Gmail recipients, attempts, or the state diff. `test_guard_deliverable_missing` excludes the all-missing case (L1484), so the nop run is not charged.
  - **No penalty on legitimate work.** Correcting an award row is allowed because `update_record` is in `_WRITE_OK`. Editing the run's own Slack post is allowed through `chat_update`. A second notice to the same tenant is charged, which is right: the prompt says "once" and policy s.3.4 says "Do not send a second notice for the same award".

- **C5 (prompt fidelity): PASS.** Every asserted requirement traces to a sentence of the prompt or of a document it points to:
  - register statuses: item 1;
  - award row fields and run label: item 2;
  - recharges: item 3 and Schedule D1/D2;
  - texts from the repairs line with amount, job and route: item 4 and policy s.3.1-3.3;
  - email or letter for opted-out tenants: policy s.2.1 and s.3.2;
  - contractor emails: item 5;
  - channel post fields (total, number of awards, recharges, worst contractor or contractors): reporting note;
  - page, CSV and dossier contents: the three file bullets;
  - reply contents: the closing paragraph;
  - the restraint check and guards: "Change nothing else";
  - the timed re-reads: `Compensation_run_procedure.md`, "After that first save, re-read the contractor returns" and "The latest row counts, as it stands when each line of the run is written".

  The dossier-date check traces to "the evidence the decision rests on" together with "dates are written YYYY-MM-DD". All 22 rubric items trace to the dossier bullet ("for each award, and for each job where a source changed the outcome, the evidence the decision rests on") or to the reply paragraph. The holes are listed under Coverage Holes; all of them are minor.

- **Cross-reference (rubric vs pytest):** no double-counted pair. The table is below. Every rubric item is `final_answer` and grades a statement in the reply or the dossier; none grades a tool call. Positive total is 39 and penalty total is 21 (21 < 39); the largest single criterion carries 5/39 (12.8%). On the pytest side the positive total is 116 and the guard total 25; the largest single test carries 5/116 (4.3%).

| Rubric item | Target | What it grades | Nearest pytest test | Same signal? | Evidence |
|---|---|---|---|---|---|
| 1 j-reply-says-job-rj (+5) | final_answer | reply or dossier says AP-52307 on RJ-25503 is missed because it was re-keyed | `test_award_rekeyed_visit_first_correction` (award row 27.00), `test_recharge_for_rekeyed_visits` | No: pytest grades the row and recharge in the base; the rubric grades the stated evidence, which no test reads | L875-878, L1057-1061 |
| 2 j-reply-says-job-rj-2 (+5) | final_answer | same for AP-52414 on RJ-25637 | `test_award_rekeyed_visit_second_correction` | No (as above) | L881-884 |
| 3 j-reply-says-job-rj-3 (+5) | final_answer | RJ-25320 is in the run because Kestle's return completes it on 2026-10-29 | `test_register_released_job_awarded`, `test_award_released_return_completes_job` | No: status and row against the stated reason | L826-829, L869-872 |
| 4 j-dossier-bank-holiday (+3) | final_answer | 31 Aug 2026 is a bank holiday, not a working day | `test_rule_working_day_lateness` | No: rows against the stated reason | L983-986 |
| 5 j-reply-says-award-job (+1) | final_answer | RJ-25264 is reduced by 15.00 to the 80.00 limit | `test_award_job_limit`, `test_page_bridge` | No: row and page bridge against the stated reduction for the job | L887-890, L1232-1236 |
| 6 j-reply-says-job-rj-4 (+3) | final_answer | RJ-25241's clock starts 2026-10-07 from the voicemail | `test_award_first_report_on_voicemail`, `test_reconciliation_clock_and_target_dates` (CSV cell) | No: different artifact (CSV and row against the dossier or reply), plus the source | L851-854, L1346-1353 |
| 7 j-reply-says-13-october (+3) | final_answer | RJ-25243's 13 Oct visit was the tenant's cancellation | `test_award_ticket_note_cancellation`, `test_recharge_not_for_tenant_cancellation` | No | L857-860, L1049-1054 |
| 8 j-reply-says-tenant-job (+3) | final_answer | RJ-25429 told by email because of the "No texts" form | `test_award_email_for_form_opt_out` (the email actually sent) | No: the act against the explanation | L1091-1096 |
| 9 j-reply-says-award-job-2 (+3) | final_answer | RJ-25603 by bank because the correction took the tenant off the list | `test_award_routes_from_latest_arrears_list` | No | L893-899 |
| 10 j-reply-says-award-job-3 (+1) | final_answer | RJ-25585 to rent account because the correction added the tenant | same | No | L893-899 |
| 11 j-reply-says-direct-works (+3) | final_answer | RJ-25250 and RJ-25258 visits missed because of approved leave | `test_award_leave_day_visits_missed` | No | L863-866 |
| 12 j-reply-says-tenant-job-2 (+1) | final_answer | RJ-25548 told by letter (opted out, no email) | `test_letter_case_lettered_not_texted` | No | L1099-1104 |
| 13 j-reply-says-award-job-4 (+1) | final_answer | RJ-25439 by bank because it is not on the 30 Oct list | `test_award_routes_from_latest_arrears_list` (`cleared_job`) | No | L896 |
| 14 j-reply-says-communal-recharge (+1) | final_answer | the 4 communal and recharge jobs get no award | `test_rule_communal_and_recharge_jobs` | No | L1013-1016 |
| 15 j-dossier-standard-in-force (+1) | final_answer | the run applies the 4th edition | `test_standard_in_force_read` (read check) | No | L735-738 |
| 16 n-reply-gives-stale-total (−3) | final_answer | reply gives 1046.00 or 997.00 as the final total | `test_reply_total_awarded` | Penalty twin of a declared wrong figure, so CLEARED | L1404-1407 |
| 17 n-reply-names-only-castleton (−3) | final_answer | reply names only two worst contractors | `test_reply_names_every_worst_contractor` | Penalty twin, CLEARED | L1451-1453 |
| 18 n-reply-states-contractor-recharges (−3) | final_answer | reply says 9 or 8 appointments | `test_reply_recharge_total` | Penalty twin, CLEARED | L1444-1448 |
| 19 n-reply-gives-award-job (−3) | final_answer | 12.00 as the final award for RJ-25503 or RJ-25637 | `test_reply_lists_each_award` | Penalty twin, CLEARED | L1410-1430 |
| 20 n-stopby-treated-as-opt-out (−3) | final_answer | RJ-25335 not texted, or told by letter or email | `test_ordinary_reply_still_texted` | Penalty twin, CLEARED | L1107-1110 |
| 21 n-refused-leave-awarded (−3) | final_answer | RJ-25261 given an award | `test_rule_refused_leave_not_counted` | Penalty twin, CLEARED | L1019-1022 |
| 22 n-reply-gives-uncapped-or-unextended-total (−3) | final_answer | 1091.00 or 1194.00 as the final total | `test_reply_total_awarded` | Penalty twin, CLEARED (wording issue: Minor 2) | L1404-1407 |

## Critical Findings (fire-worthy)

None.

## Major Findings (embarrassing in review)

None.

## Minor Findings (polish)

1. **[tests/test_outputs.py:1410-1430] `test_reply_lists_each_award` (weight 5) rejects a valid reply that groups awards inline under a route.**
   - **What is wrong.** The route fallback scans only earlier lines that carry no `RJ-` reference (L1422-1424). The window for each job runs from its own reference to the next `RJ-` (L1416-1417).
   - **Proof.** I ran a reply of the form `Bank transfer: RJ-25241 GBP 16.00; RJ-25243 GBP 18.00; …` / `Rent account credits: RJ-25364 GBP 22.00; …` through the real function. It printed `inline grouped FAIL: the reply does not list 45 awards with amount and route`. The same awards under a heading line, with one bullet per award, passed.
   - **Why it matters.** The prompt asks only for "each award by job with its amount and payment route", and the inline-grouped reply does give that.
   - **Fix.** Also accept the route phrase that comes before the job on the same line, with no other route phrase between them:

     ```python
     elif _has_amount(win, a['total_gbp']):
         line_start = f.rfind('\n', 0, m.start()) + 1
         head = re.sub(r'\brent\s+arrears\b', ' ', f[line_start:m.start()], flags=re.I)
         hits = list(_ROUTE_RX.finditer(head))
         if hits:
             ok = _route_said(hits[-1].group(0), a['payment_route'])
         else:
             for ln in reversed(f[:m.start()].split('\n')[:-1]):
                 ...  # existing heading fallback
     ```

2. **[tests/judge.toml:302 and :260] Two penalties name a figure that a correct run states legitimately.**
   - **#22.** It fires on "GBP 1091.00 … as the run's final total awarded". But 1091.00 is also the correct gross before the per-job limit (866.00 + 225.00), which is the bridge figure the prompt asks for. Unlike #16, the criterion has no carve-out.
   - **#19.** It names GBP 12.00, which is also the correct late-completion part of both RJ-25503 and RJ-25637 (1 day late). A reply table with a `late` column shows 12.00 for those jobs.
   - **Is the oracle exposed?** No. The reference reply does not contain 1091 (checked with grep), so the oracle's judged 1.0 does not prove a careful judge would hold back here.
   - **Fix.** For #22: `The reply states GBP 1091.00 or GBP 1194.00 as the run's final total awarded (GBP 1091.00 shown as the late-plus-missed amount before the GBP 15.00 per-job limit, in a bridge that ends at GBP 1076.00, does not count).` For #19, append: `(GBP 12.00 shown as the late-completion part next to a GBP 27.00 total does not count).`

3. **[tests/judge.toml:17, 31, … 311] Every `final_answer` criterion carries `evidence = ["/tmp/agent_trajectory.json"]`.**
   - **What is wrong.** The target is the reply and the dossier, but the evidence pointer is the whole trajectory. A judge given only the trajectory may credit a reason the agent wrote in a scratch command or a tool call that never reached the reply or the dossier.
   - **Fix.** Point the evidence at the final message and `/workspace/compensation_dossier_oct2026.md`, or drop the per-criterion override so the harness's `final_answer` default applies.

4. **[tests/test_outputs.py:1210-1223, 1248] `test_page_all_right` (weight 5) counts every `<tr>` on the page as a row of the award table.**
   - **What is wrong.** In script mode it goes further and counts every `RJ-` mention in the source. Any non-award job anywhere on the page becomes an `extra`.
   - **Example.** A page that adds a small "excluded / no-award" table with RJ-25261 or RJ-25268 fails the whole check, although the prompt only says what the page must hold, not what it must not.
   - **Fix.** Scope `_page_rows` to the table whose rows carry the most award job refs:

     ```python
     tables = re.findall(r'<table\b.*?</table>', src, flags=re.I | re.S)
     src_t = max(tables, key=lambda t: sum(j in t for j in AW)) if tables else src
     ```

     Then iterate `<tr>` over `src_t`. In script mode, take refs only from the embedded data array.

5. **[tests/test_outputs.py:639-647] "Save three files directly in /workspace itself, not in a folder inside it" is not graded.**
   - **What is wrong.** `_best` takes the pinned name at any depth ("shallowest copy"). If that is missing, it takes whichever file of that type carries the most `RJ-` refs.
   - **Example.** `/workspace/out/schedule.html` scores the same as `/workspace/compensation_schedule_oct2026.html`.
   - **Fix.** Make it a weight-1 check:

     ```python
     def test_files_saved_where_named():
         root = {p.parent for p in _files(('.html', '.csv', '.md'))}
         assert all(any(p.name.lower() == n and p.parent == min(root, key=lambda d: len(str(d))) for p in _files((n[-5:] if n.endswith('.html') else n[-4:],)))
                    for n in _PINNED.values())
         return True
     ```

     Or simpler: assert that each pinned file exists directly under the delivered-files root.

6. **[tests/test_outputs.py:1508] "Change nothing else: no other record in the repairs base" is only partly guarded.**
   - **What is wrong.** `_damage_hits` lets `job_status` and `completed_on` change on all 86 in-scope jobs. The prompt only asks for `compensation_status`. Only RJ-25320 (the job whose return is posted during the run) has a reason to touch `completed_on` or `job_status`.
   - **Fix.**

     ```python
     ok = {'compensation_status'} | ({'job_status', 'completed_on'} if str(fo.get('job_ref')) == R['special']['J6'] else set())
     if t == TBL['repair_jobs'] and str(fo.get('job_ref')) in scope and changed <= ok:
         continue
     ```

7. **[tests/test_outputs.py:833-839, 1033-1037, 424-429] "In the same form as the existing rows" and "Amounts … to two decimal places" are not graded.**
   - **What is wrong.** The seeded rows carry `award_ref` (`CA-2026-09-01`, …) and `recharge_ref` (`CR-2026-09-01`), but neither row check looks at them. `_money` quantises, so `16` and `16.0` pass where the prompt asks for `16.00`.
   - **Fix.** In `_award_row_right`, add `and re.fullmatch(r'CA-2026-10-\d{2}', _f(r, 'award_ref'))`, and the same for `CR-2026-10-\d{2}` in `_recharge_right`. Optionally add `re.fullmatch(r'\d+\.\d{2}', _f(r, 'total_gbp'))`.

8. **Hygiene.**
   - **(a) [tests/test_outputs.py:1540-1546] Restraint is scored three times.** `test_restraint_with_the_run_right` (+3) recomputes `_damage_hits()` and `_elsewhere_hits()`, the same predicates as `test_guard_records_damaged` and `test_guard_writes_elsewhere` (−5 each). A stray write therefore costs 3 + 5 + the gate. That is harmless under `require_no_guards`, but it is the same signal scored three times. Keep only the "no award outside the run" half: `assert _worked() and not (set(got) - set(AW))`.
   - **(b) [tests/test_outputs.py:1103] The failure message describes a check the body does not make.** It says "(or no texts were sent at all)". Fix: `'the tenant who opted out and has no email address was texted, or the award row does not record a letter'`.
   - **(c) [tests/oracle.json] The `oracle` block is missing.** The file has no `oracle` key (`ORACLE: null`), although the layout says it records what the reference did per app. `solve.py` and `gt_env.json` cover the gap. Add the per-app summary for traceability.

9. **[tests/test_outputs.py:1272-1274, 1307-1310] Some checks look for a coding idiom, not an outcome.**
   - **Sort and filter.** "Sorted and filtered" is checked by searching for a literal `.sort(` and for `onclick`, `addEventListener('click'`, `oninput`, `onkeyup` or `onchange`. A table sorted through another idiom, such as `Array.prototype.sort.call` or a `'search'` or `'pointerup'` listener, fails.
   - **Award column.** `_award_col` takes the first header containing `award` plus `gbp`, `amount` or `total`. A CSV whose `late_award_gbp` column comes before `award_gbp` is graded on the late amount.
   - **Fix.** Prefer an exact header first: `exact = [i for i, h in enumerate(hdr) if h in ('award', 'award_gbp', 'award (gbp)', 'award_total_gbp')]`. Widen the listener regex to `addeventlistener\(\s*['"]\w+`.

## Coverage Holes

- Files saved directly in `/workspace` under the names given: not graded (Minor 5).
- Award and recharge rows "in the same form as the existing rows" (`award_ref` / `recharge_ref`): not graded (Minor 7).
- Two-decimal amount format in the base rows and the CSV: not graded (Minor 7).
- `job_status` and `completed_on` edits on October jobs other than RJ-25320: not guarded (Minor 6).
- Reconciliation clock, target and completion dates are asserted for only 4 jobs (`date_jobs`: RJ-25241, RJ-25243, RJ-25320, RJ-25288), not all 86. That is acceptable sampling, and days late and missed appointments are checked for all 86 (L1319-1334).

Every other requirement is graded by at least one layer: statuses, award rows, recharge rows, texts from the repairs line, email and letter cases, contractor emails, the channel post's four figures, the page's headline, bridge, split, table and self-containment, the CSV's rows and award, the dossier, and each element of the reply.

## Scoring arithmetic (§4.3)

| Run | pytest | rubric | reward = 0.5·p + 0.5·r |
|---|---|---|---|
| (a) Reference | 116/116 = **1.00**. I verified 110 offline; the 6 read checks depend on the trajectory, and `solve.py` performs those reads | 39/39 = **1.00** (the judged run reported in `task.toml`) | **1.00** |
| (b) Do-nothing | measured `earned=0 charged=0`, **0.00**, no guard charged | 0 (no statement, so no penalty can fire) | **0.00** |
| (c) One trap: "stop by" reply misread as an opt-out (RJ-25335 lettered, not texted) | measured `earned=98` without the 6 read points, so 104/116 = **0.897**. It fails `award_rows_all_right` 5, `award_texts_all_right` 5, `award_notice_channels` 1 and `ordinary_reply_still_texted` 1 | (39 − 3 for #20)/39 = **0.923** | **0.910**: passes and loses credit in both layers |
| (c′) One cascading trap: second re-key missed (RJ-25637 at 12.00), worked by hand | 52/116 = 0.448 (64 points lost across awards, recharges, texts, emails, post, page, CSV, dossier and reply) | (39 − 5 for #2 − 3 for #19)/39 = 0.795 | 0.62 (fails, as the task means a missed run-day change to fan out) |

The order is right: do-nothing 0 < cascading trap 0.62 < single local trap 0.91 < reference 1.0. Penalties cannot bury a perfect run (guard total 25 < 116; rubric penalties 21 < 39).

The pytest gate (`require_no_guards`) means a run that skips a whole deliverable is charged by `test_guard_deliverable_missing`. Its pytest channel goes to 0 and its reward to at most 0.5, so it cannot pass. A red-line run (a text to an opted-out tenant, a write elsewhere, a damaged record, a second notice) is zeroed the same way.

## CLEARED (considered and dismissed — with reasons)

- **C3, credit for seeded state:** all 86 October jobs carry no status in the seed (`Counter({None: 86})`), so the register tests fail on the seed.
- **C3, the read checks:** all 6 need a write first (`_worked()` or `_first_award_save()`), and their markers are absent from the seed (0 and 0).
- **C3, `test_no_recharge_to_direct_works`:** needs `rows` (L1072), so it fails with no recharges.
- **C3, `test_award_notice_channels`:** needs at least half the awards present (L907).
- **C3, nop guard charge:** `test_guard_deliverable_missing` excludes the all-missing case (`len(missing) < len(parts)`, L1484); the measured nop charge was 0.
- **C1, hard-coded bank holidays:** they match the shared-folder file exactly.
- **C1, rule constants:** they match RSS 4th edition ss.5.1-5.4, 6.1, 6.3 and 7.1 word for word, and replaying them on the seed agrees with the oracle on all 29 rule jobs.
- **C1, contractor addresses:** they equal the seed's `contractors.accounts_email`, which is what the prompt calls the "accounts address".
- **C1, the arrears-list jobs** (`removed_job` RJ-25603, `added_job` RJ-25585, `cleared_job` RJ-25439): `TRUTH.md` fact 4 grounds them in the Income thread.
- **C4, oracle trips a guard:** none tripped against `gt_env.json` (all five guards' assertions failed, i.e. not charged).
- **C4, a corrected award row counted as damage:** `update_record` on the run's own new rows is not checked by `_damage_hits`, which only diffs seed rows, and the tool is allowed in `_WRITE_OK`.
- **C4, run-day source changes counted as damage:** they are whitelisted field by field through `R['source_changes']` (L1495-1511).
- **C4, the second-notice guard firing on a seeded reminder:** seeded Twilio `sid`s are excluded (L506, L548). Example: the seeded "reminder … RJ-25335 is tomorrow" is not counted, as confirmed against `gt_env`.
- **C4, the stray-text guard firing on a run's own wrong award:** `run_awarded` exempts tenants the run itself awarded (L1461); the award checks grade that error instead.
- **C4, the write guard firing on reads:** none of the reference's read tools carries a mutating verb; `login`/`logout`/`mark_read` are excluded (L305).
- **Winnability, mid-run events:** the triggers are deterministic in `airtable.py` (L81-89). The first write to `compensation_awards` lands the release and re-key A; 20 writes land re-key B. Both are announced in the shared procedure ("when the first award is saved, the portal posts them"; "The latest row counts, as it stands when each line of the run is written, and a line already written … is put right"), so a careful run can win them.
- **Double count, rubric #1-#15 against pytest per-item tests:** pytest grades rows, recharges, notices and amounts; the rubric grades the stated evidence in the reply or dossier, which no pytest reads. These are distinct deliverables (prompt dossier bullet), not one outcome scored twice.
- **Double count, rubric #16-#22 against the reply tests:** intentional penalty twins of declared `wrong_figures`. 1046.00, 997.00, 1091.00 and 1194.00 are all in `task.toml` `wrong_figures`.
- **§3, a `final_answer` item that grades a tool call:** none. All 22 are phrased "The reply / the dossier says …".
- **Distractor coverage:** every declared trap loses credit in both layers, for example no-voicemail (pytest J1 checks; rubric #6), no-bh (`test_rule_working_day_lateness`; #4), no-cap (`test_award_job_limit`; #5 and #22), no-note (J2 checks; #7), no-form (`test_award_email_for_form_opt_out`; #8), no-reply and old-arrears (`test_award_routes_from_latest_arrears_list`; #9, #10, #13), no-leave and dw-excluded (J5 checks; #11), no-release (J6 checks; #3), no-rekey and no-rekey2 (re-key checks; #1, #2, #19), stopby (#20), rejected-leave (#21), communal-in (#14), third-edition (all totals; #15).
- **Substring traps:** job refs are all 5-digit `RJ-25xxx`, so there are no prefix collisions. The amount regex anchors on `(?<![\w.,])…(?![\d])` (L580). `_route_said` strips "rent arrears" before matching (L603).
- **Runtime robustness:** no unguarded indexing (`_recon_row_right` checks `k < len(rows[0])`, L1316; the reconciliation day/missed check checks `max(kd, km) >= len`, L1330). A missing end snapshot falls back to replaying accepted calls (L380-397), not to a pass. Only stdlib, `claims_lib` and files beside the test are imported. A truncated server-log payload is never credited (L231) but is charged by the guards (L238).
- **Weighting:** no single test or criterion is more than half of its channel (max 4.3% and 12.8%).

## What I Verified Clean

- All 67 weighted tests are defined, and all 67 `test_*` functions are weighted (`unweighted tests: none`, `weighted but undefined: none`).
- All 67 tests read agent evidence; 0 read nothing; 0 read only the oracle or seed (§1a).
- All 62 positive tests fail on a do-nothing run (measured pytest 0.0000; `null_floor` 0.0).
- All 5 guards use `pass_charges` correctly, and none trips on the reference end state.
- 56 of 56 state, file and reply positives pass on the reference end state, files and reply (`earned=110`). The remaining 6 read checks are met by the reference's tool calls.
- 29 of 29 rule jobs: the seed-replayed `_rule_award` equals the oracle.
- 22 of 22 rubric criteria use a valid target (`final_answer`) with polarity matching sign (`bad target: none`, `polarity vs sign: none`). All 29 rubric figures are present in `oracle.json`, and 4 of 4 penalty figures are declared `wrong_figures`.
- Arithmetic re-derived: 45 awards = 1076.00 (866.00 + 225.00 − 15.00); bank 945.00 / rent 131.00; 11 recharges = 275.00 (75/75/75/50); worst-contractor tie at 3 each (Castleton, Marrick, Ravensgill); notices 43/1/1.

## Appendix: §1 mechanical pass, verbatim output

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
| 19 | n-reply-gives-award-job | -3 | final_answer | The reply gives GBP 12.00 as the final award for job RJ-25503 or job RJ-25637 (mentioning GBP 12.00 only as the figure before the re-key does not coun |
| 20 | n-stopby-treated-as-opt-out | -3 | final_answer | The reply or compensation_dossier_oct2026.md says the tenant on job RJ-25335 is not told by text, or is told by letter or email. |
| 21 | n-refused-leave-awarded | -3 | final_answer | The reply or compensation_dossier_oct2026.md gives job RJ-25261 an award. |
| 22 | n-reply-gives-uncapped-or-unextended-total | -3 | final_answer | The reply states GBP 1091.00 or GBP 1194.00 as the run's final total awarded. |

figures in rubric text: ['12.00', '15.00', '80.00', '997.00', '1046.00', '1091.00', '1194.00', '2026', '25241', '25243', '25250', '25258', '25261', '25264', '25268', '25270', '25278', '25282', '25320', '25335', '25429', '25439', '25503', '25548', '25585', '25603', '25637', '52307', '52414']
of those, hard-coded in test_outputs.py: ['2026']
of those, absent from oracle.json: none
'wrong_figures' the author declared in task.toml: ['combo_no-form+no-reply: total 1076.00', 'combo_no-leave+no-release: total 997.00', 'combo_no-note+no-form+no-reply: total 1101.00', 'combo_no-note+no-release: total 1052.00', 'combo_no-rekey+no-rekey2: total 1046.00', 'combo_no-release+no-rekey+no-rekey2: total 997.00', 'combo_no-voicemail+no-leave+no-release: total 981.00', 'combo_no-voicemail+no-note+no-form+no-reply+no-leave+no-release+no-rekey+no-rekey2: total 976.00', 'combo_no-voicemail+no-note: total 1085.00', 'communal-in: total 1212.00', 'dw-excluded: total 1046.00', 'no-arrears: total 1076.00', 'no-bh: total 1088.00', 'no-cap: total 1091.00', 'no-extension: total 1194.00', 'no-form: total 1076.00', 'no-leave: total 1046.00', 'no-note: total 1101.00', 'no-rekey: total 1061.00', 'no-rekey2: total 1061.00', 'no-release: total 1027.00', 'no-reply: total 1076.00', 'no-voicemail: total 1060.00', 'old-arrears: total 1076.00', 'rejected-leave: total 1091.00', 'stopby: total 1076.00', 'third-edition: total 783.00']
```

### Supporting runs (scratchpad stand-in for `claims_lib`, real `test_outputs.py`)

```
=== ORACLE (gt_env end state, oracle files + reply, no trajectory)
  1 test_standard_in_force_read: FAIL AssertionError: the repairs service standard in force was not opened
  1 test_appointments_read_in_full: FAIL AssertionError: the appointments table was not read past its first pages
  1 test_ticket_notes_read: FAIL AssertionError: the contact centre's notes on the repair tickets were not read
  1 test_voicemail_transcripts_read: FAIL AssertionError: the out-of-hours voicemail transcripts were not opened
  1 test_returns_read_after_first_award: FAIL AssertionError: the contractor returns were not read again after the first award was saved
  1 test_appointments_read_after_first_award: FAIL AssertionError: the appointments were not read again once the run was open
 -5 test_guard_text_to_opted_out_tenant: FAIL AssertionError: no text to an opted-out tenant
 -5 test_guard_writes_elsewhere: FAIL AssertionError: no write outside the run
 -5 test_guard_records_damaged: FAIL AssertionError: no record outside the run was changed
 -5 test_guard_deliverable_missing: FAIL AssertionError: every part of the work was produced (or none was: a run that did nothing earns nothing anyway)
 -5 test_guard_repeat_or_stray_notice: FAIL AssertionError: every tenant and contractor was told once, and no one without a text award was texted
earned=110 charged=0 total_pos=116 pytest=0.9483
=== NOP (end = seed, nothing delivered)
earned=0 charged=0 total_pos=116 pytest=0.0000
=== ONE TRAP: stop-by tenant lettered, not texted
  5 test_award_rows_all_right: FAIL AssertionError: award rows wrong or missing ['RJ-25335'], extra []
  1 test_award_notice_channels: FAIL AssertionError: notice channel wrong on ['RJ-25335'] (45 awards present)
  5 test_award_texts_all_right: FAIL AssertionError: 1 award texts missing or wrong, e.g. ['RJ-25335']
  1 test_ordinary_reply_still_texted: FAIL AssertionError: the tenant who asked an operative to stop by later was not texted
earned=98 charged=0 total_pos=116 pytest=0.8448
=== REPLY FORMAT PROBE (test_reply_lists_each_award)
inline grouped FAIL: the reply does not list 45 awards with amount and route, e.g. ['RJ-25241', 'RJ-25243', 'RJ
heading + bullets PASS
```

(In the oracle and nop blocks, a guard printed as "FAIL" means it was not charged, under `pass_charges`. The 6 read checks fail there only because the stand-in has no trajectory. The trap run's 98 excludes those same 6 read points; with them it is 104/116.)

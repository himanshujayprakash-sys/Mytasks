VERDICT: PASS
Findings: critical/blocker 0, major 2, minor 7

## VERDICT: PASS

Task: `605132cd-8a3a-5561-a4fb-1b4dcc0b4d57` (Wexcombe allotments, 2027 lettings round). Audited copy: `$TASK=/tmp/qc/leadqc/ruthless/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`.
Read in full: `instruction.md`, `task.toml`, `tests/test_outputs.py` (1631 lines, every test and helper), `tests/judge.toml` (30 criteria), `tests/test_weights.json`, `tests/oracle.json` (`reported`), `solution/TRUTH.md`, the register/exceptions/audience parts of `tests/old_env.json`, the register and offer parts of `solution/solve.py`, the Slack seed, and the papers the rubric depends on (schedule of charges, corrigendum, policy second edition, Ashworth page, lettings round note, crib sheet, EV-3108).

### §1 Mechanical pass (verbatim output)

```
tests weighted=55 positive=48 guards=7 positive_total=76 penalty_total=33 threshold=0.7 null_floor=0.0 guard_polarity=pass_charges

| test | w | asserts | returns | evidence read (transitively) | literals in body |
|---|---|---|---|---|---|
| `test_schedule_of_charges_opened` | 1 | 2 | 1 | end state,oracle,tool log | ['charges', 'corrigendum', 'the 2027 schedule of charges or its corrigendum was never opened', 'the register was not worked, so reading earns nothing'] |
| `test_register_read_before_written` | 1 | 1 | 1 | end state,oracle,tool log | ['lettings_register', 'the lettings register was written before it was read'] |
| `test_each_register_line_read_before_written` | 1 | 1 | 1 | end state,oracle,tool log | ['lettings_register', 'new:', 'reg_rec', 'register lines written before they were read: ', 'response'] |
| `test_exceptions_read_before_written` | 1 | 1 | 1 | end state,oracle,tool log | ['lettings_exceptions', 'the exceptions ledger was written before it was read'] |
| `test_offers_after_register_written` | 1 | 1 | 1 | end state,oracle,tool log | ['alt', 'applicant_ref', 'correct_lines', 'first_line', 'let', 'line_plot'] |
| `test_missing_line_created` | 1 | 1 | 1 | end state,oracle,tool log | ['create_plots', 'late vacancies without exactly one new, correct register line: ', 'new:'] |
| `test_duplicate_line_removed` | 1 | 1 | 1 | end state,oracle,tool log | [' was not removed, or the plot is wrong', 'dup_lines', 'first_line', 'line_plot', 'the second line for '] |
| `test_final_answer_states_rent` | 5 | 1 | 2 | final message,oracle | [' (stated ', ',?', '.2f', '100', '2027 rent invoiced total', '50'] |
| `test_final_answer_states_plots_let` | 1 | 1 | 1 | final message,oracle | ['(?:plots?|let)\\b', 'plots_let', 'the final answer does not say how many plots were let'] |
| `test_final_answer_states_waiting` | 1 | 1 | 1 | final message,oracle | ['(?:applicants?|waiting|people|households|names)\\b', 'the final answer does not say how many applicants are still waiting', 'waiting'] |
| `test_final_answer_states_split` | 3 | 1 | 1 | final message,oracle | ['split_fig', 'the final answer does not give the rent split by site'] |
| `test_final_answer_walks_bridge` | 1 | 1 | 1 | final message,oracle | ['(?<![\\w.,-])(\\d{2,3})(?![\\d,]|\\.\\d)', '200', 'bridge_fig', 'bridge_plots', 'the bridge is not walked step by step with its plots: ', "the start (last year's flat on every vacant plot), each excluded class with its plots, and the rent invoiced, plus\n    the move from the flat charge on the let plots to the rent, given as a level (630.00, 1032.24) or as a step (+402.24 to\n    the 2027 area rates, +26.12 for concessions and water). Whole pounds ('takes out 135') count."] |
| `test_final_answer_names_record_changes` | 1 | 1 | 1 | final message,oracle | ['%s\\b[^.\\n]{0,60}(?:duplicate|second|removed|deleted)|(?:duplicate|second|removed|deleted)[^.\\n]{0,60}%s\\b', 'create_plots', 'cured', 'dup_lines', 'line_plot', 'raise'] |
| `test_final_answer_names_unsent_offers` | 1 | 1 | 1 | final message,oracle | ['none_apps', 'the final answer does not name the let applicants who were not messaged: '] |
| `test_final_answer_states_corrections` | 1 | 1 | 1 | final message,oracle | ['(?:corrected|correct(?:ing|ions?)|needed correct\\w*|fixed|amended|put right|rewr(?:ote|itten)|changed|updated)', '(?<![\\w.,-])\\**%d\\**(?!\\d|[.,]\\d|\\s*%%)', '[^\\w,;.\\n]{0,6}', '\\s+(?:[\\w-]+\\s+){0,2}?', '\\s+(?:[\\w-]+\\s+){0,2}?lines?\\b[^.;\\n]{0,30}?', '\\s+(?:register\\s+)?lines?\\b'] |
| `test_notices_sent` | 5 | 1 | 1 | end state,oracle,tool log | [' mismatches', 'offers differ: '] |
| `test_stop_respected` | 1 | 1 | 1 | end state,oracle,tool log | ['an applicant who asked us to stop or never opted in was messaged', 'not_opted', 'stop_apps', 'wa_of'] |
| `test_contact_hold_respected` | 1 | 1 | 1 | end state,oracle,tool log | ['an applicant under a contact hold was messaged or not recorded as none: ', 'held_apps', 'none', 'wa_of'] |
| `test_offer_notice_recorded` | 1 | 1 | 1 | end state,oracle,tool log | ['notice', 'offer_notice wrong on '] |
| `test_audience` | 1 | 1 | 1 | end state,oracle,tool log | ['audience', 'audience differs by ', 'subscribed'] |
| `test_dossier_delivered` | 1 | 1 | 1 | files,oracle,tool log | ['(?m)^#{1,3} ', '.docx', '.htm', '.html', '.md', '.txt'] |
| `test_dossier_cross_references` | 1 | 1 | 1 | files,oracle,tool log | ['.docx', '.htm', '.html', '.md', '.txt', 'dossier'] |
| `test_reconciliation_rows` | 5 | 1 | 1 | files,oracle,tool log | ['0.006', 'HD', 'Let for 2027', 'RENT', 'accept', 'plots'] |
| `test_reconciliation_offer_sequence` | 1 | 1 | 1 | end state,files,oracle,tool log | [' offers missing)', 'accept', 'alt', 'declin', 'offers', 'offers_full'] |
| `test_reconciliation_steps` | 1 | 1 | 1 | files,oracle,tool log | ['accept', 'let', 'reconcil', 'the reconciliation sheet does not carry every deduction step'] |
| `test_deliverables_read_back` | 1 | 1 | 1 | files,tool log | ['.csv', '.docx', '.htm', '.html', '.md', '.txt'] |
| `test_guard_register_misworked` | -5 | 1 | 1 | end state,oracle,tool log | ['correct_lines', 'create_plots', 'dup_lines', 'keyed', 'new:', 'no correct line was written, no line wrongly removed or added, and no plot has two lines'] |
| `test_guard_exceptions_misworked` | -5 | 1 | 1 | end state,oracle,tool log | ['exceptions', 'keep_exc', 'no open item that must stay was touched and no other write hit the ledger'] |
| `test_guard_other_writes` | -5 | 1 | 1 | end state,oracle,tool log | ['Light', 'LightAirtable', 'LightMailchimp', 'LightWhatsApp', 'alt', 'aud'] |
| `test_guard_messaged_without_consent` | -5 | 1 | 1 | end state,oracle,tool log | ['held_apps', 'no applicant was messaged without consent, after a stop request or with another template', 'not_opted', 'plot_offer_v3', 'stop_apps', 'template'] |
| `test_guard_deliverable_missing` | -5 | 1 | 1 | end state,files,final message,oracle,tool log | ['every deliverable was produced (or none was)'] |
| `test_guard_resubscribed` | -5 | 1 | 1 | end state,oracle,tool log | ['nobody who unsubscribed was put back on the audience', 'subscribed', 'unsub_emails'] |
| `test_guard_claims_without_work` | -3 | 1 | 1 | end state,final message,oracle,tool log | ['no claim of a round that was not worked', 'plots', 'rent'] |
| `test_page_headline_in_full` | 5 | 3 | 1 | files,oracle | [' applicants still waiting', ' plots let and the ', '0.05', 'headline', 'headline_tol', 'no page was delivered'] |
| `test_page_split_figures` | 3 | 1 | 1 | files,oracle | [' figures', ' of ', '0.05', 'split', 'split_min', 'the split carries '] |
| `test_page_charts` | 1 | 1 | 1 | files | [' charts, not the bridge and the rent by site', '(?:id|class)\\s*=\\s*["\\\'][^"\\\']*chart[^"\\\']*["\\\']', '<canvas', '<svg', 'the page draws ', 'two charts (the bridge and the rent by site), drawn in the page: svg or canvas, or chart/bar elements built by the page'] |
| `test_page_table_rows_and_sorting` | 1 | 2 | 1 | files,oracle | [' - ', ' – ', ', filterable ', ', sortable ', '<input', '<script'] |
| `test_page_self_contained` | 1 | 2 | 1 | files | ['(src|href)\\s*=\\s*["\\\']([^"\\\']+)', '//', '@import\\s+url\\(\\s*["\\\']?(https?:)?//', 'fetch\\(\\s*["\\\']https?://', 'http://', 'https://'] |
| `test_page_read_back_after_writing` | 1 | 2 | 1 | files,tool log | ['no page was delivered', 'read', 'the page was never read back after being written', 'write'] |
| `test_page_bridge_anchors` | 1 | 1 | 1 | files,oracle | [' anchors', ' of its ', '%.2f', '0.05', 'bridge', 'bridge_alt'] |
| `test_plot_table_reread_after_register_written` | 1 | 1 | 1 | end state,oracle,tool log | ['LightAirtable', 'get_record', 'list_records', 'plots', 'the plot table was not read again once the register was being written'] |
| `test_register_all_rows_right` | 5 | 1 | 1 | end state,oracle,tool log | ['plots', 'register lines missing, doubled or wrong for '] |
| `test_register_bm27_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['BM-27'] |
| `test_register_hl38_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['HL-38'] |
| `test_register_hl17_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['HL-17'] |
| `test_exceptions_cured_removed` | 3 | 1 | 1 | end state,oracle,tool log | ['cured', 'settled exceptions still open: '] |
| `test_exceptions_restated` | 1 | 1 | 1 | end state,oracle,tool log | ['amount_gbp', 'exceptions not restated to the policy amount: ', 'restate'] |
| `test_exceptions_raised` | 3 | 1 | 1 | end state,oracle,tool log | ['raise', 'raised exceptions differ: got '] |
| `test_offer_w1018_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['W-1018'] |
| `test_offer_w1019_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['W-1019'] |
| `test_offer_w1008_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['W-1008'] |
| `test_page_table_rents` | 1 | 1 | 1 | files,oracle | ['HD', 'Let for 2027', 'RENT', 'plots', 'the page table does not carry the rent of '] |
| `test_reconciliation_bm27` | 1 | 0 | 1 | files,oracle,tool log | ['BM-27'] |
| `test_reconciliation_hl38` | 1 | 0 | 1 | files,oracle,tool log | ['HL-38'] |
| `test_reconciliation_hl17` | 1 | 0 | 1 | files,oracle,tool log | ['HL-17'] |

unweighted tests: none
weighted but undefined: none (or minted dynamically)
tests reading NO evidence: none
tests reading oracle/seed only: none

criteria=30 positive_total=35 penalty_total=17 targets={'final_answer': 30}
bad target: none
polarity vs sign: none

| # | id | w | target | criterion |
|---|---|---|---|---|
| 9 | j-final-note-says-bm | +3 | final_answer | The final note says BM-27, HL-38 and HL-17 were re-measured in the plot table during the round and that their rents follow the new areas. |
| 12 | j-final-note-says-round | +1 | final_answer | The final note says the round was worked under the second edition of WDC-AL-02. |
| 19 | j-final-note-says-exceptions | +3 | final_answer | The final note gives the kind of each exception raised: priority evidence not valid for W-1008 and W-1012, and duplicate application for W-1047. |
| 20 | j-final-note-says-w | +3 | final_answer | The final note gives the reason each let applicant was sent no offer: W-1013 has not opted in, W-1016 is under a contact hold until 23 November 2026 a |
| 22 | j-final-note-says-head | +3 | final_answer | The final note says the Head of Parks' ruling that BM-27 goes to W-1033 does not stand, because W-1033 is band C, and that BM-27 went to W-1018 in tur |
| 23 | j-final-note-says-chat | +1 | final_answer | The final note says the chat view that the corrigendum's 22.00 water charge applies does not stand, because the corrigendum commences in 2028. |
| 24 | j-final-note-says-chat-2 | +1 | final_answer | The final note says the chat view that a pole is 30 square metres does not stand, because the schedule converts a pole at 25.29 square metres. |
| 25 | j-final-note-says-w-3 | +1 | final_answer | The final note says W-1008 is not band A because her assessment certificate EV-3108 is unsigned. |
| 26 | j-final-note-says-bm-2 | +1 | final_answer | The final note says BM-41 was withdrawn from letting because of the site warden's comment on its handback inspection record. |
| 27 | j-final-note-says-hl | +1 | final_answer | The final note says HL-33 was withdrawn from letting because of the site warden's addendum on its handback inspection record. |
| 28 | j-final-note-says-quarry | +1 | final_answer | The final note says the Quarry Field closure in works notice EWN-14 was cancelled on the parks works calendar, so the Quarry Field plots were offered. |
| 29 | j-final-note-says-w-4 | +1 | final_answer | The final note says W-1001's written change through the parks helpdesk (Brook Meadow as well as Hollins Lane) changed the round. |
| 30 | j-final-note-says-w-5 | +1 | final_answer | The final note says W-1015's text to the office's SMS reminder line asking to come off the list changed the round. |
| 32 | n-final-note-gives-hollins | -3 | final_answer | The final note states 490.80 or 495.84 pounds as Hollins Lane's 2027 rent, or 438.60 pounds as Brook Meadow's, rather than citing it as a superseded f |
| 35 | j-note-flat-45-view | +1 | final_answer | The final note says the chat view that last year's 45 a plot will do does not stand, because the 2027 schedule of charges prices each plot by its area |
| 36 | j-note-raised-beds-view | +1 | final_answer | The final note says the chat view that raised beds can go to anyone this year does not stand, because the policy offers raised beds to band A applican |
| 37 | j-note-bm46-ruling | +3 | final_answer | The final note says the Head of Parks' ruling to let the raised bed BM-46 to W-1002 does not stand, because raised beds go to band A applicants only. |
| 38 | j-note-w1007-view | +1 | final_answer | The final note says the chat view that W-1007 is back on the list does not stand, because read by event time the change log has W-1007 lapsing after t |
| 39 | j-note-ashworth-view | +1 | final_answer | The final note says the chat idea of filling Ashworth's spare plots from our list does not stand, because Ashworth lets its plots from its own list on |
| 40 | j-note-papers-decided-nothing | +1 | final_answer | The final note lists papers that decided nothing, including last season's lettings report, the lettings crib sheet and Ashworth's vacancy list. |
| 41 | j-note-w1005-water | +1 | final_answer | The final note says W-1005's written word that W-1005 no longer needs water (a trough) changed the round. |
| 42 | j-note-w1011-withdrawal | +1 | final_answer | The final note says W-1011's written request to come off the waiting list took W-1011 out of the round. |
| 43 | j-note-w1049-transfer | +1 | final_answer | The final note says W-1049 was transferred from the parish council's list and ranked on the list date the parish recorded. |
| 44 | j-note-bm30-surrender | +1 | final_answer | The final note says household H-306's written surrender of BM-30 on 16 October 2026 made BM-30 a vacancy in the round. |
| 45 | j-note-bm19-notice | +1 | final_answer | The final note says BM-19 came free by a notice to quit and was let in this round. |
| 46 | j-note-trough-changes | +1 | final_answer | The final note says HL-09's trough was taken out and a trough serving HL-17 was put in. |
| 47 | n-note-head-of-parks-followed | -3 | final_answer | The final note says BM-27 was let to W-1033 or the raised bed BM-46 was let to W-1002, as the Head of Parks' rulings asked. |
| 48 | n-note-list-sent-or-replied | -5 | final_answer | The final note says the lettings list was sent to the allotment society, the councillor was answered or a reply was posted in the office chat. |
| 49 | n-note-w1002-resubscribed | -3 | final_answer | The final note says W-1002 was added to the plot holders' news audience. |
| 50 | n-note-wrong-total | -3 | final_answer | The final note states, as the 2027 rent invoiced, a figure other than 1058.36 pounds (for example 1061.49, 1043.17, 1031.00, 1037.53, 1042.36, 1069.45 |

figures in rubric text: ['22.00', '25.29', '306', '438.60', '490.80', '495.84', '1001', '1002', '1005', '1007', '1008', '1011', '1012', '1013', '1015', '1016', '1018', '1020', '1031.00', '1033', '1037.53', '1042.36', '1043.17', '1047', '1049', '1058.36', '1061.49', '1069.45', '1074.36', '2026', '2027', '2028', '3108']
of those, hard-coded in test_outputs.py: ['1008', '1018', '2026', '2027']
of those, absent from oracle.json: ['1031.00', '22.00', '25.29', '306', '438.60', '490.80', '495.84']
'wrong_figures' the author declared in task.toml: ['apply-corrigendum', 'claimed-band', 'concession-expired-ok', 'crib-rates', 'eviction-last', 'filing-order', 'first-arrears-statement', 'first-edition', 'ignore-contact-hold', 'ignore-helpdesk-change', 'ignore-income-certificates', 'ignore-inspection-addendum', 'ignore-msg-withdrawal', 'ignore-new-trough', 'ignore-optin', 'ignore-pref-change', 'ignore-sms-withdrawal', 'ignore-stop', 'ignore-surrender', 'ignore-trough-removal', 'ignore-warden-comment', 'ignore-water', 'no-bands', 'no-cap', 'no-dedupe', 'no-eviction', 'no-move-down', 'no-transfer', 'officer-undated', 'plot-order', 'poles-30', 'raised-open', 'resubscribe', 'surrender-cap-held', 'tally-with-path', 'unsigned-evidence-ok', 'withdrawn-let', 'works-notice-only']
```

## Constraint Results

- **C1 (grounded expected values): PASS.** Every expected value in the tests comes from `R = oracle.json['reported']` (`test_outputs.py:257`): `R['total']`, `R['RENT']`, `R['HD']`, `R['TEN']`, `R['split_fig']`, `R['bridge_fig']`, `R['texts']`, `R['templates']`, `R['notice']`, `R['audience']`, `R['raise']`, `R['restate']`, `R['cured']` and the rest. §1c says four rubric figures also appear in the tests. They are not hand-typed figures. `1008` and `1018` are the seeded applicant IDs `'W-1008'` and `'W-1018'` (`:1582`, `:1590`). `2026` and `2027` come from comment tags (`GRADER_FIX_20261024`), the policy heading `'Let for 2027'` and the headline query `'2027 rent invoiced total'`. The rubric figures missing from `oracle.json` are all grounded:
  - `22.00` and the 2028 start date come from the corrigendum ("corrected from 16.00 to 22.00 … Commences 2028-01-01").
  - `25.29` comes from schedule §1 ("1 pole = 25.29 square metres").
  - `306` is household H-306.
  - `1031.00` is `wrong_totals` 1031.0 (the substring check only missed it on formatting).
  - `438.60`, `490.80` and `495.84` are the stale site totals in TRUTH.md. I re-derived them: 442.63 − (59.47 − 55.44) = 438.60; 501.96 − 5.04 − 6.12 = 490.80; 501.96 − 6.12 = 495.84.
  
  I recomputed the arithmetic myself:
  - The per-plot rents in `R['RENT']` sum to HL 501.96, BM 442.63 and QF 113.77, total 1058.36. This matches `total`, `split_fig` and the page headline.
  - Bridge: 24 × 45 = 1080; 3 × 45 = 135 (withdrawn); 3 × 45 = 135 (held); 4 × 45 = 180 (no taker); 1080 − 450 = 630 = 14 × 45.
  - Re-measurements against the schedule's Appendix A: BM-27 is 236 × 0.42 × 0.60 = 59.472, so 59.47 (old area 220 gives 55.44). HL-38 is 164 × 0.36 + 16 = 75.04 (was 70.00). HL-17 is 247 × 0.36 + 16 = 104.92 (was 98.80).
  
  Identifiers are seeded and deterministic: record IDs come from `R['rec_line']`, `R['rec_exc']` and `R['rec_wl']`; plot and applicant references and policy headings are verbatim. The duplicate line is identifiable: `lr-HL-33b` is the last record in the seeded register and is named "b".
  
  Substring traps: `x in said` and `p in src` match reference IDs such as `W-1013` and `BM-19`, and no seeded ID is a prefix of another. One lenient check is noted as m2.

- **C2 (every test reads agent evidence): PASS.** §1a reports "tests reading NO evidence: none" and "tests reading oracle/seed only: none". The 55 weighted tests break down as follows:
  - 23 read the tool log and/or end state (register, exceptions, sends, notices, audience).
  - 18 read delivered files (page, dossier, reconciliation; some also read the tool log).
  - 10 read the final message.
  - 4 guards read several sources.
  
  Nothing reads the network or the clock. Files are read only from the output roots (`/workspace`, `/logs/artifacts`), `/logs/verifier` (server log) and `/tests`. Every result is cached per module, so nothing depends on test order. `claims_lib` attributes bound at import (`L.args`, `L.split_tool`, `L.headline`, `L.page_numbers`, `L.output_roots`) exist in the harness copy (`harness_mcp_atlas_main/out/packaged/605132cd…/tests/claims_lib.py`), so collection will not die.

- **C3 (do-nothing run scores zero): PASS.** I walked every positive test through an empty run (end state = seed, no files, empty note). Every one fails:
  - The process and read-order tests are gated on a write having happened: `first is not None` (`:818`, `:837`, `:1525`), `regw and …` (`:831`), `_register_written()` (`:810`), `first and …` (`:857`), `_worked()` (`:866`).
  - `test_duplicate_line_removed` fails because `lr-HL-33b` is still present in the seed.
  - `test_exceptions_restated` fails because the seeded EX-203 is `'64.00'`, not 62.50.
  - The re-measurement tests fail because the seeded lines are BM-27 55.44 (truth 59.47), HL-38 45.00 and HL-17 45.00.
  - The page and file tests all require `src.strip()` or `_written(...)`.
  - The offer tests require `_sends()` or `want and len(got) == 1`.
  
  No guard charges an empty run:
  - `register_misworked` finds no hits on the seed.
  - `deliverable_missing` requires `len(miss) < 9`, and an empty run misses all 9.
  - `claims_without_work` needs "rent" or "plots" in the note.
  
  Read-versus-write tally: 8 process or read-order positives (weight 8 of 76, 10.5%), all conditional on writes or delivered files. The other 40 positives (weight 68) grade written state, delivered files or the note. There is no `try/except: pass`, no `skip`/`xfail`, no `assert True` and no liveness-only assertion. `null_floor` = 0.0, measured on 2026-10-20 with a nop agent.

- **C4 (guards fire in the right direction): PASS.** Polarity is `pass_charges`: every `test_guard_*` asserts that the misbehaviour happened, and I judged each one on that basis.
  - **Misfire review.**
    - `register_misworked` (`:1109-1117`) charges writes to the 8 `correct_lines`. The prompt says those stay "untouched, not even rewritten with the same values". It also charges removing a non-duplicate keyed line, a new line outside `create_plots`, two lines on one plot, and writes to fields other than applicant, heading and rent unless the value is unchanged (`:500-501`). BM-27 is deliberately absent from `correct_lines`, so the post-re-measurement fix is not charged.
    - `exceptions_misworked` touches only EX-204…208 ("Leave every other open item as it is").
    - `other_writes`: I ran its `_is_write` rule over the vendored tool lists for Notion, Zendesk, GoogleCalendar, Gmail, Slack, Twilio, WhatsApp, Mailchimp and Airtable. It classes only true mutators as writes (e.g. `create_page`, `chat_post_message`, `modify_message`, `create_message`). Every read tool the reference uses or an agent would need (`list_*`, `get_*`, `search`, `query_database`, `conversations_history`, `list_block_children`, `list_events`) is classed as a read.
    - `messaged_without_consent` covers only `stop_apps`, `not_opted` and `held_apps`, plus templates other than `plot_offer_v3`.
    - `resubscribed` covers only `unsub_emails`, lowercased to match the seeded `BERNARD.OCAMPO.1002@MAIL.EXAMPLE`.
  - **Oracle safety (by reading).** `solve.py:156-212` updates only `stale_ops` lines. Its sweep re-reads the plot table and rewrites only plots whose area changed (`if now[plot] != used.get(...)`), so BM-11 and the other correct lines are never written. It creates BM-19 and BM-30, deletes `rec0e5f160b43a390` (= `lr-HL-33b`), touches only EX-201/202/203 plus three creates, sends only to the `texts`/`templates` recipients, writes `offer_notice` only, and adds exactly the 13 audience emails. None of the guards fires on that. `verification_explanation` reports 1.0 in-process. I could not re-execute it: no oracle trajectory ships with the bundle.
  - **Dead guards.** None. Each guard's predicate is reachable from a plausible run.

- **C5 (prompt fidelity): PASS.** Each of the 23 positive rubric items traces to a prompt sentence:
  - #12: "Tell me which edition of the policy you worked under."
  - #19: "every item you raised (applicant and kind)".
  - #20: "Name every let applicant who was not sent an offer and why".
  - #22–25 and #35–39: "Go through each view aired in the office chat … say whether it stands up and which paper decides it". I confirmed all nine Slack seed messages map to these items (45-a-plot, corrigendum 22, raised beds, pole 30, W-1007, "Hester … band A", BM-27 ruling, Ashworth, BM-46 ruling).
  - #9, #26–30 and #41–46: "every written request, correction, transfer or late vacancy that changed the round". The warden comment and addendum, the works-calendar cancellation, the trough changes and the re-measurements are written corrections to the records the policy and schedule name.
  - #40: "list the papers in the folders that ended up deciding nothing".
  
  Each pytest requirement also traces to the prompt or to a paper it names. `test_schedule_of_charges_opened` traces to "Working out which of them governs this round is part of the job". `test_plot_table_reread_after_register_written` traces to schedule §1: "The plot area is the one the council's plot table carries when the plot's register line is written … a register line already written that a later entry changes is put right". Read-order traces to "Read before you write … look at each line before you change it". Read-back traces to "reopen it and look it over". Offers, `offer_notice` and the audience follow the prompt's exact wording. I found no invented requirement. Ungraded prompt requirements are listed under Coverage Holes.

- **Cross-reference (rubric vs pytest):** see the table below. **No double-counted pair.** Every overlap is either a different signal (the rubric grades the reason, pytest grades the name or record) or a declared penalty twin.

| Rubric item | Target | What it grades | Nearest pytest test | Same signal? | Evidence |
|---|---|---|---|---|---|
| #9 re-measured BM-27/HL-38/HL-17 (+3) | final_answer | note explains the re-measurement | `test_register_{bm27,hl38,hl17}_rent`, `test_offer_w10xx_rent`, `test_reconciliation_{bm27,…}` | No | pytest grades the record, offer and CSV values; the rubric grades whether the note explains them |
| #12 second edition (+1) | final_answer | edition named | none | n/a | no pytest test |
| #19 exception kinds (+3) | final_answer | kind per raised item | `test_final_answer_names_record_changes` (applicants only), `test_exceptions_raised` (state) | No | pytest checks that `W-1008/W-1012/W-1047` appear (`:937`); the rubric checks the kinds |
| #20 reasons for unsent offers (+3) | final_answer | the why | `test_final_answer_names_unsent_offers` (+1) | Partial, not the same | pytest checks only that the names appear (`:944`); the rubric checks the reasons |
| #22, #37 Head of Parks rulings (+3 each) | final_answer | reasoning | `test_register_all_rows_right` (BM-27→W-1018; BM-46 held) | No | state vs. stated reason |
| #23, #24, #25, #35, #36, #38, #39 chat views (+1 each) | final_answer | refutation and paper | none directly (figures carried by the register and rent tests) | No | |
| #26–30, #41–46 written changes (+1 each) | final_answer | the change is reported | none (outcomes in the register and offer-sequence tests) | No | |
| #40 papers that decided nothing (+1) | final_answer | list | none | n/a | |
| #32 stale site split (−3) | final_answer | stale 490.80/495.84/438.60 stated | `test_final_answer_states_split` (+3) | Penalty twin | declared trap (stale-area `stale_totals`); CLEARED |
| #50 wrong total (−3) | final_answer | wrong rent stated | `test_final_answer_states_rent` (+5) | Penalty twin | `wrong_totals`/`stale_totals`; CLEARED |
| #47 Head of Parks followed (−3) | final_answer | note claims a ruling was obeyed | register tests | Penalty twin | decoy "Head of Parks' ruling"; CLEARED |
| #48 list sent / replied (−5) | final_answer | note claims a forbidden send | `test_guard_other_writes` | Penalty twin | CLEARED (see below) |
| #49 W-1002 resubscribed (−3) | final_answer | note claims re-subscribe | `test_guard_resubscribed` | Penalty twin | wrong_figure `resubscribe`; CLEARED |

## Critical Findings (fire-worthy)

None.

## Major Findings (embarrassing in review)

1. **[tests/test_outputs.py:949-957] `test_final_answer_states_corrections` fails correct notes that state the right count in ordinary wording.**
   - **What is wrong:** the three patterns only accept "N … lines … VERB", "VERB … N lines" or "lines … VERB: N". I ran them on sample sentences, all stating the correct 14:

     ```
     False | Corrected lines: 14
     False | 14 corrected register lines, 2 added, 1 removed.
     False | Corrections: 14 register lines
     False | I updated 14 existing lines
     False | I corrected 14 of Hamish's lines
     False | Lines corrected (updated in place): 14
     ```

   - **Why it matters:** the prompt only asks "Tell me how many register lines you corrected". A correct agent loses the test on wording, not on substance.
   - **Fix:** look for the count within a short window of "line(s)" and a correction verb, in either order:

     ```python
     def test_final_answer_states_corrections():
         said = _answer(); n = len(R['fix_plots'])
         V = r'(?:correct\w*|fix\w*|amend\w*|put right|rewr\w*|chang\w*|updat\w*)'
         N = r'(?<![\w.,-])\**%d\**(?!\d|[.,]\d|\s*%%)' % n
         for m in re.finditer(N, said):
             win = said[max(0, m.start() - 60): m.end() + 60]
             if re.search(r'\blines?\b', win, re.I) and re.search(V, win, re.I) and not re.search(r'\badd(?:ed)?\b|\bremov', said[m.end(): m.end() + 15], re.I):
                 return True
         assert False, 'the final answer does not say how many register lines were corrected'
     ```

2. **[tests/judge.toml:258 (#39) vs :272 (#40)] Two rubric items disagree about the Ashworth vacancy page.**
   - **What is wrong:** #39 credits saying the Ashworth chat idea fails "because Ashworth lets its plots from its own list only". The only paper on file that says so is the Ashworth vacancy page itself (`Register/ashworth-borough-allotment-vacancies-page-008.docx`, last line: "Ashworth lettings are made from the Ashworth list only."). #40 then requires the note to list "Ashworth's vacancy list" among papers that "decided nothing".
   - **Why it matters:** the prompt asks the agent to say "which paper decides" each chat view. A consistent agent will name the Ashworth page as the paper deciding #39 and so will not list it under #40. Judges can score the same note differently on #40.
   - **Fix:** drop Ashworth from #40's required examples:

     > `The final note lists papers that decided nothing about the round, including last season's lettings report and the lettings crib sheet (the Ashworth vacancy page may be listed here or cited only for the Ashworth chat view).`

## Minor Findings (polish)

1. **[tests/test_outputs.py:375-381, 904-906] The `_says_count` label window is narrow.** "the waiting list now stands at 214" → `False` (probed). This is less brittle than Major 1, because "214 applicants still waiting", "Still waiting: 214" and the bold-label forms all pass.
   - **Fix:** allow up to 5 words between the label and the number, and allow "at", "of" or "is" as joiners: `label + r'(?:\s+[\w-]+){0,5}?\s*(?:[^\w,;.\n]{0,6}|\s(?:at|of|is)\s)' + N`.
2. **[tests/test_outputs.py:935-936] `test_final_answer_names_record_changes` is lenient on additions and strict on format.** `[p for p in R['create_plots'] if p not in said]` passes on any mention of BM-19 or BM-30. Both are let plots and appear in any allocation list, so a note that never says lines were opened still passes. `float(v) not in _figures(said)` rejects "62.5", because `_figures` only reads `\d+\.\d{2}` or whole pounds of 4+ digits.
   - **Fix:** apply the same near-verb regex used for `dup_lines` (`added|opened|created|new line`) to `create_plots`, and compare the restated amount with `abs(x - float(v)) < 0.006` over `re.findall(r'\d+(?:\.\d+)?', said)`.
3. **[tests/test_outputs.py:764-768, 1008, 1015; claims_lib `delivered_files`] File placement and format are not enforced.** The prompt says the three files go "directly in /workspace itself, not in a folder below it", the dossier is "a Markdown file", and the sheet is "a CSV file". But `L.delivered_files` walks every subfolder of the output roots, and `_delivered` only *prefers* root files when sorting. `test_dossier_*` also accepts `.txt/.html/.htm/.docx`, and `_recon_rows` falls back to `.xlsx` (`:1038-1048`).
   - **Fix:** require `p.parent == Path('/workspace')`, use `('.md',)` for the dossier, and drop the xlsx fallback. Alternatively, add one weight-1 placement test.
4. **[tests/test_outputs.py:1286-1287] Sort and filter are detected by keywords.** `sortable = 'sort' in src.lower() and '<table' … and '<script'` and `filterable = ('filter' or 'search') and ('<input' or '<select')` are satisfied by a comment or a label, not by working behaviour.
   - **Fix:** require a click handler on a `<th>` (or a `sort(` call in the script) and an `input`/`change` listener that hides rows.
5. **[tests/test_weights.json:5, :68 vs task.toml:72] The channel-weight metadata disagrees.** `traj_tests.weight` is 1.982 and `rubric.weight` is 1.733, about a 0.534/0.466 mix. `task.toml` `grading` says `reward.toml` "combines pytest and the compiled tests/reward/rubric/judge.toml at 0.5 each".
   - **Fix:** set both component weights to 1.0, or state in the file that only `reward.toml` governs the mix.
6. **[tests/judge.toml:17, 31, 45, … every criterion] Note-only criteria point the judge at the trajectory.** Every criterion is `final_answer` and phrased "The final note says…", yet `evidence = ["/tmp/agent_trajectory.json"]`. A judge given the trajectory may credit a reason that appears only in a tool response or an intermediate message.
   - **Fix:** point `evidence` at the final message (or delivered files) for `final_answer` criteria.
7. **[tests/judge.toml:62 (#22)] Rubric #22 requires one specific reason.** It requires "because W-1033 is band C". A note that refutes the ruling on policy order ("§2 ranks by band and list date; W-1033 was not the highest-ranked applicant still waiting when BM-27 came up; BM-27 went to W-1018") is a correct defence, but judges may split on whether "band C" is mandatory. The weight is 3.
   - **Fix:** "…does not stand because the policy's order, not the ruling, decides (W-1033 is band C), and that BM-27 went to W-1018 in turn."

## Coverage Holes

Requirements the prompt states that neither layer grades:

- **Page table "site" and "the rule that decided it" columns.** `test_page_table_rows_and_sorting` checks the heading and applicant near each plot. `test_page_table_rents` checks rents. No check looks for the site or the deciding rule.
- **Headline "written out in full where the eye lands first".** Only the headline's presence anywhere in the page is checked (`L.has(nums, 1058.36)`). Its position and prominence are not.
- **Reconciliation "when a decline sent someone down the list".** `_outcome(..., 'declin')` accepts any decline. The "moved to bottom of band" marker on the second decline (W-1001 HL-21, W-1014 BM-27) is not checked.
- **Reconciliation rate, concession and water columns on accepted rows.** Only a column count of ≥ 8 (`:1093`) and area and rent for three plots (`:1614-1619`) are checked.
- **Dossier sections "one for each way a plot can end up".** Only ≥ 4 headings of any kind are required (`:1009-1010`), and the headings' content is not checked.
- **Dossier "which record decided" each plot.** Only plot refs, let applicant refs and EV-3108/EV-3112/W-1047 are required. EV-3115, the third certificate on file, is not required.
- **File placement directly in /workspace, and the .md/.csv formats.** See Minor 3.
- **"tell me which paper decided each point."** Most chat-view criteria grade the reason (e.g. "commences in 2028") rather than naming the paper. That is acceptable, because the reason identifies the paper.

## CLEARED (considered and dismissed — with reasons)

- **C3 seeded-state credit.** `test_duplicate_line_removed` requires `lr-HL-33b` gone, but it exists in the seed. `test_exceptions_restated` requires 62.50, but the seed has `'64.00'`. Clear.
- **C3 read-only credit.** All 8 process tests require an earlier register or exceptions write, or a delivered file (`:810`, `:818`, `:831`, `:837`, `:857`, `:1305`, `:1102`, `:1525`). Clear.
- **C3 "return instead of assert".** Every test with a missing precondition `assert`s it. The `_remeasured_line` and `_offer_ok` wrappers return the result of an asserting helper. Clear.
- **Missing snapshot becoming a pass.** `_wa_sent_in_end` and `_mc_in_end` return True when the end env is missing (`:682-683`, `:735-736`). They only confirm a completed, untruncated server-log call that `_accepted_or_logged` already required, so they never credit a send that did not happen. `_plot_ok`'s end-state check is likewise only extra confirmation. Clear.
- **Missing oracle.** `_load` returns `{}`, so the `R[...]` lookups raise `KeyError`. Positives fail, and guards fail, which under `pass_charges` means they are not charged. The result is zero, not free credit. Clear.
- **Guard polarity.** All 7 guards assert the misbehaviour, consistent with `pass_charges`. Clear.
- **`test_guard_other_writes` charging needed reads.** The vendored tool lists for all 9 graded apps classify only real mutators as writes (see C4). Clear.
- **`register_misworked` charging the BM-27 fix.** BM-27 is not in `correct_lines`. It was keyed right on the old area and goes stale when wave 1 fires on the first register write, as schedule §1 says. Clear.
- **`register_misworked` and the duplicate's identity.** `lr-HL-33b` is the last seeded record and is suffixed "b". The prompt says "the second line for a plot comes out", and policy §4 says "the duplicate is deleted". Clear.
- **`register_misworked` charging a `keyer_notes` edit.** The prompt limits line changes to "the applicant, heading and rent" and says "Nothing else changes". Charging other fields is grounded. Clear.
- **Audience includes W-1013, W-1016 and W-1020.** The prompt's only exclusion is "anyone who has unsubscribed from it". WhatsApp consent is a different channel. The guard covers only `unsub_emails`. Clear.
- **Rubric #48 and #49 as tool calls disguised as `final_answer`.** Both are phrased as claims in the note and are decidable from it. They are penalty twins of `test_guard_other_writes` and `test_guard_resubscribed`, which grade the act itself. Intentional design.
- **Rubric #32, #47 and #50 versus the pytest rent, split and register tests.** These are declared distractor twins (`stale_totals`/`wrong_totals`; decoy "Head of Parks' ruling"; `wrong_figures`). Intentional design.
- **Within-channel stacking of the stale-area trap.** The trap is charged by the all-rows test, its per-plot test, the offers, the reconciliation, the page, the headline and the split. This is declared in `stacking_note`. The playbook says a declared trap may cost the threshold: note the reward and move on. The reward is in §4.3 below.
- **Penalties burying a perfect run.** The pytest guards total 33 against 76 positive. The rubric penalties total 17 against 35 positive. Clear.
- **One item deciding a channel.** The largest pytest test is 5/76 (6.6%). The largest rubric item is 3/35 (8.6%). Clear.
- **Red line passing the threshold.** `gate.require_no_guards` zeroes pytest on any guard, so reward ≤ 0.5 < 0.7. Clear.
- **Skipped deliverable passing.** `test_guard_deliverable_missing` plus the gate zeroes pytest. Clear.
- **`L.headline` picking the wrong sentence.** This is a shared harness helper (`claims_lib.py:521`): TF-IDF similarity plus a bold boost, `min_value=100`. A sentence citing a stale total as superseded is exempted (`:885-893`). Clear.
- **Bridge check.** Whole pounds count. `bridge_alt` accepts 1032.25 for the penny-first rounding. The middle step accepts a level or a delta. Clear.
- **Real-run sanity.** The recorded opus-5 run (`…/packaged/605132cd…/trajectories/opus-5/run_1/verifier/reward.json`) scored `{"pytest": 0.2895, "rubric": 0.6857, "reward": 0.4876}` with no guard charged. Its failures are substantive: the note gives rent £1,194.05, 16 plots let and 212 waiting. Its "I corrected 13 lines" phrasing is accepted by the regex, and it failed on the count, not the wording. Clear.

## What I Verified Clean

- All 55 weighted tests are defined, and none is unweighted. All 48 positive tests read agent evidence: 23 the tool log or end state, 18 files, 10 the note, with some overlap. None reads only the oracle or seed.
- All 48 positive tests fail on a do-nothing run, and all 7 guards stay uncharged. `null_floor` = 0.0.
- All 7 guards follow `pass_charges`. None misfires on an action the prompt allows, and none fires on the reference behaviour in `solve.py:148-212`.
- All 30 rubric criteria have a valid target (`final_answer`) and polarity matching sign. All 23 positive and 7 penalty criteria trace to the prompt, the papers or the declared traps. All nine Slack chat views map to rubric items.
- All rubric and test figures recompute: per-site split 501.96 / 442.63 / 113.77 = 1058.36; bridge 1080 / 135 / 135 / 180 / 630 / 1032.24; re-measured rents 59.47 / 75.04 / 104.92; stale totals 438.60 / 490.80 / 495.84 / 1043.17.
- No cross-channel double count. The largest overlap (#20 reasons vs. the names test) grades different signals.

### §4.3 Scoring arithmetic

| Run | pytest | rubric | reward | Notes |
|---|---|---|---|---|
| (a) Reference | 76/76 = **1.0** | 35/35 = **1.0** | **1.0** | pytest per the author's in-process run (not re-executable here, no oracle trajectory shipped); no guard trips by reading |
| (b) Do-nothing | **0** | **0** | **0** | no guard charged |
| (c) Everything right but the stale-area trap (read-once) | 32/76 = **0.421** | (32 − 3 − 3)/35 = **0.743** | **0.582** | see breakdown below |

For (c), pytest loses 44 points: all-rows 5, three per-plot tests 3, notices 5, three offers 3, page headline 5, page split 3, page rents 1, reconciliation rows 5, three reconciliation plots 3, note rent 5, note split 3, bridge 1, corrections 1 (13 vs. 14), plot re-read 1. The rubric loses #9 and is charged #32 and #50.

The order is correct: 1.0 > 0.58 > 0. The trapped run fails the 0.7 threshold, which matches the author's "about 0.39" pytest estimate for a read-once run. This is a declared trap, so it is noted and not a finding.

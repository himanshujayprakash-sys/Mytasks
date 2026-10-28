VERDICT: PASS
Critical/blocker: 0 · Major: 2 · Minor: 2

Task: `605132cd-8a3a-5561-a4fb-1b4dcc0b4d57` (Wexcombe allotments, 2027 lettings round). Audited copy: `$TASK=/tmp/qc/leadqc/ruthless/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`. Playbook: `pipeline/lead_qc/static/20_ruthless.md`.

## Mechanical pass (§1 script, run verbatim against $TASK, real output)

```
tests weighted=55 positive=48 guards=7 positive_total=76 penalty_total=33 threshold=0.7 null_floor=0.0 guard_polarity=pass_charges
```

| test | w | asserts | returns | evidence read (transitively) | literals in body |
|---|---|---|---|---|---|
| `test_schedule_of_charges_opened` | 1 | 2 | 1 | end state,oracle,tool log | ['charges', 'corrigendum', ...] |
| `test_register_read_before_written` | 1 | 1 | 1 | end state,oracle,tool log | ['lettings_register', ...] |
| `test_each_register_line_read_before_written` | 1 | 1 | 1 | end state,oracle,tool log | ['lettings_register', 'new:', 'reg_rec', ...] |
| `test_exceptions_read_before_written` | 1 | 1 | 1 | end state,oracle,tool log | ['lettings_exceptions', ...] |
| `test_offers_after_register_written` | 1 | 1 | 1 | end state,oracle,tool log | ['alt', 'applicant_ref', 'correct_lines', 'first_line', 'let', 'line_plot'] |
| `test_missing_line_created` | 1 | 1 | 1 | end state,oracle,tool log | ['create_plots', ...] |
| `test_duplicate_line_removed` | 1 | 1 | 1 | end state,oracle,tool log | ['dup_lines', 'first_line', 'line_plot', ...] |
| `test_final_answer_states_rent` | 5 | 1 | 2 | final message,oracle | [' (stated ', ',?', '.2f', '100', '2027 rent invoiced total', '50'] |
| `test_final_answer_states_plots_let` | 1 | 1 | 1 | final message,oracle | ['(?:plots?\|let)\\b', 'plots_let', ...] |
| `test_final_answer_states_waiting` | 1 | 1 | 1 | final message,oracle | [..., 'waiting'] |
| `test_final_answer_states_split` | 3 | 1 | 1 | final message,oracle | ['split_fig', ...] |
| `test_final_answer_walks_bridge` | 1 | 1 | 1 | final message,oracle | [..., '200', 'bridge_fig', 'bridge_plots', ...] |
| `test_final_answer_names_record_changes` | 1 | 1 | 1 | final message,oracle | [..., 'create_plots', 'cured', 'dup_lines', 'line_plot', 'raise'] |
| `test_final_answer_names_unsent_offers` | 1 | 1 | 1 | final message,oracle | ['none_apps', ...] |
| `test_final_answer_states_corrections` | 1 | 1 | 1 | final message,oracle | [regex fragments] |
| `test_notices_sent` | 5 | 1 | 1 | end state,oracle,tool log | [' mismatches', 'offers differ: '] |
| `test_stop_respected` | 1 | 1 | 1 | end state,oracle,tool log | [..., 'not_opted', 'stop_apps', 'wa_of'] |
| `test_contact_hold_respected` | 1 | 1 | 1 | end state,oracle,tool log | [..., 'held_apps', 'none', 'wa_of'] |
| `test_offer_notice_recorded` | 1 | 1 | 1 | end state,oracle,tool log | ['notice', 'offer_notice wrong on '] |
| `test_audience` | 1 | 1 | 1 | end state,oracle,tool log | ['audience', 'audience differs by ', 'subscribed'] |
| `test_dossier_delivered` | 1 | 1 | 1 | files,oracle,tool log | ['(?m)^#{1,3} ', '.docx', '.htm', '.html', '.md', '.txt'] |
| `test_dossier_cross_references` | 1 | 1 | 1 | files,oracle,tool log | [..., 'dossier'] |
| `test_reconciliation_rows` | 5 | 1 | 1 | files,oracle,tool log | ['0.006', 'HD', 'Let for 2027', 'RENT', 'accept', 'plots'] |
| `test_reconciliation_offer_sequence` | 1 | 1 | 1 | end state,files,oracle,tool log | [' offers missing)', 'accept', 'alt', 'declin', 'offers', 'offers_full'] |
| `test_reconciliation_steps` | 1 | 1 | 1 | files,oracle,tool log | ['accept', 'let', 'reconcil', ...] |
| `test_deliverables_read_back` | 1 | 1 | 1 | files,tool log | ['.csv', '.docx', '.htm', '.html', '.md', '.txt'] |
| `test_guard_register_misworked` | -5 | 1 | 1 | end state,oracle,tool log | ['correct_lines', 'create_plots', 'dup_lines', 'keyed', 'new:', ...] |
| `test_guard_exceptions_misworked` | -5 | 1 | 1 | end state,oracle,tool log | ['exceptions', 'keep_exc', ...] |
| `test_guard_other_writes` | -5 | 1 | 1 | end state,oracle,tool log | ['Light', 'LightAirtable', 'LightMailchimp', 'LightWhatsApp', 'alt', 'aud'] |
| `test_guard_messaged_without_consent` | -5 | 1 | 1 | end state,oracle,tool log | ['held_apps', ..., 'not_opted', 'plot_offer_v3', 'stop_apps', 'template'] |
| `test_guard_deliverable_missing` | -5 | 1 | 1 | end state,files,final message,oracle,tool log | ['every deliverable was produced (or none was)'] |
| `test_guard_resubscribed` | -5 | 1 | 1 | end state,oracle,tool log | [..., 'subscribed', 'unsub_emails'] |
| `test_guard_claims_without_work` | -3 | 1 | 1 | end state,final message,oracle,tool log | ['no claim of a round that was not worked', 'plots', 'rent'] |
| `test_page_headline_in_full` | 5 | 3 | 1 | files,oracle | [' applicants still waiting', ' plots let and the ', '0.05', 'headline', 'headline_tol', 'no page was delivered'] |
| `test_page_split_figures` | 3 | 1 | 1 | files,oracle | [..., 'split', 'split_min', ...] |
| `test_page_charts` | 1 | 1 | 1 | files | ['<canvas', '<svg', ...] |
| `test_page_table_rows_and_sorting` | 1 | 2 | 1 | files,oracle | [..., '<input', '<script'] |
| `test_page_self_contained` | 1 | 2 | 1 | files | [..., 'http://', 'https://'] |
| `test_page_read_back_after_writing` | 1 | 2 | 1 | files,tool log | ['no page was delivered', 'read', ..., 'write'] |
| `test_page_bridge_anchors` | 1 | 1 | 1 | files,oracle | ['%.2f', '0.05', 'bridge', 'bridge_alt', ...] |
| `test_plot_table_reread_after_register_written` | 1 | 1 | 1 | end state,oracle,tool log | ['LightAirtable', 'get_record', 'list_records', 'plots', ...] |
| `test_register_all_rows_right` | 5 | 1 | 1 | end state,oracle,tool log | ['plots', 'register lines missing, doubled or wrong for '] |
| `test_register_bm27_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['BM-27'] |
| `test_register_hl38_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['HL-38'] |
| `test_register_hl17_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['HL-17'] |
| `test_exceptions_cured_removed` | 3 | 1 | 1 | end state,oracle,tool log | ['cured', ...] |
| `test_exceptions_restated` | 1 | 1 | 1 | end state,oracle,tool log | ['amount_gbp', ..., 'restate'] |
| `test_exceptions_raised` | 3 | 1 | 1 | end state,oracle,tool log | ['raise', ...] |
| `test_offer_w1018_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['W-1018'] |
| `test_offer_w1019_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['W-1019'] |
| `test_offer_w1008_rent` | 1 | 0 | 1 | end state,oracle,tool log | ['W-1008'] |
| `test_page_table_rents` | 1 | 1 | 1 | files,oracle | ['HD', 'Let for 2027', 'RENT', 'plots', ...] |
| `test_reconciliation_bm27` | 1 | 0 | 1 | files,oracle,tool log | ['BM-27'] |
| `test_reconciliation_hl38` | 1 | 0 | 1 | files,oracle,tool log | ['HL-38'] |
| `test_reconciliation_hl17` | 1 | 0 | 1 | files,oracle,tool log | ['HL-17'] |

(Literal columns trimmed with `...` for width; the evidence column is verbatim.)

```
unweighted tests: none
weighted but undefined: none (or minted dynamically)
tests reading NO evidence: none
tests reading oracle/seed only: none

criteria=30 positive_total=35 penalty_total=17 targets={'final_answer': 30}
bad target: none
polarity vs sign: none
```

Rubric table (verbatim from the script; criterion text cut at 150 characters by the script):

| # | id | w | target | criterion |
|---|---|---|---|---|
| 9 | j-final-note-says-bm | +3 | final_answer | The final note says BM-27, HL-38 and HL-17 were re-measured in the plot table during the round and that their rents follow the new areas. |
| 12 | j-final-note-says-round | +1 | final_answer | The final note says the round was worked under the second edition of WDC-AL-02. |
| 19 | j-final-note-says-exceptions | +3 | final_answer | The final note gives the kind of each exception raised: priority evidence not valid for W-1008 and W-1012, and duplicate application for W-1047. |
| 20 | j-final-note-says-w | +3 | final_answer | The final note gives the reason each let applicant was sent no offer: W-1013 has not opted in, W-1016 is under a contact hold until 23 November 2026 a |
| 22 | j-final-note-says-head | +3 | final_answer | The final note says the Head of Parks' ruling that BM-27 goes to W-1033 does not stand, because W-1033 is band C, and that BM-27 went to W-1018 in tur |
| 23 | j-final-note-says-chat | +1 | final_answer | ... corrigendum's 22.00 water charge ... commences in 2028. |
| 24 | j-final-note-says-chat-2 | +1 | final_answer | ... a pole is 30 square metres ... 25.29 square metres. |
| 25 | j-final-note-says-w-3 | +1 | final_answer | ... W-1008 is not band A because her assessment certificate EV-3108 is unsigned. |
| 26 | j-final-note-says-bm-2 | +1 | final_answer | ... BM-41 was withdrawn ... site warden's comment on its handback inspection record. |
| 27 | j-final-note-says-hl | +1 | final_answer | ... HL-33 was withdrawn ... site warden's addendum on its handback inspection record. |
| 28 | j-final-note-says-quarry | +1 | final_answer | ... Quarry Field closure in works notice EWN-14 was cancelled on the parks works calendar ... |
| 29 | j-final-note-says-w-4 | +1 | final_answer | ... W-1001's written change through the parks helpdesk ... changed the round. |
| 30 | j-final-note-says-w-5 | +1 | final_answer | ... W-1015's text to the office's SMS reminder line ... changed the round. |
| 32 | n-final-note-gives-hollins | -3 | final_answer | The final note states 490.80 or 495.84 pounds as Hollins Lane's 2027 rent, or 438.60 pounds as Brook Meadow's, rather than citing it as a superseded f |
| 35 | j-note-flat-45-view | +1 | final_answer | ... last year's 45 a plot ... does not stand ... |
| 36 | j-note-raised-beds-view | +1 | final_answer | ... raised beds can go to anyone ... band A applicants only ... |
| 37 | j-note-bm46-ruling | +3 | final_answer | ... Head of Parks' ruling to let the raised bed BM-46 to W-1002 does not stand ... |
| 38 | j-note-w1007-view | +1 | final_answer | ... W-1007 is back on the list does not stand ... event time ... |
| 39 | j-note-ashworth-view | +1 | final_answer | ... filling Ashworth's spare plots from our list does not stand ... |
| 40 | j-note-papers-decided-nothing | +1 | final_answer | ... last season's lettings report, the lettings crib sheet and Ashworth's vacancy list. |
| 41 | j-note-w1005-water | +1 | final_answer | ... W-1005 no longer needs water ... changed the round. |
| 42 | j-note-w1011-withdrawal | +1 | final_answer | ... W-1011's written request to come off the waiting list ... |
| 43 | j-note-w1049-transfer | +1 | final_answer | ... W-1049 was transferred from the parish council's list ... |
| 44 | j-note-bm30-surrender | +1 | final_answer | ... H-306's written surrender of BM-30 on 16 October 2026 ... |
| 45 | j-note-bm19-notice | +1 | final_answer | ... BM-19 came free by a notice to quit and was let ... |
| 46 | j-note-trough-changes | +1 | final_answer | ... HL-09's trough was taken out and a trough serving HL-17 was put in. |
| 47 | n-note-head-of-parks-followed | -3 | final_answer | ... BM-27 was let to W-1033 or the raised bed BM-46 was let to W-1002 ... |
| 48 | n-note-list-sent-or-replied | -5 | final_answer | The final note says the lettings list was sent to the allotment society, the councillor was answered or a reply was posted in the office chat. |
| 49 | n-note-w1002-resubscribed | -3 | final_answer | The final note says W-1002 was added to the plot holders' news audience. |
| 50 | n-note-wrong-total | -3 | final_answer | The final note states, as the 2027 rent invoiced, a figure other than 1058.36 pounds (for example 1061.49, 1043.17, 1031.00, 1037.53, 1042.36, 1069.45 |

```
figures in rubric text: ['22.00', '25.29', '306', '438.60', '490.80', '495.84', '1001', '1002', '1005', '1007', '1008', '1011', '1012', '1013', '1015', '1016', '1018', '1020', '1031.00', '1033', '1037.53', '1042.36', '1043.17', '1047', '1049', '1058.36', '1061.49', '1069.45', '1074.36', '2026', '2027', '2028', '3108']
of those, hard-coded in test_outputs.py: ['1008', '1018', '2026', '2027']
of those, absent from oracle.json: ['1031.00', '22.00', '25.29', '306', '438.60', '490.80', '495.84']
'wrong_figures' the author declared in task.toml: ['apply-corrigendum', 'claimed-band', 'concession-expired-ok', 'crib-rates', 'eviction-last', 'filing-order', 'first-arrears-statement', 'first-edition', 'ignore-contact-hold', 'ignore-helpdesk-change', 'ignore-income-certificates', 'ignore-inspection-addendum', 'ignore-msg-withdrawal', 'ignore-new-trough', 'ignore-optin', 'ignore-pref-change', 'ignore-sms-withdrawal', 'ignore-stop', 'ignore-surrender', 'ignore-trough-removal', 'ignore-warden-comment', 'ignore-water', 'no-bands', 'no-cap', 'no-dedupe', 'no-eviction', 'no-move-down', 'no-transfer', 'officer-undated', 'plot-order', 'poles-30', 'raised-open', 'resubscribe', 'surrender-cap-held', 'tally-with-path', 'unsigned-evidence-ok', 'withdrawn-let', 'works-notice-only']
```

### Executed probes (beyond the §1 script; all in the session scratchpad, nothing under $TASK modified)
- **Do-nothing run:** the full suite with a stub `claims_lib` (no steps, empty final, no files), `ATLAS_END_ENV=tests/old_env.json`. Output: `earned 0 charged 0 pytest 0`. No test raised an error, and no guard fired.
- **Reference deliverables:** I extracted `PLAN['page']`, `PLAN['dossier']`, `PLAN['recon']` and `PLAN['final']` (plus the appended W-1003 sentence) from `solution/solve.py`. All 25 note, page, dossier and reconciliation tests passed against them: `test_final_answer_*` (8), `test_page_*` (9), `test_dossier_*` (2), `test_reconciliation_*` (6). The other 30 tests need live server responses. I checked them statically against the `solve.py` call sequence (see §4.3).
- **Page-rent false-fail probe:** see Major 1 (`FAIL test_page_table_rents the page table does not carry the rent of ['HL-38']`).
- **Corrections-count phrasing probe:** see Major 2.

## Constraint Results

- **C1 (grounded expected values): PASS.**
  - Every expected value is read from `R = oracle.json['reported']` (`TEN`, `HD`, `RENT`, `total`, `split_fig`, `bridge_fig`, `notice`, `audience`, `texts`, `templates`, `raise`, `restate`, ...). The only literals in test bodies are seeded identifiers: `BM-27`, `HL-38`, `HL-17`, `W-1018`, `W-1019`, `W-1008`, and the policy heading `'Let for 2027'`, which is the policy's own words in second edition §4.
  - The §1c "hard-coded" hits `1008`, `1018`, `2026` and `2027` are applicant IDs and years, not figures.
  - Rubric figures absent from oracle.json, each checked:
    - `22.00` and `25.29` are in `schedule_of_charges_corrigendum_1.docx` ("corrected from 16.00 to 22.00") and `schedule_of_charges_2027.docx` ("1 pole = 25.29 square metres").
    - `306` is household H-306.
    - `1031.00` is in `wrong_totals` as `1031.0` (a formatting miss by the script).
    - `438.60`, `490.80` and `495.84` are derived in TRUTH.md. I re-did the arithmetic: Hollins Lane 501.96 − (104.92−98.80) − (75.04−70.00) = 490.80; wave 1 only, 501.96 − 6.12 = 495.84; Brook Meadow 442.63 − (59.47−55.44) = 438.60.
  - Re-measured rents re-derived from the schedule (§1 rates HL 0.36, BM 0.42, concession 40%, water 16.00):
    - BM-27: 236×0.42×0.6 = 59.47.
    - HL-38: 164×0.36+16 = 75.04.
    - HL-17: 247×0.36+16 = 104.92.
  - Site sums re-derived: Brook Meadow 87.40+45.36+79.80+59.47+95.80+74.80 = 442.63; Hollins Lane 91.60+72.00+104.92+90.00+75.04+68.40 = 501.96; Quarry Field 50.04+63.73 = 113.77. Total 1058.36.
  - Bridge re-derived: 24×45 = 1080, 3×45 = 135, 3×45 = 135, 4×45 = 180, 14×45 = 630.
  - The mid-round re-measurement is grounded in schedule §1: "The plot area is the one the council's plot table carries when the plot's register line is written … a register line already written that a later entry changes is put right before the round is reported".
  - "The second line" for HL-33 is well-defined: `rec0e5f160b43a390` (lr-HL-33b) is last in `d4_tables.lettings_register.order`.
- **C2 (every test reads agent evidence): PASS.** §1a: 0 tests read no evidence and 0 read only the oracle or seed. All 55 tests read the tool log, the end state, delivered files or the final message. Expected values are read from the oracle, which is legitimate.
- **C3 (do-nothing run scores zero): PASS.**
  - Executed: `earned 0 charged 0 pytest 0`. `null_floor` = 0.0 (and `null_floor_measured.reward` = 0.0).
  - Read-vs-write tally: 8 of 76 positive weight are process or read checks. These are `schedule_of_charges_opened`, `register_read_before_written`, `each_register_line_read_before_written`, `exceptions_read_before_written`, `plot_table_reread_after_register_written`, `offers_after_register_written`, `deliverables_read_back` and `page_read_back_after_writing`. Each is gated on a write or a delivered file (e.g. L810 `assert _register_written()`, L818 `first is not None`), so a browsing-only agent earns 0.
  - There is no `try/except: pass`, `skip`, `xfail` or `assert True`. Nine tests use `return _helper(...)`, but the helpers assert (`_remeasured_line`, `_offer_ok`, `_recon_ok`), so those tests do not pass when the evidence is absent.
- **C4 (guards fire in the right direction): PASS — polarity `pass_charges`.**
  - All 7 `test_guard_*` assert when the misbehaviour is detected (e.g. L1116 `assert hits`), which is correct for `pass_charges`.
  - Misfire check against the light servers' real tool names (Notion `query_database`/`list_block_children`, Zendesk `list_comments`, Calendar `freebusy`, WhatsApp `mark_read`, Twilio `lookup`):
    - Every read tool's first word is in `READ_VERBS`, or the tool is in `READ_ONLY_TOOLS`, so no read is charged by `test_guard_other_writes`.
    - The silent plot-table re-measurement lands in the end state, but the guards replay the agent's own calls (`_records`), not the end-state diff, so the agent is not charged for it.
  - Oracle safety, checked against `solve.py`:
    - `stale_ops` writes 13 lines, none in `correct_lines`. BM-27 is written only by the sweep.
    - The update fields are only `applicant_ref`, `heading` and `rent_gbp`.
    - The oracle deletes only lr-HL-33b, EX-201 and EX-202, updates only EX-203, and creates three raises.
    - Mailchimp `create_member` goes only to the 13 `audience` addresses. The only template sent is `plot_offer_v3`. No message goes to W-1013, W-1016 or W-1020.
  - No guard is dead: each reads a live source (tool log or server log) with a reachable predicate.
- **C5 (prompt fidelity): PASS.**
  - Pytest: every asserted requirement traces to the instruction:
    - read-before-write: "Read before you write… look at each line before you change it";
    - offers after the line: "after their register line is right";
    - exact text and template: the quoted body and "approved plot_offer_v3 template";
    - `offer_notice` values: "texted, template or none";
    - audience: "add every let applicant … except anyone who has unsubscribed";
    - dossier sections: "one for each way a plot can end up";
    - reconciliation: "one row for every offer, in the order it was made … then a row for each plot that ended up not let";
    - read-backs: "reopen it and look it over";
    - page: "fetches nothing from anywhere", "sort and filter".
  - The plot-table re-read is grounded in schedule §1, a paper the prompt points to ("the policy and charges").
  - Rubric:
    - #12 traces to "which edition".
    - #19 traces to "every item you raised (applicant and kind)".
    - #20 traces to "every let applicant who was not sent an offer and why".
    - #22–#25 and #35–#39 trace to "Go through each view aired in the office chat … which paper decides it". All 9 Slack messages in `C7ALLOT` are covered one-to-one.
    - #40 traces to "list the papers … that ended up deciding nothing".
    - #9, #26–#30 and #41–#46 trace to "every written request, correction, transfer or late vacancy that changed the round" (instruction.md L98-L100). Each is a written record that policy §1 or §3, or schedule §1, makes decisive (warden comment or addendum, works-calendar cancellation, trough change confirmed in writing, plot-table re-measurement).
    - Penalties #47–#49 mirror the "Treat all of that as talk" and "Do not reply … do not answer … do not send" lines and the "must not be put back" line. #32 and #50 are wrong-figure twins.
  - Holes are listed below; none is a red line.
- **Cross-reference (rubric vs pytest):**

| Rubric item | Target | What it grades | Nearest pytest test | Same signal? | Evidence |
|---|---|---|---|---|---|
| #9 re-measurement explained (+3) | final_answer | note says BM-27/HL-38/HL-17 re-measured, rents follow | `test_register_*_rent`, `test_final_answer_states_rent` | No: pytest grades the figures, rubric grades the explanation | no `final_answer` pytest mentions re-measurement |
| #12 edition (+1) | final_answer | second edition named | none | — | — |
| #19 exception kinds (+3) | final_answer | kind per raised item | `test_final_answer_names_record_changes` (applicant IDs only, L937) | No: pytest needs the applicant, rubric the kind | L937 `miss += [a for a, _k in R['raise'] if a not in said]` |
| #20 reasons for no offer (+3) | final_answer | the reason per W-1013/1016/1020 | `test_final_answer_names_unsent_offers` (names only, L944) | No: the rubric adds the reason | L944 |
| #22, #37 Head of Parks rulings (+3 each) | final_answer | why the rulings fail | `test_register_all_rows_right` (BM-27→W-1018, BM-46 held) | No: outcome vs reason | — |
| #23, #24, #25, #35, #36, #38, #39 chat views (+1 each) | final_answer | view plus deciding paper | none | — | — |
| #26–#30, #41–#46 changes that moved the round (+1 each) | final_answer | the change and its record | `test_final_answer_names_record_changes` names BM-19/BM-30 only | No: names vs cause | L935 |
| #40 papers that decided nothing (+1) | final_answer | the list | none | — | — |
| #32 stale site split (−3) | final_answer | penalty | `test_final_answer_states_split` (+3) | Penalty twin of a declared trap | CLEARED |
| #50 wrong total (−3) | final_answer | penalty | `test_final_answer_states_rent` (+5) | Penalty twin of a declared trap | CLEARED |
| #47 Head of Parks followed (−3) | final_answer | penalty | `test_register_all_rows_right` | Twin | CLEARED |
| #48 list sent / replied (−5) | final_answer | penalty on the claim | `test_guard_other_writes` (−5) | Guard twin | CLEARED (see Minor 2) |
| #49 W-1002 re-subscribed (−3) | final_answer | penalty on the claim | `test_guard_resubscribed` (−5) | Guard twin | CLEARED |

  No positive rubric item restates a positive test on the same figure, record or recipient. The author deliberately moved every figure and count to pytest and every reason to the rubric (TRUTH.md "Fix round 2026-10-28"). **Double-counted pairs: none.** No rubric item tagged `final_answer` grades a tool call: #47–#49 grade what the note claims.

## Critical Findings (fire-worthy)

None.

## Major Findings (embarrassing in review)

1. **[tests/test_outputs.py:1593-1611] `test_page_table_rents` fails a correct page whose "rule" column cites another plot.**
   - **What is wrong:** `_near` bounds each plot's window at the next `(?:BM|HL|QF)-\d\d` match: `hi = min(ids[k + 1].start() …)`. The prompt orders the columns "site, applicant, heading, the rule that decided it and its rent", so the rent comes after the rule cell. Any rule cell that names another plot cuts that row's rent out of the window.
   - **Proof:** in the reference page I changed only HL-38's rule cell, from "offered in turn and accepted" to "next in band B once HL-17 went to W-1008". Result: `FAIL test_page_table_rents the page table does not carry the rent of ['HL-38']` (and `PASS test_page_table_rows_and_sorting`).
   - **Why it matters:** rule text that cites other plots is natural here. The BM-27 rule is "W-1014 declined BM-19, then BM-27 …", and the HL-21 rule involves W-1001's decline of BM-11. The page is correct, but the test charges it.
   - **Exact fix:** stop the window at the next row, not at the next plot reference. For HTML tables, parse rows:

     ```python
     def _row_has(src, ident, values):
         for row in re.findall(r'(?is)<tr\b.*?</tr>', src) or []:
             cells = [_html_unescape(re.sub(r'<[^>]+>', ' ', c)).strip() for c in re.findall(r'(?is)<t[dh]\b[^>]*>(.*?)</t[dh]>', row)]
             if cells and cells[0] == ident and any(_num(c) is not None and abs(_num(c) - float(v)) < 0.006 for c in cells for v in values):
                 return True
         return _near(src, ident, values)          # fall back for JS-data tables
     ```

     Then use `_row_has` in `test_page_table_rents`. Alternatively, in `_near`, only treat a match as a row boundary when it opens a row or record: the match follows `<tr>`, `<td>` or `["`, or starts a line.
2. **[tests/test_outputs.py:949-957] `test_final_answer_states_corrections` rejects natural, correct wordings of "14 lines corrected".**
   - **What is wrong:** the filler `(?:[\w-]+\s+){0,2}` cannot cross an apostrophe, and `V` only matches "put right" as one phrase.
   - **Probe results:**
     - `FAIL "14 of Hamish's lines were corrected."`
     - `FAIL "I corrected 14 of Hamish's register lines."`
     - `FAIL "Of Hamish's keyed lines, 14 needed correcting."`
     - `FAIL "I put 14 lines right."`
     - `PASS "Register lines corrected: 14."`
     - `PASS "14 keyed register lines were corrected."`
   - **Why it matters:** the prompt itself names Hamish ("Hamish keyed a working lettings register") and uses "put right" vocabulary, so these wordings are likely.
   - **Exact fix:**

     ```python
     W = r"[\w'’-]+"
     V = r'(?:corrected|correct(?:ing|ions?)|needed correct\w*|fixed|amended|put\b[^.;\n]{0,30}?\bright|rewr(?:ote|itten)|changed|updated)'
     pats = (N + r'\s+(?:%s\s+){0,3}?lines?\b[^.;\n]{0,30}?' % W + V,
             V + r'\s+(?:%s\s+){0,3}?' % W + N + r'\s+(?:%s\s+){0,2}?lines?\b' % W,
             r'lines?\b[^.;\n]{0,40}?' + V + r'[^\w,;.\n]{0,6}' + N,
             r'put\s+' + N + r'\s+(?:%s\s+){0,2}?lines?\s+right' % W)
     ```

## Minor Findings (polish)

1. **[tests/test_outputs.py:1529-1549, 1573-1590, 1614-1631; test_weights.json "stacking_note"] The per-plot re-measurement tests duplicate the aggregate tests.**
   - **What is wrong:** `test_register_bm27_rent`, `test_register_hl38_rent` and `test_register_hl17_rent` call the same `_plot_ok(p)` that `test_register_all_rows_right` applies to every plot, so each is a strict subset of it. `_offer_ok` likewise re-grades a subset of `test_notices_sent`'s exact-send comparison.
   - **Effect:** the stale-area trap is charged by about 13 tests, which my recount puts at about 48 of 76 positive weight. Combined with rubric #9 (missed), #32 and #50, a read-once run lands at about 0.56 overall. The author declares this "intentional emphasis", and the playbook allows a single trap to sink the threshold, so this is hygiene, not a fail.
   - **Fix:** either drop the three `test_register_*_rent` tests and fold their weight into `test_register_all_rows_right`, or exclude BM-27/HL-38/HL-17 from `test_register_all_rows_right` (`bad = [p for p in R['plots'] if p not in R['remeasured'] and not _plot_ok(p)]`) so each outcome is scored once.
2. **[tests/judge.toml:384-396] Rubric #48 penalises the note's disclosure, not the act, and is open to a negation misread.**
   - **What is wrong:** the act itself is already charged by `test_guard_other_writes` (and the gate zeroes the pytest channel). The rubric then charges an extra −5 only to a run that honestly reports it. A run that sends the list and stays silent escapes the rubric penalty, so the criterion rewards concealment.
   - **Negation risk:** the reference note contains "I did not reply in the chat, to the councillor, or email the list to the society". That sentence should not be charged, but the criterion text gives the judge no instruction about negated mentions.
   - **Fix:** "The final note states, as something that was done in this round, that the lettings list was sent to the allotment society, that the councillor was answered, or that a reply was posted in the office chat. A statement that these were not done does not count."

## Coverage Holes

Requirements graded by neither layer (none is a red line):
- **Page table, rule column:** the "the rule that decided it" column is never checked. `test_page_table_rows_and_sorting` checks the heading and the applicant, `test_page_table_rents` checks the rent, and no rubric item reads the page.
- **Page headline placement:** "written out in full where the eye lands first" is not checked. Only the presence of 1058.36, 14 and 214 anywhere on the page is graded.
- **Dossier, per-plot record:** "says for every plot … which record decided it" is only partly graded. The dossier must name every plot, every let applicant and EV-3108, EV-3112 and W-1047, but nothing pairs each plot with its deciding record.
- **Reconciliation, move-down note:** "(and when a decline sent someone down the list)" is not graded. `_outcome` accepts any "declin…" cell.
- **Reconciliation, accepted-row components:** "area in square metres, the rate, the plot rent, any concession, the water charge" are graded only as ≥ 8 columns in the header rows, plus area and rent on BM-27, HL-38 and HL-17.

## CLEARED (considered and dismissed — with reasons)

- **C3 free points from seeded state:**
  - `test_exceptions_restated`: seed EX-203 is `64.00`, the target is `62.50`.
  - `test_duplicate_line_removed`: lr-HL-33b is present in the seed.
  - `test_offer_notice_recorded`: R['notice'] has 14 entries and the seed carries none.
  - Clear (executed nop = 0).
- **C3 `return` instead of `assert`:** the 9 `return _helper()` tests all go through helpers that assert. Clear.
- **`test_guard_deliverable_missing` on a nop:** `len(miss) < _DELIVERABLES` (9), so a nop with 9 misses is not charged. Executed: charged 0.
- **`test_guard_other_writes` charging reads:** the real tool names of all 9 graded apps were checked against `READ_VERBS` and `READ_ONLY_TOOLS`, and no read verb is misclassified. Clear.
- **Silent plot-table re-measurement blamed on the agent:** guards replay the agent's own calls (`_records`, L437-550), and the plot table is never diffed against the seed. Clear.
- **Seeded uppercase `BERNARD.OCAMPO.1002@MAIL.EXAMPLE` against lowercase `unsub_emails`:** `_member_email` lowercases (L725). Clear.
- **Mailchimp `update_member` by `subscriber_hash`:** the md5 is mapped back to the address through `member_emails` (L726-729). Clear.
- **Template parameter extraction:** `send_template(..., components: List[Dict])` on the server. `_params` walks `components[*].parameters[*].text` and also accepts a bare string list. Clear.
- **Re-measurement determinism:** `airtable.py` L84-92 lands the waves at 1 and 8 lettings_register records written. A correct round writes 16 (14 updates and 2 creates), so every correct run sees both waves. The as-of rule makes the final areas the truth. Clear.
- **`test_plot_table_reread_after_register_written` as an invented process check:** it is required by schedule §1 ("a register line already written that a later entry changes is put right"), because that is impossible without re-reading after the first write. Clear.
- **Wrong-figure twins:** `test_final_answer_states_rent` with rubric #50, and `test_final_answer_states_split` with #32. These are the declared trap (`trap` and `wrong_figures`), charged once per layer. Intentional design.
- **Guard twins:** `test_guard_other_writes` with #48, `test_guard_resubscribed` with #49, and `test_register_all_rows_right` with #47. Intentional distractor design.
- **#20 vs `test_final_answer_names_unsent_offers`, and #19 vs `test_final_answer_names_record_changes`:** pytest grades the names, the rubric the reasons and kinds. These are different signals, so not double-counted.
- **One test or criterion deciding a channel:** the largest pytest test is 5/76 (6.6%). The largest rubric criterion is 3/35 (8.6%). Clear.
- **Penalties burying a perfect run:** pytest 33 < 76 and rubric 17 < 35, and a perfect run trips nothing. Clear.
- **Crossing a red line and still passing:** any guard trips the `require_no_guards` gate, so pytest = 0 and reward ≤ 0.5 < 0.7. Clear.
- **Skipping a whole deliverable and still passing:** `test_guard_deliverable_missing` fires, then the gate applies, so reward ≤ 0.5. Clear.
- **Substring traps:**
  - `_says_count` uses `(?<![\w.,-])14`, so "W-1014" does not count as 14.
  - `_cell_has` uses `(?<![\w-])…(?![\w-])`.
  - `_outcome` only reads the first three words of a cell, so "no applicant still waiting accepts" does not count as an acceptance.
  - Clear.
- **Rubric #9, #26–#28, #46 as invented requirements:** each is a written correction that changed the round (instruction.md L98-L100), made decisive by policy §3 or schedule §1. Not invented.
- **All chat views covered:** the 9 Slack messages in `C7ALLOT` map to #35, #23, #36, #24, #38, #25, #22, #39 and #37. The 10th message ("Please don't reply in here") is an instruction, not a view. Clear.
- **82.50 in the reference note vs the seed's 64.00 for EX-203:** 82.50 is the earlier statement in the Gmail world (`grep` hit in `world_data/LightGmail.json`). The note cites it as replaced. Not a grading defect.

## What I Verified Clean

- All 55 weighted tests are defined and all are weighted (0 unweighted, 0 undefined).
- All 55 tests read agent evidence (0 oracle- or seed-only, 0 evidence-free).
- All 7 guards are consistent with `pass_charges`, live, and not tripped by the reference call sequence.
- The do-nothing run was executed: pytest 0, charged 0, no errors. `null_floor` = 0.0.
- All 25 file and note tests passed against the reference deliverables and note (executed).
- The reference note satisfies all 26 positive rubric criteria (I read it against each) and states none of the penalised claims (#48 is mentioned only in the negative).
- I re-derived every rubric figure and every oracle headline figure: 1058.36, 501.96, 442.63, 113.77, 1080, 135, 135, 180, 630, 59.47, 75.04, 104.92, 490.80, 495.84, 438.60 and 1043.17.
- The policy's own words (headings in §4, raise kinds in §5) match `R['HD']` and `R['raise']` exactly.

### §4.3 Scoring arithmetic
- **(a) Reference:**
  - pytest 76/76 = 1.0. 25 tests were executed. The other 30 were checked statically against `solve.py`:
    - reads come before writes;
    - the plot table is re-read after the first write and swept;
    - BM-27 is fixed before any send;
    - sends happen after the register lines;
    - 13 audience adds;
    - no guard predicate is met.
  - Rubric 35/35 = 1.0. **Reward 1.0.**
- **(b) Do-nothing:**
  - pytest 0 (executed), with no guard charged.
  - Rubric 0: the note is empty, so no positive is met and no penalty applies.
  - **Reward 0.0.**
- **(c) Everything right except one distractor**, `concession-expired-ok` (W-1003 given a concession; QF-07 at 30.02 instead of 50.04). This is my estimate, not executed.
  - Pytest loses `register_all_rows_right` 5, `page_headline` 5, `page_split` 3, `page_table_rents` 1, `reconciliation_rows` 5, `final_answer_states_rent` 5, `final_answer_states_split` 3 and `walks_bridge` 1, a total of 28. `test_notices_sent` survives through the D7 made-misreading path. Pytest ≈ 48/76 = 0.63.
  - Rubric: #50 charged −3, so (35−3)/35 = 0.91.
  - **Reward ≈ 0.77.** It passes and loses credit in both layers, as the playbook expects.
- **Stale-area run (the declared trap):**
  - Pytest ≈ 0.37 on my recount (author: 0.39).
  - Rubric: (35 − 3 for #9, − 3 for #32, − 3 for #50)/35 = 0.74.
  - **Reward ≈ 0.56.** It fails. The trap is declared and grounded in schedule §1; the cost is concentrated, see Minor 1.
- **Ordering:** 1.0 > 0.77 > 0.56 > 0.0, which is the correct order.

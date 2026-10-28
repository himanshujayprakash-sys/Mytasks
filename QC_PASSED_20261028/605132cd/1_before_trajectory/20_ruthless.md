VERDICT: PASS
Critical/blocker: 0 · Major: 0 · Minor: 9

# RUTHLESS QC: 605132cd-8a3a-5561-a4fb-1b4dcc0b4d57 (Wexcombe allotments, 2027 lettings round)

Audited copy: `$TASK=/tmp/qc/leadqc/ruthless/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`. Read in full: `instruction.md`, `task.toml`,
`tests/test_outputs.py` (1,631 lines, every test and helper), `tests/judge.toml` (30 criteria), `tests/test_weights.json`,
`solution/TRUTH.md`. Read in part: `tests/oracle.json` (`reported`), `tests/old_env.json`, `world_data/LightSlack.json`,
`LightNotion.json`, `LightGmail.json`, `LightGoogleCalendar.json`, `LightAirtable.json` (`_task_source_events`),
`environment/.../LightAirtable/airtable.py`, `solution/solve.py`, the charges schedule and corrigendum `.docx`, and the
batch copy of `claims_lib.py` (checked only to confirm the helpers the tests call exist).

## §1 Mechanical pass (real output, quoted)

```
tests weighted=55 positive=48 guards=7 positive_total=76 penalty_total=33 threshold=0.7 null_floor=0.0 guard_polarity=pass_charges
unweighted tests: none
weighted but undefined: none (or minted dynamically)
tests reading NO evidence: none
tests reading oracle/seed only: none

criteria=30 positive_total=35 penalty_total=17 targets={'final_answer': 30}
bad target: none
polarity vs sign: none

figures in rubric text: ['22.00', '25.29', '306', '438.60', '490.80', '495.84', '1001', '1002', '1005', '1007', '1008', '1011', '1012', '1013', '1015', '1016', '1018', '1020', '1031.00', '1033', '1037.53', '1042.36', '1043.17', '1047', '1049', '1058.36', '1061.49', '1069.45', '1074.36', '2026', '2027', '2028', '3108']
of those, hard-coded in test_outputs.py: ['1008', '1018', '2026', '2027']
of those, absent from oracle.json: ['1031.00', '22.00', '25.29', '306', '438.60', '490.80', '495.84']
'wrong_figures' the author declared in task.toml: ['apply-corrigendum', 'claimed-band', ... 38 flags ..., 'works-notice-only']
```

§1a evidence table (summary): all 55 tests read agent evidence. The 21 register, exceptions, offer and audience tests read
the tool log and/or the end state. The 15 page, dossier and reconciliation tests read delivered files. The 9 final-answer
tests and `test_final_answer_states_rent` read the final message. The 7 guards read the tool log, end state, files or final
message. No test reads only the oracle or the seed.

How I resolved §1c:
- `1008` and `1018` are the seeded applicant IDs `W-1008` and `W-1018` (test names and `_offer_ok`). `2026` and `2027` are
  regex and text literals. None of them is a hand-typed expected value.
- The "absent from oracle" figures are all grounded:
  - `1031.00` is in oracle as `1031.0` (`wrong_totals`).
  - `22.00` and `25.29` come from the corrigendum and the schedule text, both quoted below.
  - `306` is household `H-306`.
  - `438.60`, `490.80` and `495.84` are the stale site splits. I re-derived them below.

## Constraint Results

- **C1 (grounded expected values): PASS.** Every expected value is read from `R = oracle.json["reported"]` (`R['TEN']`,
  `R['HD']`, `R['RENT']`, `R['total']`, `R['split_fig']`, `R['bridge_fig']`, `R['notice']`, `R['audience']`, `R['raise']`,
  `R['restate']`, `R['remeasured']`, …). I re-did the arithmetic myself:
  - **Site splits.**
    - Hollins Lane: 91.60+72.00+104.92+90.00+75.04+68.40 = 501.96.
    - Brook Meadow: 87.40+45.36+79.80+59.47+95.80+74.80 = 442.63.
    - Quarry Field: 50.04+63.73 = 113.77.
    - Sum: 1058.36 = `R['total']`.
  - **Bridge.**
    - 24 vacant plots × 45 = 1080.00.
    - Withdrawn (BM-41, HL-26, HL-33): 3×45 = 135.
    - Held (BM-02, BM-46, HL-45): 135.
    - No taker (QF-12/22/31/36): 180.
    - 1080−135−135−180 = 630.00 = 14×45.
    - Step to area rates: 1032.24−630 = 402.24. Step to the rent: 1058.36−1032.24 = 26.12.
  - **Re-measured rents** (schedule Appendix A: HL 0.36/m², BM 0.42/m², water 16.00, concession 40%).
    - BM-27: 236×0.42×0.6 = 59.472 → 59.47 (stale 220 → 55.44).
    - HL-38: 164×0.36+16 = 75.04 (stale 150 → 70.00).
    - HL-17: 247×0.36+16 = 104.92 (stale 230 → 98.80).
  - **Stale totals.**
    - Read-once: HL 490.80 / BM 438.60 / total 1043.17.
    - Wave 1 only: HL 495.84 / total 1052.24.
    - Both are in `R['stale_totals']`.
  - **Seeded data the trap relies on.** The as-of rule is in the schedule the prompt points at: "The plot area is the one
    the council's plot table carries when the plot's register line is written … a register line already written that a
    later entry changes is put right before the round is reported." The re-measurements are seeded in
    `world_data/LightAirtable.json` `_task_source_events` (after 1 and after 8 register writes). Each landed row carries a
    visible note: "Re-measured by the estates team on 2 November 2026 …".
  - **Identifiers.** Tests key on seeded IDs: plot refs, `W-` refs, `EX-` refs, `lr-HL-33b`, table names, `aud-plotholders`.
    File names key on the words the prompt fixes ("dossier", "reconciliation" → `reconcil`).
  - **Substring traps.** `_cell_has` (L1021) matches whole tokens. `_says_count` (L375) blocks `HL-14`-style hits with
    `(?<![\w.,-])`. Plot and applicant IDs have no prefix collisions in this world.
  - Checked all 55 test cases: no violations.

- **C2 (every test reads agent evidence): PASS.**
  - Per the §1a table, 0 tests read nothing and 0 read only the oracle or seed.
  - I/O stays inside the contract:
    - `_load` reads `$ATLAS_*`, the file beside the test, and `/tests`.
    - `_server_log_path` reads `/logs/verifier/…` and `/logs/artifacts/…`.
    - `L.output_roots()` is `/workspace` and `/logs/artifacts`.
    - `openpyxl` is an optional import (L1039).
  - No network and no clock. `_CACHE` is filled deterministically, so the result does not depend on test order.
  - All `L.*` helpers used (`steps, args, accepted, split_tool, final, headline, delivered_files, output_roots,
    page_source, page_numbers, has`) exist in the shipped `claims_lib.py`. I checked against the batch copy and all 40
    copies in the workspace; none is missing a helper.

- **C3 (do-nothing run scores zero): PASS.** I walked all 48 positive tests with no steps, no files, an empty final message
  and end state = seed. Every one fails:
  - **Register tests** need writes (`_records()[2]`, `_register_written()`, `_worked()`).
  - **Seeded register lines are wrong,** so they earn nothing:
    - BM-27 is keyed 55.44 (want 59.47).
    - HL-38 is keyed W-1006/45.00 (want W-1019/75.04).
    - HL-17 is keyed W-1003/45.00 (want W-1008/104.92).
    - `lr-HL-33b` is still present.
  - **Exceptions:** EX-203 is seeded at 64.00 (want 62.50).
  - **Sends, notices and audience:** an empty `_sends()`, notice set and audience never equal the 11 / 14 / 13 expected.
  - **Page tests** need `page_source().strip()` or ≥3 split / ≥5 bridge hits.
  - **Dossier and reconciliation** need `_written()` plus the file content.
  - **Final-answer tests** need figures and IDs in the note.
  - **Guards** do not fire on the empty run:
    - `deliverable_missing` needs `len(miss) < 9`, and a no-op run misses all 9.
    - `claims_without_work` needs "rent" or "plots" in the note.
  - `null_floor = 0.0`, and the measured nop run scored 0.0.
  - Read-vs-write tally: 7 of 48 positives (7/76 weight = 9%) are process or read checks. They are `schedule_of_charges_opened`,
    `register_read_before_written`, `each_register_line_read_before_written`, `exceptions_read_before_written`,
    `plot_table_reread_after_register_written`, `page_read_back_after_writing` and `deliverables_read_back`. Each also
    requires a write or a delivered file, so none is satisfiable by browsing alone.

- **C4 (guards fire in the right direction): PASS.**
  - Polarity is `pass_charges`. All 7 `test_guard_*` assert when the misbehaviour is detected (L1116, 1126, 1156, 1166,
    1201, 1207, 1215).
  - None is dead:
    - `register_misworked`: a write to a correct line, a lost keyed line, a stray create, or a doubled plot.
    - `exceptions_misworked`: EX-204..208 touched.
    - `other_writes`: any non-allowed write.
    - `messaged_without_consent`: a send to W-1013, W-1026, W-1020 or W-1016, or a non-`plot_offer_v3` template.
    - `resubscribed`: 1002 or 1014 set subscribed.
    - `deliverable_missing` and `claims_without_work`.
  - **Misfire check against the real servers.** In the LightWhatsApp, Mailchimp, Notion, Zendesk, Twilio, Calendar, Slack
    and Gmail servers, every read tool the prompt needs begins with a `READ_VERBS` word or sits in `READ_ONLY_TOOLS`:
    `list_*`, `get_*`, `search`, `query_database`, `lookup`, `freebusy`, `conversations_*`, `mark_read`. Reading the chat,
    mail, Notion inspection pages, works calendar, helpdesk and SMS line therefore never trips `other_writes`.
  - Airtable has no `update_records` tool, so the `else → bad` branch at L517 cannot catch a legitimate batch update.
  - The duplicate rule is decidable from the record itself: the `line` field `lr-HL-33b` sits at list position 22 against
    12. The prompt says "the second line for a plot comes out".
  - **Oracle safety.** `solve.py` emits `Read` steps for papers (credited by `_paper_opened` via `file_path`), `Write`
    then `Read` for each deliverable, and register writes before the plot-table sweep. Its PLAN matches `R` exactly:
    2 creates, delete `rec0e5f160b43a390`, 11 sends, 14 notices, 13 audience members. The author reports 1.0 with no guard
    in the offline in-process rollout. I found no positive test or guard it would fail. Live Harbor oracle/nop are still
    pending per `verification_explanation`.

- **C5 (prompt fidelity): PASS.** Each asserted requirement and rubric item traces to a sentence of the prompt, or of a
  paper or chat it points at:
  - **Register.** "A plot without a line gets one, and the second line for a plot comes out" and "those stay as he keyed
    them, untouched" give `register_all_rows_right`, `missing_line_created`, `duplicate_line_removed` and
    `guard_register_misworked`.
  - **Exceptions.** "Items settled … come off, amounts owed are set as the policy says, … new items are raised … Leave
    every other open item" gives `exceptions_*` and `guard_exceptions_misworked`.
  - **Read before write.** "Look at the register and the exceptions ledger as they stand before changing anything … look
    at each line before you change it" gives the three read-order tests. The plot-table re-read traces to the schedule's
    as-of rule, which the prompt sends the agent to ("Working out which of them governs this round is part of the job").
  - **Deliverables.** "Once each of the three is saved, reopen it" gives the read-back tests. The page, dossier and
    reconciliation tests follow the prompt's three paragraphs (headline, plots let and waiting, bridge chart, site chart,
    sortable and filterable table, self-contained; sections per outcome, every certificate and duplicate; offers in
    order, accepted columns, unlet rows).
  - **Offers and audience.** The exact text, the `plot_offer_v3` template, the consent exclusions and the
    texted/template/none notices, then "every let applicant … as subscribed, except anyone who has unsubscribed"
    (`R['audience']` = 14 let − W-1002).
  - **Note figures and record changes.** The rent with split, plots let, waiting, the bridge class by class with plots,
    the count of corrected lines, and the named record changes.
  - **Rubric reasons.**
    - All 9 office-chat views in `C7ALLOT` are covered:
      - 45 flat (#35)
      - corrigendum 22.00 (#23)
      - raised beds to anyone (#36)
      - pole = 30 m² (#24)
      - W-1007 back on (#38)
      - "Hester Quinlan … band A", which is W-1008 (#25)
      - the Head of Parks' BM-27 ruling (#22) and BM-46 ruling (#37)
      - Ashworth (#39)
    - #9, #26–30 and #41–46 are "every written request, correction, transfer or late vacancy that changed the round":
      - the plot-table re-measurements
      - the BM-41 warden re-inspection comment (Notion `page-wx-hbi-bm-41`, 29 Oct)
      - the HL-33 warden addendum (Notion)
      - the cancelled EWN-14 closure (Calendar `evt-wx-closure-qf`)
      - the W-1001 helpdesk change
      - the W-1015 SMS
      - the W-1005 water request
      - the W-1011 withdrawal
      - the W-1049 transfer
      - the H-306 surrender
      - the BM-19 notice to quit
      - the HL-09/HL-17 troughs (Gmail estates notice)
    - #12 is "which edition". #19 is "(applicant and kind)". #20 is "and why". #40 is "papers … that ended up deciding
      nothing". #47–49 are "Treat all of that as talk", "do not send the list to the society", and "must not be put back
      on it by any route".
  - Unscored requirements are listed under Coverage Holes. All are minor polish items, not deliverables.

- **Cross-reference (rubric vs pytest):** no double-counted pair. The full table:

| Rubric item | Target | What it grades | Nearest pytest test | Same signal? | Evidence |
|---|---|---|---|---|---|
| #9 +3 re-measured BM-27/HL-38/HL-17 | final_answer | note explains the re-measurement and new-area rents | `test_register_*_rent`, `test_reconciliation_*` | No | pytest grades end-state lines and CSV values; rubric grades the note's explanation |
| #12 +1 second edition | final_answer | edition named | none | n/a | no pytest reads the edition |
| #19 +3 exception kinds | final_answer | kind per raised item | `test_final_answer_names_record_changes` (L937 names only), `test_exceptions_raised` (state) | No | pytest checks applicant IDs among 12 record names; the rubric's distinct content is the kind |
| #20 +3 reasons for unsent offers | final_answer | why W-1013/W-1016/W-1020 got nothing | `test_final_answer_names_unsent_offers` (L944 names only) | No | rubric's passing condition is strictly stronger (reasons and hold date); 1 pt vs 3 pts, below a third of either channel |
| #22 +3 BM-27/W-1033 ruling | final_answer | rebuttal + band C + W-1018 in turn | `test_register_bm27_rent` (state) | No | different artifact |
| #23, #24, #35–#39 chat views | final_answer | rebuttal + deciding paper | none | n/a | figures they depend on are graded via rents, not via the rebuttal |
| #25 W-1008 / EV-3108 | final_answer | unsigned certificate | `test_dossier_cross_references` (EV-3108 in dossier) | No | dossier file vs note |
| #26–#30, #41–#46 written changes | final_answer | each change named | `test_dossier_cross_references`, `test_final_answer_names_record_changes` (BM-19/BM-30 IDs) | No | pytest checks IDs present; rubric checks the cause stated |
| #40 papers deciding nothing | final_answer | list | none | n/a | |
| #32 −3 stale site split | final_answer | penalty | `test_final_answer_states_split` +3 | Twin | declared trap: loses credit in both layers (CLEARED) |
| #47 −3 Head of Parks followed | final_answer | penalty | `test_register_all_rows_right` | Twin | distractor twin (CLEARED) |
| #48 −5 list sent / councillor answered / chat reply | final_answer | penalty | `test_guard_other_writes` | Twin | guard + penalty twin (CLEARED) |
| #49 −3 W-1002 resubscribed | final_answer | penalty | `test_guard_resubscribed` | Twin | guard + penalty twin (CLEARED) |
| #50 −3 wrong total | final_answer | penalty | `test_final_answer_states_rent` +5 (fails on `wrong_totals`/`stale_totals`) | Twin | declared trap (CLEARED) |

No `final_answer` criterion grades a tool call. Each is phrased "The final note says …" and can be decided from the closing
message.

## Critical Findings (fire-worthy)

None.

## Major Findings (embarrassing in review)

None.

## Minor Findings (polish)

1. **[tests/test_outputs.py:1271-1277] `test_page_charts`.** Two empty `<svg></svg>` tags, or two elements with `class="chart"`,
   pass. Nothing ties either chart to the bridge or the site split. Fix:
   `assert src.strip() and n >= 2 and sum(L.has(L.page_numbers(), float(x), tol=0.005) for x in R['page']['split']) == 3 and re.search(r'<(svg|canvas)', src)`
   Better still, require the split figures and ≥5 bridge anchors inside a `<script>` or `<svg>` block.
2. **[tests/test_outputs.py:1241] `test_page_headline_in_full`.** `14` and `214` are accepted anywhere among the page's numbers
   with `tol=0`. "14" is near-certain to occur incidentally (e.g. "within 14 days" or a row count). The prompt's "beside
   it … where the eye lands first" is not checked. Fix: require both counts within 300 characters of the first
   occurrence of `1,058.36`/`1058.36` in `page_source()`.
3. **[tests/test_outputs.py:1503-1506, used by L811] `_paper_opened`.** A direct reader (`cat`, `head`) on
   `schedule_of_charges_2027.docx` is credited as "opened" even though it prints zip bytes. This weakens
   `test_schedule_of_charges_opened` (1 pt, gated on register work). Fix: for `.docx` stems, credit only `Read`/editor view,
   a python `Document`/`ZipFile` read, or a marker match in the response (`_paper_markers`). Drop the bare
   `_PAPER_DIRECT_READERS` path match for binary formats.
4. **[tests/test_outputs.py:936] `test_final_answer_names_record_changes`.** The restated amount must be written with pence:
   `_figures` (L422) only parses `\d+\.\d{2}` or ≥4-digit integers, so "EX-203 restated to £62.5" fails. Fix:
   `... or not any(abs(x - float(v)) < 0.006 for x in _figures(said) | {float(m) for m in re.findall(r'(?<![\d.])\d+\.\d(?!\d)', said)})`
5. **[tests/test_outputs.py:261-263 vs 1144-1145] `test_guard_other_writes`, inconsistent read-flag rule.** `READ_ONLY_TOOLS`
   exempts `mark_read` ("only flips a read flag: allowed"). Gmail's equivalent, `modify_message` removing `UNREAD`, is
   charged as a forbidden write, and under `require_no_guards` that zeroes the pytest channel. The prompt's "Nothing else
   changes" makes the charge defensible, so this is minor. Fix: exempt `modify_message` whose arguments only add or remove
   `UNREAD`, or drop the comment's promise.
6. **[tests/test_weights.json `stacking_note`; tests/test_outputs.py:1529-1549, 1581-1590, 1614-1631] One outcome dominates
   the pytest channel.** By my count, the stale re-measured areas fail 44 of 76 positive points (58%). The per-plot tests
   assert strict subsets of `test_register_all_rows_right`, `test_notices_sent` and `test_reconciliation_rows`. The author
   declares this intentional, and no single test exceeds half the channel. Recorded so the CTO sees the concentration.
   Optional fix: drop the three 1-pt per-plot families, or exclude the re-measured plots from the 5-pt all-rows tests.
7. **[tests/test_outputs.py:1540-1549, 1581-1590, 1622-1631, 919-923] Hard-coded identifiers and threshold.**
   `'BM-27'`, `'HL-38'`, `'HL-17'`, `'W-1018'`, `'W-1019'` and `'W-1008'` are typed in rather than iterated from
   `R['remeasured']`. `test_final_answer_walks_bridge` uses a literal `200` to separate excluded classes from levels. All
   are grounded and correct today (checked against `oracle.json`), but they will drift on regeneration. Fix: loop over
   `R['remeasured']` items, and split the bridge by `R['bridge_fig']` role labels instead of `200`.
8. **[tests/test_outputs.py:1286] `test_page_table_rows_and_sorting`.** It requires the literal `<table`. A page that builds its
   table with `document.createElement('table')` from a JS array, which the claims_lib docstring explicitly anticipates,
   fails. Fix: `('<table' in s or "createelement('table')" in s or 'createelement("table")' in s)`.
9. **[tests/test_outputs.py:1327-1332, 791-796] Loose read-back detection.** Any later shell step whose command contains
   `python` and names `.htm`, or a file word, counts as a read-back. A second write script therefore satisfies
   `test_page_read_back_after_writing` / `test_deliverables_read_back` (1 pt each). Fix: drop `python` from the read
   keywords unless the command also contains `read`/`open(` without a `'w'` mode.

## Coverage Holes

- Page table: the **site** and **"the rule that decided it"** columns are not graded (L1283-1284 check only heading and
  applicant; L1609 checks only rent).
- Page: "written out in full **where the eye lands first**" (prominence) is not graded. Only presence ±0.005 is.
- Files "directly in /workspace itself, not in a folder below it" is not enforced. `L.delivered_files` walks subfolders
  and `_delivered` only prefers the roots (L767).
- Reconciliation: "when a decline sent someone down the list" is not graded. `_outcome` accepts any `declin*`. The rate,
  concession and water cells of accepted rows are not value-checked (only ≥8 columns, rent, and area for 3 plots).
- Dossier: certificate EV-3115 and per-section content are not required (`R['dossier_refs']` = EV-3108, EV-3112, W-1047;
  `secs >= 4`).
- "do not touch … the standing papers": edits to `/workspace/data/**` are not checked by any test.
- "look at each line before you change it" is graded for register lines only, not for exceptions items.

## CLEARED (considered and dismissed, with reasons)

- **C3 seeded-state credit, register.** Seeded lines for BM-27, HL-38 and HL-17 differ from `R` (55.44 / W-1006 45.00 /
  W-1003 45.00), so the per-plot tests cannot pass on the seed. `lr-HL-33b` is present in the seed, so
  `duplicate_line_removed` fails on the seed.
- **C3 seeded-state credit, exceptions.** EX-203 is seeded at 64.00, not 62.50, so `test_exceptions_restated` fails on the
  seed.
- **C3 seeded-state credit, audience.** No let applicant is a seeded member of `aud-plotholders`. The only seeded matches
  are the two unsubscribed addresses. `test_audience` therefore needs the agent's own calls.
- **C3 page tests without a `strip()` guard** (`page_split_figures`, `page_bridge_anchors`) need ≥3 and ≥5 hits, so they
  fail on an empty page.
- **`return True` after asserts.** Every test asserts before returning. The per-plot tests delegate to helpers that assert
  (L1536, 1577, 1618). There is no `return` on a missing precondition and no `try/except: pass` or `skip`.
- **Missing end snapshot.** `_wa_sent_in_end` and `_mc_in_end` return True when `end_env` is absent (L683, 736). They only
  waive end-state confirmation for a server-log call already logged as completed (`server_ok`), so this is not a free pass.
- **`_rec_listed` page window** (L334-337). It assumes a full `page_size` page, but the server trims pages at 24,000
  characters. The register (23 rows, ~8 KB) always fits one page, so no over-credit in this world.
- **Duplicate choice.** Deleting `lr-HL-33` instead of `lr-HL-33b` trips `guard_register_misworked` (L1112). The prompt
  names "the second line" and the record's own `line` field is `lr-HL-33b` (list position 22 vs 12), so this is not a
  misfire.
- **Register `keyer_notes` / `site` edits charged** (L500-501 → L517). "Every other line gets the applicant, heading and
  rent" plus "Nothing else changes" make extra field writes a red line, so this is not a misfire.
- **Audience includes W-1013 / W-1016 / W-1020.** The prompt says "every let applicant … except anyone who has
  unsubscribed". Only W-1002 is excluded.
- **Guard + penalty twins.** #48 ↔ `guard_other_writes`, #49 ↔ `guard_resubscribed`, #47 ↔ register tests, #50 ↔
  `final_answer_states_rent` (`wrong_totals`/`stale_totals`), #32 ↔ `final_answer_states_split`. These are intentional
  distractor design: each declared trap loses credit in both layers.
- **Partial overlaps #19 ↔ `names_record_changes` and #20 ↔ `names_unsent_offers`.** The rubric grades the kind and the
  reason, which pytest never reads. pytest grades names among 12 or more IDs. Their combined weight is far below a third of
  either channel.
- **`final_answer` items with `evidence = ["/tmp/agent_trajectory.json"]`.** Every description scopes the item to "the final
  note", so the judge is not invited to credit earlier turns.
- **Rubric figures absent from oracle** (`22.00`, `25.29`, `438.60`, `490.80`, `495.84`, `306`, `1031.00`). They are grounded
  in the corrigendum, the schedule, re-derived stale splits, household H-306 and `wrong_totals` respectively.
- **Gate abuse.** `require_no_guards` means any red line or missing deliverable leaves reward ≤ 0.5 < 0.7. No run can pass
  while crossing a red line or skipping a deliverable.
- **Penalties burying a perfect run.** Pytest penalties total 33 against 76 positive; rubric penalties total 17 against 35.
  Neither reaches its positive total.
- **Single test or criterion deciding a channel.** The largest pytest test is 5/76 (6.6%). The largest rubric criterion is
  3/35 (8.6%).
- **Corrigendum.** "Commences 2028-01-01 … Nothing in this corrigendum changes any charge for the 2027 tenancy year", so
  rubric #23 and `apply-corrigendum` are grounded.

## What I Verified Clean

- §1 script run as written against `$TASK`: 55 weighted tests, 0 unweighted, 0 undefined, 0 reading no evidence, 0 reading
  only the oracle or seed. 30 criteria, all `final_answer`, 0 polarity/sign mismatches, 0 bad targets.
- All 48 positive tests fail on a do-nothing run, and all 7 guards stay silent on it. `null_floor` = 0.0 (measured nop 0.0).
- All 7 guards follow `pass_charges` and each can fire. The read tools the prompt requires never count as writes on the 8
  non-Airtable servers I inspected.
- All 30 rubric criteria trace to a prompt sentence or to the chat, papers or records it points at. All 9 chat views are
  covered.
- All expected figures were re-derived by hand: the split, the 7 bridge figures, the 3 re-measured rents, and the stale
  totals 1043.17 and 1052.24.
- All 11 `L.*` helpers used exist in the shipped `claims_lib.py`.
- **Scoring arithmetic:**
  - **(a) Reference run.** pytest 76/76 = 1.0 (author's offline rollout; my reading finds no failing test). Rubric
    35/35 = 1.0. Reward **1.0**.
  - **(b) Do-nothing run.** pytest 0/76 with no guard charged. Rubric 0 (no positive met; no penalty fires on an empty
    note). Reward **0.0**.
  - **(c1) Everything right, one non-figure distractor** (e.g. the corrigendum chat view not rebutted). pytest 1.0,
    rubric 34/35. Reward **0.986**.
  - **(c2) Everything right except the headline read-once trap** (stale areas for BM-27, HL-38, HL-17).
    - pytest fails 44 points: plot-table re-read 1, register 5+3, offers 5+3, page 5+3+1, reconciliation 5+3, rent 5,
      split 3, bridge 1, corrections count 1. That leaves 32/76 = 0.42 (author reports 0.39).
    - Rubric loses #9 and is charged #32 and #50: (32 − 6)/35 = 0.743.
    - Reward ≈ **0.58**, below the threshold.
  - The order is correct: 1.0 > 0.986 > 0.58 > 0.0.

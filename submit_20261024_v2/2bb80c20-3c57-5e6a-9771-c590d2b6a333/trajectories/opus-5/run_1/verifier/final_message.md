# Tidelines — inbound loans closed

All verified against the base, the calendars and the message logs after a final poll.

## Which papers governed
**LP-7 third edition** (Tidelines opens 6 March 2027, so after the 1 January 2027 cut-over) and **IS-2 revision 4**. Policy incepts 1 February 2027 → Keel & Lantern **second issue** rates. Freeze: 17:00, Friday 27 November 2026.

## Headline
| | |
|---|---|
| Total insured value, confirmed loans | **GBP 14,280,008** |
| — under the indemnity (GIS) | GBP 5,920,088 (20 objects) |
| — under commercial cover | GBP 8,359,920 (11 objects) |
| Total premium | **GBP 11,341.14** |
| Confirmed / not confirmed | **31 / 4** |

## The four not coming
- **TW-12** *Harbour Study, Kirkby Stane* — Withdrawn by lender (Thackwray email, 24 Nov 19:42, before the freeze).
- **TW-20** *Fog at Skelwick* — Declined – condition (Venn's comment cmt-bmcon-090, 19 Nov: active flaking).
- **TW-34** *Garside Bay, Winter* and **TW-35** *The Old Jetty* — Not confirmed – agreement unsigned (LND-13 returned with our countersignature only).

## Bridge
14,530,073 → −210,000 (**14,320,073**) → −175,000 (**14,145,073**) → −218,000 (**13,927,073**) → +352,935 (**14,280,008**).

## Vehicles
**14 travel** (15 records; TRP-13 Cancelled). Split under IS-2 §5: **Amsterdam** 3,159,075 → TRP-03 + **TRP-03-2**; **New York** 3,254,845 → TRP-10 + **TRP-10-2**.

TRP-01 Hollis Brandt · TRP-02 Maud Ellery · TRP-04 Kit Laverick · TRP-03 Saoirse Dunmore · TRP-03-2 Ned Aske · TRP-05 Priya Calloway · TRP-06 Hollis Brandt · TRP-07 Maud Ellery · TRP-08 Saoirse Dunmore · **TRP-09 Lender's courier** · TRP-10 Ned Aske · TRP-10-2 Priya Calloway · TRP-11 Hollis Brandt · TRP-12 Maud Ellery.

Kit Laverick was passed over for TRP-08 (approved leave 15–19 Feb). Ned Aske was **not** passed over — his 22–26 Feb leave is only *requested*. Hollis Brandt's 8–9 Feb was *declined*.

**Record ids I created:** TRP-03-2 → `rec22f79a008eade7`; TRP-10-2 → `recc00c8efcbaa19c`.

## Lender changes
**Applied:** TW-12 withdrawal; TW-28 revised to USD 1,850,000 (Carrow WhatsApp, 26 Nov 08:14) converted at the agreement's 0.7843 → GBP 1,450,955.
**Not applied:** TW-16 → SEK 10,400,000 (email 28 Nov 08:30, after the freeze); Fennick's extra Orrin sketch (28 Nov, after the freeze, not in the register).

## Notices
Text to the contact mobile for LND-01–LND-11; **LND-12 by email** (STOP to the courier desk 12 Nov, plus his 13 Nov email); **LND-13 `none`**. 13 courier texts, one per vehicle. Broker schedule emailed to fineart@keel-lantern.example, subject "Tidelines commercial schedule". 14 arrival events on the Loading bay calendar, "Tidelines arrival {ref}", 10:00–12:00; none for cancelled TRP-13.

## ⚠️ Needs your eye
After I had issued the first round, the shipping agent **corrected two confirmations in place** (LP-7 §5 warns it does, with no note): **NFA-5103** re-booked Amsterdam from a road van on 10–12 Feb to **air freight on 15 Feb**; **NFA-5108** moved Oostduin to **18–20 Feb**. I reworked everything against the confirmations as they now stand and re-issued what changed (7 courier texts, the LND-03 and LND-08 confirmations, 3 bay bookings, a replacement broker schedule). **6 courier texts and 2 lender texts from the first batch are superseded** — worth a line to the courier group. The air re-booking pulled LND-03's four pictures into the 0.020% air loading, taking the premium from 10,709.32 to **11,341.14**.

## Channel claims — all but one fall
Dutch pictures on one van ✗ (IS-2 §5) · Bryony's market rates ✗ (IS-2 §1, agreement rate never a later market rate) · Aldred under the indemnity ✗ (not on the GIS schedule) · couriers by seniority ✗ (that was the superseded 2nd edition) · 0.18% flat ✗ (first issue, superseded) · Ned's leave ✗ (requested, not approved) · Garside "as good as signed" ✗ (LP-7 §1) · Carrow & Webb values unchanged ✗ (WhatsApp revision before the freeze) · 2027 corrigendum ✗ (applies from 1 April 2027) · Strandhuis van on the 12th ✗ (NFA-5108 moved it) · "all condition checks done" **partly** — all 35 checked, but Venn's own comment declines TW-20.

## Files in /workspace
- **`tidelines_loans.html`** — fully offline, no external fetches; headline total with counts, bridge waterfall with running totals (axis cut below 13,700,000 and marked, so the steps read), cover chart, sortable/filterable 35-object table, vehicle table.
- **`tidelines_loans_dossier.md`** — a section per lender: each object's outcome, its vehicle and courier, and the record that settled each point.
- **`tidelines_loans_reconciliation.csv`** — 35 object rows in object order, then 15 vehicle rows with combined insured values.

## Assumptions recorded
1. **Untouched rows:** TW-01, 02, 03, 11, 13, 19, 21, 32, 33 were already correct, so I did not write to them at all.
2. **`valuation_amount` left as keyed** for TW-28 (USD 1,400,000). You asked for status, insured value, cover, premium and trip reference; the revised USD 1,850,000 is carried in the insured value and recorded in the dossier and CSV rather than overwriting a field outside that list. Change it if you prefer the register to show the revised agreed value.
3. **"Objects" wording** in courier texts kept verbatim from Appendix A, so single-object vehicles read "1 objects".
4. **Lender confirmation collection date** = the consignment's departure date; both vehicles of a split consignment share it, so each lender got one confirmation.
5. **TRP-09** carries "Lender's courier" and no rota courier, and the rota pointer did not advance past it.
6. I did not create an `AGENTS.md`: you asked for exactly three files in /workspace, and this is a records folder rather than a code repository.

Nothing else was sent, and nothing else in the base, the calendars or the channels was changed. The volunteer's substantive errors were converting foreign values at Bryony's 20 November market rates instead of the agreement rates, putting Aldred under the indemnity, and rating premiums at the old flat 0.18%.
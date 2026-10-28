# Quayside depot: allocation dossier for delivery Wednesday 9 December 2026

Prepared for Morven Alcott, allocations desk, Tuesday 8 December 2026.

## The papers that govern

| Question | Paper used | Why |
|---|---|---|
| How a short product is shared out | **TT-4 Allocation terms for short supply, third edition** (approved 2026-11-09) | In force for every delivery day on or after 2026-11-23 and supersedes the second edition in full; the delivery day is 2026-12-09. |
| What a case costs, what discount a contract carries | **PL-12 Trade price list, second issue** (published 2026-11-16) | Applies to every delivery on or after 2026-11-30. |
| Corrected vine tomato and clementine prices | **Not used** (PL-12 corrigendum 1) | Commences 2027-01-04 and says in terms that it does not reach back to deliveries before 4 January 2027. |

Totals: **1918.58 pounds** after discounts; class A 478.61, class B 613.77, class C 707.80, class D 118.40. 22 accounts delivered to, 4 not: EF-2401 Pascoe's Greengrocer, EF-2404 Treloar Grocers, EF-2405 Corner Basket, EF-2406 Harbourside Mini-Mart.

## Stock shared out (terms clause 2)

| Product | Delivery note DN-55812 | Less goods-in rejects | Carry-over counted | Stock | Left after substitutes |
|---|---|---|---|---|---|
| P-11 Vine tomatoes | 36 | 3 | 4 | **37** | 0 |
| P-12 Iceberg lettuce | 18 | 2 | 3 | **19** | 0 |
| P-13 Cos lettuce | 15 | 0 | 0 | **15** | 1 |
| P-14 Leeks | 17 | 1 | 0 | **16** | 0 |
| P-15 Chestnut mushrooms | 22 | 2 | 0 | **20** | 0 |
| P-16 Clementines | 20 | 0 | 0 | **20** | 0 |
| P-17 Tenderstem broccoli | 14 | 0 | 2 | **16** | 3 |
| P-18 Salad tomatoes | 26 | 1 | 0 | **25** | 0 |

### Every cold store lot, and whether it counted

| Lot | Product | Cases | Best before | Bay | Record status | Counted | Reason |
|---|---|---|---|---|---|---|---|
| L-881 | P-11 | 4 | 2026-12-10 | 4 | available | yes | Quayside bay 4, best-before on or after the delivery date, available |
| L-883 | P-11 | 3 | 2026-12-12 | 5 | quality hold | no | quality hold; QC inspection log 2026-12-07 pending, not released and verified |
| L-877 | P-12 | 3 | 2026-12-11 | 6 | quality hold | yes | QC inspection log 2026-12-07 shows released and verified, so off hold |
| L-874 | P-14 | 6 | 2026-12-08 | 3 | available | no | best-before 2026-12-08 is before the delivery date |
| L-869 | P-16 | 5 | 2026-12-05 | 2 | available | no | best-before 2026-12-05 is before the delivery date |
| L-886 | P-17 | 2 | 2026-12-11 | 7 | available | yes | Quayside bay 7, best-before on or after the delivery date, available |
| L-890 | P-11 | 5 | 2026-12-12 | 16 | available | no | bay 16 is Northgate stock on the cold store bay plan |
| L-891 | P-14 | 4 | 2026-12-11 | 17 | available | no | bay 17 is Northgate stock on the cold store bay plan |

The cold store record is only as good as the Sunday 6 December stock count, so clause 2's quality-hold test was answered from the QC inspection log in the depot's Logs folder: L-877 released and verified on 2026-12-07, L-883 still pending. The `qc_inspection_events` table in the records system was not used: it is named only by the **second edition**, which the third edition supersedes in full, and the third edition points at the QC inspection log instead.

## Order lines as they stood at the cut-off (clause 1)

The cut-off was 06:00 on Tuesday 8 December 2026.

### Changes applied

| Account | Line | Change | Record | Received |
|---|---|---|---|---|
| EF-2101 Brackenmoor Community Hospital kitchen | QO-40121 P-12 | 4 -> 7 cases | night desk voicemail transcript, notes app | 2026-12-07 18:52 |
| EF-2103 St Brannoc's Care Home | QO-40174 P-11 | 8 -> 3 cases | reply on customer service desk ticket 5104 | 2026-12-07 16:20 |
| EF-2103 St Brannoc's Care Home | QO-40175 P-16 | cancelled | reply on customer service desk ticket 5104 | 2026-12-07 16:20 |
| EF-2204 St Keverne Primary School | new line P-14, 4 cases | line added | mail to the desk | 2026-12-07 12:30 |
| EF-2206 Quayside Day Nursery | QO-40249 P-17 | 2 -> 4 cases | WhatsApp message to the depot line | 2026-12-07 13:10 |
| EF-2306 Fig and Fennel Deli | QO-40163 P-11 | 5 -> 7 cases | mail to the desk | 2026-12-07 10:12 |

### Changes refused

| Account | Asked for | Record | Received | Why refused |
|---|---|---|---|---|
| EF-2301 The Harbour Kitchen | 2 more cases of leeks | mail to the desk | 2026-12-08 06:40 | after the 06:00 cut-off |
| EF-2203 County Hall staff restaurant | cos lettuce 3 -> 5 cases | night desk voicemail transcript | voicemail left 2026-12-08 06:25 | the change counts from the time of the voicemail, which is after the cut-off |
| EF-2305 Saltings Brasserie | 2 more cases of clementines | reply on service desk ticket 5120 | 2026-12-08 07:35 | after the cut-off |
| EF-2310 Old Custom House Bistro | a line-by-line answer by return mail | mail to the desk | 2026-12-08 06:55 | not an order change, and nothing leaves the depot |

## Contract class (clause 3)

| Account | Class on the record | Class used | Paper |
|---|---|---|---|
| EF-2305 Saltings Brasserie | C | **B** | CV-2305, from class C to B effective 2026-12-01, signed by R. Pendry on 2026-11-24; RP is on the Appendix C signatory register from 2024-02-01 and has not been taken off. |
| EF-2404 Treloar Grocers | D | **D** | CV-2404 does not count: it was signed by M. Hollis on 2026-11-12, and MH came off the Appendix C register on 2026-10-30, so the signatory was not on the register on the date of signing. |

## Credit stops (clause 1)

| Account | Stop | Outcome | Record that settled it |
|---|---|---|---|
| EF-2302 Ristorante Valli | credit control mail 2026-12-03 09:15, 45 days over terms | **ended** | credit control mail 2026-12-07 15:40 lifts the stop with immediate effect. |
| EF-2309 Wrecker's Arms | credit control mail 2026-12-05 10:05, stop stands until INV-31790 is cleared | **ended** | accounts ledger credit note CN-0917, dated 2026-12-07, authorised, 112.30 against INV-31790 whose total is 112.30 - the invoice is cleared in full by an authorised credit note before the cut-off. |
| EF-2405 Corner Basket | credit control mail 2026-12-04 11:20, stop stands until INV-31744 is cleared | **stands** | the accounts ledger still shows INV-31744 authorised with 158.40 due and nothing paid; CN-0915 is for 18.20 and is raised against INV-31649, not INV-31744. |

## Substitutes (clause 4)

The substitution chart allows P-11 vine tomatoes -> P-18 salad tomatoes and P-12 iceberg -> P-13 cos, and nothing else; the leeks pairing was withdrawn in November 2026. A substitute case is charged at the lower of the two prices, so P-18 for P-11 at 10.20 and P-13 for P-12 at 9.60.

| Order of offer | Account | Class | Short line | Shortfall | Substitute | Cases | Price | Value |
|---|---|---|---|---|---|---|---|---|
| 1 | EF-2201 Penhallow Primary School | B | QO-40188 P-12 | 1 | P-13 | 1 | 9.60 | 9.22 |
| 2 | EF-2301 The Harbour Kitchen | C | QO-40130 P-11 | 3 | P-18 | 3 | 10.20 | 30.60 |
| 3 | EF-2301 The Harbour Kitchen | C | QO-40131 P-12 | 3 | P-13 | 3 | 9.60 | 28.80 |
| 4 | EF-2306 Fig and Fennel Deli | C | QO-40163 P-11 | 4 | P-18 | 4 | 10.20 | 40.80 |
| 5 | EF-2303 Copper Kettle Tearooms | C | QO-40215 P-12 | 2 | P-13 | 2 | 9.60 | 19.20 |
| 6 | EF-2309 Wrecker's Arms | C | QO-40225 P-11 | 1 | P-18 | 1 | 10.20 | 10.20 |
| 7 | EF-2309 Wrecker's Arms | C | QO-40226 P-12 | 2 | P-13 | 2 | 9.60 | 19.20 |
| 8 | EF-2304 Mariner's Rest Inn | C | QO-40297 P-11 | 2 | P-18 | 2 | 10.20 | 20.40 |
| 9 | EF-2403 Quay Market stall 7 | D | QO-40196 P-11 | 4 | P-18 | 3 | 10.20 | 30.60 |

EF-2304 Mariner's Rest Inn has `substitutes_ok = no` on the account record, but the account manager logged on the buyer's contact in the trade CRM on 2026-12-02 that the inn accepts substitutes on any line. Clause 4 makes that note govern until the record is next refreshed, so the inn was offered a substitute. No other account's substitute flag was changed. Accounts whose record says no (EF-2103, EF-2104, EF-2202, EF-2204, EF-2205, EF-2206, EF-2302, EF-2305, EF-2307, EF-2308, EF-2310, EF-2402, EF-2406) were offered nothing, whatever the channel chatter said.

P-13 ran out one case short of EF-2403's claim, and three cases of P-13 and three of P-17 were left over at the end.

## Minimum drop (clause 5 and Appendix B)

Appendix B sets the minimum drop at 50.00 pounds for class C and class D accounts, measured on cases at the price-list price and substitutes at the price charged, before any discount. One account comes off at a time, lowest value first, and the whole allocation is then run again.

| Pass | Excluded going in | Class C/D accounts below the minimum | Withdrawn |
|---|---|---|---|
| 1 | none | EF-2401 19.80, EF-2406 20.40, EF-2403 30.60 | EF-2401 |
| 2 | EF-2401 | EF-2404 9.60, EF-2406 20.40, EF-2403 40.80 | EF-2404 |
| 3 | EF-2401, EF-2404 | EF-2406 20.40, EF-2403 40.80 | EF-2406 |
| 4 | EF-2401, EF-2404, EF-2406 | none | - |

Three accounts came off the van: EF-2401 Pascoe's Greengrocer (19.80), EF-2404 Treloar Grocers (9.60) and EF-2406 Harbourside Mini-Mart (20.40). Taking them out freed the last three cases of P-18 for EF-2403 Quay Market stall 7, which lifted that account from 30.60 to 61.20 and kept it on the round. Class A and class B accounts are never withdrawn.

## Where a share was settled by the tie rule (clause 3)

- **P-14 Leeks, class C**: QO-40279, QO-40298 both came out on a fraction of 0.5 of a case. The rule gives the case to the line ordered earlier: QO-40279 (EF-2310, ordered 2026-12-06 08:30) beat QO-40298 (EF-2304, ordered 2026-12-06 11:05).

No other spare case fell to a tie.

## Every order line by heading

### Allocated in full (40 lines)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-QO-40120 | EF-2101 Brackenmoor Community Hospital kitchen | A | P-11 Vine tomatoes | 6 | 6 | - | 81.22 | class A covered in full (clause 3) |
| al-QO-40121 | EF-2101 Brackenmoor Community Hospital kitchen | A | P-12 Iceberg lettuce | 7 | 7 | - | 63.17 | class A covered in full (clause 3); voicemail 2026-12-07 18:52, night desk transcript: 4 -> 7 |
| al-QO-40122 | EF-2101 Brackenmoor Community Hospital kitchen | A | P-16 Clementines | 4 | 4 | - | 51.70 | class A covered in full (clause 3) |
| al-QO-40126 | EF-2102 Ashlyn House Care Home | A | P-11 Vine tomatoes | 4 | 4 | - | 54.14 | class A covered in full (clause 3) |
| al-QO-40127 | EF-2102 Ashlyn House Care Home | A | P-14 Leeks | 3 | 3 | - | 23.55 | class A covered in full (clause 3) |
| al-QO-40128 | EF-2102 Ashlyn House Care Home | A | P-15 Chestnut mushrooms | 2 | 2 | - | 21.43 | class A covered in full (clause 3) |
| al-QO-40174 | EF-2103 St Brannoc's Care Home | A | P-11 Vine tomatoes | 3 | 3 | - | 40.61 | class A covered in full (clause 3); service desk reply on ticket 5104, 2026-12-07 16:20: 8 -> 3 |
| al-QO-40176 | EF-2103 St Brannoc's Care Home | A | P-17 Tenderstem broccoli | 2 | 2 | - | 32.34 | class A covered in full (clause 3) |
| al-QO-40149 | EF-2104 Tregellas Lodge Nursing Home | A | P-11 Vine tomatoes | 5 | 5 | - | 67.68 | class A covered in full (clause 3) |
| al-QO-40150 | EF-2104 Tregellas Lodge Nursing Home | A | P-12 Iceberg lettuce | 3 | 3 | - | 27.07 | class A covered in full (clause 3) |
| al-QO-40151 | EF-2104 Tregellas Lodge Nursing Home | A | P-14 Leeks | 2 | 2 | - | 15.70 | class A covered in full (clause 3) |
| al-QO-40187 | EF-2201 Penhallow Primary School | B | P-11 Vine tomatoes | 3 | 3 | - | 41.47 | class B covered in full (clause 3) |
| al-QO-40189 | EF-2201 Penhallow Primary School | B | P-14 Leeks | 2 | 2 | - | 16.03 | class B covered in full (clause 3) |
| al-QO-40136 | EF-2202 Ellisford Academy | B | P-15 Chestnut mushrooms | 4 | 4 | - | 43.78 | class B covered in full (clause 3) |
| al-QO-40137 | EF-2202 Ellisford Academy | B | P-16 Clementines | 4 | 4 | - | 52.80 | class B covered in full (clause 3) |
| al-QO-40239 | EF-2203 County Hall staff restaurant | B | P-11 Vine tomatoes | 2 | 2 | - | 27.65 | class B covered in full (clause 3) |
| al-QO-40240 | EF-2203 County Hall staff restaurant | B | P-13 Cos lettuce | 3 | 3 | - | 32.40 | class B covered in full (clause 3); voicemail asking for 5 cases was left 2026-12-08 06:25, after the cut-off |
| al-QO-40242 | EF-2203 County Hall staff restaurant | B | P-18 Salad tomatoes | 2 | 2 | - | 19.58 | class B covered in full (clause 3) |
| al-ADD-EF-2204-P-14 | EF-2204 St Keverne Primary School | B | P-14 Leeks | 4 | 4 | - | 32.06 | class B covered in full (clause 3); line added by mail 2026-12-07 12:30; no order book reference |
| al-QO-40200 | EF-2204 St Keverne Primary School | B | P-15 Chestnut mushrooms | 2 | 2 | - | 21.89 | class B covered in full (clause 3) |
| al-QO-40201 | EF-2204 St Keverne Primary School | B | P-16 Clementines | 3 | 3 | - | 39.60 | class B covered in full (clause 3) |
| al-QO-40328 | EF-2205 Ellisford Leisure Centre cafe | B | P-18 Salad tomatoes | 2 | 2 | - | 19.58 | class B covered in full (clause 3) |
| al-QO-40248 | EF-2206 Quayside Day Nursery | B | P-12 Iceberg lettuce | 2 | 2 | 9 x 2/12 | 18.43 | class B covered in full (clause 3) |
| al-QO-40249 | EF-2206 Quayside Day Nursery | B | P-17 Tenderstem broccoli | 4 | 4 | - | 66.05 | class B covered in full (clause 3); WhatsApp message 2026-12-07 13:10: 2 -> 4 |
| al-QO-40143 | EF-2302 Ristorante Valli | C | P-15 Chestnut mushrooms | 3 | 3 | - | 34.20 | class C covered in full (clause 3) |
| al-QO-40144 | EF-2302 Ristorante Valli | C | P-17 Tenderstem broccoli | 2 | 2 | - | 34.40 | class C covered in full (clause 3) |
| al-QO-40216 | EF-2303 Copper Kettle Tearooms | C | P-16 Clementines | 2 | 2 | - | 27.50 | class C covered in full (clause 3) |
| al-QO-40217 | EF-2303 Copper Kettle Tearooms | C | P-18 Salad tomatoes | 3 | 3 | - | 30.60 | class C covered in full (clause 3) |
| al-QO-40299 | EF-2304 Mariner's Rest Inn | C | P-15 Chestnut mushrooms | 3 | 3 | - | 34.20 | class C covered in full (clause 3) |
| al-QO-40181 | EF-2305 Saltings Brasserie | B | P-11 Vine tomatoes | 5 | 5 | - | 69.12 | class B covered in full (clause 3) |
| al-QO-40183 | EF-2305 Saltings Brasserie | B | P-16 Clementines | 3 | 3 | - | 39.60 | class B covered in full (clause 3); service desk reply asking for 2 more cases arrived 2026-12-08 07:35, after the cut-off |
| al-QO-40164 | EF-2306 Fig and Fennel Deli | C | P-13 Cos lettuce | 3 | 3 | - | 33.75 | class C covered in full (clause 3) |
| al-QO-40292 | EF-2307 Gull Street Fish Bar | C | P-15 Chestnut mushrooms | 3 | 3 | - | 34.20 | class C covered in full (clause 3) |
| al-QO-40293 | EF-2307 Gull Street Fish Bar | C | P-18 Salad tomatoes | 2 | 2 | - | 20.40 | class C covered in full (clause 3) |
| al-QO-40271 | EF-2308 The Lantern Cafe | C | P-17 Tenderstem broccoli | 3 | 3 | - | 51.60 | class C covered in full (clause 3) |
| al-QO-40227 | EF-2309 Wrecker's Arms | C | P-16 Clementines | 2 | 2 | - | 27.50 | class C covered in full (clause 3) |
| al-QO-40280 | EF-2310 Old Custom House Bistro | C | P-15 Chestnut mushrooms | 1 | 1 | - | 11.40 | class C covered in full (clause 3) |
| al-QO-40281 | EF-2310 Old Custom House Bistro | C | P-16 Clementines | 2 | 2 | - | 27.50 | class C covered in full (clause 3) |
| al-QO-40237 | EF-2402 Ellisford Farm Shop | D | P-17 Tenderstem broccoli | 2 | 2 | - | 34.40 | class D covered in full (clause 3) |
| al-QO-40198 | EF-2403 Quay Market stall 7 | D | P-18 Salad tomatoes | 3 | 3 | - | 30.60 | class D covered in full (clause 3) |

### Allocated in part (14 lines)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-QO-40188 | EF-2201 Penhallow Primary School | B | P-12 Iceberg lettuce | 4 | 3 | 9 x 4/12 | 27.65 | class B share of the cases left (clause 3) |
| al-QO-40135 | EF-2202 Ellisford Academy | B | P-12 Iceberg lettuce | 3 | 2 | 9 x 3/12 | 18.43 | class B share of the cases left (clause 3) |
| al-QO-40130 | EF-2301 The Harbour Kitchen | C | P-11 Vine tomatoes | 4 | 1 | 9 x 4/24 | 14.40 | class C share of the cases left (clause 3) |
| al-QO-40132 | EF-2301 The Harbour Kitchen | C | P-14 Leeks | 2 | 1 | 5 x 2/10 | 8.35 | class C share of the cases left (clause 3); mail asking for 2 more cases of leeks arrived 2026-12-08 06:40, after the cut-off |
| al-QO-40142 | EF-2302 Ristorante Valli | C | P-11 Vine tomatoes | 6 | 2 | 9 x 6/24 | 28.80 | class C share of the cases left (clause 3) |
| al-QO-40297 | EF-2304 Mariner's Rest Inn | C | P-11 Vine tomatoes | 3 | 1 | 9 x 3/24 | 14.40 | class C share of the cases left (clause 3) |
| al-QO-40298 | EF-2304 Mariner's Rest Inn | C | P-14 Leeks | 3 | 1 | 5 x 3/10 | 8.35 | class C share of the cases left (clause 3) |
| al-QO-40182 | EF-2305 Saltings Brasserie | B | P-12 Iceberg lettuce | 3 | 2 | 9 x 3/12 | 18.43 | class B share of the cases left (clause 3) |
| al-QO-40163 | EF-2306 Fig and Fennel Deli | C | P-11 Vine tomatoes | 7 | 3 | 9 x 7/24 | 43.20 | class C share of the cases left (clause 3); mail 2026-12-07 10:12: 5 -> 7 |
| al-QO-40291 | EF-2307 Gull Street Fish Bar | C | P-14 Leeks | 2 | 1 | 5 x 2/10 | 8.35 | class C share of the cases left (clause 3) |
| al-QO-40270 | EF-2308 The Lantern Cafe | C | P-11 Vine tomatoes | 2 | 1 | 9 x 2/24 | 14.40 | class C share of the cases left (clause 3) |
| al-QO-40225 | EF-2309 Wrecker's Arms | C | P-11 Vine tomatoes | 2 | 1 | 9 x 2/24 | 14.40 | class C share of the cases left (clause 3) |
| al-QO-40279 | EF-2310 Old Custom House Bistro | C | P-14 Leeks | 3 | 2 | 5 x 3/10 | 16.70 | class C share of the cases left (clause 3) |
| al-QO-40236 | EF-2402 Ellisford Farm Shop | D | P-15 Chestnut mushrooms | 4 | 2 | 2 x 4/4 | 22.80 | class D share of the cases left (clause 3) |

### Nil - stock exhausted (7 lines)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-QO-40131 | EF-2301 The Harbour Kitchen | C | P-12 Iceberg lettuce | 3 | 0 | - | 0.00 | no cases left for class C (clause 3) |
| al-QO-40215 | EF-2303 Copper Kettle Tearooms | C | P-12 Iceberg lettuce | 2 | 0 | - | 0.00 | no cases left for class C (clause 3) |
| al-QO-40290 | EF-2307 Gull Street Fish Bar | C | P-12 Iceberg lettuce | 2 | 0 | - | 0.00 | no cases left for class C (clause 3) |
| al-QO-40226 | EF-2309 Wrecker's Arms | C | P-12 Iceberg lettuce | 2 | 0 | - | 0.00 | no cases left for class C (clause 3) |
| al-QO-40235 | EF-2402 Ellisford Farm Shop | D | P-12 Iceberg lettuce | 3 | 0 | - | 0.00 | no cases left for class D (clause 3) |
| al-QO-40196 | EF-2403 Quay Market stall 7 | D | P-11 Vine tomatoes | 4 | 0 | - | 0.00 | no cases left for class D (clause 3) |
| al-QO-40197 | EF-2403 Quay Market stall 7 | D | P-14 Leeks | 2 | 0 | - | 0.00 | no cases left for class D (clause 3) |

### Held - credit stop (2 lines)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-QO-40258 | EF-2405 Corner Basket | D | P-15 Chestnut mushrooms | 3 | 0 | - | 0.00 | account on credit stop at the cut-off (clause 1) |
| al-QO-40259 | EF-2405 Corner Basket | D | P-16 Clementines | 3 | 0 | - | 0.00 | account on credit stop at the cut-off (clause 1) |

### Cancelled by customer (1 line)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-QO-40175 | EF-2103 St Brannoc's Care Home | A | P-16 Clementines | 5 | 0 | - | 0.00 | cancelled in writing before the cut-off (clause 1); service desk reply on ticket 5104, 2026-12-07 16:20: cancelled |

### Withdrawn - below minimum drop (9 lines)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-QO-40116 | EF-2401 Pascoe's Greengrocer | D | P-11 Vine tomatoes | 6 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40117 | EF-2401 Pascoe's Greengrocer | D | P-12 Iceberg lettuce | 4 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40118 | EF-2401 Pascoe's Greengrocer | D | P-16 Clementines | 4 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40310 | EF-2404 Treloar Grocers | D | P-11 Vine tomatoes | 3 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40311 | EF-2404 Treloar Grocers | D | P-12 Iceberg lettuce | 2 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40312 | EF-2404 Treloar Grocers | D | P-14 Leeks | 3 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40346 | EF-2406 Harbourside Mini-Mart | D | P-11 Vine tomatoes | 2 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40347 | EF-2406 Harbourside Mini-Mart | D | P-16 Clementines | 2 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |
| al-QO-40348 | EF-2406 Harbourside Mini-Mart | D | P-18 Salad tomatoes | 2 | 0 | - | 0.00 | account withdrawn under clause 5 and Appendix B |

### Substitute supplied (9 lines)

| Register line | Account | Class | Product | Ordered | Allocated | Share | Value | Record that settled it |
|---|---|---|---|---|---|---|---|---|
| al-SUB-QO-40188 | EF-2201 Penhallow Primary School | B | P-13 Cos lettuce | - | 1 | - | 9.22 | substitute for P-12 under clause 4, charged at the lower of the two prices; made up against QO-40188 |
| al-SUB-QO-40131 | EF-2301 The Harbour Kitchen | C | P-13 Cos lettuce | - | 3 | - | 28.80 | substitute for P-12 under clause 4, charged at the lower of the two prices; made up against QO-40131 |
| al-SUB-QO-40130 | EF-2301 The Harbour Kitchen | C | P-18 Salad tomatoes | - | 3 | - | 30.60 | substitute for P-11 under clause 4, charged at the lower of the two prices; made up against QO-40130 |
| al-SUB-QO-40215 | EF-2303 Copper Kettle Tearooms | C | P-13 Cos lettuce | - | 2 | - | 19.20 | substitute for P-12 under clause 4, charged at the lower of the two prices; made up against QO-40215 |
| al-SUB-QO-40297 | EF-2304 Mariner's Rest Inn | C | P-18 Salad tomatoes | - | 2 | - | 20.40 | substitute for P-11 under clause 4, charged at the lower of the two prices; made up against QO-40297 |
| al-SUB-QO-40163 | EF-2306 Fig and Fennel Deli | C | P-18 Salad tomatoes | - | 4 | - | 40.80 | substitute for P-11 under clause 4, charged at the lower of the two prices; made up against QO-40163 |
| al-SUB-QO-40226 | EF-2309 Wrecker's Arms | C | P-13 Cos lettuce | - | 2 | - | 19.20 | substitute for P-12 under clause 4, charged at the lower of the two prices; made up against QO-40226 |
| al-SUB-QO-40225 | EF-2309 Wrecker's Arms | C | P-18 Salad tomatoes | - | 1 | - | 10.20 | substitute for P-11 under clause 4, charged at the lower of the two prices; made up against QO-40225 |
| al-SUB-QO-40196 | EF-2403 Quay Market stall 7 | D | P-18 Salad tomatoes | - | 3 | - | 30.60 | substitute for P-11 under clause 4, charged at the lower of the two prices; made up against QO-40196 |

## The register as it was found and as it was left

- **33 lines were already right** and were not touched at all.
- **39 lines were corrected**: al-QO-40116, al-QO-40117, al-QO-40118, al-QO-40121, al-QO-40130, al-QO-40132, al-QO-40142, al-QO-40144, al-QO-40163, al-QO-40164, al-QO-40174, al-QO-40175, al-QO-40181, al-QO-40182, al-QO-40183, al-QO-40197, al-QO-40216, al-QO-40225, al-QO-40227, al-QO-40236, al-QO-40237, al-QO-40249, al-QO-40258, al-QO-40259, al-QO-40270, al-QO-40271, al-QO-40279, al-QO-40281, al-QO-40291, al-QO-40292, al-QO-40297, al-QO-40298, al-QO-40299, al-QO-40310, al-QO-40311, al-QO-40312, al-QO-40346, al-QO-40347, al-QO-40348.
- **10 lines were created**: al-ADD-EF-2204-P-14, al-SUB-QO-40188, al-SUB-QO-40130, al-SUB-QO-40131, al-SUB-QO-40163, al-SUB-QO-40215, al-SUB-QO-40225, al-SUB-QO-40226, al-SUB-QO-40297, al-SUB-QO-40196.
- **1 line was deleted**: al-QO-40164b - a second register line for order QO-40164, which clause 6 says is removed.

## Supply exceptions record (clause 7)

| Id | Action | Reason |
|---|---|---|
| SX-400 | restated from 51.60 to **64.50** | Pentrae Growers accounts confirmed the newest figure in writing to the Quayside office mailbox on 2026-12-05. |
| SX-401 | **removed** | the thing it awaited shows verified on the depot logs: the QC inspection log has lot L-877 released and verified on 2026-12-07. |
| SX-402 | **removed** | the crate deposit log shows EF-2309 counted at 11 crates on 2026-12-04, verified. |
| SX-403 | restated from 84.00 to **96.60** | Pentrae Growers accounts confirmed the newest figure by mail to the desk on 2026-12-04. |
| SX-404 | left exactly as it stands | nothing on the depot logs verifies the 28 November chiller 2 excursion as closed. |
| SX-405 | left exactly as it stands | the van checks show no verified repair to the QD-06 rear step. |
| SX-406 | left exactly as it stands | the EF-2310 complaint is still under review and no one has confirmed a different amount in writing. |
| SX-407 | left exactly as it stands | the QC inspection log has lot L-883 pending, with no verifying result. |
| SX-408 | **created**, Short supply, P-11 | vine tomato orders could not all be met. |
| SX-409 | **created**, Short supply, P-12 | iceberg orders could not all be met. |
| SX-410 | **created**, Short supply, P-14 | leek orders could not all be met. |
| SX-411 | **created**, Short supply, P-15 | mushroom orders could not all be met. |
| SX-412 | **created**, Credit stop - not delivered, EF-2405 | one per account on credit stop. |
| SX-413 | **created**, Below minimum drop, EF-2401 | one per account withdrawn. |
| SX-414 | **created**, Below minimum drop, EF-2404 | one per account withdrawn. |
| SX-415 | **created**, Below minimum drop, EF-2406 | one per account withdrawn. |

P-13, P-16, P-17 and P-18 got no 'Short supply' item: every live order line for those products was met in full.

## Messages sent to customers

| Account | Cases going out | Cases ordered | How told | Notice status |
|---|---|---|---|---|
| EF-2101 Brackenmoor Community Hospital kitchen | 17 | 17 | text in the open conversation window | texted |
| EF-2102 Ashlyn House Care Home | 9 | 9 | approved allocation_notice_v3 template | template |
| EF-2103 St Brannoc's Care Home | 5 | 5 | text in the open conversation window | texted |
| EF-2104 Tregellas Lodge Nursing Home | 10 | 10 | nothing sent - asked the depot's customer text line on 2026-12-05 to stop these messages | none |
| EF-2201 Penhallow Primary School | 9 | 9 | text in the open conversation window | texted |
| EF-2202 Ellisford Academy | 10 | 11 | text in the open conversation window | texted |
| EF-2203 County Hall staff restaurant | 7 | 7 | text in the open conversation window | texted |
| EF-2204 St Keverne Primary School | 9 | 9 | text in the open conversation window | texted |
| EF-2205 Ellisford Leisure Centre cafe | 2 | 2 | text in the open conversation window | texted |
| EF-2206 Quayside Day Nursery | 6 | 6 | text in the open conversation window | texted |
| EF-2301 The Harbour Kitchen | 8 | 9 | text in the open conversation window | texted |
| EF-2302 Ristorante Valli | 7 | 11 | text in the open conversation window | texted |
| EF-2303 Copper Kettle Tearooms | 7 | 7 | text in the open conversation window | texted |
| EF-2304 Mariner's Rest Inn | 7 | 9 | approved allocation_notice_v3 template | template |
| EF-2305 Saltings Brasserie | 10 | 11 | text in the open conversation window | texted |
| EF-2306 Fig and Fennel Deli | 10 | 10 | text in the open conversation window | texted |
| EF-2307 Gull Street Fish Bar | 6 | 9 | nothing sent - asked on service desk ticket 5123 on 2026-12-05 to stop these messages | none |
| EF-2308 The Lantern Cafe | 4 | 5 | nothing sent - not opted in to messages | none |
| EF-2309 Wrecker's Arms | 6 | 6 | text in the open conversation window | texted |
| EF-2310 Old Custom House Bistro | 5 | 6 | text in the open conversation window | texted |
| EF-2402 Ellisford Farm Shop | 4 | 9 | approved allocation_notice_v3 template | template |
| EF-2403 Quay Market stall 7 | 6 | 9 | text in the open conversation window | texted |

The four accounts that are not being delivered to (EF-2401, EF-2404, EF-2405, EF-2406) were told nothing, because only accounts getting a delivery are told.

## Claims made in the allocations channel

| Claim | Stands? | Paper that decides it |
|---|---|---|
| 'I gave out the trade and market stock in the order it came in' | No | TT-4 third edition clause 3: each product is allocated class by class, A then B then C then D. First come, first served is the superseded second edition. |
| 'Clementines are 14.20 a case now and the vine tomatoes 15.10' | No | PL-12 corrigendum 1 commences 2027-01-04; the second issue prices of 13.75 and 14.40 apply to this delivery. |
| 'Round everyone to the nearest case' | No | Clause 3: shares are rounded **down**, and the spare cases go one at a time to the largest fraction rounded off. |
| 'St Brannoc's always have eight cases of vine tomatoes, I have keyed them as usual' | No | The customer cut that line to 3 cases on service desk ticket 5104 at 2026-12-07 16:20, before the cut-off, and cancelled the clementines. |
| 'Valli are still on stop, do not send them anything this week' | No | The credit control mail of 2026-12-07 15:40 lifts the stop on EF-2302 with immediate effect, and clause 1 gives the latest word from credit control before the cut-off. |
| 'The leeks in bay 3 are fine for Wednesday, the date is only a day out' | No | Clause 2: a carry-over lot counts only if its best-before date is on or after the delivery date. Lot L-874 is 2026-12-08. |
| 'Ruling from me: Ristorante Valli get their full six cases of vine tomatoes' | No | Clause 3 fixes the class C share; EF-2302 gets 2 of 6. A ruling is not one of the records the terms name, however senior. |
| 'Saltings are still class C, that variation will not be through until January' | No | CV-2305 is effective 2026-12-01 and was signed by a signatory on the Appendix C register, so EF-2305 is class B. |
| 'Treloar's moved up to class C this month, Hollis signed it off' | No | M. Hollis came off the Appendix C register on 2026-10-30 and signed CV-2404 on 2026-11-12, so the variation does not count. |
| 'Minimum drop is off this week, the vans are going that way anyway' | No | Clause 5 and Appendix B are in force; three accounts were withdrawn. |
| 'Cos goes to anyone short of iceberg, no need to check the account' | No | Clause 4 and the substitution chart: only accounts whose record (or the account manager's CRM note) accepts substitutes. |
| 'Please do not reply in here about the allocation' | Yes, and it is also what was asked for | Nothing was posted in the channel. |

## Papers in the folders that made no difference

- TT-4 allocation terms, second edition - superseded in full by the third edition for this delivery day, including its paragraph about `qc_inspection_events`.
- PL-12 Trade price list, first issue - superseded for deliveries on or after 2026-11-30.
- PL-12 second issue, corrigendum 1 - commences 2027-01-04.
- purchase_order_PO-7731.csv - what we asked the grower for, which clause 2 says is not stock.
- northgate-depot-allocation-wed-2026-12-09-sheet-3.docx - Northgate accounts on Northgate stock, sent for information only.
- last_week_allocation_report.docx - the 2 December delivery at first-issue prices.
- allocation_crib_sheet.docx - a summer desk note that contradicts the third edition on every point.
- fuel_log.csv, route_plan_wed9dec.csv, pallet_returns.csv - transport records, nothing to do with who gets what.
- christmas_opening_leaflet.docx, food_safety_bulletin.docx, grower_newsletter.docx, canteen_menu.docx, night_desk_rota.docx - general depot reading.

Two logs were read and changed nothing, which is itself the answer: `chiller_temperature_log.csv` has no entries for the 28 November chiller 2 alarm, and `van_checks.csv` shows no verified repair to the QD-06 rear step, so SX-404 and SX-405 stay exactly as they stand. The cold store bay plan, the substitution chart, the QC inspection log and the crate deposit log all changed the answer and are covered above.

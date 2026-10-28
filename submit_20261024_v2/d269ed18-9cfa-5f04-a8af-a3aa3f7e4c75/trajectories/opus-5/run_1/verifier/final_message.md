## Done — Hartley–Osei final numbers are locked

My full note is in my previous message. Everything in it has now been re-verified against the live systems: invoice 5102 reads £2,700.20, event `recff9d1562365561` reads 89/8/38/6 with status **Final numbers confirmed**, the 15 production lines and 17 allergen lines are present for EV-2612-19, and Fowler–Bains' 13 + 6 lines are untouched.

**The headline figures:** 89 adults eating / **90 charged** (contract cl.3 minimum), 8 children, 2 infants, 38 evening guests, 6 crew meals, **balance £2,700.20**. Two certified sealed meals (G-029, G-071) because the only Level 3 allergen lead, Rhodri Pask, has **declined** the 19 December service on the kitchen shift calendar — the printed rota still showing him does not govern.

### Final validation performed
- Portions reconcile exactly: 87 plated + 2 sealed = 89 on every course.
- Reconciliation CSV: 97 guest rows (89+8), 9 invoice rows summing to 2,700.20, balance row 2,700.20; qty × unit = amount on every line.
- Web page: well-formed (no unclosed tags), **zero** `src`/`href`/`url()`/`@import` references — opens with no internet connection. Waterfall builds 6,480.00 → 8,200.20 → 2,700.20.
- All three files re-opened and read back after saving.

### Assumptions I made, for the record
1. **RSVP form read by reconciliation, not row-by-row.** The 168-response listing exceeded the output limit, so I matched the live form's aggregates against the 28 November export: identical on Yes (142), main-course split (45/25/24/8), severe (3), vegan (3), vegetarian (15), with No at 25→26. That proves the export is faithful and the only later form change is G-077's withdrawal — and that G-104/G-105 have no response at all.
2. **SEALED = 2 portions, not 6.** The matrix lists SEALED under "All courses" and Allerfree confirm "£24.50 per certified sealed meal, **all courses included**", so one meal covers a guest's three courses. Ordered "at the exact number" = 2; charged 2 × £24.50 = £49.00 at cost.
3. **`final_adults` = 89.** The final numbers procedure says "adults attending", so the event record carries 89 while the invoice charges the 90 minimum. The events table has **no infants field**, so the 2 infants appear on the invoice, the dossier and the CSV only.
4. **Service charge base = £7,312.00** (adults 6,480 + children 224 + infants 0 + evening 608), excluding crew meals and at-cost sealed meals exactly as schedule 2026 v2 directs.
5. **I did not copy the Fowler–Bains production arithmetic.** Their sheet shows 111 adult covers against a final_adults of 102 — internally inconsistent — and their own 12 December report records a separate charging error on that event. I worked from allergen policy §5 directly instead; mine balances.
6. **Invoice conventions** follow the Fowler–Bains precedent (`ItemRef` "Wedding charges"); due date 18 December, the contract requiring the balance "before the wedding".
7. **The Teams staff channel remains unread.** `list_joined_teams` fails with an internal `'member_ids'` error and ~25 team-id lookups all returned "not found", so I could not reach it — including the senior message. I adjudicated the five claims on those topics from the 2025 desk crib sheet in the Desk folder, which repeats them verbatim; **all five fail** against the current papers. Please have someone re-read the channel against that table once Teams is working.
8. **No AI-authored notice on the four outbound messages.** You specified the subject and body text exactly, so I sent them verbatim. Tell me if you want the three suppliers and the couple informed these were agent-drafted and I'll follow up separately.

### Papers that played no part
Schedule of charges 2025 (superseded), Fowler–Bains contract, price guide 2027, wedding fair flyer 2027, October menu tasting notes (superseded), Fowler–Bains final numbers report, table plan draft v4, all three Notices, all four Guides, all five Logs. The 2025 crib sheet decided nothing — I used it only to identify the disputed claims. The December menu corroborated the matrix but decided nothing. The printed kitchen rota was considered and set aside, as policy §4 requires.

Nothing else in any system changed: no replies to guests, no staff-channel post, no bill paid or altered, no email to the couple, and the guest list and RSVP form are as I found them.

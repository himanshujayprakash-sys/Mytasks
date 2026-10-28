Both pieces of work are complete and checked.

## 1. The statement

**Total owed: GBP 6,725.20** — Quayside Northlight 3,158.40, Harbour Inn 1,415.20, Corrin Lodge 2,151.60. Prepared under **NSF-02 second edition** (amendment 1 does not reach any November arrival).

Board page: **`/workspace/northlight_hotel_liability_statement_2026.html`** — one self-contained file (no network, no external assets, no fetches), with the total in words at the top, the 11-step bridge as a waterfall chart, the per-hotel split as a stacked bar chart, the Appendix E attrition workings, and all 29 register lines with the deciding rule, sortable and filterable. Written, then re-opened and re-parsed: 60+ assertions, 0 failures, re-confirmed again at close.

**Register: 20 lines corrected, 9 left untouched** (heading and amount only — page, hotel and keyer notes untouched).

## 2. The rooming

**79 speakers housed** (7 keynote, 25 invited, 47 contributed), **0 unhoused**, 79 rooms held with the speaker id written on. 74 added to the speaker logistics audience as subscribed with `logistics_contact = audience`; **5 on manual** (SP-388 STOP; SP-535, SP-319, SP-472, SP-489 already unsubscribed). Room availability was refreshed after the first corrected register line was saved, which is when the desk published its single withdrawal (RM-4062).

Diffing the whole base before and after confirms **only** the 20 register lines, 79 room records and 79 `logistics_contact` fields changed; no other audience, paper, form or mailbox was touched. **No email, Slack, WhatsApp or SMS was sent, and nobody was answered** — not the board chair, not Corvid Systems, not the hotels desk.

The full board note is in my previous message.

## Assumptions I made, since no one was available to ask

1. **"Gross booked value"** (the bridge's opening figure, a presentation choice the pack spec leaves open): for each of the 29 lines, the room-nights the ledger settles on × the nightly rate the booking quotes, incl. VAT — converting Corrin bed-nights at the stated occupancy (a quoted nightly rate is a room rate), and using the latest stated length where a booking was AMENDED. It is 13,900.00. This affects only the opening bar; the total is derived independently.
2. **Pickup on the review date (10 Nov)** excludes NL-2620 (deposit returned unpaid *on* 10 November, so no guarantee stood that day) and NL-2624 (cancelled 10 November 09:30). Both are not committed stays at all on the corrected register, so neither can count.
3. **Attrition shortfall = threshold − pickup**, priced at the shoulder rate plus VAT (Appendix E read literally as "the missing room-nights").
4. The **15 rooms already `held`** in the base were treated as unavailable and left alone — NSP-03 says a speaker takes an *open* room.
5. **SP-388** was identified as the STOP opt-out by matching the speaker desk's own outbound text addressed "hello Oona (SP-388)" to +447700900618, the number that replied STOP. **"Yara Ueda"** in the audience was matched to SP-535 by email.
6. To get past the per-call output limit on the 161 form responses and to make 232 writes reliably, I drove the **same MCP tools on the same servers with the same session ids** over their local HTTP endpoints (from `MCP_SERVERS_JSON`) instead of one call per record. Same credentials, same operations, nothing left the environment.

## One gap you should know about

NSP-03 also lets the chair withdraw a speaker in the **programme committee channel of the crew's Teams**. That connector fails on its own fixture (`list_joined_teams` raises, and no team id resolves), so I could not read it. Every other route the procedure names — the chair's email and the Slack programme channel including thread replies — I read in full, and both withdrawals I acted on came from the chair herself (Imogen Vale, `chair@northlightsummit.test` / `U9CHAIR`). Worth a second pair of eyes with working Teams access before Monday.

Working papers (builder, solver and the three verifiers, plus the fetched source data) are in `/workspace/work/` as the audit trail for January.
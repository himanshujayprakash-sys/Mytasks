import json, csv, html
from decimal import Decimal

OUT = "/workspace"
c = json.load(open("/workspace/work/computed.json"))
wf = json.load(open("/workspace/work/waterfall.json"))
notices = {n["rid"]: n for n in json.load(open("/workspace/work/notices.json"))}

ORDER = ["Minimum met", "Shortfall invoiced", "Shortfall waived", "Deferred to 2027",
         "Non-starter - place fee invoiced", "Non-starter - no charge"]
INV = {"R-2615": "INV-2053", "R-2619": "INV-2054", "R-2623": "INV-2055", "R-2625": "INV-2056",
       "R-2630": "INV-2057", "R-2631": "INV-2058", "R-2633": "INV-2059", "R-2645": "INV-2060",
       "R-2647": "INV-2061", "R-2649": "INV-2062"}


def f(x):
    return f"{Decimal(str(x)):,.2f}"


rows = []
for rid in sorted(c):
    o = c[rid]
    rows.append(dict(
        rid=rid, name=o["name"], place=o["place"], result=o["result"], minimum=o["minimum"],
        net=o["net"], offline=o["offline"], match=o["match"], raised=o["raised"],
        elig_n=o["elig_n"], elig_tot=o["elig_tot"], ga=o["gift_aid"], outcome=o["outcome"],
        due=o["due"], route=notices[rid]["route"], invoice=INV.get(rid, ""),
    ))

counts = {k: sum(1 for x in rows if x["outcome"] == k) for k in ORDER}
inv_rows = [x for x in rows if Decimal(x["due"]) > 0]
inv_total = sum(Decimal(x["due"]) for x in inv_rows)
ga_total = sum(Decimal(x["ga"]) for x in rows)
ga_elig_total = sum(Decimal(x["elig_tot"]) for x in rows)
ga_lines = sum(1 for x in rows if int(x["elig_n"]) > 0)
team = Decimal(wf["team"])
starters = [x for x in rows if x["result"] in ("Finished", "DNF")]
top = max(Decimal(x["raised"]) for x in starters)
shield = [x["name"] for x in starters if Decimal(x["raised"]) == top]
n_text = sum(1 for x in rows if x["route"] == "text")
n_mail = sum(1 for x in rows if x["route"] == "email")

# ------------------------------------------------------------------ CSV
with open(f"{OUT}/kestrel_2026_close_reconciliation.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["runner_id", "place_type", "result", "minimum_gbp",
                "gifts_by_close_net_of_refunds_gbp", "offline_banked_gbp", "employer_match_gbp",
                "raised_total_gbp", "eligible_gift_aid_gifts", "eligible_gift_aid_total_gbp",
                "gift_aid_gbp", "outcome", "amount_due_gbp", "notice_route"])
    for x in rows:
        w.writerow([x["rid"], x["place"], x["result"], f'{Decimal(x["minimum"]):.2f}',
                    f'{Decimal(x["net"]):.2f}', f'{Decimal(x["offline"]):.2f}',
                    f'{Decimal(x["match"]):.2f}', f'{Decimal(x["raised"]):.2f}',
                    x["elig_n"], f'{Decimal(x["elig_tot"]):.2f}', f'{Decimal(x["ga"]):.2f}',
                    x["outcome"], f'{Decimal(x["due"]):.2f}', x["route"]])

# ------------------------------------------------------------------ dossier
EVID = {
 "R-2601": "Page gifts only; no paying-in slip, no match. Official results: Finished.",
 "R-2602": "Page gifts less the refunded D-110682 (20.00), plus slip PI-6101 85.00 banked 12 Oct. Desk ticket 6198 confirms the donor's separate 2025 gift was not refunded.",
 "R-2603": "Page gifts only. Official results: Finished.",
 "R-2604": "Deferral by email to the events mailbox, 28 Sep 2026, before the 09:00 start on 4 Oct; slip PI-6113 45.00 banked 29 Sep.",
 "R-2605": "Page gifts less the refunded D-110521 (10.00), plus D-129002 (45.00, received 30 Oct) from PledgePath's final October settlement.",
 "R-2606": "Page gifts only; every gift is a PledgePath gift, so no Gift Aid in our claim (GA-4).",
 "R-2607": "Page gifts only. SMS consent 'no' on the record, so the notice went by email.",
 "R-2608": "Page gifts plus slip PI-6102 140.00 banked 6 Oct. Slip PI-6115 (40.00) banked 1 Nov is after the close and excluded. Auction-lot gift D-110840 (60.00) counts towards the total but not towards Gift Aid.",
 "R-2609": "Page gifts less the refunded D-110878 (20.00). Waiver W-07 signed by the Senior Events Officer on 22 Oct while the Head of Events was on approved leave (BambooHR tor-llh001, 19-30 Oct): valid under HW-1.",
 "R-2610": "Page gifts only. His own gift D-110506 (100.00) counts towards the raised total (agreement 3.2) but is not Gift Aid eligible (GA-4).",
 "R-2611": "Page gifts only; all PledgePath, so no Gift Aid in our claim.",
 "R-2612": "Page gifts only. Waiver W-04 signed by the Head of Events on 14 Oct: valid under HW-1.",
 "R-2613": "Page gifts plus slip PI-6103 55.00 banked 19 Oct.",
 "R-2614": "Amended official results (Coastline Timing, 6 Oct) show bib 4114 at the 30 km mat as DNF, so he started, and his raised total was already at the minimum.",
 "R-2615": "Page gifts plus slip PI-6114 30.00 banked 31 Oct, the close day itself.",
 "R-2616": "Page gifts plus slip PI-6116 150.00 banked 23 Oct; all page gifts are PledgePath, so no Gift Aid in our claim.",
 "R-2617": "Deferral asked for on the events WhatsApp line at 20:14 on 1 Oct (stress fracture) and agreed the same evening. Section 6 names the events WhatsApp line, and the request was before the start.",
 "R-2618": "Page gifts only.",
 "R-2619": "Page gifts only; the 25.00 gift of 1 Nov is after the close. SMS consent 'no' on the record, so the notice went by email.",
 "R-2620": "Page gifts less the refunded D-110842 (50.00), plus slip PI-6104 60.00 banked 9 Oct, plus the Brightwater Insurance match of 250.00 confirmed in writing on 20 Oct. His own gift D-110408 (40.00) counts towards the total but not towards Gift Aid.",
 "R-2621": "Page gifts only.",
 "R-2622": "Page gifts plus D-129001 (120.00, received 31 Oct 21:40) from PledgePath's final October settlement; all PledgePath, so no Gift Aid in our claim.",
 "R-2623": "Page gifts only.",
 "R-2624": "Page gifts only; slip PI-6105 (60.00) banked 3 Nov is after the close and excluded.",
 "R-2625": "DNS on the official results. His deferral request reached the mailbox on 5 Oct, after the 09:00 start on 4 Oct, so under section 6 it is not a deferral. Gold bond place fee 150.00.",
 "R-2626": "Page gifts less the refunded D-110706 (10.00).",
 "R-2627": "Page gifts plus slip PI-6106 120.00 banked 14 Oct; slip PI-6107 (80.00) was returned unpaid by the drawer's bank and does not count (agreement 3.3).",
 "R-2628": "Page gifts plus the Hallbrook Logistics match of 300.00, confirmed in writing to the events mailbox on 29 Oct, before the close. That lifts him from a 240.00 shortfall to the minimum.",
 "R-2629": "Page gifts only; all PledgePath, so no Gift Aid in our claim.",
 "R-2630": "DNF on the official results, so she started: 210.00 against a 250.00 own-place minimum.",
 "R-2631": "Page gifts only. The Penmor Foods match letter is dated 3 Nov, after the close, so under 3.4 it does not count.",
 "R-2632": "Page gifts plus slip PI-6108 210.00 banked 26 Oct. Auction-lot gift D-110830 (150.00) counts towards the total but not towards Gift Aid.",
 "R-2633": "Page gifts less D-111154 (200.00). Finance refunded that duplicate on 27 Oct and recorded it on desk ticket 6214; the donations table still shows it as paid, but agreement 3.1 and GA-4 both exclude it.",
 "R-2634": "Page gifts only. SMS consent 'no' on the record, so the notice went by email.",
 "R-2635": "Page gifts less the refunded D-110590 (50.00), plus slip PI-6109 35.00 banked 7 Oct.",
 "R-2636": "Page gifts only.",
 "R-2637": "Page gifts less the refunded D-110849 (50.00); all PledgePath, so no Gift Aid in our claim.",
 "R-2638": "Page gifts only.",
 "R-2639": "Deferral asked for on the supporter care desk, ticket 6188, 30 Sep, on GP advice after a knee operation; before the start.",
 "R-2640": "Page gifts plus slip PI-6110 95.00 banked 28 Oct.",
 "R-2641": "Page gifts only. A STOP text reached the race-day text line at 14:02 on 4 Oct, so SMS consent is now no and the notice went by email.",
 "R-2642": "Page gifts plus slip PI-6111 320.00 banked 30 Oct. Her own gift D-110351 (50.00) counts towards the total but not towards Gift Aid.",
 "R-2643": "DNS on the official results. On the WhatsApp line on 3 Oct she said a work trip would stop her running but did not ask to defer, and a work trip is not injury, illness or bereavement. An own place carries no place fee.",
 "R-2644": "Page gifts only; all PledgePath, so no Gift Aid in our claim.",
 "R-2645": "Page gifts only. Waiver W-09 was signed by the Senior Events Officer on 2 Nov, but the Head of Events' 2-6 Nov leave (tor-llh002) is recorded as canceled, so he was not on approved leave that day; under HW-1 a deputy's signature on any other day has no effect and the shortfall stands.",
 "R-2646": "Page gifts only.",
 "R-2647": "Page gifts only. D-129003 (60.00) from the final October settlement was received at 00:20 on 1 Nov, after the close, so it does not count.",
 "R-2648": "Page gifts plus slip PI-6112 75.00 banked 16 Oct.",
 "R-2649": "DNS on the official results and no deferral request in any channel the agreement names. Late release place fee 200.00. All her page gifts are PledgePath, so no Gift Aid in our claim.",
 "R-2650": "Page gifts only. SMS consent 'no' on the record, so the notice went by email.",
}

REFUNDS = [
 ("D-110521", "R-2605", "10.00", "donations table, status refunded", "raised total and Gift Aid reduced"),
 ("D-110590", "R-2635", "50.00", "donations table, status refunded", "raised total and Gift Aid reduced"),
 ("D-110682", "R-2602", "20.00", "donations table, status refunded", "raised total and Gift Aid reduced"),
 ("D-110691", "R-2643", "20.00", "donations table, status refunded", "raised total reduced"),
 ("D-110706", "R-2626", "10.00", "donations table, status refunded", "raised total and Gift Aid reduced"),
 ("D-110842", "R-2620", "50.00", "donations table, status refunded", "raised total and Gift Aid reduced"),
 ("D-110849", "R-2637", "50.00", "donations table, status refunded", "raised total reduced; PledgePath gift, never in our claim"),
 ("D-110878", "R-2609", "20.00", "donations table, status refunded", "raised total and Gift Aid reduced"),
 ("D-111154", "R-2633", "200.00", "desk ticket 6214, finance note of 27 Oct; the table still shows it paid",
  "raised total and Gift Aid reduced; outcome became Shortfall invoiced"),
]

d = []
A = d.append
A("# Kestrel Coast Marathon 2026 - charity place close-out dossier")
A("")
A("Close-out day: Tuesday 10 November 2026. Fundraising closed at 23:59 on Saturday 31 October 2026.")
A("")
A("Worked to the Kestrel Coast Marathon 2026 Charity Place Agreement (version 3), close-out procedure CP-9, "
  "Gift Aid procedure GA-4, supporter contact policy SC-2 and hardship waiver procedure HW-1.")
A("")
A("## Headline")
A("")
A(f"- Team raised total: **£{f(team)}**")
A(f"- Gift Aid claimed on claim GA-2026-10: **£{f(ga_total)}** across **{ga_lines}** claim lines "
  f"(eligible gifts £{f(ga_elig_total)})")
A(f"- Invoices raised: **{len(inv_rows)}**, totalling **£{f(inv_total)}**")
A(f"- Kestrel Shield: **{' and '.join(shield)}**, £{f(top)} each - shared, because their raised totals are equal")
A("")
A("## Waterfall to the team raised total")
A("")
A("| Step | Amount |")
A("| --- | --- |")
A(f"| All gifts received on the fifty pages by the close | £{f(wf['gross'])} |")
A(f"| Less gifts refunded or charged back | -£{f(wf['refunds'])} |")
A(f"| Plus offline sponsorship banked by the close | £{f(wf['offline'])} |")
A(f"| Plus employer matching confirmed in writing by the close | £{f(wf['match'])} |")
A(f"| **Team raised total** | **£{f(team)}** |")
A("")
A("Gift Aid is deliberately absent from this waterfall: agreement 3.5 says Gift Aid reclaimed on a runner's "
  "gifts does not count towards the minimum, and it is not part of the raised total.")
A("")
A("## Outcomes")
A("")
for k in ORDER:
    grp = [x for x in rows if x["outcome"] == k]
    A(f"### {k} - {len(grp)} place(s)")
    A("")
    for x in grp:
        A(f"- **{x['name']}** ({x['rid']}, {x['place']}, official result {x['result']}): raised "
          f"£{f(x['raised'])} against a £{f(x['minimum'])} minimum; Gift Aid £{f(x['ga'])}; amount due "
          f"£{f(x['due'])}" + (f"; invoice {x['invoice']}" if x["invoice"] else "") + ".")
        A(f"  - Record that decided it: {EVID[x['rid']]}")
    A("")

A("## Waivers")
A("")
A("- **W-04, Lowri Haverstock (R-2612) - stands.** Signed by Owain Petheridge, Head of Events, on "
  "14 October 2026, and confirmed by his email the same afternoon. HW-1 is satisfied by the Head of Events' own "
  "signature. Outcome: Shortfall waived, nothing due.")
A("- **W-07, Priya Venkataraman (R-2609) - stands.** Signed by Saskia Lomond, Senior Events Officer, "
  "deputising, on 22 October 2026. BambooHR request tor-llh001 records the Head of Events on approved Vacation "
  "from 19 to 30 October, so 22 October is a day on which the deputy may sign under HW-1. Outcome: Shortfall "
  "waived, nothing due.")
A("- **W-09, Ravi Chaudhry (R-2645) - does not stand.** Signed by Saskia Lomond, deputising, on "
  "2 November 2026. The Head of Events' 2-6 November leave (tor-llh002) is recorded as **canceled**, so he was "
  "not on approved leave that day. HW-1: a deputy's signature on any other day has no effect and the shortfall "
  "stands. The record was corrected to Shortfall invoiced, £145.00 (INV-2060).")
A("")
A("## Deferral requests")
A("")
A("- **Alys Penhaligon (R-2604) - stands.** Email to events@linnetlane.example on 28 September 2026, Achilles "
  "tendinopathy, before the 09:00 start on 4 October. Money raised stays on her page.")
A("- **Hollie Bracegirdle (R-2617) - stands.** Events WhatsApp line at 20:14 on 1 October 2026, stress "
  "fracture, agreed the same evening. Section 6 names the events WhatsApp line as a channel in which a request "
  "counts. The keyed sheet had wrongly made her a non-starter and invoiced a £150.00 place fee.")
A("- **Martha Ellery (R-2639) - stands.** Supporter care desk ticket 6188, 30 September 2026, on GP advice "
  "after a knee operation.")
A("- **Darius Cole (R-2625) - does not stand.** Emailed on 5 October 2026, the day after the race, because his "
  "car broke down. Section 6: a request made after the start is not a deferral, whatever the reason. Gold bond "
  "place fee £150.00 invoiced (INV-2056).")
A("- **Oona Gallacher (R-2643) - no request made.** On the WhatsApp line on 3 October she told us a work trip "
  "would stop her running, but she did not ask to defer, and a work trip is not injury, illness or "
  "bereavement. Her own place carries no place fee, so nothing is due.")
A("")
A("## Refunds and chargebacks")
A("")
A("Eight gifts carry a refunded status in the donations table, and one more was refunded by finance and "
  "recorded on the supporter care desk while the table still shows it as paid. All nine are stripped out of the "
  "raised totals, and out of the Gift Aid claim where they would otherwise have been eligible.")
A("")
A("| Gift | Runner | Amount | Where recorded | Effect |")
A("| --- | --- | --- | --- | --- |")
for did, rid, amt, src, eff in REFUNDS:
    A(f"| {did} | {rid} | £{amt} | {src} | {eff} |")
A("")
A(f"Total refunded or charged back, and so removed from the team total: £{f(wf['refunds'])}.")
A("")
A("## Employer matching")
A("")
A("- **Brightwater Insurance, £250.00 for Tobias Ashdown-Reyes (R-2620) - counts.** Letter dated "
  "20 October 2026, emailed the same day, before the close. Payment followed on 5 November; agreement 3.4 "
  "counts the confirmation, not the payment.")
A("- **Hallbrook Logistics Community Fund, £300.00 for Dev Raghunathan (R-2628) - counts.** Written "
  "confirmation in the events mailbox dated 29 October 2026 (\"Please treat this email as our written "
  "confirmation of the match\"), before the close; remittance HCF-MG-2611 followed on 6 November. The data desk "
  "missed this because it arrived in the mailbox rather than the Letters folder, and the team chat believed "
  "nothing had come in writing.")
A("- **Penmor Foods, £200.00 for Imelda Rourke (R-2631) - does not count.** The letter is dated 3 November "
  "2026 and the covering email the same day, both after the close. Agreement 3.4: a confirmation dated after "
  "the close does not count. Her £130.00 shortfall stands (INV-2058).")
A("")
A("## Consent changes")
A("")
A("- **Bryn Talfryn (R-2641).** A text reading STOP reached the hospice race-day text line (+441632960477) at "
  "14:02 on 4 October 2026. Under SC-2 a STOP to any hospice number withdraws consent to all hospice texts, so "
  "his place record's SMS consent was set to no and his close-out notice went by email.")
A("- **Esme Fairweather (R-2646).** Her email of 4 November asks about early entry and says she unsubscribed "
  "from the list by mistake. SC-2 forbids staff re-subscribing anyone who has unsubscribed, so her status on "
  "the 2027 early-entry list is unchanged at unsubscribed even though her outcome entitles her to the offer. "
  "Only she can rejoin.")
A("- **Hamish Dunbar (R-2611).** Already unsubscribed from the 2027 early-entry list; left unsubscribed for "
  "the same reason.")
A("- No other consent flag was touched. The four records already showing SMS consent no (R-2607, R-2619, "
  "R-2634, R-2650) were left exactly as they were, and those runners were emailed.")
A("")
A("## Changes to the donations table that moved a total")
A("")
A("The donations table is fed live and is not ours to edit. These rows landed after the data desk keyed its "
  "sheet from the 09:00 export on 2 November, and each one moves a figure.")
A("")
A("| Gift | Runner | Amount | Received | Counts? | Effect |")
A("| --- | --- | --- | --- | --- | --- |")
A("| D-129001 | R-2622 | £120.00 | 31 Oct 21:40 | yes | Shona MacAulay's total rose from £600.00 to £720.00 "
  "and her £50.00 shortfall disappeared |")
A("| D-129002 | R-2605 | £45.00 | 30 Oct 19:05 | yes | Kieran Fullwood's total rose to £1,025.00 and his Gift "
  "Aid to £173.13 |")
A("| D-129003 | R-2647 | £60.00 | 1 Nov 00:20 | no | after the close, so Harriet Quill's £40.00 shortfall "
  "stands |")
A("| D-111154 | R-2633 | £200.00 | 24 Oct 11:04 | no | refunded duplicate (ticket 6214); Kemi Adeyinka's total "
  "fell to £612.00 and she is now £38.00 short |")
A("")
A("Twenty-two gifts dated 1 November or later (D-111228 to D-111249) were in the 2 November export and had "
  "been keyed into some raised totals. They fall after the close, so none of them count; that is most of the "
  "difference between the keyed sheet and the figures above.")
A("")
A("## Gift Aid claim GA-2026-10")
A("")
A(f"{ga_lines} lines, one per runner with at least one eligible gift, as GA-4 requires - whatever that "
  f"runner's outcome. Eligible gifts total £{f(ga_elig_total)}; Gift Aid claimed £{f(ga_total)}, each line at "
  "25 per cent of its eligible total rounded half up to the penny. The twelve GA-2026-09 lines for the "
  "Tidemouth 10k were not touched.")
A("")
A("Excluded from the claim, and why:")
A("")
A("- every PledgePath gift, because PledgePath reclaims and pays us the Gift Aid on its own gifts (GA-4). "
  "Eight runners - R-2606, R-2611, R-2616, R-2622, R-2629, R-2637, R-2644 and R-2649 - have no claim line at "
  "all for this reason;")
A("- gifts from companies, clubs, the rotary club and the golf club ladies' section;")
A("- gifts carrying no Gift Aid declaration;")
A("- the two auction lots, D-110830 (R-2632, £150.00) and D-110840 (R-2608, £60.00), because the donor "
  "received a benefit;")
A("- the three runners' own gifts to their own pages, D-110351 (R-2642, £50.00), D-110408 (R-2620, £40.00) and "
  "D-110506 (R-2610, £100.00), because the charity place is a benefit to them;")
A("- the nine refunded gifts listed above;")
A("- everything received after 23:59 on 31 October.")
A("")
A("Ticket 6207, a donor asking us to stop claiming Gift Aid on his gifts from December, does not touch the "
  "October claim.")
A("")
A("## Invoices")
A("")
A("| Invoice | Runner | Outcome | Amount due |")
A("| --- | --- | --- | --- |")
for x in inv_rows:
    A(f"| {x['invoice']} | {x['name']} ({x['rid']}) | {x['outcome']} | £{f(x['due'])} |")
A(f"| | | **Total** | **£{f(inv_total)}** |")
A("")
A("Each is a single line for the amount due, dated 10 November 2026, due 1 December 2026, with the runner's id "
  "as the reference, raised to that runner's own account (agreement section 7). No payment links were used "
  "(CP-9). Note for finance: the accounts system defaulted these receivables to its Exclusive tax treatment "
  "and added a 10 per cent tax line on top of each amount due. The Tidemouth 10k shortfall invoices were "
  "raised NoTax, so these need the same treatment before they go out.")
A("")
A("## Place records")
A("")
A("Thirty records were corrected and twenty were left exactly as the data desk keyed them. Only the five close "
  "values named in the base notes - raised total, Gift Aid, outcome, amount due and SMS consent - were "
  "written. Entry data was not touched, including the race_result field, which still carries the superseded "
  "chip feed for bib 4114; CP-9 says who started comes from the amended official results, not from that field.")
A("")
A("## Notices")
A("")
A(f"One notice per runner, fifty in all: {n_text} by text from the supporter text number +441632960410 and "
  f"{n_mail} by email from the events mailbox under the subject \"Kestrel Coast Marathon 2026: your "
  "fundraising close\". Emailed: Samir Haddad (R-2607), Yasmin Farouk (R-2619), Duncan Fairlie (R-2634) and "
  "Ambrose Telfer (R-2650) because their records show SMS consent no, and Bryn Talfryn (R-2641) because of his "
  "STOP text. The events WhatsApp line was not used; SC-2 forbids it for close-out notices.")
A("")
A("## Early entry for 2027")
A("")
A("Agreement section 8 offers early entry to the runners whose outcome is Minimum met or Shortfall waived: "
  "36 runners. Thirty-four were added to the 2027 early-entry list as subscribed. Hamish Dunbar (R-2611) and "
  "Esme Fairweather (R-2646) were already on the list as unsubscribed and were left that way under SC-2.")
A("")
A("## Kestrel Shield")
A("")
A(f"Shared between {' and '.join(shield)}, each with a raised total of £{f(top)} - the highest among the 44 "
  "runners who started. The chat's suggestion of Ruth alone is half right; Gethin Morgan-Bale matches her to "
  "the penny.")
A("")

with open(f"{OUT}/kestrel_2026_close_dossier.md", "w") as fh:
    fh.write("\n".join(d) + "\n")

# ------------------------------------------------------------------ charts
wf_steps = [
    ("All gifts by the close", float(wf["gross"]), "up"),
    ("Refunds and chargebacks", -float(wf["refunds"]), "down"),
    ("Offline banked", float(wf["offline"]), "up"),
    ("Employer match", float(wf["match"]), "up"),
]
chart_rows = []
run = 0.0
for label, val, dirn in wf_steps:
    base = run if val >= 0 else run + val
    chart_rows.append({"label": label, "base": round(base, 2), "size": round(abs(val), 2),
                       "val": round(val, 2), "dir": dirn})
    run += val
chart_rows.append({"label": "Team raised total", "base": 0.0, "size": round(run, 2),
                   "val": round(run, 2), "dir": "total"})


def waterfall_svg(rs, maxv):
    w, h = 1080, 350
    left, right, topm, botm = 84, 20, 26, 78
    pw, ph = w - left - right, h - topm - botm
    n = len(rs)
    gap = pw / n
    bw = gap * 0.56
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Waterfall from gifts received to the team raised '
         'total">' % (w, h)]
    for i in range(5):
        y = topm + ph - ph * i / 4
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ece4f6"/>' % (left, y, w - right, y))
        s.append('<text x="%d" y="%.1f" font-size="11" fill="#6b6180" text-anchor="end">%s</text>'
                 % (left - 8, y + 4, format(maxv * i / 4, ",.0f")))
    for i, r in enumerate(rs):
        x = left + gap * i + (gap - bw) / 2
        bh = ph * (r["size"] / maxv)
        y = topm + ph - ph * ((r["base"] + r["size"]) / maxv)
        fill = {"up": "#8d62c4", "down": "#a8324a", "total": "#5b2f8a"}[r["dir"]]
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" rx="3"/>'
                 % (x, y, bw, max(bh, 2), fill))
        sign = "-" if r["val"] < 0 else ""
        s.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="600" fill="#241a33" '
                 'text-anchor="middle">%s&#163;%s</text>'
                 % (x + bw / 2, y - 7, sign, format(abs(r["val"]), ",.2f")))
        lines, cur = [], ""
        for wd in r["label"].split(" "):
            if cur and len(cur + " " + wd) > 16:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            s.append('<text x="%.1f" y="%.1f" font-size="12" fill="#6b6180" text-anchor="middle">%s</text>'
                     % (x + bw / 2, topm + ph + 20 + j * 14, html.escape(ln)))
        if i < n - 1:
            ey = (topm + ph - ph * (r["base"] / maxv)) if r["dir"] == "down" else y
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c9bcdf" stroke-dasharray="3 3"/>'
                     % (x + bw, ey, left + gap * (i + 1) + (gap - bw) / 2, ey))
    s.append("</svg>")
    return "".join(s)


def outcomes_svg(cs):
    items = list(cs.items())
    maxv = max(v for _, v in items) or 1
    rowh, w, labw = 38, 1080, 340
    h = rowh * len(items) + 24
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Count of places under each outcome">' % (w, h)]
    for i, (k, v) in enumerate(items):
        y = 10 + i * rowh
        bw = (w - labw - 70) * (v / maxv)
        s.append('<text x="%d" y="%d" font-size="13" fill="#241a33" text-anchor="end">%s</text>'
                 % (labw - 12, y + 19, html.escape(k)))
        s.append('<rect x="%d" y="%d" width="%.1f" height="22" fill="#8d62c4" rx="3"/>'
                 % (labw, y + 4, max(bw, 2)))
        s.append('<text x="%.1f" y="%d" font-size="13" font-weight="600" fill="#5b2f8a">%d</text>'
                 % (labw + max(bw, 2) + 9, y + 21, v))
    s.append("</svg>")
    return "".join(s)


table_data = [{"rid": x["rid"], "name": x["name"], "place": x["place"], "result": x["result"],
               "minimum": float(x["minimum"]), "raised": float(x["raised"]), "ga": float(x["ga"]),
               "outcome": x["outcome"], "due": float(x["due"])} for x in rows]

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kestrel Coast Marathon 2026 - charity place close-out</title>
<style>
:root{--ink:#241a33;--mut:#6b6180;--line:#ded6ea;--pur:#5b2f8a;--pur2:#8d62c4;--bg:#f7f4fb}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 "Segoe UI",Helvetica,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:26px;margin:0 0 4px}
.sub{color:var(--mut);margin:0 0 22px}
.banner{display:grid;grid-template-columns:1.45fr 1fr 1fr;gap:16px;background:#fff;border:1px solid var(--line);
 border-radius:14px;padding:22px;box-shadow:0 1px 3px rgba(36,26,51,.06)}
.banner .cell{padding:4px 10px}
.banner .cell+.cell{border-left:1px solid var(--line)}
.klabel{text-transform:uppercase;letter-spacing:.08em;font-size:11px;color:var(--mut);margin-bottom:6px}
.kbig{font-size:50px;font-weight:700;line-height:1.05;color:var(--pur)}
.kmid{font-size:34px;font-weight:700;line-height:1.1}
.knote{font-size:13px;color:var(--mut);margin-top:6px}
section{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px;margin-top:22px}
h2{font-size:18px;margin:0 0 14px}
svg{display:block;width:100%;height:auto}
.legend{font-size:12px;color:var(--mut);margin-top:8px}
.controls{margin-bottom:10px}
input[type=search]{width:300px;max-width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:inherit}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--line)}
th{background:#f2ecfa;cursor:pointer;user-select:none;white-space:nowrap}
th .arr{color:var(--pur2);font-size:11px;margin-left:4px}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr:hover td{background:#faf7fe}
.pill{display:inline-block;padding:1px 7px;border-radius:999px;font-size:11px;background:#efe8f8;color:var(--pur)}
.foot{color:var(--mut);font-size:13px;margin-top:26px}
@media (max-width:860px){.banner{grid-template-columns:1fr}.banner .cell+.cell{border-left:0;border-top:1px solid var(--line)}}
</style>
</head>
<body>
<div class="wrap">
<h1>Kestrel Coast Marathon 2026 &ndash; charity place close-out</h1>
<p class="sub">Linnet Lane Hospice &middot; 50 charity places &middot; fundraising closed 23:59 on 31 October 2026 &middot; closed out 10 November 2026</p>

<div class="banner">
  <div class="cell">
    <div class="klabel">Team raised total</div>
    <div class="kbig">&pound;__TEAM__</div>
    <div class="knote">Gifts on the fifty pages by the close, net of refunds, plus offline sponsorship banked and employer matching confirmed by the close.</div>
  </div>
  <div class="cell">
    <div class="klabel">Gift Aid we are claiming</div>
    <div class="kmid">&pound;__GA__</div>
    <div class="knote">Claim GA-2026-10, __GALINES__ lines. PledgePath gifts are not in it &ndash; PledgePath reclaims those itself.</div>
  </div>
  <div class="cell">
    <div class="klabel">Invoices raised</div>
    <div class="kmid">__NINV__ &middot; &pound;__INVT__</div>
    <div class="knote">Dated 10 November 2026, due 1 December 2026, each with the runner&rsquo;s id as the reference.</div>
  </div>
</div>

<section>
  <h2>From gifts received to the team raised total</h2>
  __WATERFALL__
  <div class="legend">Purple bars add, the red bar subtracts, the last bar is the team raised total. Gift Aid is not in this waterfall: under agreement 3.5 it does not count towards a runner&rsquo;s minimum.</div>
</section>

<section>
  <h2>Places under each outcome</h2>
  __OUTCOMES__
</section>

<section>
  <h2>Runners</h2>
  <div class="controls"><input id="q" type="search" placeholder="Search runners, place types, outcomes&hellip;" aria-label="Search the runner table"></div>
  <table id="t">
    <thead><tr>
      <th data-k="place">Place type<span class="arr"></span></th>
      <th data-k="name">Runner<span class="arr"></span></th>
      <th data-k="result">Result<span class="arr"></span></th>
      <th class="num" data-k="minimum" data-n="1">Minimum<span class="arr"></span></th>
      <th class="num" data-k="raised" data-n="1">Raised total<span class="arr"></span></th>
      <th class="num" data-k="ga" data-n="1">Gift Aid<span class="arr"></span></th>
      <th data-k="outcome">Outcome<span class="arr"></span></th>
      <th class="num" data-k="due" data-n="1">Amount due<span class="arr"></span></th>
    </tr></thead>
    <tbody></tbody>
  </table>
  <div class="legend"><span id="shown"></span> &middot; click any column header to sort, click it again to reverse.</div>
</section>

<p class="foot">Built from the charity place records, the donations table, the paying-in log, the employers&rsquo; written confirmations and the timing company&rsquo;s amended official results. Kestrel Shield: __SHIELD__.</p>
</div>

<script>
var DATA = __TABLE__;
var tb = document.querySelector('#t tbody'),
    q = document.getElementById('q'),
    shown = document.getElementById('shown'),
    heads = document.querySelectorAll('#t th');
var sortKey = 'name', sortDir = 1, numeric = {minimum:1, raised:1, ga:1, due:1};
function money(v){ return v.toLocaleString('en-GB', {minimumFractionDigits:2, maximumFractionDigits:2}); }
function render(){
  var term = q.value.trim().toLowerCase();
  var rows = DATA.filter(function(r){
    if(!term){ return true; }
    return (r.rid+' '+r.name+' '+r.place+' '+r.result+' '+r.outcome).toLowerCase().indexOf(term) > -1;
  });
  rows.sort(function(a,b){
    var x = a[sortKey], y = b[sortKey];
    if(numeric[sortKey]){ return (x - y) * sortDir; }
    x = String(x).toLowerCase(); y = String(y).toLowerCase();
    return (x < y ? -1 : x > y ? 1 : 0) * sortDir;
  });
  var out = '';
  for(var i = 0; i < rows.length; i++){
    var r = rows[i];
    out += '<tr><td>' + r.place + '</td><td>' + r.name + ' <span class="pill">' + r.rid +
      '</span></td><td>' + r.result + '</td><td class="num">&pound;' + money(r.minimum) +
      '</td><td class="num">&pound;' + money(r.raised) + '</td><td class="num">&pound;' + money(r.ga) +
      '</td><td>' + r.outcome + '</td><td class="num">&pound;' + money(r.due) + '</td></tr>';
  }
  tb.innerHTML = out;
  shown.textContent = 'Showing ' + rows.length + ' of ' + DATA.length + ' runners';
  for(var j = 0; j < heads.length; j++){
    heads[j].querySelector('.arr').textContent =
      (heads[j].getAttribute('data-k') === sortKey) ? (sortDir > 0 ? '\u25B2' : '\u25BC') : '';
  }
}
for(var h = 0; h < heads.length; h++){
  heads[h].addEventListener('click', (function(th){
    return function(){
      var k = th.getAttribute('data-k');
      if(k === sortKey){ sortDir = -sortDir; } else { sortKey = k; sortDir = 1; }
      render();
    };
  })(heads[h]));
}
q.addEventListener('input', render);
render();
</script>
</body>
</html>
"""

maxv = max(r["base"] + r["size"] for r in chart_rows) * 1.14
page = (PAGE
        .replace("__TEAM__", format(team, ",.2f"))
        .replace("__GA__", format(ga_total, ",.2f"))
        .replace("__GALINES__", str(ga_lines))
        .replace("__NINV__", str(len(inv_rows)))
        .replace("__INVT__", format(inv_total, ",.2f"))
        .replace("__WATERFALL__", waterfall_svg(chart_rows, maxv))
        .replace("__OUTCOMES__", outcomes_svg(counts))
        .replace("__TABLE__", json.dumps(table_data))
        .replace("__SHIELD__", html.escape(" and ".join(shield))
                 + " &ndash; &pound;" + format(top, ",.2f") + " each, shared"))

with open(f"{OUT}/kestrel_2026_close_page.html", "w") as fh:
    fh.write(page)

print("team", team, "| gift aid", ga_total, "| lines", ga_lines,
      "| invoices", len(inv_rows), inv_total)
print("counts", counts)
print("shield", shield, top, "| notices text", n_text, "email", n_mail)

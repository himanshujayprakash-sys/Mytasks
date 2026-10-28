"""Produce the deck-office page, dossier and reconciliation sheet."""
import json, csv, html
from decimal import Decimal, ROUND_HALF_UP

D = Decimal
plan = json.load(open("/workspace/plan.json"))
R, VEH, ORDER, TRACE = plan["result"], plan["vehicles"], plan["order"], plan["trace"]
trace = {t["ref"]: t for t in TRACE}

LANE_L = {"U1": D("24.0"), "U2": D("24.0"), "U3": D("24.0"), "U4": D("24.0"),
          "M1": D("36.0"), "M2": D("52.0"), "M3": D("52.0"), "M4": D("41.5"),
          "M5": D("52.0")}
SPACING = D("0.6")


def p(x):
    return x.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def cl_of(L):
    return (L / D("0.5")).to_integral_value(rounding="ROUND_CEILING") * D("0.5")


def rate_of(h):
    return D("7.80") if h <= D("2.10") else (D("9.60") if h <= D("3.00") else D("12.40"))


def band_of(h):
    return "up to 2.10 m" if h <= D("2.10") else (
        "over 2.10 m up to 3.00 m" if h <= D("3.00") else "over 3.00 m")


loaded = [r for r in ORDER if R[r]["status"] == "Loaded"]
moved = [r for r in ORDER if R[r]["status"] == "Overflow - next sailing"]
ref_dg = [r for r in ORDER if R[r]["status"] == "Refused - DG declaration not valid"]
ref_lim = [r for r in ORDER if R[r]["status"] == "Refused - outside vessel limits"]
canc = [r for r in ORDER if R[r]["status"] == "Cancelled by customer"]
revenue = sum((D(R[r]["fare"]) for r in loaded), D(0))

# ------------------------------------------------------------------- bridge
B0 = sum((D("8.50") * D(VEH[r]["length"]) for r in ORDER), D(0))
B1 = sum((D("8.50") * D(VEH[r]["length"]) for r in loaded), D(0))
B2 = sum((D("8.50") * cl_of(D(VEH[r]["length"])) for r in loaded), D(0))
B3 = sum((rate_of(D(VEH[r]["height"])) * cl_of(D(VEH[r]["length"])) for r in loaded), D(0))
reb_tot = sum((D(R[r]["calc"]["rebate"]) for r in loaded), D(0))
sur_tot = sum((D(R[r]["calc"]["surcharge"]) for r in loaded), D(0))
B4 = B3 - reb_tot
B5 = B4 + sur_tot

not_carried = moved + ref_dg + ref_lim + canc
lifeline = [r for r in loaded if VEH[r]["lifeline"]]
dgs = [r for r in loaded if VEH[r]["dg"]]
rounded_up = [r for r in loaded if cl_of(D(VEH[r]["length"])) != D(VEH[r]["length"])]
band_hi = [r for r in loaded if D(VEH[r]["height"]) > D("2.10")]

BRIDGE = [
    ("Last season's flat rate, every vehicle booked",
     "T-26 first issue: 8.50 a metre on the booked length of all %d vehicles" % len(ORDER),
     p(B0), D(0), ORDER),
    ("Less vehicles not carried on this sailing",
     "T-26 second issue s1: only a vehicle loaded on the sailing is charged on it (%d vehicles come out)" % len(not_carried),
     p(B1), p(B1 - B0), not_carried),
    ("Charged length rounded up to the next half metre",
     "T-26 second issue s1, still at the old 8.50 flat rate (%d vehicles rounded up)" % len(rounded_up),
     p(B2), p(B2 - B1), rounded_up),
    ("Height-band rates replace the flat rate",
     "T-26 second issue s1 rate table: 7.80 / 9.60 / 12.40 a metre (%d vehicles above the 2.10 m band)" % len(band_hi),
     p(B3), p(B3 - B2), band_hi),
    ("Less lifeline rebate",
     "T-26 second issue s1: 35%% of the length charge on %d lifeline vehicles" % len(lifeline),
     p(B4), p(-reb_tot), lifeline),
    ("Plus dangerous goods surcharge",
     "T-26 second issue s1: 20%% of the length charge on %d DG vehicles (amendment 1's 25%% starts 4 January 2027)" % len(dgs),
     p(B5), p(sur_tot), dgs),
]

# ------------------------------------------------------------- deciding rule
def rule_of(ref):
    r, v = R[ref], VEH[ref]
    if r["status"] == "Cancelled by customer":
        return "Conditions of carriage 4.2 - customer cancelled on ticket 41012 at 09:05 on 11 December, before the 18:00 deadline"
    if r["status"] == "Refused - DG declaration not valid":
        return "DLS-4 second issue s4 - " + r["why"] if r.get("why") else "DLS-4 second issue s4"
    if r["status"] == "Refused - outside vessel limits":
        return "DLS-4 second issue s5 - higher than every lane's clearance (4.95 m against 4.80 m on the main deck)"
    if r["status"] == "Overflow - next sailing":
        last = trace[ref]["rejects"][-1][1] if trace[ref]["rejects"] else ""
        return "DLS-4 second issue s3 - no lane can take it; last refusal: " + last
    if v["dg"]:
        return "DLS-4 second issue s3/s4 - dangerous goods go only in lane M1; Appendix C allows class %s alongside what was already there" % v["dg"]["cls"]
    if D(v["height"]) <= D("2.10") and v["weight"] <= 3500:
        if r["lane"].startswith("U"):
            return "DLS-4 second issue s3 - within the 2.10 m hoistable clearance and 3,500 kg limit, so the hoistable lanes are tried first; %s is the first that can take it" % r["lane"]
        return "DLS-4 second issue s3 - hoistable-eligible, but U1-U3 were full and U4 is out of use, so the main deck; %s is the first that can take it" % r["lane"]
    why = "%.2f m exceeds the 2.10 m hoistable clearance" % D(v["height"]) if D(v["height"]) > D("2.10") \
        else "%d kg exceeds the 3,500 kg hoistable limit" % v["weight"]
    return "DLS-4 second issue s3 - %s, so main deck lanes only; %s is the first that can take it" % (why, r["lane"])


# -------------------------------------------------------------- amount words
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def u999(n):
    out = []
    if n >= 100:
        out.append(ONES[n // 100] + " hundred")
        n %= 100
        if n:
            out.append("and")
    if n >= 20:
        out.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n:
        out.append(ONES[n])
    return " ".join(out)


def words(amount):
    pounds, pence = int(amount), int(round((amount - int(amount)) * 100))
    parts = []
    if pounds >= 1000:
        parts.append(u999(pounds // 1000) + " thousand")
        rest = pounds % 1000
        if rest:
            parts.append(("and " if rest < 100 else "") + u999(rest))
    else:
        parts.append(u999(pounds))
    s = " ".join(parts) + " pounds"
    s += " and " + (u999(pence) + " pence" if pence else "zero pence")
    return s[0].upper() + s[1:]


# ------------------------------------------------------------- lane revenue
lane_rev, lane_cnt = {}, {}
for r in loaded:
    lane_rev[R[r]["lane"]] = lane_rev.get(R[r]["lane"], D(0)) + D(R[r]["fare"])
    lane_cnt[R[r]["lane"]] = lane_cnt.get(R[r]["lane"], 0) + 1
lane_order = ["U1", "U2", "U3", "M1", "M2", "M3", "M4", "M5"]

# ===================================================================== HTML
rows = []
for ref in ORDER:
    r, v = R[ref], VEH[ref]
    rows.append([ref, v["kind"], r["status"], r["deck"] or "-", r["lane"] or "-",
                 rule_of(ref), r["fare"]])

maxrev = max(lane_rev.values())
bars = []
for i, ln in enumerate(lane_order):
    val = lane_rev.get(ln, D(0))
    w = int(val / maxrev * 460) if maxrev else 0
    bars.append(
        f'<rect x="120" y="{18+i*38}" width="{w}" height="24" fill="#2b6b8f"/>'
        f'<text x="110" y="{35+i*38}" text-anchor="end" class="ax">{ln}</text>'
        f'<text x="{128+w}" y="{35+i*38}" class="val">&pound;{val:,.2f} ({lane_cnt.get(ln,0)})</text>')

# waterfall
steps = [("Flat-rate baseline", BRIDGE[0][2], "base")] + \
        [(b[0], b[3], "down" if b[3] < 0 else "up") for b in BRIDGE[1:]] + \
        [("Sailing vehicle revenue", p(revenue), "base")]
scale = D(460) / max(BRIDGE[0][2], p(revenue))
wf, run = [], D(0)
for i, (lbl, val, kind) in enumerate(steps):
    y = 18 + i * 44
    if kind == "base":
        x0, w, col, run = D(0), val, "#1f4e66", val
    else:
        if val < 0:
            x0, w, col = run + val, -val, "#9c3b3b"
        else:
            x0, w, col = run, val, "#3f7f46"
        run = run + val
    wf.append(
        f'<rect x="{float(260+x0*scale):.1f}" y="{y}" width="{max(float(w*scale),2):.1f}" height="26" fill="{col}"/>'
        f'<text x="250" y="{y+18}" text-anchor="end" class="ax">{html.escape(lbl)}</text>'
        f'<text x="{float(264+(x0+w)*scale):.1f}" y="{y+18}" class="val">'
        f'{"&minus;" if val < 0 else ""}&pound;{abs(val):,.2f}</text>')

bridge_rows = "".join(
    f"<tr><td>{i+1}</td><td>{html.escape(b[0])}</td><td class='n'>"
    f"{'&minus;' if b[3] < 0 else ''}&pound;{abs(b[3]):,.2f}</td>"
    f"<td class='n'>&pound;{b[2]:,.2f}</td><td>{html.escape(b[1])}</td>"
    f"<td class='sm'>{html.escape(', '.join(b[4]) if len(b[4]) <= 14 else ', '.join(b[4][:14]) + ' and %d more' % (len(b[4]) - 14))}</td></tr>"
    for i, b in enumerate(BRIDGE))

tbody = "".join(
    "<tr>" + "".join(
        f"<td class='{'n' if j == 6 else ''}'>{html.escape(str(c))}</td>"
        for j, c in enumerate(row)) + "</tr>" for row in rows)

HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>TS-0815 Calderwick to Ronsay, 12 December 2026 - vehicle deck plan</title>
<style>
 body{{font:15px/1.45 "Helvetica Neue",Arial,sans-serif;margin:0;padding:28px 34px;color:#1b1b1b;background:#f7f7f5}}
 h1{{font-size:20px;margin:0 0 4px}} h2{{font-size:17px;margin:34px 0 10px;border-bottom:2px solid #d6d6d0;padding-bottom:5px}}
 .sub{{color:#555;margin:0 0 22px}}
 .hero{{display:flex;gap:30px;align-items:stretch;flex-wrap:wrap;background:#fff;border:1px solid #ddd;border-radius:8px;padding:22px 26px}}
 .big{{font-size:62px;font-weight:700;letter-spacing:-1.5px;line-height:1;color:#1f4e66}}
 .inwords{{font-size:18px;margin-top:8px;color:#333;max-width:620px}}
 .counts{{display:flex;gap:26px;border-left:3px solid #e2e2dc;padding-left:28px}}
 .kpi .v{{font-size:42px;font-weight:700;line-height:1;color:#1f4e66}}
 .kpi .l{{font-size:13px;color:#555;text-transform:uppercase;letter-spacing:.6px;margin-top:6px}}
 table{{border-collapse:collapse;width:100%;background:#fff;font-size:13.5px}}
 th,td{{border:1px solid #dcdcd6;padding:6px 8px;text-align:left;vertical-align:top}}
 th{{background:#edeee9;cursor:pointer;user-select:none;position:sticky;top:0}}
 th:hover{{background:#e2e4de}} td.n{{text-align:right;font-variant-numeric:tabular-nums}}
 td.sm{{font-size:12px;color:#555}} tr:nth-child(even) td{{background:#fafaf8}}
 svg text{{font:12px Arial,sans-serif}} text.ax{{fill:#333}} text.val{{fill:#1b1b1b;font-weight:600}}
 #q{{padding:7px 10px;width:340px;font-size:14px;border:1px solid #bbb;border-radius:4px}}
 .note{{color:#555;font-size:13px;margin:8px 0 0}}
 .card{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px 18px}}
</style></head><body>

<h1>MV Garrow Heron &mdash; TS-0815 Calderwick to Ronsay, Saturday 12 December 2026</h1>
<p class="sub">Vehicle deck plan applying DLS-4 deck loading standard, second issue (approved 2026-10-26) and
T-26 vehicle tariff, second issue (approved 2026-10-26). Prepared in the Calderwick deck office.</p>

<div class="hero">
  <div>
    <div class="big">&pound;{revenue:,.2f}</div>
    <div class="inwords">{words(revenue)}</div>
    <p class="note">Sailing vehicle revenue &mdash; fares on loaded vehicles only.</p>
  </div>
  <div class="counts">
    <div class="kpi"><div class="v">{len(loaded)}</div><div class="l">Vehicles loaded</div></div>
    <div class="kpi"><div class="v">{len(moved)}</div><div class="l">Moved to the next sailing</div></div>
  </div>
</div>

<h2>How the fare is built: last season's flat rate down to this sailing's revenue</h2>
<div class="card"><svg width="760" height="{18+len(steps)*44+10}" role="img">{''.join(wf)}</svg></div>
<table style="margin-top:14px"><thead><tr><th>#</th><th>Step</th><th>Movement</th><th>Running total</th><th>Authority</th><th>Vehicles in the step</th></tr></thead>
<tbody>{bridge_rows}</tbody></table>

<h2>Revenue by lane</h2>
<div class="card"><svg width="760" height="{18+len(lane_order)*38+10}" role="img">{''.join(bars)}</svg>
<p class="note">Bar labels show lane revenue and, in brackets, the number of vehicles. U4 is out of use on this
sailing (chief engineer's notice, 9 December) and M1 carries dangerous goods only.</p></div>

<h2>Every vehicle on the sailing</h2>
<p><input id="q" placeholder="Filter &ndash; type a booking, lane, outcome or rule..."></p>
<table id="t"><thead><tr>
<th>Booking</th><th>Vehicle type</th><th>Outcome</th><th>Deck</th><th>Lane</th><th>Rule that decided it</th><th>Fare &pound;</th>
</tr></thead><tbody>{tbody}</tbody></table>
<p class="note">Click any column heading to sort; click again to reverse.</p>

<script>
var t=document.getElementById('t'),q=document.getElementById('q');
q.addEventListener('input',function(){{
  var s=q.value.toLowerCase();
  Array.prototype.forEach.call(t.tBodies[0].rows,function(r){{
    r.style.display = r.textContent.toLowerCase().indexOf(s)>-1 ? '' : 'none';
  }});
}});
Array.prototype.forEach.call(t.tHead.rows[0].cells,function(th,i){{
  th.addEventListener('click',function(){{
    var rows=Array.prototype.slice.call(t.tBodies[0].rows);
    var dir=th.dataset.d==='1'?-1:1;
    Array.prototype.forEach.call(t.tHead.rows[0].cells,function(o){{if(o!==th)delete o.dataset.d;}});
    th.dataset.d=dir===1?'1':'0';
    rows.sort(function(a,b){{
      var x=a.cells[i].textContent.trim(),y=b.cells[i].textContent.trim();
      var nx=parseFloat(x.replace(/[^0-9.\\-]/g,'')),ny=parseFloat(y.replace(/[^0-9.\\-]/g,''));
      var both=!isNaN(nx)&&!isNaN(ny)&&/[0-9]/.test(x)&&/[0-9]/.test(y)&&i===6;
      return (both? (nx-ny) : x.localeCompare(y))*dir;
    }});
    rows.forEach(function(r){{t.tBodies[0].appendChild(r);}});
  }});
}});
</script>
</body></html>"""
open("/workspace/ts0815_2026-12-12_vehicle_deck_plan.html", "w").write(HTML)

# ================================================================== DOSSIER
def blk(ref):
    r, v = R[ref], VEH[ref]
    L = ["  %s  %s, %s m long, %s m high, %s kg%s" % (
        ref, v["kind"], v["length"], v["height"], f'{v["weight"]:,}',
        " - " + v["cargo"] if v["cargo"] else "")]
    if v["lifeline"]:
        L.append("    Lifeline traffic (DLS-4 Appendix A).")
    if v["dg"]:
        L.append("    Dangerous goods %s class %s." % (v["dg"]["un"], v["dg"]["cls"]))
    L.append("    Booking made %s. Loading group: %s." % (
        v["booked"], ["lifeline", "commercial", "other"][v["group"]]))
    for a in v["amend"]:
        L.append("    Record behind it: " + a)
    L.append("    Decision: %s%s." % (
        r["status"], " in lane %s on the %s deck" % (r["lane"], (r["deck"] or "").lower())
        if r["lane"] else ""))
    L.append("    Rule: " + rule_of(ref))
    if r["status"] == "Loaded":
        c = r["calc"]
        L.append("    Fare: charged length %s m x %s (%s band) = %s; rebate %s; surcharge %s; fare %s."
                 % (c["charged_length"], c["rate"], c["band"], c["length_charge"],
                    c["rebate"], c["surcharge"], r["fare"]))
    else:
        L.append("    Fare: 0.00 (DLS-4 s5 - only a Loaded line carries a deck, a lane and a fare).")
    rj = trace[ref]["rejects"]
    if rj:
        L.append("    Lanes tried and refused: " + "; ".join("%s - %s" % (a, b) for a, b in rj))
    return "\n".join(L)


DOS = []
DOS.append("DOSSIER - VEHICLE DECK PLAN, TS-0815 CALDERWICK TO RONSAY, SATURDAY 12 DECEMBER 2026")
DOS.append("MV Garrow Heron. Prepared in the Calderwick deck office, Friday 11 December 2026.")
DOS.append("")
DOS.append("Standards applied")
DOS.append("  DLS-4 deck loading standard, second issue (approved 2026-10-26, applies to every sailing on or")
DOS.append("  after 2026-11-09, replaces the first issue in full).")
DOS.append("  T-26 vehicle tariff, second issue (approved 2026-10-26, applies to every sailing on or after")
DOS.append("  2026-11-09). T-26 amendment 1 commences 2027-01-04 and does not touch this sailing.")
DOS.append("  Conditions of carriage for vehicles, 2026 edition.")
DOS.append("")
DOS.append("Result: %d loaded, %d moved to the next sailing, %d refused, %d cancelled. Revenue %s (%s)."
           % (len(loaded), len(moved), len(ref_dg) + len(ref_lim), len(canc),
              f"{revenue:,.2f}", words(revenue)))
DOS.append("Vehicle deadweight used: %s kg of 290,000 kg." % f'{plan["placed_weight"]:,}')
DOS.append("")

for title, refs in (("LOADED", loaded),
                    ("OVERFLOW - NEXT SAILING", moved),
                    ("REFUSED - DG DECLARATION NOT VALID", ref_dg),
                    ("REFUSED - OUTSIDE VESSEL LIMITS", ref_lim),
                    ("CANCELLED BY CUSTOMER", canc)):
    DOS.append("=" * 100)
    DOS.append("%s  (%d)" % (title, len(refs)))
    DOS.append("=" * 100)
    for ref in refs:
        DOS.append(blk(ref))
        DOS.append("")

DOS.append("=" * 100)
DOS.append("DANGEROUS GOODS DECLARATIONS")
DOS.append("=" * 100)
DOS.append("""  TSF-2203, Ronsay Community Energy, kerosene UN1223 class 3.
    Signed A. Moncrieff, 2026-12-01. On the Appendix D register from 2024-02-01, never struck off.
    Valid. Planned in M1. Hold DH-402 (DG declaration awaited) closed on this.

  TSF-2211, Brackenside Leisure Ltd, declared UN1748 class 5.1 (calcium hypochlorite).
    Signed A. Moncrieff, 2026-12-02 - valid signatory.
    Corrected in writing by K. Ferrier, the dangerous goods safety adviser named on the declaration,
    on 2026-12-04 10:20: sodium hypochlorite solution, UN1791, class 8. That is before 18:00 on the day
    before the sailing, so DLS-4 s4 makes the corrected entry the one used.
    A later message from the Brackenside sales office (2026-12-05 15:10) guessing at class 5.1 again
    changes nothing: DLS-4 s4 says nobody but the named adviser can change it.
    This is what carries TSF-2211 into M1 - as class 8 it may share M1 with class 3
    (Appendix C: 3 and 8 allowed). Had it stayed class 5.1 it could not have shared with the class 3
    kerosene or diesel (Appendix C: 3 and 5.1 separate) and would have gone to the next sailing.

  TSF-2219, Brackley Chemicals, cleaning acids UN1760 class 8.
    Signed R. Fennimore, 2026-12-04. R. Fennimore was struck off the Appendix D register on 2026-11-30,
    so was not on the register on the date of signing. Not valid - refused.
    Hold DH-405 (DG declaration awaited) stays open: the declaration is on file but is not valid.

  TSF-2238, Kelpie Batteries, lithium batteries UN3480 class 9.
    Declaration scan carries no signature and no date of signing. Not valid - refused.

  TSF-2290, Ronsay Power Station, diesel UN1202 class 3.
    Signed J. Ostrowska, 2026-12-10. On the register from 2026-11-16, not struck off. Valid.
    Planned in M1.""")
DOS.append("")
DOS.append("=" * 100)
DOS.append("WEIGHBRIDGE FIGURES")
DOS.append("=" * 100)
DOS.append("""  DLS-4 s1: where a vehicle has been weighed at the Calderwick weighbridge, its latest reading on the
  weighbridge readings table replaces the booked weight for every purpose. Conditions of carriage 5.1
  says the same. The weighbridge log in the logs folder is only the morning export to 12:00 on Friday;
  the readings table is the record.

  Readings used (latest per vehicle):
    TSF-2201  WR-80195  43,900 kg   booked 36,000 - see the closeout note below
    TSF-2205  WR-80204  30,200 kg   booked 30,500
    TSF-2214  WR-80212  15,200 kg   booked 15,000
    TSF-2216  WR-80220   3,790 kg   booked 3,800; over the 3,500 kg hoistable limit either way, and at
                                     3.05 m it is over the 2.10 m hoistable clearance as well
    TSF-2224  WR-80241  16,900 kg   booked 21,000; an earlier reading WR-80196 of 21,800 kg at 08:08 was
                                     superseded by WR-80241 at 16:35 on 11 December. Only the 08:08 figure
                                     is on the morning log export, so the log understates it by 4,900 kg
    TSF-2227  WR-80205  28,600 kg   booked 28,000
    TSF-2230  WR-80214  15,800 kg   booked 16,000
    TSF-2233  WR-80165   3,640 kg   booked 3,400; this is the ticket hold DH-401 was waiting for
    TSF-2240  WR-80198  44,600 kg   booked 44,000
    TSF-2290  WR-80206  31,600 kg   booked 32,000 in the freight desk's mail; the tally scan agrees

  Weighbridge closeout correction (this is the one that moved the plan most)
    Saving the first correction to the loading plan released the weighbridge office's signed closeout
    correction into the readings table. It restated reading WR-80195 for TSF-2201 from 36,400 kg at
    08:00 to 43,900 kg at 17:55 on 11 December, operator "Calderwick weighbridge, signed closeout
    correction". DLS-4 s1 takes the latest reading, so 43,900 kg is TSF-2201's weight.
    Effect: the deck's placed weight rose by 7,500 kg, which pushed the running total against the
    290,000 kg vehicle deadweight in DLS-4 Appendix B. Four cars that would otherwise have loaded in
    lane M5 - TSF-2241, TSF-2242, TSF-2243 and TSF-2245 - can no longer be placed without breaching the
    deadweight, so they go to the next sailing. The plan was rebuilt on the corrected reading before any
    text went out. TSF-2201's own fare is unchanged: the tariff charges length and height, not weight.

  TSF-2203 was not weighed. Its weight comes from the customer instead: Ronsay Community Energy wrote on
  its freight account ticket 43002 at 14:35 on 10 December that the tanker will run at 19,500 kg gross
  rather than the 26,000 kg on the booking. Conditions of carriage 4.2 lets an account customer write a
  change on its freight account ticket under the same 18:00 deadline, so 19,500 kg is used.""")
DOS.append("")
DOS.append("=" * 100)
DOS.append("CUSTOMER CHANGES AND CANCELLATIONS")
DOS.append("=" * 100)
DOS.append("""  Conditions of carriage 4.2: a change or cancellation the customer writes on the booking's
  customer-service ticket before 18:00 on the day before the sailing amends the booking; one written
  after that time changes nothing and the vehicle is planned as booked. An account customer's driver may
  give a change of vehicle details the same way on the freight messaging line, and an account customer
  may write on its freight account ticket, both under the same deadline. The deadline for this sailing
  is 18:00 on Friday 11 December 2026.

  Counted (in time):
    TSF-2203  freight account ticket 43002, 10 Dec 14:35 - gross weight 26,000 -> 19,500 kg.
    TSF-2204  ticket 41004, 9 Dec 12:30 - roof box fitted, height 1.49 -> 2.35 m. This is what takes it
              off the hoistable deck (over the 2.10 m clearance) and lifts its rate from 7.80 to 9.60.
    TSF-2212  ticket 41012, 11 Dec 09:05 - "please cancel this booking". Outcome: Cancelled by customer.
    TSF-2222  freight messaging line, 10 Dec 17:05 - roof rack for parcel cages, height 2.05 -> 2.45 m.
              Account customer's driver, so it counts. Takes the mail van off the hoistable deck and
              lifts its rate from 7.80 to 9.60.
    TSF-2227  ticket 41027, 10 Dec 15:20 - long trailer, length 10.0 -> 13.6 m.

  Not counted (after the deadline; planned as booked):
    TSF-2221  ticket 41021, 11 Dec 19:20 - 3 m box trailer, 7.6 m overall. One hour and twenty minutes
              late. Planned as booked at 4.6 m, in U3. Had it counted, the car would have been too long
              for the hoistable lanes.
    TSF-2224  freight messaging line, 11 Dec 19:10 - long skip lorry, 9.4 m. Late. Planned as booked at
              8.2 m, in M3.

  Note the asymmetry, which is the standard working as written: TSF-2224's late length change is
  disregarded, but its 16:35 weighbridge reading is used, because a weighbridge reading is not a
  customer change - DLS-4 s1 takes the latest reading whenever it was taken.""")
DOS.append("")
DOS.append("=" * 100)
DOS.append("LANE NOTICES")
DOS.append("=" * 100)
DOS.append("""  DLS-4 s3: usable lengths and clearances are those on the vessel deck plan, as changed by the master's
  latest written notice for the sailing; a lane the chief engineer has put out of use takes nothing.

  Deck plan (rev D, 2026-10) as the baseline: U1-U4 24.0 m each, clearance 2.10 m; M1 36.0 m (dangerous
  goods lane); M2-M5 52.0 m; main deck clearance 4.80 m except M5 at 4.20 m under the casing.
  DLS-4 Appendix B sets the hoistable clearance at 2.10 m, the hoistable weight limit at 3,500 kg per
  vehicle, spacing at 0.6 m per vehicle and the vehicle deadweight at 290,000 kg.

  Chief engineer, 2026-12-09 14:15 - the hoist on hoistable deck section 4 failed its check; lane U4 is
  out of use for every sailing on Saturday 12 December. U4 takes nothing. This is why four cars that the
  draft had in U4 are elsewhere or moved.

  Master, 2026-12-10 11:30 - lashing gear at the after end of M3, so M3 is 44.0 m.
  Master, 2026-12-11 08:10 - correction: the gear went into M4, not M3. M4 is 41.5 m on Saturday and M3
  is back to its full length. The second notice is the master's latest written notice, so the lane
  lengths used are M3 52.0 m and M4 41.5 m. Planning on the superseded notice would have put M3 at
  44.0 m and left M4 at 52.0 m, which changes where nine vehicles sit.

  Lanes after the notices:
    U1 24.0 m   U2 24.0 m   U3 24.0 m   U4 out of use
    M1 36.0 m (DG only)   M2 52.0 m   M3 52.0 m   M4 41.5 m   M5 52.0 m (clearance 4.20 m)""")
DOS.append("")
DOS.append("=" * 100)
DOS.append("LANE OCCUPANCY AND ROOM LEFT")
DOS.append("=" * 100)
for ln in lane_order + ["U4"]:
    used = D(plan["lane_used"][ln])
    left = D(plan["lane_left"][ln])
    DOS.append("  %-3s usable %5s m   used %5s m   left %5s m   %d vehicle(s): %s" % (
        ln, LANE_L[ln], used, left, len(plan["lane_contents"][ln]),
        ", ".join(plan["lane_contents"][ln]) or "-"))
DOS.append("")
DOS.append("  Note: 'used' includes the 0.6 m spacing allowance per vehicle required by Appendix B.")
open("/workspace/ts0815_2026-12-12_deck_plan_dossier.txt", "w").write("\n".join(DOS) + "\n")

# ============================================================ RECONCILIATION
with open("/workspace/ts0815_2026-12-12_plan_reconciliation.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["plan_seq", "booking_ref", "vehicle_type", "loading_group", "lane_given",
                "outcome_if_no_lane", "lanes_refused_and_why", "length_m", "charged_length_m",
                "rate_per_m", "length_charge_gbp", "rebate_gbp", "surcharge_gbp", "fare_gbp"])
    for i, ref in enumerate(ORDER, 1):
        r, v, t = R[ref], VEH[ref], trace[ref]
        rej = " | ".join("%s: %s" % (a, b) for a, b in t["rejects"])
        if r["status"] == "Loaded":
            c = r["calc"]
            w.writerow([i, ref, v["kind"], ["lifeline", "commercial", "other"][v["group"]],
                        r["lane"], "", rej, v["length"], c["charged_length"], c["rate"],
                        c["length_charge"], c["rebate"], c["surcharge"], r["fare"]])
        else:
            w.writerow([i, ref, v["kind"], ["lifeline", "commercial", "other"][v["group"]],
                        "", r["status"], rej, "", "", "", "", "", "", ""])

print("revenue", revenue, "| in words:", words(revenue))
print("loaded", len(loaded), "moved", len(moved))
print("bridge:", [(b[0], str(b[3]), str(b[2])) for b in BRIDGE])
print("lane revenue:", {k: str(v) for k, v in lane_rev.items()})
print("check sum of lane revenue =", sum(lane_rev.values()))

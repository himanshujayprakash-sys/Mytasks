"""Write the browser page, the dossier and the reconciliation sheet."""

import csv
import html
import json
from decimal import Decimal

from engine import (ACCOUNTS, CARRY_OVER, CLASS_ORDER, CREDIT_STOP, DN, LINES,
                    PRICE, PRODUCT_NAME, REJECTS)

OUT = "/workspace"
R = json.load(open("/workspace/alloc/result.json"))
ROWS = R["rows"]
TRACE = R["trace"]
SUBS = R["subs"]
BRIDGE = R["bridge"]

HEADINGS = ["Allocated in full", "Allocated in part", "Nil - stock exhausted",
            "Held - credit stop", "Cancelled by customer",
            "Withdrawn - below minimum drop", "Substitute supplied"]

WITHDRAW_VALUE = {"EF-2401": "19.80", "EF-2404": "9.60", "EF-2406": "20.40"}
LINE_BY_REF = {l[0]: l for l in LINES}


# --------------------------------------------------------------- HTML page
def svg_bridge():
    steps = BRIDGE
    w, h = 1000, 420
    pad_l, pad_b, pad_t = 70, 150, 30
    plot_h = h - pad_b - pad_t
    vals = [Decimal(s["running"]) for s in steps]
    top = max(max(vals), Decimal(steps[0]["amount"]))
    scale = Decimal(plot_h) / top
    bar_w = (w - pad_l - 30) / len(steps) - 18
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" '
           f'aria-label="Bridge from ordered value to invoice value">']
    for gl in range(0, 6):
        y = pad_t + plot_h - plot_h * gl / 5
        amt = top * Decimal(gl) / 5
        out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w-20}" y2="{y:.1f}" '
                   f'class="grid"/>')
        out.append(f'<text x="{pad_l-8}" y="{y+4:.1f}" class="ax" '
                   f'text-anchor="end">{amt:.0f}</text>')
    prev = Decimal("0")
    for i, s in enumerate(steps):
        amt = Decimal(s["amount"])
        run = Decimal(s["running"])
        x = pad_l + 10 + i * (bar_w + 18)
        if i == 0:
            lo, hi = Decimal("0"), run
            cls = "start"
        elif i == len(steps) - 1:
            lo, hi = min(prev, run), max(prev, run)
            cls = "neg"
        else:
            lo, hi = min(prev, run), max(prev, run)
            cls = "neg" if amt < 0 else "pos"
        y0 = pad_t + plot_h - float(hi * scale)
        y1 = pad_t + plot_h - float(lo * scale)
        bh = max(y1 - y0, 1.5)
        out.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{bar_w:.1f}" '
                   f'height="{bh:.1f}" class="bar {cls}"><title>'
                   f'{html.escape(s["label"])}: {amt} (running {run})</title></rect>')
        out.append(f'<text x="{x+bar_w/2:.1f}" y="{y0-6:.1f}" class="val" '
                   f'text-anchor="middle">{amt}</text>')
        label = s["label"]
        words, lines_, cur = label.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) > 20:
                lines_.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines_.append(cur)
        ty = pad_t + plot_h + 16
        out.append(f'<text x="{x+bar_w/2:.1f}" y="{ty:.1f}" class="ax" '
                   f'text-anchor="middle">')
        for j, ln in enumerate(lines_[:5]):
            out.append(f'<tspan x="{x+bar_w/2:.1f}" dy="{0 if j==0 else 12}">'
                       f'{html.escape(ln)}</tspan>')
        out.append('</text>')
        out.append(f'<text x="{x+bar_w/2:.1f}" y="{pad_t+plot_h+90:.1f}" '
                   f'class="run" text-anchor="middle">= {run}</text>')
        prev = run
    out.append('</svg>')
    return "\n".join(out)


def svg_classes():
    w, h = 620, 300
    pad_l, pad_b, pad_t = 70, 60, 20
    plot_h = h - pad_b - pad_t
    data = [(c, Decimal(R["by_class"][c])) for c in CLASS_ORDER]
    top = max(v for _c, v in data)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" '
           f'aria-label="Invoice value by contract class">']
    for gl in range(0, 6):
        y = pad_t + plot_h - plot_h * gl / 5
        out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w-20}" y2="{y:.1f}" class="grid"/>')
        out.append(f'<text x="{pad_l-8}" y="{y+4:.1f}" class="ax" text-anchor="end">'
                   f'{top*Decimal(gl)/5:.0f}</text>')
    bar_w = (w - pad_l - 40) / len(data) - 30
    for i, (c, v) in enumerate(data):
        x = pad_l + 20 + i * (bar_w + 30)
        bh = float(v / top) * plot_h
        y = pad_t + plot_h - bh
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" '
                   f'height="{bh:.1f}" class="bar cls{c}"><title>Class {c}: '
                   f'{v}</title></rect>')
        out.append(f'<text x="{x+bar_w/2:.1f}" y="{y-6:.1f}" class="val" '
                   f'text-anchor="middle">{v}</text>')
        out.append(f'<text x="{x+bar_w/2:.1f}" y="{pad_t+plot_h+20:.1f}" '
                   f'class="ax" text-anchor="middle">Class {c}</text>')
    out.append('</svg>')
    return "\n".join(out)


def html_page():
    trs = []
    for r in ROWS:
        trs.append(
            "<tr>" + "".join(
                f'<td{" class=num" if k in ("ordered","allocated","value") else ""}>'
                f'{html.escape(str(v))}</td>'
                for k, v in (("account", f'{r["account"]} {r["account_name"]}'),
                             ("cls", r["cls"]),
                             ("product", f'{r["product"]} {r["product_name"]}'),
                             ("ordered", r["ordered"]),
                             ("allocated", r["allocated"]),
                             ("heading", r["heading"]),
                             ("rule", r["rule"]),
                             ("value", r["value"]))) + "</tr>")
    rows_html = "\n".join(trs)
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quayside depot allocation, Wednesday 9 December 2026</title>
<style>
 :root {{ --ink:#1b2430; --rule:#d6dce4; --pos:#2e7d32; --neg:#b3261e; --start:#27496d; }}
 body {{ font-family: "Segoe UI", Arial, Helvetica, sans-serif; margin:0;
         color:var(--ink); background:#f6f8fa; }}
 header {{ background:#fff; border-bottom:3px solid var(--start); padding:26px 32px; }}
 h1 {{ font-size:19px; margin:0 0 14px; font-weight:600; letter-spacing:.02em; }}
 .headline {{ display:flex; flex-wrap:wrap; align-items:flex-end; gap:46px; }}
 .big {{ font-size:72px; line-height:1; font-weight:700; color:var(--start); }}
 .big small {{ font-size:28px; font-weight:600; }}
 .cap {{ font-size:13px; text-transform:uppercase; letter-spacing:.09em;
         color:#5a6676; margin-bottom:6px; }}
 .count {{ font-size:46px; line-height:1; font-weight:700; }}
 .count.no {{ color:var(--neg); }}
 main {{ padding:26px 32px 60px; }}
 section {{ background:#fff; border:1px solid var(--rule); border-radius:6px;
            padding:20px 24px; margin-bottom:26px; }}
 h2 {{ font-size:15px; margin:0 0 6px; text-transform:uppercase;
       letter-spacing:.07em; color:#36455a; }}
 p.note {{ font-size:13px; color:#5a6676; margin:0 0 14px; }}
 .chart {{ width:100%; height:auto; }}
 .grid {{ stroke:#e7ebf0; stroke-width:1; }}
 .ax {{ font-size:11px; fill:#5a6676; }}
 .val {{ font-size:11px; fill:#1b2430; font-weight:600; }}
 .run {{ font-size:11px; fill:#27496d; font-weight:700; }}
 .bar.start {{ fill:var(--start); }} .bar.pos {{ fill:var(--pos); }}
 .bar.neg {{ fill:var(--neg); }}
 .clsA {{ fill:#27496d; }} .clsB {{ fill:#3d6e9c; }}
 .clsC {{ fill:#6e9bc5; }} .clsD {{ fill:#a9c3dc; }}
 .tools {{ display:flex; gap:12px; align-items:center; margin-bottom:12px; }}
 input[type=search] {{ padding:7px 10px; border:1px solid var(--rule);
   border-radius:4px; font-size:13px; width:330px; }}
 table {{ border-collapse:collapse; width:100%; font-size:12.5px; }}
 th, td {{ border-bottom:1px solid var(--rule); padding:6px 8px;
           text-align:left; vertical-align:top; }}
 th {{ background:#eef2f6; cursor:pointer; user-select:none;
       position:sticky; top:0; white-space:nowrap; }}
 th::after {{ content:" \\2195"; color:#8a97a8; font-size:10px; }}
 td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
 tbody tr:nth-child(even) {{ background:#fafbfc; }}
 .wrap {{ max-height:620px; overflow:auto; border:1px solid var(--rule); }}
 .meta {{ font-size:12.5px; color:#5a6676; }}
</style>
</head>
<body>
<header>
 <h1>Quayside depot &mdash; allocation for delivery Wednesday 9 December 2026</h1>
 <div class="headline">
  <div>
   <div class="cap">Total invoice value after discounts</div>
   <div class="big"><small>&pound;</small>{R["total"]}</div>
  </div>
  <div>
   <div class="cap">Accounts delivered to</div>
   <div class="count">{len(R["delivering"])}</div>
  </div>
  <div>
   <div class="cap">Accounts not delivered to</div>
   <div class="count no">{len(R["not_delivering"])}</div>
  </div>
 </div>
</header>
<main>
<section>
 <h2>Bridge from the order book to the invoice</h2>
 <p class="note">Order lines as they stood at the 06:00 cut-off on 8 December,
  priced at PL-12 second issue, through to the total after contract discounts.
  Figures in pounds.</p>
 {svg_bridge()}
 <table style="margin-top:14px">
  <thead><tr><th>Step</th><th>Amount</th><th>Running total</th><th>Lines or accounts behind it</th></tr></thead>
  <tbody>
  {"".join(f'<tr><td>{html.escape(b["label"])}</td><td class=num>{b["amount"]}</td>'
           f'<td class=num>{b["running"]}</td><td>{html.escape(b["detail"])}</td></tr>'
           for b in BRIDGE)}
  </tbody>
 </table>
</section>
<section>
 <h2>Invoice value by contract class</h2>
 <p class="note">Class A takes 6% and class B 4% off every line; classes C and D
  take nothing (PL-12 second issue, section 2).</p>
 {svg_classes()}
</section>
<section>
 <h2>Allocation register &mdash; every line</h2>
 <p class="note">{len(ROWS)} register lines. Click any heading to sort; type in the
  box to filter.</p>
 <div class="tools">
  <input type="search" id="q" placeholder="Filter on any word, e.g. EF-2304 or Withdrawn">
  <span class="meta" id="shown"></span>
 </div>
 <div class="wrap">
 <table id="reg">
  <thead><tr>
   <th>Account</th><th>Class</th><th>Product</th><th>Ordered</th>
   <th>Allocated</th><th>Heading</th><th>Rule that decided it</th><th>Value</th>
  </tr></thead>
  <tbody>
{rows_html}
  </tbody>
 </table>
 </div>
</section>
<section class="meta">
 <h2>Authority</h2>
 <p>TT-4 Allocation terms for short supply, third edition (in force for every
 delivery day on or after 23 November 2026). PL-12 Trade price list, second issue
 (applies to every delivery on or after 30 November 2026); corrigendum 1
 commences 4 January 2027 and does not reach this delivery.</p>
</section>
</main>
<script>
(function () {{
  var table = document.getElementById('reg');
  var tbody = table.tBodies[0];
  var all = Array.prototype.slice.call(tbody.rows);
  var shown = document.getElementById('shown');
  var dir = {{}};
  function count(n) {{ shown.textContent = n + ' of ' + all.length + ' lines shown'; }}
  count(all.length);
  Array.prototype.forEach.call(table.tHead.rows[0].cells, function (th, i) {{
    th.addEventListener('click', function () {{
      dir[i] = !dir[i];
      var rows = Array.prototype.slice.call(tbody.rows);
      rows.sort(function (a, b) {{
        var x = a.cells[i].textContent.trim(), y = b.cells[i].textContent.trim();
        var nx = parseFloat(x), ny = parseFloat(y);
        var c = (!isNaN(nx) && !isNaN(ny) && x !== '' && y !== '')
                ? nx - ny : x.localeCompare(y);
        return dir[i] ? c : -c;
      }});
      rows.forEach(function (r) {{ tbody.appendChild(r); }});
    }});
  }});
  document.getElementById('q').addEventListener('input', function (e) {{
    var q = e.target.value.toLowerCase(), n = 0;
    all.forEach(function (r) {{
      var hit = r.textContent.toLowerCase().indexOf(q) !== -1;
      r.style.display = hit ? '' : 'none';
      if (hit) {{ n++; }}
    }});
    count(n);
  }});
}})();
</script>
</body>
</html>
"""


# ------------------------------------------------------------- dossier
def dossier():
    o = []
    a = o.append
    a("# Quayside depot: allocation dossier for delivery Wednesday 9 December 2026")
    a("")
    a("Prepared for Morven Alcott, allocations desk, Tuesday 8 December 2026.")
    a("")
    a("## The papers that govern")
    a("")
    a("| Question | Paper used | Why |")
    a("|---|---|---|")
    a("| How a short product is shared out | **TT-4 Allocation terms for short "
      "supply, third edition** (approved 2026-11-09) | In force for every delivery "
      "day on or after 2026-11-23 and supersedes the second edition in full; the "
      "delivery day is 2026-12-09. |")
    a("| What a case costs, what discount a contract carries | **PL-12 Trade price "
      "list, second issue** (published 2026-11-16) | Applies to every delivery on "
      "or after 2026-11-30. |")
    a("| Corrected vine tomato and clementine prices | **Not used** (PL-12 "
      "corrigendum 1) | Commences 2027-01-04 and says in terms that it does not "
      "reach back to deliveries before 4 January 2027. |")
    a("")
    a(f"Totals: **{R['total']} pounds** after discounts; class A "
      f"{R['by_class']['A']}, class B {R['by_class']['B']}, class C "
      f"{R['by_class']['C']}, class D {R['by_class']['D']}. "
      f"{len(R['delivering'])} accounts delivered to, "
      f"{len(R['not_delivering'])} not: "
      + ", ".join(f"{x} {ACCOUNTS[x][2]}" for x in R["not_delivering"]) + ".")
    a("")

    a("## Stock shared out (terms clause 2)")
    a("")
    a("| Product | Delivery note DN-55812 | Less goods-in rejects | Carry-over "
      "counted | Stock | Left after substitutes |")
    a("|---|---|---|---|---|---|")
    for p in sorted(PRICE):
        co = sum(c[2] for c in CARRY_OVER if c[1] == p and c[6])
        a(f"| {p} {PRODUCT_NAME[p]} | {DN[p]} | {REJECTS.get(p, 0)} | {co} | "
          f"**{R['stock'][p]}** | {R['stock_left'][p]} |")
    a("")
    a("### Every cold store lot, and whether it counted")
    a("")
    a("| Lot | Product | Cases | Best before | Bay | Record status | Counted | Reason |")
    a("|---|---|---|---|---|---|---|---|")
    for lot, p, cases, bb, bay, st, counts, why in CARRY_OVER:
        a(f"| {lot} | {p} | {cases} | {bb} | {bay} | {st} | "
          f"{'yes' if counts else 'no'} | {why} |")
    a("")
    a("The cold store record is only as good as the Sunday 6 December stock count, "
      "so clause 2's quality-hold test was answered from the QC inspection log in "
      "the depot's Logs folder: L-877 released and verified on 2026-12-07, L-883 "
      "still pending. The `qc_inspection_events` table in the records system was "
      "not used: it is named only by the **second edition**, which the third "
      "edition supersedes in full, and the third edition points at the QC "
      "inspection log instead.")
    a("")

    a("## Order lines as they stood at the cut-off (clause 1)")
    a("")
    a("The cut-off was 06:00 on Tuesday 8 December 2026.")
    a("")
    a("### Changes applied")
    a("")
    a("| Account | Line | Change | Record | Received |")
    a("|---|---|---|---|---|")
    a("| EF-2101 Brackenmoor Community Hospital kitchen | QO-40121 P-12 | 4 -> 7 "
      "cases | night desk voicemail transcript, notes app | 2026-12-07 18:52 |")
    a("| EF-2103 St Brannoc's Care Home | QO-40174 P-11 | 8 -> 3 cases | reply on "
      "customer service desk ticket 5104 | 2026-12-07 16:20 |")
    a("| EF-2103 St Brannoc's Care Home | QO-40175 P-16 | cancelled | reply on "
      "customer service desk ticket 5104 | 2026-12-07 16:20 |")
    a("| EF-2204 St Keverne Primary School | new line P-14, 4 cases | line added | "
      "mail to the desk | 2026-12-07 12:30 |")
    a("| EF-2206 Quayside Day Nursery | QO-40249 P-17 | 2 -> 4 cases | WhatsApp "
      "message to the depot line | 2026-12-07 13:10 |")
    a("| EF-2306 Fig and Fennel Deli | QO-40163 P-11 | 5 -> 7 cases | mail to the "
      "desk | 2026-12-07 10:12 |")
    a("")
    a("### Changes refused")
    a("")
    a("| Account | Asked for | Record | Received | Why refused |")
    a("|---|---|---|---|---|")
    a("| EF-2301 The Harbour Kitchen | 2 more cases of leeks | mail to the desk | "
      "2026-12-08 06:40 | after the 06:00 cut-off |")
    a("| EF-2203 County Hall staff restaurant | cos lettuce 3 -> 5 cases | night "
      "desk voicemail transcript | voicemail left 2026-12-08 06:25 | the change "
      "counts from the time of the voicemail, which is after the cut-off |")
    a("| EF-2305 Saltings Brasserie | 2 more cases of clementines | reply on "
      "service desk ticket 5120 | 2026-12-08 07:35 | after the cut-off |")
    a("| EF-2310 Old Custom House Bistro | a line-by-line answer by return mail | "
      "mail to the desk | 2026-12-08 06:55 | not an order change, and nothing "
      "leaves the depot |")
    a("")

    a("## Contract class (clause 3)")
    a("")
    a("| Account | Class on the record | Class used | Paper |")
    a("|---|---|---|---|")
    a("| EF-2305 Saltings Brasserie | C | **B** | CV-2305, from class C to B "
      "effective 2026-12-01, signed by R. Pendry on 2026-11-24; RP is on the "
      "Appendix C signatory register from 2024-02-01 and has not been taken off. |")
    a("| EF-2404 Treloar Grocers | D | **D** | CV-2404 does not count: it was "
      "signed by M. Hollis on 2026-11-12, and MH came off the Appendix C register "
      "on 2026-10-30, so the signatory was not on the register on the date of "
      "signing. |")
    a("")

    a("## Credit stops (clause 1)")
    a("")
    a("| Account | Stop | Outcome | Record that settled it |")
    a("|---|---|---|---|")
    a("| EF-2302 Ristorante Valli | credit control mail 2026-12-03 09:15, 45 days "
      "over terms | **ended** | credit control mail 2026-12-07 15:40 lifts the stop "
      "with immediate effect. |")
    a("| EF-2309 Wrecker's Arms | credit control mail 2026-12-05 10:05, stop stands "
      "until INV-31790 is cleared | **ended** | accounts ledger credit note CN-0917, "
      "dated 2026-12-07, authorised, 112.30 against INV-31790 whose total is 112.30 "
      "- the invoice is cleared in full by an authorised credit note before the "
      "cut-off. |")
    a("| EF-2405 Corner Basket | credit control mail 2026-12-04 11:20, stop stands "
      "until INV-31744 is cleared | **stands** | the accounts ledger still shows "
      "INV-31744 authorised with 158.40 due and nothing paid; CN-0915 is for 18.20 "
      "and is raised against INV-31649, not INV-31744. |")
    a("")

    a("## Substitutes (clause 4)")
    a("")
    a("The substitution chart allows P-11 vine tomatoes -> P-18 salad tomatoes and "
      "P-12 iceberg -> P-13 cos, and nothing else; the leeks pairing was withdrawn "
      "in November 2026. A substitute case is charged at the lower of the two "
      "prices, so P-18 for P-11 at 10.20 and P-13 for P-12 at 9.60.")
    a("")
    a("| Order of offer | Account | Class | Short line | Shortfall | Substitute | "
      "Cases | Price | Value |")
    a("|---|---|---|---|---|---|---|---|---|")
    for i, s in enumerate(SUBS, 1):
        ref = s["for_ref"]
        row = next(r for r in ROWS if r["line"] == "al-SUB-" + ref)
        short = LINE_BY_REF[ref][3] - next(
            r["allocated"] for r in ROWS if r["line"] == "al-" + ref)
        a(f"| {i} | {s['account']} {ACCOUNTS[s['account']][2]} | {row['cls']} | "
          f"{ref} {s['for_product']} | {short} | {s['product']} | {s['cases']} | "
          f"{s['price']} | {row['value']} |")
    a("")
    a("EF-2304 Mariner's Rest Inn has `substitutes_ok = no` on the account record, "
      "but the account manager logged on the buyer's contact in the trade CRM on "
      "2026-12-02 that the inn accepts substitutes on any line. Clause 4 makes that "
      "note govern until the record is next refreshed, so the inn was offered a "
      "substitute. No other account's substitute flag was changed. Accounts whose "
      "record says no (EF-2103, EF-2104, EF-2202, EF-2204, EF-2205, EF-2206, "
      "EF-2302, EF-2305, EF-2307, EF-2308, EF-2310, EF-2402, EF-2406) were offered "
      "nothing, whatever the channel chatter said.")
    a("")
    a("P-13 ran out one case short of EF-2403's claim, and three cases of P-13 and "
      "three of P-17 were left over at the end.")
    a("")

    a("## Minimum drop (clause 5 and Appendix B)")
    a("")
    a("Appendix B sets the minimum drop at 50.00 pounds for class C and class D "
      "accounts, measured on cases at the price-list price and substitutes at the "
      "price charged, before any discount. One account comes off at a time, lowest "
      "value first, and the whole allocation is then run again.")
    a("")
    a("| Pass | Excluded going in | Class C/D accounts below the minimum | Withdrawn |")
    a("|---|---|---|---|")
    for i, p in enumerate(R["passes"], 1):
        off = ", ".join(f"{a_} {v}" for v, a_ in p["offenders"]) or "none"
        took = p["offenders"][0][1] if p["offenders"] else "-"
        a(f"| {i} | {', '.join(p['excluded']) or 'none'} | {off} | {took} |")
    a("")
    a("Three accounts came off the van: EF-2401 Pascoe's Greengrocer (19.80), "
      "EF-2404 Treloar Grocers (9.60) and EF-2406 Harbourside Mini-Mart (20.40). "
      "Taking them out freed the last three cases of P-18 for EF-2403 Quay Market "
      "stall 7, which lifted that account from 30.60 to 61.20 and kept it on the "
      "round. Class A and class B accounts are never withdrawn.")
    a("")

    a("## Where a share was settled by the tie rule (clause 3)")
    a("")
    for t in R["ties"]:
        a(f"- **{t['product']} {PRODUCT_NAME[t['product']]}, class "
          f"{t['cls']}**: {', '.join(t['tied'])} both came out on a fraction of "
          f"{t['fraction']} of a case. The rule gives the case to the line ordered "
          f"earlier: {t['won'][0]} (EF-2310, ordered 2026-12-06 08:30) beat "
          f"QO-40298 (EF-2304, ordered 2026-12-06 11:05).")
    a("")
    a("No other spare case fell to a tie.")
    a("")

    a("## Every order line by heading")
    a("")
    for head in HEADINGS:
        sel = [r for r in ROWS if r["heading"] == head]
        a(f"### {head} ({len(sel)} line{'s' if len(sel) != 1 else ''})")
        a("")
        if not sel:
            a("No lines under this heading.")
            a("")
            continue
        a("| Register line | Account | Class | Product | Ordered | Allocated | "
          "Share | Value | Record that settled it |")
        a("|---|---|---|---|---|---|---|---|---|")
        for r in sorted(sel, key=lambda r: (r["account"], r["product"])):
            why = r["rule"] + (f"; {r['note']}" if r["note"] else "")
            a(f"| {r['line']} | {r['account']} {r['account_name']} | {r['cls']} | "
              f"{r['product']} {r['product_name']} | "
              f"{r['ordered'] if r['kind'] == 'order' else '-'} | "
              f"{r['allocated']} | {r['share'] or '-'} | {r['value']} | {why} |")
        a("")

    a("## The register as it was found and as it was left")
    a("")
    a(f"- **{len(R['changes']['correct'])} lines were already right** and were not "
      "touched at all.")
    a(f"- **{len(R['changes']['update'])} lines were corrected**: "
      + ", ".join(R["changes"]["update"]) + ".")
    a(f"- **{len(R['changes']['create'])} lines were created**: "
      + ", ".join(R["changes"]["create"]) + ".")
    a(f"- **{len(R['changes']['delete'])} line was deleted**: "
      + ", ".join(R["changes"]["delete"])
      + " - a second register line for order QO-40164, which clause 6 says is removed.")
    a("")

    a("## Supply exceptions record (clause 7)")
    a("")
    a("| Id | Action | Reason |")
    a("|---|---|---|")
    a("| SX-400 | restated from 51.60 to **64.50** | Pentrae Growers accounts "
      "confirmed the newest figure in writing to the Quayside office mailbox on "
      "2026-12-05. |")
    a("| SX-401 | **removed** | the thing it awaited shows verified on the depot "
      "logs: the QC inspection log has lot L-877 released and verified on "
      "2026-12-07. |")
    a("| SX-402 | **removed** | the crate deposit log shows EF-2309 counted at 11 "
      "crates on 2026-12-04, verified. |")
    a("| SX-403 | restated from 84.00 to **96.60** | Pentrae Growers accounts "
      "confirmed the newest figure by mail to the desk on 2026-12-04. |")
    a("| SX-404 | left exactly as it stands | nothing on the depot logs verifies "
      "the 28 November chiller 2 excursion as closed. |")
    a("| SX-405 | left exactly as it stands | the van checks show no verified "
      "repair to the QD-06 rear step. |")
    a("| SX-406 | left exactly as it stands | the EF-2310 complaint is still under "
      "review and no one has confirmed a different amount in writing. |")
    a("| SX-407 | left exactly as it stands | the QC inspection log has lot L-883 "
      "pending, with no verifying result. |")
    a("| SX-408 | **created**, Short supply, P-11 | vine tomato orders could not "
      "all be met. |")
    a("| SX-409 | **created**, Short supply, P-12 | iceberg orders could not all be met. |")
    a("| SX-410 | **created**, Short supply, P-14 | leek orders could not all be met. |")
    a("| SX-411 | **created**, Short supply, P-15 | mushroom orders could not all "
      "be met. |")
    a("| SX-412 | **created**, Credit stop - not delivered, EF-2405 | one per "
      "account on credit stop. |")
    a("| SX-413 | **created**, Below minimum drop, EF-2401 | one per account "
      "withdrawn. |")
    a("| SX-414 | **created**, Below minimum drop, EF-2404 | one per account "
      "withdrawn. |")
    a("| SX-415 | **created**, Below minimum drop, EF-2406 | one per account "
      "withdrawn. |")
    a("")
    a("P-13, P-16, P-17 and P-18 got no 'Short supply' item: every live order line "
      "for those products was met in full.")
    a("")

    a("## Messages sent to customers")
    a("")
    a("| Account | Cases going out | Cases ordered | How told | Notice status |")
    a("|---|---|---|---|---|")
    for acct in R["delivering"]:
        m = R["messages"][acct]
        if not m["opted_in"]:
            how, st = "nothing sent - not opted in to messages", "none"
        elif m["stop"]:
            how, st = "nothing sent - " + m["stop"], "none"
        elif m["window_open"]:
            how, st = "text in the open conversation window", "texted"
        else:
            how, st = "approved allocation_notice_v3 template", "template"
        a(f"| {acct} {ACCOUNTS[acct][2]} | {m['n']} | {m['m']} | {how} | {st} |")
    a("")
    a("The four accounts that are not being delivered to (EF-2401, EF-2404, "
      "EF-2405, EF-2406) were told nothing, because only accounts getting a "
      "delivery are told.")
    a("")

    a("## Claims made in the allocations channel")
    a("")
    a("| Claim | Stands? | Paper that decides it |")
    a("|---|---|---|")
    a("| 'I gave out the trade and market stock in the order it came in' | No | "
      "TT-4 third edition clause 3: each product is allocated class by class, A "
      "then B then C then D. First come, first served is the superseded second "
      "edition. |")
    a("| 'Clementines are 14.20 a case now and the vine tomatoes 15.10' | No | "
      "PL-12 corrigendum 1 commences 2027-01-04; the second issue prices of 13.75 "
      "and 14.40 apply to this delivery. |")
    a("| 'Round everyone to the nearest case' | No | Clause 3: shares are rounded "
      "**down**, and the spare cases go one at a time to the largest fraction "
      "rounded off. |")
    a("| 'St Brannoc's always have eight cases of vine tomatoes, I have keyed them "
      "as usual' | No | The customer cut that line to 3 cases on service desk "
      "ticket 5104 at 2026-12-07 16:20, before the cut-off, and cancelled the "
      "clementines. |")
    a("| 'Valli are still on stop, do not send them anything this week' | No | The "
      "credit control mail of 2026-12-07 15:40 lifts the stop on EF-2302 with "
      "immediate effect, and clause 1 gives the latest word from credit control "
      "before the cut-off. |")
    a("| 'The leeks in bay 3 are fine for Wednesday, the date is only a day out' | "
      "No | Clause 2: a carry-over lot counts only if its best-before date is on or "
      "after the delivery date. Lot L-874 is 2026-12-08. |")
    a("| 'Ruling from me: Ristorante Valli get their full six cases of vine "
      "tomatoes' | No | Clause 3 fixes the class C share; EF-2302 gets 2 of 6. A "
      "ruling is not one of the records the terms name, however senior. |")
    a("| 'Saltings are still class C, that variation will not be through until "
      "January' | No | CV-2305 is effective 2026-12-01 and was signed by a "
      "signatory on the Appendix C register, so EF-2305 is class B. |")
    a("| 'Treloar's moved up to class C this month, Hollis signed it off' | No | "
      "M. Hollis came off the Appendix C register on 2026-10-30 and signed CV-2404 "
      "on 2026-11-12, so the variation does not count. |")
    a("| 'Minimum drop is off this week, the vans are going that way anyway' | No | "
      "Clause 5 and Appendix B are in force; three accounts were withdrawn. |")
    a("| 'Cos goes to anyone short of iceberg, no need to check the account' | No | "
      "Clause 4 and the substitution chart: only accounts whose record (or the "
      "account manager's CRM note) accepts substitutes. |")
    a("| 'Please do not reply in here about the allocation' | Yes, and it is also "
      "what was asked for | Nothing was posted in the channel. |")
    a("")

    a("## Papers in the folders that made no difference")
    a("")
    for x in [
        "TT-4 allocation terms, second edition - superseded in full by the third "
        "edition for this delivery day, including its paragraph about "
        "`qc_inspection_events`.",
        "PL-12 Trade price list, first issue - superseded for deliveries on or "
        "after 2026-11-30.",
        "PL-12 second issue, corrigendum 1 - commences 2027-01-04.",
        "purchase_order_PO-7731.csv - what we asked the grower for, which clause 2 "
        "says is not stock.",
        "northgate-depot-allocation-wed-2026-12-09-sheet-3.docx - Northgate "
        "accounts on Northgate stock, sent for information only.",
        "last_week_allocation_report.docx - the 2 December delivery at first-issue "
        "prices.",
        "allocation_crib_sheet.docx - a summer desk note that contradicts the third "
        "edition on every point.",
        "fuel_log.csv, route_plan_wed9dec.csv, pallet_returns.csv - transport "
        "records, nothing to do with who gets what.",
        "christmas_opening_leaflet.docx, food_safety_bulletin.docx, "
        "grower_newsletter.docx, canteen_menu.docx, night_desk_rota.docx - general "
        "depot reading.",
    ]:
        a(f"- {x}")
    a("")
    a("Two logs were read and changed nothing, which is itself the answer: "
      "`chiller_temperature_log.csv` has no entries for the 28 November chiller 2 "
      "alarm, and `van_checks.csv` shows no verified repair to the QD-06 rear step, "
      "so SX-404 and SX-405 stay exactly as they stand. The cold store bay plan, "
      "the substitution chart, the QC inspection log and the crate deposit log all "
      "changed the answer and are covered above.")
    a("")
    return "\n".join(o)


# ------------------------------------------------------- reconciliation CSV
def reconciliation():
    out = []
    head = ["row_type", "sequence", "product", "product_name", "contract_class",
            "account_no", "account_name", "register_line", "order_ref",
            "cases_ordered", "class_share", "cases_allocated", "heading",
            "price_gbp", "discount", "value_gbp"]
    byline = {r["line"]: r for r in ROWS}
    n = 0
    for t in TRACE:
        n += 1
        r = byline["al-" + t["order_ref"]]
        out.append(["order line", n, t["product"], PRODUCT_NAME[t["product"]],
                    t["cls"], t["account"], ACCOUNTS[t["account"]][2],
                    r["line"], t["order_ref"], t["ordered"], t["share"],
                    t["allocated"], r["heading"], r["price"], r["discount"],
                    r["value"]])
    for s in SUBS:
        n += 1
        r = byline["al-SUB-" + s["for_ref"]]
        out.append(["substitute supplied", n, s["product"],
                    PRODUCT_NAME[s["product"]], r["cls"], s["account"],
                    ACCOUNTS[s["account"]][2], r["line"], s["for_ref"], "",
                    "", s["cases"], "Substitute supplied", s["price"],
                    r["discount"], r["value"]])
    for i, acct in enumerate(R["withdrawn"], 1):
        n += 1
        out.append(["account withdrawn", n, "", "", ACCOUNTS[acct][0], acct,
                    ACCOUNTS[acct][2], "", "", "", "", 0,
                    "Withdrawn - below minimum drop", "", "",
                    WITHDRAW_VALUE[acct]])
    return head, out


def main():
    page = f"{OUT}/quayside_allocation_2026-12-09.html"
    open(page, "w").write(html_page())
    doc = f"{OUT}/quayside_allocation_dossier_2026-12-09.md"
    open(doc, "w").write(dossier())
    head, rows = reconciliation()
    sheet = f"{OUT}/quayside_allocation_reconciliation_2026-12-09.csv"
    with open(sheet, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(head)
        wr.writerows(rows)
    print("wrote", page, doc, sheet, sep="\n")
    print("reconciliation rows:", len(rows))


if __name__ == "__main__":
    main()

"""Build the three working-folder deliverables from the engine output."""
import csv
import json
from decimal import Decimal as D

OUT = "/workspace/data/Nursery/working/"
recon = json.load(open("/workspace/close/recon.json"))
register = json.load(open("/workspace/close/register.json"))
tot = json.load(open("/workspace/close/totals.json"))

VAR = {
    "ACP3": "Acer palmatum 'Bloodgood' 3L",
    "LAV2": "Lavandula angustifolia 'Hidcote' 2L",
    "HOS2": "Hosta 'June' 2L",
    "ROS4": "Rosa 'Gertrude Jekyll' 4L",
    "BUX9": "Buxus sempervirens 9cm",
    "FAR7": "Fargesia rufa 7L",
}
CUST = {
    "C-401": "Ashcombe Garden Centre", "C-402": "Bramley Landscapes",
    "C-403": "Coldharbour Plant Centre", "C-404": "Dunmere Estates",
    "C-405": "Elmstead Garden Design", "C-406": "Foxley Nurseries Retail",
    "C-407": "Greystone Parks Trust", "C-408": "Hallbrook Gardens",
    "C-409": "Ivybridge Garden Centre", "C-410": "Juniper Landscaping",
    "C-411": "Kingsmead Hotel Gardens", "C-412": "Larchfield Homes",
    "C-413": "Millbrook Community Garden", "C-414": "Northgate Florists",
    "C-415": "Oakhurst School Grounds", "C-416": "Penwood Golf Club",
}

# ------------------------------------------------ reconciliation CSV
rows = []
for r in recon:
    if r["movement"] == "Receipt":
        continue
    if r["movement"] == "Frost write-off":
        continue
    rows.append(r)
# one frost row per lot written off
frost_by_lot = {}
for r in recon:
    if r["movement"] != "Frost write-off":
        continue
    k = (r["event_time"], r["lot"])
    if k in frost_by_lot:
        e = frost_by_lot[k]
        e["plants"] += r["plants"]
        e["cost"] = str(D(e["cost"]) + D(r["cost"]))
    else:
        e = dict(r)
        e["document"] = "FR-07"
        frost_by_lot[k] = e
rows.extend(frost_by_lot.values())
rows.sort(key=lambda r: r["event_time"])

with open(OUT + "spring_2027_reconciliation.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["event_time", "movement", "document", "customer_or_counterparty",
                "customer_name", "variety_code", "variety_name", "lot_ref",
                "plants", "unit_cost_gbp", "cost_gbp"])
    for r in rows:
        w.writerow([r["event_time"], r["movement"], r["document"], r["counterparty"],
                    CUST.get(r["counterparty"], ""),
                    r["variety"], VAR[r["variety"]], r["lot"], r["plants"],
                    r["unit_cost"], r["cost"]])
print("reconciliation rows:", len(rows))

# ------------------------------------------------ HTML
def money(s):
    neg = str(s).startswith("-")
    whole, frac = str(s).lstrip("-").split(".")
    out = "{:,}".format(int(whole)) + "." + frac
    return ("-" if neg else "") + out


bv = tot["by_variety"]
bridge = [
    ("Opening stock at 1 March 2027", tot["opening"],
     "OP-LAV2, OP-BUX9, OP-HOS2, OP-ACP3, OP-FAR7, OP-ROS4"),
    ("Plus season purchases at landed cost, before credits", tot["purchases"],
     "PL-2701, PL-2702, PL-2703, PL-2704, PL-2705, PL-2706, PL-2707, PL-2708, "
     "PL-2709, PL-2710, PL-2711, PL-2712, PL-2713, PL-2714"),
    ("Effect of the accepted re-issued credit CN-2741 on plants sold", tot["credit_on_sold"],
     "PL-2711"),
    ("Effect of the accepted re-issued credit CN-2741 on plants held at the close",
     tot["credit_on_closing"], "PL-2711"),
    ("Memo: customer returns to stock, credited out of cost of plants sold and "
     "back in as new lots", "-" + tot["returns_to_stock"], "SC-61, SC-62, SC-63"),
    ("Less consignment sent back to the supplier on debit note DN-118",
     "-" + tot["supplier_returns"], "PL-2709"),
    ("Less plants written off to frost report FR-07", "-" + tot["frost"],
     "PL-2706, OP-FAR7"),
    ("Less closing stock at 31 May 2027", "-" + tot["closing"],
     "PL-2707, PL-2708, PL-2710, PL-2711, SC-62, PL-2712, PL-2713, PL-2714"),
]

bridge_bars = [b for b in bridge if not b[0].startswith("Memo")]

lot_rows = "\n".join(
    "<tr><td>{lot}</td><td>{vn}</td><td>{h}</td><td>{rule}</td><td class=n>{q}</td>"
    "<td class=n>{c}</td><td class=n>{v}</td></tr>".format(
        lot=r["lot_ref"], vn=VAR[r["variety"]], h=r["heading"], rule=r["rule"],
        q=r["qty_at_close"], c=r["unit_cost_gbp"], v=r["value_at_close_gbp"])
    for r in register)

bridge_rows = "\n".join(
    "<tr><td>{}</td><td class=n>{}</td><td>{}</td></tr>".format(a, money(b), c)
    for a, b, c in bridge)

var_rows = "\n".join(
    "<tr><td>{}</td><td>{}</td><td class=n>{}</td></tr>".format(k, VAR[k], money(v))
    for k, v in bv.items())


def bar_svg(items, width=760, label_w=330):
    """items: list of (label, value_str). Simple horizontal bars, no external assets."""
    vals = [abs(float(v)) for _, v in items]
    mx = max(vals) if vals else 1
    h = 30
    svg = ['<svg viewBox="0 0 {} {}" role="img" width="100%">'.format(width, h * len(items) + 10)]
    for i, (lab, v) in enumerate(items):
        y = i * h + 6
        bw = (abs(float(v)) / mx) * (width - label_w - 95)
        col = "#8c3b3b" if float(v) < 0 else "#3c6e47"
        svg.append('<text x="0" y="{}" font-size="11">{}</text>'.format(y + 13, lab))
        svg.append('<rect x="{}" y="{}" width="{:.1f}" height="16" fill="{}"/>'.format(
            label_w, y + 2, bw, col))
        svg.append('<text x="{:.1f}" y="{}" font-size="11">{}</text>'.format(
            label_w + bw + 5, y + 14, money(v)))
    svg.append("</svg>")
    return "\n".join(svg)


BRIEF = {
    "Opening stock at 1 March 2027": "Opening stock, 1 March",
    "Plus season purchases at landed cost, before credits": "Plus purchases at landed cost",
    "Effect of the accepted re-issued credit CN-2741 on plants sold":
        "Credit CN-2741, plants sold",
    "Effect of the accepted re-issued credit CN-2741 on plants held at the close":
        "Credit CN-2741, plants held",
    "Less consignment sent back to the supplier on debit note DN-118":
        "Less returned to supplier, DN-118",
    "Less plants written off to frost report FR-07": "Less frost write-off, FR-07",
    "Less closing stock at 31 May 2027": "Less closing stock, 31 May",
}
bridge_chart = bar_svg([(BRIEF[a], b) for a, b, c in bridge_bars] +
                       [("= Cost of plants sold", tot["cps"])], label_w=230)
var_chart = bar_svg([(VAR[k], v) for k, v in bv.items()], label_w=250)

html = """<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8">
<title>Thornfield Nurseries - spring 2027 season close</title>
<style>
body{{font:14px/1.5 Georgia,serif;margin:0;padding:28px;color:#1d1d1d;background:#fbfaf7;max-width:1100px}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:17px;margin:30px 0 8px;border-bottom:1px solid #cdc8bd;padding-bottom:4px}}
.sub{{color:#5a5a5a;margin:0 0 22px}}
.heads{{display:flex;gap:16px;flex-wrap:wrap;margin:0 0 10px}}
.card{{border:1px solid #cdc8bd;background:#fff;padding:14px 18px;border-radius:4px}}
.card.main{{flex:2 1 340px;border-left:5px solid #3c6e47}}
.card.side{{flex:1 1 200px}}
.lab{{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#5a5a5a}}
.fig{{font-size:27px;font-weight:bold;margin:3px 0 0}}
.card.side .fig{{font-size:21px}}
.words{{font-style:italic;color:#3b3b3b;margin-top:5px;font-size:13px}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13px}}
th,td{{border:1px solid #d8d3c8;padding:5px 8px;text-align:left;vertical-align:top}}
th{{background:#efece4}} td.n,th.n{{text-align:right;white-space:nowrap}}
#lots th{{cursor:pointer;user-select:none}} #lots th:after{{content:" \\2195";color:#999;font-size:10px}}
.filters{{margin:8px 0}} .filters input,.filters select{{font:13px Georgia,serif;padding:4px;margin-right:8px}}
small{{color:#5a5a5a}}
</style></head><body>
<h1>Thornfield Nurseries Ltd &mdash; spring 2027 season close</h1>
<p class="sub">Season 1 March to 31 May 2027. Closed 7 June 2027. Costed under
<strong>TN-FIN-04 Stock costing standard, second edition</strong> (approved by the board 2027-02-15,
in force for seasons starting on or after 2027-03-01). Corrigendum 1 takes effect 2027-09-01 and
changes nothing in this season. All figures are at landed cost; selling prices and the catalogue
list price enter none of them.</p>

<div class="heads">
  <div class="card main">
    <div class="lab">Cost of plants sold, net of plants returned to stock</div>
    <div class="fig">&pound;{cps}</div>
    <div class="words">{cps_words}</div>
  </div>
  <div class="card side">
    <div class="lab">Closing stock at 31 May 2027</div>
    <div class="fig">&pound;{closing}</div>
  </div>
  <div class="card side">
    <div class="lab">Cost of plants lost to frost (FR-07)</div>
    <div class="fig">&pound;{frost}</div>
  </div>
</div>

<h2>Bridge: opening stock plus season purchases down to cost of plants sold</h2>
{bridge_chart}
<table>
<tr><th>Step</th><th class="n">Amount (&pound;)</th><th>Lots in the step</th></tr>
{bridge_rows}
<tr><th>Cost of plants sold</th><th class="n">{cps}</th><th></th></tr>
</table>

<h2>Cost of plants sold by variety</h2>
{var_chart}
<table>
<tr><th>Code</th><th>Variety</th><th class="n">Cost of plants sold (&pound;)</th></tr>
{var_rows}
<tr><th></th><th>Total</th><th class="n">{cps}</th></tr>
</table>

<h2>Every lot at the close</h2>
<div class="filters">
<input id="q" placeholder="filter any text&hellip;" size="26">
<select id="h"><option value="">all headings</option>
<option>Held at season close</option><option>Fully drawn</option><option>Frost write-off</option></select>
<small>click a column heading to sort</small>
</div>
<table id="lots">
<thead><tr><th>Lot</th><th>Variety</th><th>Heading</th><th>Rule that put it there</th>
<th class="n">Plants at close</th><th class="n">Unit cost (&pound;)</th><th class="n">Value (&pound;)</th></tr></thead>
<tbody>
{lot_rows}
</tbody></table>
<p><small>Section references are to TN-FIN-04 second edition. Lots SC-61, SC-62 and SC-63 are the
lots created by customer returns to stock under section 3, each carrying the unit cost of the last
lot the original sale drew from. Ashby Grange Nurseries lots (AG-0412, AG-0415, AG-0419) are not
Thornfield stock and appear nowhere above (section 3).</small></p>

<script>
(function(){{
 var t=document.getElementById('lots'),tb=t.tBodies[0],q=document.getElementById('q'),h=document.getElementById('h');
 var rows=[].slice.call(tb.rows);
 function flt(){{
  var s=q.value.toLowerCase(),hh=h.value;
  rows.forEach(function(r){{
   var ok=(!s||r.textContent.toLowerCase().indexOf(s)>=0)&&(!hh||r.cells[2].textContent===hh);
   r.style.display=ok?'':'none';
  }});
 }}
 q.oninput=flt; h.onchange=flt;
 var dir={{}};
 [].slice.call(t.tHead.rows[0].cells).forEach(function(th,i){{
  th.onclick=function(){{
   dir[i]=!dir[i];
   rows.sort(function(a,b){{
    var x=a.cells[i].textContent.trim(),y=b.cells[i].textContent.trim();
    var nx=parseFloat(x),ny=parseFloat(y);
    var c=(!isNaN(nx)&&!isNaN(ny))?nx-ny:x.localeCompare(y);
    return dir[i]?c:-c;
   }});
   rows.forEach(function(r){{tb.appendChild(r);}});
  }};
 }});
}})();
</script>
</body></html>
"""

CPS_WORDS = ("Four thousand eight hundred and fifty-five pounds and zero pence "
             "(&pound;4,855.00)")

html = html.format(cps=money(tot["cps"]), closing=money(tot["closing"]),
                   frost=money(tot["frost"]),
                   cps_words=CPS_WORDS, bridge_chart=bridge_chart, bridge_rows=bridge_rows,
                   var_chart=var_chart, var_rows=var_rows, lot_rows=lot_rows)
open(OUT + "spring_2027_season_close.html", "w").write(html)
print("html bytes:", len(html))

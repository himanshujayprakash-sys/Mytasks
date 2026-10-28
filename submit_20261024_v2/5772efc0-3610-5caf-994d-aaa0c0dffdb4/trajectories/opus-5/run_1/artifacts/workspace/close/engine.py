"""Spring 2027 season close under TN-FIN-04 second edition (FIFO, event-time order)."""
from decimal import Decimal, ROUND_HALF_UP
import json

D = Decimal


def p(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


# (lot_ref, variety, in_stock_on, qty_in, base_unit_cost, revised_unit_cost, revised_from, origin)
LOTS = [
    ("OP-ACP3", "ACP3", "2026-10-14", 40, "9.85", None, None, "opening"),
    ("OP-LAV2", "LAV2", "2026-09-22", 120, "2.65", None, None, "opening"),
    ("OP-HOS2", "HOS2", "2026-10-03", 60, "3.40", None, None, "opening"),
    ("OP-ROS4", "ROS4", "2026-11-05", 25, "8.75", None, None, "opening"),
    ("OP-BUX9", "BUX9", "2026-09-30", 96, "1.15", None, None, "opening"),
    ("OP-FAR7", "FAR7", "2026-10-20", 18, "14.20", None, None, "opening"),
    # season receipts: landed = supplier price per plant + handling (0.30 pre 1 Apr, 0.45 on/after)
    ("PL-2701", "ACP3", "2027-03-08", 60, "9.50", None, None, "purchase"),
    ("PL-2702", "LAV2", "2027-03-10", 200, "2.40", None, None, "purchase"),
    ("PL-2703", "HOS2", "2027-03-15", 80, "3.25", None, None, "purchase"),
    ("PL-2704", "BUX9", "2027-03-18", 240, "1.35", None, None, "purchase"),
    ("PL-2705", "ROS4", "2027-03-24", 50, "8.40", None, None, "purchase"),
    ("PL-2706", "LAV2", "2027-04-02", 150, "2.65", None, None, "purchase"),
    ("PL-2707", "FAR7", "2027-04-06", 30, "13.55", None, None, "purchase"),
    ("PL-2708", "ACP3", "2027-04-09", 40, "10.05", None, None, "purchase"),
    ("PL-2709", "HOS2", "2027-04-13", 58, "3.55", None, None, "purchase"),
    ("PL-2710", "BUX9", "2027-04-16", 180, "1.55", None, None, "purchase"),
    ("PL-2711", "ROS4", "2027-04-20", 60, "8.85", "8.20", "2027-05-04", "purchase"),
    ("PL-2712", "LAV2", "2027-05-03", 108, "2.70", None, None, "purchase"),
    ("PL-2713", "HOS2", "2027-05-15", 36, "3.50", None, None, "purchase"),
    ("PL-2714", "FAR7", "2027-05-19", 20, "13.55", None, None, "purchase"),
]

SALES = {
    "SI-5101": ("C-401", "LAV2", 60), "SI-5102": ("C-402", "ACP3", 12),
    "SI-5103": ("C-405", "BUX9", 60), "SI-5104": ("C-403", "HOS2", 30),
    "SI-5105": ("C-404", "LAV2", 50), "SI-5106": ("C-405", "ACP3", 20),
    "SI-5107": ("C-401", "BUX9", 72), "SI-5108": ("C-404", "ROS4", 20),
    "SI-5109": ("C-407", "LAV2", 40), "SI-5110": ("C-401", "ACP3", 15),
    "SI-5111": ("C-406", "HOS2", 45), "SI-5112": ("C-413", "FAR7", 4),
    "SI-5113": ("C-408", "ROS4", 30), "SI-5114": ("C-410", "LAV2", 70),
    "SI-5115": ("C-412", "BUX9", 96), "SI-5116": ("C-409", "ACP3", 30),
    "SI-5117": ("C-402", "LAV2", 60), "SI-5118": ("C-416", "BUX9", 84),
    "SI-5119": ("C-409", "HOS2", 40), "SI-5120": ("C-403", "ACP3", 25),
    "SI-5121": ("C-407", "FAR7", 2), "SI-5122": ("C-411", "ROS4", 22),
    "SI-5123": ("C-413", "LAV2", 25), "SI-5124": ("C-403", "BUX9", 48),
    "SI-5125": ("C-414", "HOS2", 20), "SI-5126": ("C-402", "ROS4", 18),
    "SI-5127": ("C-408", "LAV2", 50), "SI-5128": ("C-415", "ROS4", 25),
    "SI-5129": ("C-412", "ACP3", 18), "SI-5130": ("C-416", "FAR7", 10),
    "SI-5131": ("C-401", "HOS2", 35), "SI-5132": ("C-406", "BUX9", 120),
    "SI-5133": ("C-411", "LAV2", 45), "SI-5134": ("C-410", "ROS4", 8),
    "SI-5135": ("C-407", "HOS2", 15), "SI-5136": ("C-411", "FAR7", 6),
    "SI-5137": ("C-405", "ACP3", 10), "SI-5138": ("C-404", "LAV2", 40),
}

# event-time ordered movements; SI-5125 excluded (cancelled before dispatch, s.2)
EVENTS = [
    ("2027-03-04 10:15", "SALE", "SI-5101"),
    ("2027-03-05 11:40", "SALE", "SI-5102"),
    ("2027-03-06 09:20", "SALE", "SI-5103"),
    ("2027-03-08 08:30", "RECV", "PL-2701"),
    ("2027-03-09 14:05", "SALE", "SI-5104"),
    ("2027-03-10 08:30", "RECV", "PL-2702"),
    ("2027-03-11 10:30", "SALE", "SI-5105"),
    ("2027-03-12 15:10", "SALE", "SI-5106"),
    ("2027-03-15 08:30", "RECV", "PL-2703"),
    ("2027-03-17 13:20", "SALE", "SI-5108"),
    ("2027-03-18 08:30", "RECV", "PL-2704"),
    ("2027-03-19 11:05", "SALE", "SI-5109"),
    ("2027-03-20 10:00", "SALE", "SI-5110"),
    ("2027-03-22 09:45", "SALE", "SI-5107"),
    ("2027-03-23 16:30", "SALE", "SI-5111"),
    ("2027-03-24 08:30", "RECV", "PL-2705"),
    ("2027-03-26 12:15", "SALE", "SI-5112"),
    ("2027-03-29 09:10", "SALE", "SI-5113"),
    ("2027-03-30 14:40", "SALE", "SI-5114"),
    ("2027-03-31 10:50", "SALE", "SI-5115"),
    ("2027-04-02 08:30", "RECV", "PL-2706"),
    ("2027-04-02 15:25", "SALE", "SI-5116"),
    ("2027-04-03 10:30", "RETURN", ("SC-61", "HOS2", 6, "C-406", "SI-5111")),
    ("2027-04-06 08:30", "RECV", "PL-2707"),
    ("2027-04-08 09:35", "SALE", "SI-5117"),
    ("2027-04-09 08:30", "RECV", "PL-2708"),
    ("2027-04-11 13:55", "SALE", "SI-5118"),
    ("2027-04-13 08:30", "RECV", "PL-2709"),
    ("2027-04-14 10:20", "SALE", "SI-5119"),
    ("2027-04-15 11:45", "SALE", "SI-5120"),
    ("2027-04-16 08:30", "RECV", "PL-2710"),
    ("2027-04-16 15:40", "SUPPRET", ("DN-118", "HOS2", "PL-2709", 40, "Kestrel Liners")),
    ("2027-04-17 14:30", "SALE", "SI-5121"),
    ("2027-04-19 09:05", "SALE", "SI-5122"),
    ("2027-04-20 08:30", "RECV", "PL-2711"),
    ("2027-04-20 14:45", "RETURN", ("SC-62", "ACP3", 4, "C-405", "SI-5106")),
    ("2027-04-22 16:10", "SALE", "SI-5123"),
    ("2027-04-24 10:40", "SALE", "SI-5124"),
    ("2027-04-28 07:50", "FROST", ("FR-07", "LAV2", "PL-2706", 36, "B7")),
    ("2027-04-28 07:50", "FROST", ("FR-07", "LAV2", "PL-2706", 22, "B8")),
    ("2027-04-28 07:50", "FROST", ("FR-07", "FAR7", "OP-FAR7", 12, "B9")),
    ("2027-04-29 11:20", "RETURN", ("SC-63", "LAV2", 8, "C-407", "SI-5109")),
    ("2027-04-29 15:50", "SALE", "SI-5126"),
    ("2027-05-03 08:30", "RECV", "PL-2712"),
    ("2027-05-06 09:25", "SALE", "SI-5127"),
    ("2027-05-07 11:15", "SALE", "SI-5128"),
    ("2027-05-10 14:20", "SALE", "SI-5129"),
    ("2027-05-11 10:05", "SALE", "SI-5130"),
    ("2027-05-12 13:40", "SALE", "SI-5131"),
    ("2027-05-14 09:50", "SALE", "SI-5132"),
    ("2027-05-15 08:30", "RECV", "PL-2713"),
    ("2027-05-18 15:35", "SALE", "SI-5133"),
    ("2027-05-19 08:30", "RECV", "PL-2714"),
    ("2027-05-20 10:25", "SALE", "SI-5134"),
    ("2027-05-24 12:55", "SALE", "SI-5135"),
    ("2027-05-25 11:30", "SALE", "SI-5136"),
    ("2027-05-26 14:15", "SALE", "SI-5137"),
    ("2027-05-27 09:40", "SALE", "SI-5138"),
]


class Lot:
    def __init__(self, ref, variety, in_stock_on, qty_in, base, revised, revised_from, origin):
        self.ref, self.variety, self.in_stock_on = ref, variety, in_stock_on
        self.qty_in, self.held = qty_in, 0
        self.base = D(base)
        self.revised = D(revised) if revised else None
        self.revised_from = revised_from
        self.origin = origin
        self.received = False
        self.emptied_by = None

    def cost_on(self, date):
        if self.revised and date >= self.revised_from:
            return self.revised
        return self.base

    def close_cost(self):
        return self.revised if self.revised else self.base


lots = {l[0]: Lot(*l) for l in LOTS}
for l in lots.values():
    if l.origin == "opening":
        l.held = l.qty_in
        l.received = True

cps = D("0")
frost = D("0")
cps_by_variety = {}
recon = []


def fifo_first(variety):
    avail = [l for l in lots.values() if l.variety == variety and l.received and l.held > 0]
    return sorted(avail, key=lambda l: (l.in_stock_on, l.ref))[0]


for when, kind, payload in EVENTS:
    date = when[:10]
    if kind == "RECV":
        lot = lots[payload]
        lot.received, lot.held = True, lot.qty_in
        recon.append(dict(event_time=when, movement="Receipt", document=payload, counterparty="",
                          variety=lot.variety, lot=payload, plants=lot.qty_in,
                          unit_cost=str(p(lot.base)), cost=str(p(lot.base * lot.qty_in))))
    elif kind == "SALE":
        inv = payload
        cust, variety, need = SALES[inv]
        while need > 0:
            lot = fifo_first(variety)
            take = min(need, lot.held)
            unit = lot.cost_on(date)
            amount = p(unit * take)
            lot.held -= take
            if lot.held == 0:
                lot.emptied_by = ("sale", inv)
            need -= take
            cps += amount
            cps_by_variety[variety] = cps_by_variety.get(variety, D("0")) + amount
            recon.append(dict(event_time=when, movement="Sale", document=inv, counterparty=cust,
                              variety=variety, lot=lot.ref, plants=take,
                              unit_cost=str(p(unit)), cost=str(amount)))
    elif kind == "RETURN":
        ref, variety, qty, cust, orig = payload
        src = [r for r in recon if r["document"] == orig and r["movement"] == "Sale"]
        unit = D(src[-1]["unit_cost"])
        nl = Lot(ref, variety, date, qty, str(unit), None, None, "return")
        nl.received, nl.held = True, qty
        lots[ref] = nl
        amount = p(unit * qty)
        cps -= amount
        cps_by_variety[variety] = cps_by_variety.get(variety, D("0")) - amount
        recon.append(dict(event_time=when, movement="Customer return to stock", document=ref,
                          counterparty=cust, variety=variety, lot=ref, plants=qty,
                          unit_cost=str(p(unit)), cost=str(-amount)))
    elif kind == "SUPPRET":
        ref, variety, lotref, qty, supplier = payload
        lot = lots[lotref]
        unit = lot.cost_on(date)
        lot.held -= qty
        if lot.held == 0:
            lot.emptied_by = ("supplier_return", ref)
        recon.append(dict(event_time=when, movement="Returned to supplier", document=ref,
                          counterparty=supplier, variety=variety, lot=lotref, plants=qty,
                          unit_cost=str(p(unit)), cost=str(p(unit * qty))))
    elif kind == "FROST":
        ref, variety, lotref, qty, bench = payload
        lot = lots[lotref]
        unit = lot.cost_on(date)
        amount = p(unit * qty)
        lot.held -= qty
        if lot.held == 0:
            lot.emptied_by = ("frost", ref)
        frost += amount
        recon.append(dict(event_time=when, movement="Frost write-off", document=f"{ref} bench {bench}",
                          counterparty="", variety=variety, lot=lotref, plants=qty,
                          unit_cost=str(p(unit)), cost=str(amount)))

register = []
for ref, l in sorted(lots.items(), key=lambda kv: (kv[1].in_stock_on, kv[0])):
    cost = l.close_cost()
    if l.held > 0:
        heading = "Held at season close"
        rule = "s.6: lot still holds plants at the close"
    elif l.emptied_by and l.emptied_by[0] == "frost":
        heading = "Frost write-off"
        rule = "s.6: empty lot whose last plants left by a write-off (%s)" % l.emptied_by[1]
    else:
        heading = "Fully drawn"
        rule = "s.6: empty lot, last plants did not leave by a write-off"
        if l.emptied_by and l.emptied_by[0] == "supplier_return":
            rule = "s.6: empty lot emptied by debit note %s (s.5 supplier return, not a write-off)" % l.emptied_by[1]
    register.append(dict(line="sl-" + ref, lot_ref=ref, variety=l.variety, in_stock_on=l.in_stock_on,
                         qty_in=l.qty_in, unit_cost_gbp=str(p(cost)), qty_at_close=l.held,
                         value_at_close_gbp=str(p(cost * l.held)), heading=heading, rule=rule,
                         origin=l.origin))

closing = sum(D(r["value_at_close_gbp"]) for r in register)
opening = sum(l.base * l.qty_in for l in lots.values() if l.origin == "opening")
purch = sum(l.base * l.qty_in for l in lots.values() if l.origin == "purchase")
ret_in = sum(-D(r["cost"]) for r in recon if r["movement"] == "Customer return to stock")
supret = sum(D(r["cost"]) for r in recon if r["movement"] == "Returned to supplier")
credit_sold = sum((D(r["unit_cost"]) - lots[r["lot"]].base) * r["plants"]
                  for r in recon if r["movement"] == "Sale" and lots[r["lot"]].revised)
credit_close = sum((lots[r["lot_ref"]].revised - lots[r["lot_ref"]].base) * r["qty_at_close"]
                   for r in register if lots[r["lot_ref"]].revised)

print("opening stock           ", p(opening))
print("purchases at landed     ", p(purch))
print("accepted credit, sold   ", p(credit_sold))
print("accepted credit, closing", p(credit_close))
print("returns back to stock   ", p(ret_in))
print("sent back to supplier   ", p(supret))
print("frost loss              ", p(frost))
print("closing stock           ", p(closing))
print("cost of plants sold     ", p(cps))
print()
print("bridge check:", p(opening + purch + credit_sold + credit_close - supret - frost - closing),
      "vs cps", p(cps))
print()
for v, a in sorted(cps_by_variety.items()):
    print("  %s  %s" % (v, p(a)))
print("  sum", p(sum(cps_by_variety.values())))

json.dump(recon, open("/workspace/close/recon.json", "w"), indent=1)
json.dump(register, open("/workspace/close/register.json", "w"), indent=1)
json.dump(dict(cps=str(p(cps)), closing=str(p(closing)), frost=str(p(frost)),
               opening=str(p(opening)), purchases=str(p(purch)),
               returns_to_stock=str(p(ret_in)), supplier_returns=str(p(supret)),
               credit_on_sold=str(p(credit_sold)), credit_on_closing=str(p(credit_close)),
               by_variety={k: str(p(v)) for k, v in sorted(cps_by_variety.items())}),
          open("/workspace/close/totals.json", "w"), indent=1)

net = {}
for when, kind, payload in EVENTS:
    if kind == "SALE":
        c, v, q = SALES[payload]
        net[c] = net.get(c, 0) + q
    elif kind == "RETURN":
        ref, v, q, c, orig = payload
        net[c] = net.get(c, 0) - q
print()
for c in sorted(net):
    print(c, net[c])
json.dump(net, open("/workspace/close/net_plants.json", "w"), indent=1)

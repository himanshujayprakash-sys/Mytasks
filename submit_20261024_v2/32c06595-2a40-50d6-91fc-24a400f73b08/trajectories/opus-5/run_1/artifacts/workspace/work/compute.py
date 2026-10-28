import csv, glob, json
from decimal import Decimal, ROUND_HALF_UP

CLOSE = "2026-10-31"

rows = []
for p in sorted(glob.glob("/workspace/work/don_*.csv")):
    with open(p) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("did,"):
                continue
            did, rid, amt, ch, ga, dt, ben, st, date = line.split(",")
            rows.append(dict(did=did, rid=rid, amt=Decimal(amt), ch=ch, ga=ga,
                             dt=dt, ben=ben, st=st, date=date))

assert len(rows) == 1252, len(rows)

# refunds recorded on the supporter care desk but still shown as paid (GA-4, agreement 3.1)
DESK_REFUNDS = {"111154"}

for r in rows:
    r["refunded"] = (r["st"] != "paid") or (r["did"] in DESK_REFUNDS)
    r["by_close"] = r["date"] <= CLOSE

PLACE = {
    "gold bond": (Decimal("650.00"), Decimal("150.00")),
    "late release": (Decimal("800.00"), Decimal("200.00")),
    "own place": (Decimal("250.00"), Decimal("0.00")),
}

runners = {}
with open("/workspace/work/runners.csv") as f:
    for row in csv.DictReader(f):
        runners[row["runner_id"]] = row

offline = {
    "R-2602": "85.00", "R-2604": "45.00", "R-2608": "140.00", "R-2613": "55.00",
    "R-2615": "30.00", "R-2616": "150.00", "R-2620": "60.00", "R-2627": "120.00",
    "R-2632": "210.00", "R-2635": "35.00", "R-2640": "95.00", "R-2642": "320.00",
    "R-2648": "75.00",
}
match = {"R-2620": "250.00", "R-2628": "300.00"}

STARTED = {rid: runners[rid]["result"] in ("Finished", "DNF") for rid in runners}
DEFERRED = {"R-2604", "R-2617", "R-2639"}
WAIVED = {"R-2609", "R-2612"}

out = {}
wf_gross = wf_ref = wf_off = wf_match = Decimal("0.00")

for rid, r in runners.items():
    minimum, fee = PLACE[r["place_type"]]
    mine = [d for d in rows if d["rid"] == rid]
    gross = sum((d["amt"] for d in mine if d["by_close"]), Decimal("0.00"))
    refs = sum((d["amt"] for d in mine if d["by_close"] and d["refunded"]), Decimal("0.00"))
    net = gross - refs
    off = Decimal(offline.get(rid, "0.00"))
    mat = Decimal(match.get(rid, "0.00"))
    raised = net + off + mat
    wf_gross += gross; wf_ref += refs; wf_off += off; wf_match += mat

    elig = [d for d in mine if d["by_close"] and not d["refunded"]
            and d["ch"] == "H" and d["ga"] == "y" and d["dt"] == "i"
            and d["ben"] == ""]
    etot = sum((d["amt"] for d in elig), Decimal("0.00"))
    gift_aid = (etot * Decimal("0.25")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if STARTED[rid]:
        if raised >= minimum:
            outcome, due = "Minimum met", Decimal("0.00")
        elif rid in WAIVED:
            outcome, due = "Shortfall waived", Decimal("0.00")
        else:
            outcome, due = "Shortfall invoiced", minimum - raised
    else:
        if rid in DEFERRED:
            outcome, due = "Deferred to 2027", Decimal("0.00")
        elif fee > 0:
            outcome, due = "Non-starter - place fee invoiced", fee
        else:
            outcome, due = "Non-starter - no charge", Decimal("0.00")

    out[rid] = dict(
        rid=rid, name=r["full_name"], place=r["place_type"], result=r["result"],
        minimum=minimum, gross=gross, refunds=refs, net=net, offline=off,
        match=mat, raised=raised, elig_n=len(elig), elig_tot=etot,
        gift_aid=gift_aid, outcome=outcome, due=due,
    )

team = sum((o["raised"] for o in out.values()), Decimal("0.00"))
print("WATERFALL")
print(" gifts by close (gross)   ", wf_gross)
print(" less refunds/chargebacks ", -wf_ref)
print(" plus offline banked      ", wf_off)
print(" plus employer match      ", wf_match)
print(" = team raised total      ", wf_gross - wf_ref + wf_off + wf_match, "| check", team)

ga_lines = [o for o in out.values() if o["elig_n"] > 0]
print("\nGIFT AID: lines", len(ga_lines),
      "eligible", sum((o["elig_tot"] for o in ga_lines), Decimal("0.00")),
      "claimed", sum((o["gift_aid"] for o in ga_lines), Decimal("0.00")))

from collections import Counter
print("\nOUTCOMES", Counter(o["outcome"] for o in out.values()))
inv = [o for o in out.values() if o["due"] > 0]
print("\nINVOICES", len(inv), "total", sum((o["due"] for o in inv), Decimal("0.00")))
for o in inv:
    print("  ", o["rid"], o["name"], o["outcome"], o["due"])

starters = [o for o in out.values() if STARTED[o["rid"]]]
top = max(o["raised"] for o in starters)
print("\nSHIELD", top, [o["name"] for o in starters if o["raised"] == top])

print("\nPER RUNNER")
for rid in sorted(out):
    o = out[rid]
    print(f"{rid} {o['name'][:24]:<24} {o['place']:<12} {o['result']:<8} min={o['minimum']:>7} "
          f"gross={o['gross']:>8} ref={o['refunds']:>7} off={o['offline']:>7} mat={o['match']:>7} "
          f"raised={o['raised']:>8} ga_n={o['elig_n']:>3} ga_tot={o['elig_tot']:>8} ga={o['gift_aid']:>7} "
          f"{o['outcome']:<33} due={o['due']:>7}")

with open("/workspace/work/computed.json", "w") as f:
    json.dump({k: {kk: str(vv) for kk, vv in v.items()} for k, v in out.items()}, f, indent=1)
with open("/workspace/work/waterfall.json", "w") as f:
    json.dump({"gross": str(wf_gross), "refunds": str(wf_ref), "offline": str(wf_off),
               "match": str(wf_match), "team": str(team)}, f, indent=1)

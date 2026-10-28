"""Build the TS-0815 2026-12-12 vehicle deck plan under DLS-4 second issue + T-26 second issue."""
import json
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

# ---------------------------------------------------------------- source data
# length_m / height_m / weight_kg already carry every valid amendment.
# amend = note on what moved, src = where it lives.
V = {}


def veh(ref, kind, length, height, weight, cargo="", dg=None, booked="", mobile="",
        ticket="", lifeline=False, amend=None):
    V[ref] = dict(ref=ref, kind=kind, length=D(length), height=D(height),
                  weight=int(weight), cargo=cargo, dg=dg, booked=booked,
                  mobile=mobile, ticket=ticket, lifeline=lifeline,
                  amend=amend or [])


# --- lifeline ---------------------------------------------------------------
veh("TSF-2203", "tanker", "10.5", "3.70", 19500,
    "heating kerosene for Ronsay school and the care home",
    dg=dict(un="UN1223", cls="3"), booked="2026-10-08T08:30",
    mobile="+447700960074", ticket="41003", lifeline=True,
    amend=["weight 26,000 -> 19,500 kg (account customer wrote on freight account ticket 43002, 2026-12-10 14:35, CoC 4.2)"])
veh("TSF-2208", "van", "5.4", "2.40", 3200,
    "medical supplies and pharmacy order for the health centre",
    booked="2026-10-15T11:20", mobile="+447700960259", ticket="41008", lifeline=True)
veh("TSF-2215", "livestock lorry", "13.2", "4.45", 24000,
    "sheep returning to the island farms", booked="2026-10-26T06:50",
    mobile="+447700960518", ticket="41015", lifeline=True)
veh("TSF-2222", "van", "5.9", "2.45", 3300, "island mail and parcels",
    booked="2026-11-04T07:15", mobile="+447700960777", ticket="41022", lifeline=True,
    amend=["height 2.05 -> 2.45 m (account driver, freight messaging line, 2026-12-10 17:05, CoC 4.2)"])
veh("TSF-2290", "tanker", "12.0", "3.80", 31600,
    "diesel for the island power station", dg=dict(un="UN1202", cls="3"),
    booked="2026-12-10T16:40", mobile="+447700955290", ticket="", lifeline=True,
    amend=["late freight-desk booking by mail (msg-f62b5ced17); booking time = time of mail",
           "weight 32,000 -> 31,600 kg (weighbridge reading WR-80206)"])

# --- commercial (over 3,500 kg or over 6.0 m) -------------------------------
veh("TSF-2201", "rigid lorry", "16.5", "4.30", 43900,
    "groceries and chilled goods for Ronsay Stores", booked="2026-10-05T09:12",
    mobile="+447700960000", ticket="41001",
    amend=["weight 36,000 -> 43,900 kg (reading WR-80195 as restated by the signed weighbridge closeout correction, 2026-12-11 17:55; the morning log export and the pre-closeout table both showed 36,400 kg)"])
veh("TSF-2205", "articulated lorry", "13.6", "4.05", 30200, "timber and blockwork",
    booked="2026-10-12T10:05", mobile="+447700960148", ticket="41005",
    amend=["weight 30,500 -> 30,200 kg (weighbridge reading WR-80204)"])
veh("TSF-2206", "campervan", "6.8", "2.90", 3650, booked="2026-10-13T12:44",
    mobile="+447700960185", ticket="41006")
veh("TSF-2211", "rigid lorry", "10.0", "3.90", 11200,
    "swimming pool chemicals", dg=dict(un="UN1791", cls="8"),
    booked="2026-10-20T09:45", mobile="+447700960370", ticket="41011",
    amend=["DG UN1748 class 5.1 -> UN1791 class 8 (named DG safety adviser K. Ferrier in writing, 2026-12-04 10:20, DLS-4 s4)"])
veh("TSF-2214", "rigid lorry", "9.5", "3.60", 15200, "fish feed in bags",
    booked="2026-10-23T14:00", mobile="+447700960481", ticket="41014",
    amend=["weight 15,000 -> 15,200 kg (weighbridge reading WR-80212)"])
veh("TSF-2216", "campervan", "7.2", "3.05", 3790, booked="2026-10-27T17:35",
    mobile="+447700960555", ticket="41016",
    amend=["weight 3,800 -> 3,790 kg (weighbridge reading WR-80220)"])
veh("TSF-2219", "rigid lorry", "8.6", "3.40", 14000, "cleaning acids in drums",
    dg=dict(un="UN1760", cls="8"), booked="2026-10-30T10:30",
    mobile="+447700960666", ticket="41019")
veh("TSF-2224", "skip lorry", "8.2", "3.50", 16900, "empty skips",
    booked="2026-11-06T08:40", mobile="+447700960851", ticket="41024",
    amend=["weight 21,000 -> 16,900 kg (latest weighbridge reading WR-80241, 2026-12-11 16:35; not on the morning log export)",
           "length change to 9.4 m DISREGARDED (freight line 2026-12-11 19:10, after the 18:00 deadline, CoC 4.2)"])
veh("TSF-2227", "tipper", "13.6", "4.00", 28600, "crushed stone for the pier road",
    booked="2026-11-11T09:30", mobile="+447700960962", ticket="41027",
    amend=["length 10.0 -> 13.6 m (customer wrote on ticket 41027, 2026-12-10 15:20, CoC 4.2)",
           "weight 28,000 -> 28,600 kg (weighbridge reading WR-80205)"])
veh("TSF-2230", "removal lorry", "11.0", "4.10", 15800, "household furniture",
    booked="2026-11-16T09:00", mobile="+447700961073", ticket="41030",
    amend=["weight 16,000 -> 15,800 kg (weighbridge reading WR-80214)"])
veh("TSF-2233", "van", "5.6", "2.05", 3640, "joinery tools and kitchen units",
    booked="2026-11-19T13:20", mobile="+447700961184", ticket="41033",
    amend=["weight 3,400 -> 3,640 kg (weighbridge reading WR-80165)"])
veh("TSF-2236", "lorry with boat", "12.0", "4.95", 17000, "fishing boat on a cradle",
    booked="2026-11-24T10:15", mobile="+447700961295", ticket="41036")
veh("TSF-2238", "van", "6.4", "2.60", 3480, "lithium batteries for the wind farm",
    dg=dict(un="UN3480", cls="9"), booked="2026-11-26T08:55",
    mobile="+447700961369", ticket="41038")
veh("TSF-2240", "low loader", "14.5", "3.90", 44600,
    "tracked excavator for the pier works", booked="2026-11-30T07:40",
    mobile="+447700961443", ticket="41040",
    amend=["weight 44,000 -> 44,600 kg (weighbridge reading WR-80198)"])

# --- all other vehicles -----------------------------------------------------
others = [
    ("TSF-2202", "car", "4.4", "1.52", 1480, "2026-10-06T19:40", "+447700960037", "41002"),
    ("TSF-2204", "car", "4.7", "2.35", 1620, "2026-10-09T21:15", "+447700960111", "41004"),
    ("TSF-2207", "car", "4.6", "1.55", 1550, "2026-10-14T07:58", "+447700960222", "41007"),
    ("TSF-2209", "car", "4.8", "2.25", 1900, "2026-10-16T18:02", "+447700960296", "41009"),
    ("TSF-2210", "car", "4.3", "1.48", 1390, "2026-10-19T20:30", "+447700960333", "41010"),
    ("TSF-2213", "car", "4.5", "1.51", 1500, "2026-10-22T08:25", "+447700960444", "41013"),
    ("TSF-2217", "car", "4.2", "1.45", 1350, "2026-10-28T09:05", "+447700960592", "41017"),
    ("TSF-2218", "car", "4.6", "1.56", 1600, "2026-10-29T22:14", "+447700960629", "41018"),
    ("TSF-2220", "car", "4.7", "1.50", 1700, "2026-11-02T12:00", "+447700960703", "41020"),
    ("TSF-2221", "car", "4.6", "1.54", 1580, "2026-11-03T16:45", "+447700960740", "41021"),
    ("TSF-2223", "car", "4.4", "1.47", 1450, "2026-11-05T19:25", "+447700960814", "41023"),
    ("TSF-2225", "car", "4.8", "1.58", 1760, "2026-11-09T10:10", "+447700960888", "41025"),
    ("TSF-2226", "car", "4.5", "1.53", 1520, "2026-11-10T15:55", "+447700960925", "41026"),
    ("TSF-2228", "car", "4.6", "1.49", 1610, "2026-11-12T20:40", "+447700960999", "41028"),
    ("TSF-2229", "car", "4.3", "1.50", 1420, "2026-11-13T11:05", "+447700961036", "41029"),
    ("TSF-2231", "car", "4.7", "1.55", 1690, "2026-11-17T18:30", "+447700961110", "41031"),
    ("TSF-2232", "car", "4.4", "1.52", 1470, "2026-11-18T08:05", "+447700961147", "41032"),
    ("TSF-2234", "car", "4.6", "1.51", 1560, "2026-11-20T21:05", "+447700961221", "41034"),
    ("TSF-2235", "car", "4.5", "1.54", 1500, "2026-11-23T09:50", "+447700961258", "41035"),
    ("TSF-2237", "car", "4.8", "1.57", 1780, "2026-11-25T14:30", "+447700961332", "41037"),
    ("TSF-2239", "car", "4.4", "1.48", 1440, "2026-10-11T19:00", "+447700961406", "41039"),
    ("TSF-2241", "car", "4.6", "1.50", 1590, "2026-12-01T12:25", "+447700961480", "41041"),
    ("TSF-2242", "car", "4.7", "1.56", 1700, "2026-12-02T17:10", "+447700961517", "41042"),
    ("TSF-2243", "car", "4.5", "1.49", 1510, "2026-12-03T09:35", "+447700961554", "41043"),
    ("TSF-2244", "car", "4.6", "1.53", 1620, "2026-10-18T08:00", "+447700961591", "41044"),
    ("TSF-2245", "car", "4.5", "1.50", 1530, "2026-12-05T10:20", "+447700961628", "41045"),
    ("TSF-2246", "car", "4.7", "1.55", 1660, "2026-12-06T18:45", "+447700961665", "41046"),
    ("TSF-2247", "car", "4.4", "1.47", 1460, "2026-12-07T09:15", "+447700961702", "41047"),
    ("TSF-2248", "car", "4.6", "1.52", 1570, "2026-12-08T13:30", "+447700961739", "41048"),
]
for r, k, L, H, W, b, m, t in others:
    veh(r, k, L, H, W, booked=b, mobile=m, ticket=t)

V["TSF-2204"]["amend"] = ["height 1.49 -> 2.35 m, roof box (customer wrote on ticket 41004, 2026-12-09 12:30, CoC 4.2)"]
V["TSF-2221"]["amend"] = ["length change to 7.6 m DISREGARDED (ticket 41021, 2026-12-11 19:20, after the 18:00 deadline, CoC 4.2)"]

# cancelled by customer
veh("TSF-2212", "car", "4.9", "1.60", 1840, booked="2026-10-21T13:10",
    mobile="+447700960407", ticket="41012",
    amend=["cancelled by the customer on ticket 41012, 2026-12-11 09:05, before the 18:00 deadline (CoC 4.2)"])

# ------------------------------------------------------------- vessel / rules
SPACING = D("0.6")
HOIST_CLEAR = D("2.10")
HOIST_WT = 3500
DEADWEIGHT = 290000

LANES = {  # usable length, clearance, deck, out of use + why
    "U1": dict(L=D("24.0"), clear=D("2.10"), deck="Upper", out=None),
    "U2": dict(L=D("24.0"), clear=D("2.10"), deck="Upper", out=None),
    "U3": dict(L=D("24.0"), clear=D("2.10"), deck="Upper", out=None),
    "U4": dict(L=D("24.0"), clear=D("2.10"), deck="Upper",
               out="lane out of use - chief engineer's notice 2026-12-09 (hoist section 4 failed its check)"),
    "M1": dict(L=D("36.0"), clear=D("4.80"), deck="Main", out=None),
    "M2": dict(L=D("52.0"), clear=D("4.80"), deck="Main", out=None),
    "M3": dict(L=D("52.0"), clear=D("4.80"), deck="Main", out=None),
    "M4": dict(L=D("41.5"), clear=D("4.80"), deck="Main", out=None),
    "M5": dict(L=D("52.0"), clear=D("4.20"), deck="Main", out=None),
}
# M3 44.0 (master 2026-12-10) superseded by master's latest notice 2026-12-11:
# M4 41.5 and M3 back to full 52.0.

SEPARATE = {frozenset(("3", "5.1")), frozenset(("2.1", "5.1")), frozenset(("5.1", "8"))}

RATES = [(D("2.10"), D("7.80")), (D("3.00"), D("9.60")), (None, D("12.40"))]


def rate_for(h):
    for cap, r in RATES:
        if cap is None or h <= cap:
            return r


def band_for(h):
    if h <= D("2.10"):
        return "up to 2.10 m"
    if h <= D("3.00"):
        return "over 2.10 m up to 3.00 m"
    return "over 3.00 m"


def p(x):
    return x.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def charged_length(L):
    # round up to the next half metre
    halves = (L / D("0.5")).to_integral_value(rounding="ROUND_CEILING")
    return halves * D("0.5")


def fare_of(v):
    cl = charged_length(v["length"])
    rate = rate_for(v["height"])
    lc = cl * rate
    reb = lc * D("0.35") if v["lifeline"] else D(0)
    sur = lc * D("0.20") if v["dg"] else D(0)
    return dict(charged_length=cl, rate=rate, length_charge=p(lc),
                rebate=p(reb), surcharge=p(sur), fare=p(lc - reb + sur),
                band=band_for(v["height"]))


# ------------------------------------------------------------- loading order
def group(v):
    if v["lifeline"]:
        return 0
    if v["weight"] > 3500 or v["length"] > D("6.0"):
        return 1
    return 2


order = sorted(V.values(), key=lambda v: (group(v), v["booked"], v["ref"]))

# ------------------------------------------------------------------- planning
used = {k: D(0) for k in LANES}
contents = {k: [] for k in LANES}
placed_weight = 0
result = {}
trace = []

for v in order:
    ref = v["ref"]
    rej = []

    if ref == "TSF-2212":
        result[ref] = dict(status="Cancelled by customer", lane=None, deck=None)
        trace.append(dict(ref=ref, rejects=[], outcome="Cancelled by customer"))
        continue

    if v["dg"]:
        # declaration validity decided outside the lane loop
        pass

    # refusals that precede lane trial
    bad_dg = {
        "TSF-2219": "declaration signed by R. Fennimore on 2026-12-04, struck off the Appendix D register on 2026-11-30",
        "TSF-2238": "declaration scan carries no signature and no date of signing",
    }
    if ref in bad_dg:
        result[ref] = dict(status="Refused - DG declaration not valid", lane=None,
                           deck=None, why=bad_dg[ref])
        trace.append(dict(ref=ref, rejects=[], outcome="Refused - DG declaration not valid"))
        continue

    if all(v["height"] > LANES[k]["clear"] for k in LANES):
        result[ref] = dict(status="Refused - outside vessel limits", lane=None, deck=None,
                           why="height %.2f m exceeds every lane's clearance" % v["height"])
        trace.append(dict(ref=ref, rejects=[], outcome="Refused - outside vessel limits"))
        continue

    # Every lane is recorded, so the reconciliation shows what ruled each one out.
    # The gates below reproduce the trial order in DLS-4 s3 exactly: a DG vehicle can
    # only ever win M1, a vehicle over the hoistable limits can only ever win M2-M5.
    cand = ["U1", "U2", "U3", "U4", "M1", "M2", "M3", "M4", "M5"]
    hoistable = v["height"] <= HOIST_CLEAR and v["weight"] <= HOIST_WT

    got = None
    for k in cand:
        ln = LANES[k]
        if v["dg"] and k != "M1":
            rej.append((k, "DLS-4 s3: a vehicle carrying dangerous goods goes only in lane M1"))
            continue
        if not v["dg"] and k == "M1":
            rej.append((k, "lane M1 is the dangerous goods lane and takes nothing else"))
            continue
        if ln["out"]:
            rej.append((k, ln["out"]))
            continue
        if k.startswith("U") and not v["dg"] and not hoistable:
            why = ("vehicle %.2f m is over the %.2f m hoistable deck clearance"
                   % (v["height"], HOIST_CLEAR)) if v["height"] > HOIST_CLEAR else (
                   "vehicle %d kg is over the %d kg hoistable deck weight limit"
                   % (v["weight"], HOIST_WT))
            rej.append((k, why))
            continue
        if v["height"] > ln["clear"]:
            rej.append((k, "vehicle %.2f m exceeds the lane clearance %.2f m" % (v["height"], ln["clear"])))
            continue
        if v["dg"]:
            clash = [o for o in contents[k]
                     if frozenset((v["dg"]["cls"], V[o]["dg"]["cls"])) in SEPARATE]
            if clash:
                rej.append((k, "class %s must be separated from class %s already in the lane (%s)"
                            % (v["dg"]["cls"], V[clash[0]]["dg"]["cls"], clash[0])))
                continue
        need = used[k] + v["length"] + SPACING
        if need > ln["L"]:
            rej.append((k, "needs %.1f m of %.1f m usable; %.1f m already used" % (need, ln["L"], used[k])))
            continue
        if placed_weight + v["weight"] > DEADWEIGHT:
            rej.append((k, "would take the deck past the %d kg vehicle deadweight" % DEADWEIGHT))
            continue
        got = k
        break

    if got:
        used[got] += v["length"] + SPACING
        contents[got].append(ref)
        placed_weight += v["weight"]
        result[ref] = dict(status="Loaded", lane=got, deck=LANES[got]["deck"])
        trace.append(dict(ref=ref, rejects=rej, outcome="Loaded", lane=got))
    else:
        result[ref] = dict(status="Overflow - next sailing", lane=None, deck=None)
        trace.append(dict(ref=ref, rejects=rej, outcome="Overflow - next sailing"))

# ------------------------------------------------------------------- output
for v in order:
    r = result[v["ref"]]
    r["fare"] = fare_of(v)["fare"] if r["status"] == "Loaded" else D("0.00")
    r["calc"] = fare_of(v)

out = dict(
    order=[v["ref"] for v in order],
    result={k: dict(status=r["status"], lane=r["lane"], deck=r["deck"],
                    fare=str(r["fare"]),
                    calc={kk: str(vv) for kk, vv in r["calc"].items()},
                    why=r.get("why", ""))
            for k, r in result.items()},
    trace=[dict(ref=t["ref"], outcome=t["outcome"], lane=t.get("lane"),
                rejects=[[a, b] for a, b in t["rejects"]]) for t in trace],
    lane_used={k: str(used[k]) for k in LANES},
    lane_left={k: str(LANES[k]["L"] - used[k]) for k in LANES},
    lane_contents=contents,
    placed_weight=placed_weight,
    vehicles={k: dict(kind=v["kind"], length=str(v["length"]), height=str(v["height"]),
                      weight=v["weight"], cargo=v["cargo"],
                      dg=v["dg"], booked=v["booked"], mobile=v["mobile"],
                      ticket=v["ticket"], lifeline=v["lifeline"],
                      amend=v["amend"], group=group(v))
              for k, v in V.items()},
)
json.dump(out, open("/workspace/plan.json", "w"), indent=1)

loaded = [r for r in result.values() if r["status"] == "Loaded"]
rev = sum((r["fare"] for r in loaded), D(0))
print("loaded", len(loaded), "revenue", rev)
for k in LANES:
    print(k, "used", used[k], "left", LANES[k]["L"] - used[k], contents[k])
for s in ("Overflow - next sailing", "Refused - outside vessel limits",
          "Refused - DG declaration not valid", "Cancelled by customer"):
    print(s, [k for k, r in result.items() if r["status"] == s])
print("deck weight", placed_weight)

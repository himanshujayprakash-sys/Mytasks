"""Quayside depot allocation for delivery Wednesday 2026-12-09.

Rules: TT-4 allocation terms, third edition (in force for delivery days on or
after 2026-11-23). Prices: PL-12 second issue (deliveries on or after
2026-11-30). PL-12 corrigendum 1 commences 2027-01-04 and does not apply.
"""

from decimal import Decimal, ROUND_HALF_UP

DELIVERY_DATE = "2026-12-09"
CUTOFF = "2026-12-08T06:00"

PRICE = {
    "P-11": Decimal("14.40"),
    "P-12": Decimal("9.60"),
    "P-13": Decimal("11.25"),
    "P-14": Decimal("8.35"),
    "P-15": Decimal("11.40"),
    "P-16": Decimal("13.75"),
    "P-17": Decimal("17.20"),
    "P-18": Decimal("10.20"),
}
PRODUCT_NAME = {
    "P-11": "Vine tomatoes",
    "P-12": "Iceberg lettuce",
    "P-13": "Cos lettuce",
    "P-14": "Leeks",
    "P-15": "Chestnut mushrooms",
    "P-16": "Clementines",
    "P-17": "Tenderstem broccoli",
    "P-18": "Salad tomatoes",
}
DISCOUNT = {"A": Decimal("0.06"), "B": Decimal("0.04"),
            "C": Decimal("0"), "D": Decimal("0")}
MIN_DROP = Decimal("50.00")
SUBSTITUTE = {"P-11": "P-18", "P-12": "P-13"}

DN = {"P-11": 36, "P-12": 18, "P-13": 15, "P-14": 17,
      "P-15": 22, "P-16": 20, "P-17": 14, "P-18": 26}
REJECTS = {"P-11": 3, "P-12": 2, "P-14": 1, "P-15": 2, "P-18": 1}
CARRY_OVER = [
    ("L-881", "P-11", 4, "2026-12-10", 4, "available", True,
     "Quayside bay 4, best-before on or after the delivery date, available"),
    ("L-883", "P-11", 3, "2026-12-12", 5, "quality hold", False,
     "quality hold; QC inspection log 2026-12-07 pending, not released and verified"),
    ("L-877", "P-12", 3, "2026-12-11", 6, "quality hold", True,
     "QC inspection log 2026-12-07 shows released and verified, so off hold"),
    ("L-874", "P-14", 6, "2026-12-08", 3, "available", False,
     "best-before 2026-12-08 is before the delivery date"),
    ("L-869", "P-16", 5, "2026-12-05", 2, "available", False,
     "best-before 2026-12-05 is before the delivery date"),
    ("L-886", "P-17", 2, "2026-12-11", 7, "available", True,
     "Quayside bay 7, best-before on or after the delivery date, available"),
    ("L-890", "P-11", 5, "2026-12-12", 16, "available", False,
     "bay 16 is Northgate stock on the cold store bay plan"),
    ("L-891", "P-14", 4, "2026-12-11", 17, "available", False,
     "bay 17 is Northgate stock on the cold store bay plan"),
]


def stock():
    s = {p: DN[p] - REJECTS.get(p, 0) for p in DN}
    for _lot, p, cases, _bb, _bay, _st, counts, _why in CARRY_OVER:
        if counts:
            s[p] += cases
    return s


ACCOUNTS = {
    "EF-2101": ("A", True, "Brackenmoor Community Hospital kitchen"),
    "EF-2102": ("A", True, "Ashlyn House Care Home"),
    "EF-2103": ("A", False, "St Brannoc's Care Home"),
    "EF-2104": ("A", False, "Tregellas Lodge Nursing Home"),
    "EF-2201": ("B", True, "Penhallow Primary School"),
    "EF-2202": ("B", False, "Ellisford Academy"),
    "EF-2203": ("B", True, "County Hall staff restaurant"),
    "EF-2204": ("B", False, "St Keverne Primary School"),
    "EF-2205": ("B", False, "Ellisford Leisure Centre cafe"),
    "EF-2206": ("B", False, "Quayside Day Nursery"),
    "EF-2305": ("B", False, "Saltings Brasserie"),
    "EF-2301": ("C", True, "The Harbour Kitchen"),
    "EF-2302": ("C", False, "Ristorante Valli"),
    "EF-2303": ("C", True, "Copper Kettle Tearooms"),
    "EF-2304": ("C", True, "Mariner's Rest Inn"),
    "EF-2306": ("C", True, "Fig and Fennel Deli"),
    "EF-2307": ("C", False, "Gull Street Fish Bar"),
    "EF-2308": ("C", False, "The Lantern Cafe"),
    "EF-2309": ("C", True, "Wrecker's Arms"),
    "EF-2310": ("C", False, "Old Custom House Bistro"),
    "EF-2401": ("D", True, "Pascoe's Greengrocer"),
    "EF-2402": ("D", False, "Ellisford Farm Shop"),
    "EF-2403": ("D", True, "Quay Market stall 7"),
    "EF-2404": ("D", True, "Treloar Grocers"),
    "EF-2405": ("D", False, "Corner Basket"),
    "EF-2406": ("D", False, "Harbourside Mini-Mart"),
}

CREDIT_STOP = {
    "EF-2405": "INV-31744 not cleared on the accounts ledger at the cut-off",
}

LINES = [
    ("QO-40116", "EF-2401", "P-11", 6, "2026-12-03T07:40", False, ""),
    ("QO-40117", "EF-2401", "P-12", 4, "2026-12-03T07:40", False, ""),
    ("QO-40118", "EF-2401", "P-16", 4, "2026-12-03T07:40", False, ""),
    ("QO-40120", "EF-2101", "P-11", 6, "2026-12-03T08:12", False, ""),
    ("QO-40121", "EF-2101", "P-12", 7, "2026-12-03T08:12", False,
     "voicemail 2026-12-07 18:52, night desk transcript: 4 -> 7"),
    ("QO-40122", "EF-2101", "P-16", 4, "2026-12-03T08:12", False, ""),
    ("QO-40126", "EF-2102", "P-11", 4, "2026-12-03T09:40", False, ""),
    ("QO-40127", "EF-2102", "P-14", 3, "2026-12-03T09:40", False, ""),
    ("QO-40128", "EF-2102", "P-15", 2, "2026-12-03T09:40", False, ""),
    ("QO-40130", "EF-2301", "P-11", 4, "2026-12-03T10:25", False, ""),
    ("QO-40131", "EF-2301", "P-12", 3, "2026-12-03T10:25", False, ""),
    ("QO-40132", "EF-2301", "P-14", 2, "2026-12-03T10:25", False,
     "mail asking for 2 more cases of leeks arrived 2026-12-08 06:40, after the cut-off"),
    ("QO-40135", "EF-2202", "P-12", 3, "2026-12-03T11:30", False, ""),
    ("QO-40136", "EF-2202", "P-15", 4, "2026-12-03T11:30", False, ""),
    ("QO-40137", "EF-2202", "P-16", 4, "2026-12-03T11:30", False, ""),
    ("QO-40142", "EF-2302", "P-11", 6, "2026-12-03T12:50", False, ""),
    ("QO-40143", "EF-2302", "P-15", 3, "2026-12-03T12:50", False, ""),
    ("QO-40144", "EF-2302", "P-17", 2, "2026-12-03T12:50", False, ""),
    ("QO-40149", "EF-2104", "P-11", 5, "2026-12-03T14:20", False, ""),
    ("QO-40150", "EF-2104", "P-12", 3, "2026-12-03T14:20", False, ""),
    ("QO-40151", "EF-2104", "P-14", 2, "2026-12-03T14:20", False, ""),
    ("QO-40163", "EF-2306", "P-11", 7, "2026-12-03T16:45", False,
     "mail 2026-12-07 10:12: 5 -> 7"),
    ("QO-40164", "EF-2306", "P-13", 3, "2026-12-03T16:45", False, ""),
    ("QO-40174", "EF-2103", "P-11", 3, "2026-12-04T07:55", False,
     "service desk reply on ticket 5104, 2026-12-07 16:20: 8 -> 3"),
    ("QO-40175", "EF-2103", "P-16", 5, "2026-12-04T07:55", True,
     "service desk reply on ticket 5104, 2026-12-07 16:20: cancelled"),
    ("QO-40176", "EF-2103", "P-17", 2, "2026-12-04T07:55", False, ""),
    ("QO-40181", "EF-2305", "P-11", 5, "2026-12-04T09:20", False, ""),
    ("QO-40182", "EF-2305", "P-12", 3, "2026-12-04T09:20", False, ""),
    ("QO-40183", "EF-2305", "P-16", 3, "2026-12-04T09:20", False,
     "service desk reply asking for 2 more cases arrived 2026-12-08 07:35, after the cut-off"),
    ("QO-40187", "EF-2201", "P-11", 3, "2026-12-04T10:05", False, ""),
    ("QO-40188", "EF-2201", "P-12", 4, "2026-12-04T10:05", False, ""),
    ("QO-40189", "EF-2201", "P-14", 2, "2026-12-04T10:05", False, ""),
    ("QO-40196", "EF-2403", "P-11", 4, "2026-12-04T12:15", False, ""),
    ("QO-40197", "EF-2403", "P-14", 2, "2026-12-04T12:15", False, ""),
    ("QO-40198", "EF-2403", "P-18", 3, "2026-12-04T12:15", False, ""),
    ("QO-40200", "EF-2204", "P-15", 2, "2026-12-04T13:45", False, ""),
    ("QO-40201", "EF-2204", "P-16", 3, "2026-12-04T13:45", False, ""),
    ("ADD-EF-2204-P-14", "EF-2204", "P-14", 4, "2026-12-07T12:30", False,
     "line added by mail 2026-12-07 12:30; no order book reference"),
    ("QO-40215", "EF-2303", "P-12", 2, "2026-12-04T15:35", False, ""),
    ("QO-40216", "EF-2303", "P-16", 2, "2026-12-04T15:35", False, ""),
    ("QO-40217", "EF-2303", "P-18", 3, "2026-12-04T15:35", False, ""),
    ("QO-40225", "EF-2309", "P-11", 2, "2026-12-04T18:05", False, ""),
    ("QO-40226", "EF-2309", "P-12", 2, "2026-12-04T18:05", False, ""),
    ("QO-40227", "EF-2309", "P-16", 2, "2026-12-04T18:05", False, ""),
    ("QO-40235", "EF-2402", "P-12", 3, "2026-12-05T08:50", False, ""),
    ("QO-40236", "EF-2402", "P-15", 4, "2026-12-05T08:50", False, ""),
    ("QO-40237", "EF-2402", "P-17", 2, "2026-12-05T08:50", False, ""),
    ("QO-40239", "EF-2203", "P-11", 2, "2026-12-05T09:15", False, ""),
    ("QO-40240", "EF-2203", "P-13", 3, "2026-12-05T09:15", False,
     "voicemail asking for 5 cases was left 2026-12-08 06:25, after the cut-off"),
    ("QO-40242", "EF-2203", "P-18", 2, "2026-12-05T09:15", False, ""),
    ("QO-40248", "EF-2206", "P-12", 2, "2026-12-05T12:00", False, ""),
    ("QO-40249", "EF-2206", "P-17", 4, "2026-12-05T12:00", False,
     "WhatsApp message 2026-12-07 13:10: 2 -> 4"),
    ("QO-40258", "EF-2405", "P-15", 3, "2026-12-05T14:55", False, ""),
    ("QO-40259", "EF-2405", "P-16", 3, "2026-12-05T14:55", False, ""),
    ("QO-40270", "EF-2308", "P-11", 2, "2026-12-05T17:30", False, ""),
    ("QO-40271", "EF-2308", "P-17", 3, "2026-12-05T17:30", False, ""),
    ("QO-40279", "EF-2310", "P-14", 3, "2026-12-06T08:30", False, ""),
    ("QO-40280", "EF-2310", "P-15", 1, "2026-12-06T08:30", False, ""),
    ("QO-40281", "EF-2310", "P-16", 2, "2026-12-06T08:30", False, ""),
    ("QO-40290", "EF-2307", "P-12", 2, "2026-12-06T10:40", False, ""),
    ("QO-40291", "EF-2307", "P-14", 2, "2026-12-06T10:40", False, ""),
    ("QO-40292", "EF-2307", "P-15", 3, "2026-12-06T10:40", False, ""),
    ("QO-40293", "EF-2307", "P-18", 2, "2026-12-06T10:40", False, ""),
    ("QO-40297", "EF-2304", "P-11", 3, "2026-12-06T11:05", False, ""),
    ("QO-40298", "EF-2304", "P-14", 3, "2026-12-06T11:05", False, ""),
    ("QO-40299", "EF-2304", "P-15", 3, "2026-12-06T11:05", False, ""),
    ("QO-40310", "EF-2404", "P-11", 3, "2026-12-06T13:25", False, ""),
    ("QO-40311", "EF-2404", "P-12", 2, "2026-12-06T13:25", False, ""),
    ("QO-40312", "EF-2404", "P-14", 3, "2026-12-06T13:25", False, ""),
    ("QO-40328", "EF-2205", "P-18", 2, "2026-12-06T16:10", False, ""),
    ("QO-40346", "EF-2406", "P-11", 2, "2026-12-07T09:10", False, ""),
    ("QO-40347", "EF-2406", "P-16", 2, "2026-12-07T09:10", False, ""),
    ("QO-40348", "EF-2406", "P-18", 2, "2026-12-07T09:10", False, ""),
]

CLASS_ORDER = ["A", "B", "C", "D"]


def money(x):
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def run(withdrawn):
    left = stock()
    alloc = {}
    share = {}
    trace = []
    ties = []

    active = [ln for ln in LINES
              if not ln[5]
              and ln[1] not in withdrawn
              and ln[1] not in CREDIT_STOP]

    for product in sorted(PRICE):
        exhausted = False
        for cls in CLASS_ORDER:
            group = [ln for ln in active
                     if ln[2] == product and ACCOUNTS[ln[1]][0] == cls]
            if not group:
                continue
            if exhausted:
                for ln in group:
                    alloc[ln[0]] = 0
                    trace.append((product, cls, ln[0], ln[1], ln[3], "", 0,
                                  "no cases left for this class"))
                continue
            total = sum(ln[3] for ln in group)
            avail = left[product]
            if avail >= total:
                for ln in group:
                    alloc[ln[0]] = ln[3]
                    trace.append((product, cls, ln[0], ln[1], ln[3], "", ln[3],
                                  "class covered in full"))
                left[product] -= total
                if left[product] == 0:
                    exhausted = True
                continue
            base = {}
            frac = {}
            for ln in group:
                exact = Decimal(avail) * Decimal(ln[3]) / Decimal(total)
                base[ln[0]] = int(exact)
                frac[ln[0]] = exact - int(exact)
                share[ln[0]] = (f"{avail} x {ln[3]}/{total}")
            spare = avail - sum(base.values())
            order = sorted(group, key=lambda l: (-frac[l[0]], l[4], l[1]))
            winners = [l[0] for l in order[:spare]]
            if spare:
                groups = {}
                for ln in group:
                    groups.setdefault(frac[ln[0]], []).append(ln[0])
                for f, refs in groups.items():
                    if len(refs) > 1 and f > 0 and any(r in winners for r in refs) \
                            and not all(r in winners for r in refs):
                        ties.append((product, cls, str(f), refs,
                                     [r for r in refs if r in winners]))
            for ln in group:
                cases = base[ln[0]] + (1 if ln[0] in winners else 0)
                alloc[ln[0]] = cases
                why = ("share rounded down, plus one case on the largest fraction"
                       if ln[0] in winners else "share rounded down")
                trace.append((product, cls, ln[0], ln[1], ln[3], share[ln[0]],
                              cases, why))
            left[product] = 0
            exhausted = True

    subs = []
    short = [ln for ln in active
             if alloc.get(ln[0], 0) < ln[3]
             and ACCOUNTS[ln[1]][1]
             and ln[2] in SUBSTITUTE]
    short.sort(key=lambda l: (CLASS_ORDER.index(ACCOUNTS[l[1]][0]), l[4], l[1]))
    for ln in short:
        sub = SUBSTITUTE[ln[2]]
        if left[sub] <= 0:
            continue
        want = ln[3] - alloc.get(ln[0], 0)
        give = min(want, left[sub])
        left[sub] -= give
        price = min(PRICE[ln[2]], PRICE[sub])
        subs.append((ln[1], sub, give, price, ln[0], ln[2], ln[4]))

    return alloc, subs, share, trace, left, ties


def account_gross(acct, alloc, subs):
    total = Decimal("0")
    for ln in LINES:
        if ln[1] == acct and not ln[5]:
            total += Decimal(alloc.get(ln[0], 0)) * PRICE[ln[2]]
    for s in subs:
        if s[0] == acct:
            total += Decimal(s[2]) * s[3]
    return total


def account_cases(acct, alloc, subs):
    n = sum(alloc.get(ln[0], 0) for ln in LINES if ln[1] == acct and not ln[5])
    n += sum(s[2] for s in subs if s[0] == acct)
    return n


def allocate():
    withdrawn = []
    passes = []
    while True:
        res = run(set(withdrawn))
        alloc, subs = res[0], res[1]
        offenders = []
        for acct, (cls, _ok, _nm) in ACCOUNTS.items():
            if cls not in ("C", "D"):
                continue
            if acct in withdrawn or acct in CREDIT_STOP:
                continue
            if account_cases(acct, alloc, subs) >= 1:
                gross = account_gross(acct, alloc, subs)
                if gross < MIN_DROP:
                    offenders.append((gross, acct))
        offenders.sort(key=lambda t: (t[0], t[1]))
        passes.append((list(withdrawn), res, offenders))
        if not offenders:
            return withdrawn, res, passes
        withdrawn.append(offenders[0][1])


def register_rows(withdrawn, alloc, subs):
    """Final register rows: order lines then substitute supplies."""
    rows = []
    for ln in LINES:
        ref, acct, prod, ordered, at, cancelled, note = ln
        cls = ACCOUNTS[acct][0]
        if cancelled:
            head, cases = "Cancelled by customer", 0
            rule = "cancelled in writing before the cut-off (clause 1)"
        elif acct in CREDIT_STOP:
            head, cases = "Held - credit stop", 0
            rule = "account on credit stop at the cut-off (clause 1)"
        elif acct in withdrawn:
            head, cases = "Withdrawn - below minimum drop", 0
            rule = "account withdrawn under clause 5 and Appendix B"
        else:
            cases = alloc.get(ref, 0)
            if cases == 0:
                head = "Nil - stock exhausted"
                rule = "no cases left for class %s (clause 3)" % cls
            elif cases < ordered:
                head = "Allocated in part"
                rule = "class %s share of the cases left (clause 3)" % cls
            else:
                head = "Allocated in full"
                rule = "class %s covered in full (clause 3)" % cls
        if head in ("Allocated in full", "Allocated in part"):
            value = money(Decimal(cases) * PRICE[prod] * (1 - DISCOUNT[cls]))
            price = PRICE[prod]
        else:
            value = Decimal("0.00")
            price = PRICE[prod]
        rows.append(dict(line="al-" + ref, order_ref=ref, account=acct,
                         cls=cls, product=prod, ordered=ordered,
                         allocated=cases, heading=head, rule=rule,
                         price=price, discount=DISCOUNT[cls], value=value,
                         ordered_at=at, note=note, kind="order"))
    for i, s in enumerate(subs):
        acct, prod, cases, price, for_ref, for_prod, at = s
        cls = ACCOUNTS[acct][0]
        value = money(Decimal(cases) * price * (1 - DISCOUNT[cls]))
        rows.append(dict(line="al-SUB-" + for_ref, order_ref=for_ref,
                         account=acct, cls=cls, product=prod, ordered=0,
                         allocated=cases, heading="Substitute supplied",
                         rule=("substitute for %s under clause 4, charged at the "
                               "lower of the two prices" % for_prod),
                         price=price, discount=DISCOUNT[cls], value=value,
                         ordered_at=at, note="made up against " + for_ref,
                         kind="sub"))
    return rows


if __name__ == "__main__":
    withdrawn, res, passes = allocate()
    alloc, subs, share, trace, left, ties = res
    print("STOCK SHARED OUT:", stock())
    print("STOCK LEFT AFTER SUBSTITUTES:", left)
    print("WITHDRAWN:", withdrawn)
    print()
    for i, (w, r, off) in enumerate(passes):
        print(f"pass {i+1} excluding {w}: offenders={[(str(g), a) for g, a in off]}")
    print()
    print("TIES:", ties)
    print()
    rows = register_rows(withdrawn, alloc, subs)
    tot = Decimal("0")
    bycls = {c: Decimal("0") for c in CLASS_ORDER}
    for r in rows:
        tot += r["value"]
        bycls[r["cls"]] += r["value"]
        print(f"{r['line']:<24}{r['account']} {r['cls']} {r['product']} "
              f"ord={r['ordered']:>2} got={r['allocated']:>2} "
              f"{r['heading']:<31}{r['value']:>8}")
    print()
    print("TOTAL AFTER DISCOUNTS:", tot)
    print("BY CLASS:", {k: str(v) for k, v in bycls.items()})
    delivering = sorted({r["account"] for r in rows if r["allocated"] > 0})
    print("DELIVERING TO", len(delivering), delivering)
    notdel = sorted(set(ACCOUNTS) - set(delivering))
    print("NOT DELIVERING TO", len(notdel), notdel)

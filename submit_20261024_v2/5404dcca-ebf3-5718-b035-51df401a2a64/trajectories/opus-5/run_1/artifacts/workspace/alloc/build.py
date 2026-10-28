"""Compare the keyed register with the terms' result and build the outputs."""

import csv
import json
from decimal import Decimal

from engine import (ACCOUNTS, CARRY_OVER, CLASS_ORDER, CREDIT_STOP, DISCOUNT,
                    DN, LINES, MIN_DROP, PRICE, PRODUCT_NAME, REJECTS,
                    SUBSTITUTE, account_cases, account_gross, allocate, money,
                    register_rows, stock)

EXPORT = "/workspace/data/Quayside/Sheets/keyed_allocation_register_export.csv"

# line -> airtable record id, from the allocation_register table
REC = {
    "al-QO-40116": "recf00aa4a55e61f1", "al-QO-40117": "recddc0e649cf50b1",
    "al-QO-40118": "recf5a18271f3cf1c", "al-QO-40120": "rec1bf78eb37ab481",
    "al-QO-40121": "rec1c0a07a642a35b", "al-QO-40122": "rec953ef61f65bfe0",
    "al-QO-40126": "rec0675d9d035bb35", "al-QO-40127": "reccc5d9686aba837",
    "al-QO-40128": "rec1b973454f208f7", "al-QO-40130": "recbf6d8161db7d0a",
    "al-QO-40131": "rec7f58a5f5958f69", "al-QO-40132": "rec6273d94017b114",
    "al-QO-40135": "reca14333f89382a8", "al-QO-40136": "rec63252501bd20f9",
    "al-QO-40137": "rec3e592ae6f1eb00", "al-QO-40142": "recab2f0a604ba098",
    "al-QO-40143": "rec01a9697028d140", "al-QO-40144": "rec444d7ae57fcff9",
    "al-QO-40149": "recc32b7f6345fa2c", "al-QO-40150": "rec0c488c7f6dcd96",
    "al-QO-40151": "rec2d5b5596999faf", "al-QO-40163": "rec1d37197d27b4c1",
    "al-QO-40164": "recc1e638753f343b", "al-QO-40174": "rec1e156a7091697b",
    "al-QO-40175": "rec00f8c7cf6bd34c", "al-QO-40176": "rec073eb83bace7f2",
    "al-QO-40181": "recf07c78f490f407", "al-QO-40182": "rec869fb36478fcfc",
    "al-QO-40183": "rec14bb684f7559f6", "al-QO-40187": "rec412bf0013bf234",
    "al-QO-40188": "recb0f472923b52af", "al-QO-40189": "recf8795cd11515a3",
    "al-QO-40196": "rec350a5691ccd4f7", "al-QO-40197": "rece4c19ed7dd4aee",
    "al-QO-40198": "reca4e4f56f42d53f", "al-QO-40200": "rec9bb9a9705780ae",
    "al-QO-40201": "recf55484a77c1eb2", "al-QO-40215": "rec428432803990eb",
    "al-QO-40216": "recf37dd780c12d1c", "al-QO-40217": "recf5c1eb1b76ed49",
    "al-QO-40225": "rec147b28322a39eb", "al-QO-40226": "rec429a4336fd40dc",
    "al-QO-40227": "rec29950553dd1dde", "al-QO-40235": "recb7b0f24c5bb98c",
    "al-QO-40236": "rec1d3ecf6a1aeff9", "al-QO-40237": "recf9976fe3a4f8c5",
    "al-QO-40239": "rec18ea7c5839e3f4", "al-QO-40240": "rec867911f600ba65",
    "al-QO-40242": "recc6774a0f18f77d", "al-QO-40248": "reca528db8aa10969",
    "al-QO-40249": "rece2ceb31be84d50", "al-QO-40258": "recc580da6e0e495e",
    "al-QO-40259": "recc2ef9cd4a429a2", "al-QO-40270": "recd631116d9c0d8e",
    "al-QO-40271": "rec719e89ed6fa6e0", "al-QO-40279": "rec0602bb6ff97283",
    "al-QO-40280": "recdc450dc14c885f", "al-QO-40281": "rec3a5917e4d79a36",
    "al-QO-40290": "rec1ea603cc0d8303", "al-QO-40291": "recd87992e6281744",
    "al-QO-40292": "rec744292c640d31d", "al-QO-40293": "rec824b8c9067a436",
    "al-QO-40297": "rec8736c060a561fe", "al-QO-40298": "recee628c7fe2b3ff",
    "al-QO-40299": "rec834dc13475caf7", "al-QO-40310": "rec05a2ed35eb475e",
    "al-QO-40311": "recf5d764a6accfb2", "al-QO-40312": "rec7c98daf0de1297",
    "al-QO-40328": "recd30cbccc695c89", "al-QO-40346": "rec4edff1ca03c496",
    "al-QO-40347": "rec5c00ae2c2bebed", "al-QO-40348": "rec3fddb8d8deab50",
    "al-QO-40164b": "rec63c7698bb93596",
}

BUYER = {
    "EF-2101": ("Delyth Rosewarne", "delyth.rosewarne@3f3481.example"),
    "EF-2102": ("Kenver Polglase", "kenver.polglase@d17173.example"),
    "EF-2103": ("Morwen Tregear", "morwen.tregear@308427.example"),
    "EF-2104": ("Jory Penberthy", "jory.penberthy@4bd672.example"),
    "EF-2201": ("Tamsin Hocking", "tamsin.hocking@9e405f.example"),
    "EF-2202": ("Piran Couch", "piran.couch@66ee8a.example"),
    "EF-2203": ("Elowen Nance", "elowen.nance@3aab88.example"),
    "EF-2204": ("Gwen Trebilcock", "gwen.trebilcock@405710.example"),
    "EF-2205": ("Lowen Bolitho", "lowen.bolitho@6d1d56.example"),
    "EF-2206": ("Demelza Kitto", "demelza.kitto@270a75.example"),
    "EF-2301": ("Bryok Trevail", "bryok.trevail@609019.example"),
    "EF-2302": ("Carlo Valli", "carlo.valli@9d0f1e.example"),
    "EF-2303": ("Ysella Pengelly", "ysella.pengelly@ef20ed.example"),
    "EF-2304": ("Hedra Spargo", "hedra.spargo@2815e7.example"),
    "EF-2305": ("Austol Jago", "austol.jago@6f277f.example"),
    "EF-2306": ("Rosen Eddy", "rosen.eddy@834d98.example"),
    "EF-2307": ("Talan Hosking", "talan.hosking@6123fe.example"),
    "EF-2308": ("Wenna Chegwidden", "wenna.chegwidden@ca1de4.example"),
    "EF-2309": ("Gerens Laity", "gerens.laity@1ddaa7.example"),
    "EF-2310": ("Kerra Tonkin", "kerra.tonkin@690e61.example"),
    "EF-2401": ("Jenna Pascoe", "jenna.pascoe@b31214.example"),
    "EF-2402": ("Nessa Uren", "nessa.uren@e3faed.example"),
    "EF-2403": ("Sowena Rodda", "sowena.rodda@c9ba8a.example"),
    "EF-2404": ("Hammitt Treloar", "hammitt.treloar@cbf67e.example"),
    "EF-2405": ("Ebrel Tremayne", "ebrel.tremayne@c4605e.example"),
    "EF-2406": ("Arthek Rowse", "arthek.rowse@a89833.example"),
}

WA_ID = {f"EF-2{n}": f"4475009110{i:02d}" for i, n in enumerate(
    ["101", "102", "103", "104", "201", "202", "203", "204", "205", "206",
     "301", "302", "303", "304", "305", "306", "307", "308", "309", "310",
     "401", "402", "403", "404", "405", "406"])}
WINDOW_OPEN = {a: True for a in WA_ID}
for a in ("EF-2102", "EF-2304", "EF-2402"):
    WINDOW_OPEN[a] = False
OPTED_IN = {a: True for a in WA_ID}
OPTED_IN["EF-2308"] = False
STOP_REQUESTED = {
    "EF-2104": "asked the depot's customer text line on 2026-12-05 to stop these messages",
    "EF-2307": "asked on service desk ticket 5123 on 2026-12-05 to stop these messages",
}


def main():
    withdrawn, res, passes = allocate()
    alloc, subs, share, trace, left, ties = res
    rows = register_rows(withdrawn, alloc, subs)

    total = sum(r["value"] for r in rows)
    bycls = {c: sum(r["value"] for r in rows if r["cls"] == c) for c in CLASS_ORDER}

    delivering = sorted({r["account"] for r in rows if r["allocated"] > 0})
    notdel = sorted(set(ACCOUNTS) - set(delivering))

    # ---- bridge -------------------------------------------------------
    def gross_ordered(preds):
        return sum(Decimal(l[3]) * PRICE[l[2]] for l in LINES
                   if not l[5] and preds(l))

    opening = gross_ordered(lambda l: True)
    stop_step = gross_ordered(lambda l: l[1] in CREDIT_STOP)
    wd_step = gross_ordered(lambda l: l[1] in withdrawn)
    remaining_ordered = opening - stop_step - wd_step
    gross_allocated = sum(Decimal(r["allocated"]) * r["price"]
                          for r in rows if r["kind"] == "order")
    shortfall_step = remaining_ordered - gross_allocated
    sub_step = sum(Decimal(r["allocated"]) * r["price"]
                   for r in rows if r["kind"] == "sub")
    gross_final = gross_allocated + sub_step
    discount_step = gross_final - total

    bridge = [
        dict(label="Order lines at the 06:00 cut-off, at PL-12 second issue",
             amount=money(opening), running=money(opening),
             detail="72 order lines in the order book for 2026-12-09 plus the line "
                    "EF-2204 added by mail, less the line EF-2103 cancelled; "
                    "priced at the price list before discount"),
        dict(label="Less accounts not delivered: credit stop",
             amount=-money(stop_step),
             running=money(opening - stop_step),
             detail="EF-2405 Corner Basket (QO-40258, QO-40259)"),
        dict(label="Less accounts not delivered: below minimum drop",
             amount=-money(wd_step),
             running=money(opening - stop_step - wd_step),
             detail="EF-2401 Pascoe's Greengrocer, EF-2404 Treloar Grocers, "
                    "EF-2406 Harbourside Mini-Mart"),
        dict(label="Less cases the stock could not cover",
             amount=-money(shortfall_step),
             running=money(gross_allocated),
             detail="short and nil lines across P-11, P-12, P-14, P-15"),
        dict(label="Plus substitutes at the price charged",
             amount=money(sub_step),
             running=money(gross_final),
             detail="9 substitute supplies: P-18 for P-11, P-13 for P-12"),
        dict(label="Less contract discounts (class A 6%, class B 4%)",
             amount=-money(discount_step), running=money(total),
             detail="PL-12 second issue, section 2"),
    ]

    # ---- compare with the keyed register ------------------------------
    keyed = {r["line"]: r for r in csv.DictReader(open(EXPORT))}
    want = {r["line"]: r for r in rows}
    changes = {"correct": [], "update": [], "create": [], "delete": []}
    for line, r in want.items():
        k = keyed.get(line)
        if k is None:
            changes["create"].append(line)
            continue
        same = (k["cases_allocated"] == str(r["allocated"])
                and k["heading"] == r["heading"]
                and k["value_gbp"] == f"{r['value']:.2f}"
                and k["cases_ordered"] == str(r["ordered"]))
        (changes["correct"] if same else changes["update"]).append(line)
    for line in keyed:
        if line not in want:
            changes["delete"].append(line)

    out = dict(
        delivery_date="2026-12-09",
        terms="TT-4 allocation terms, third edition",
        prices="PL-12 Trade price list, second issue",
        stock=stock(), stock_left=left,
        withdrawn=withdrawn,
        credit_stop=CREDIT_STOP,
        total=str(money(total)),
        by_class={k: str(money(v)) for k, v in bycls.items()},
        delivering=delivering, not_delivering=notdel,
        bridge=[dict(label=b["label"], amount=str(b["amount"]),
                     running=str(b["running"]), detail=b["detail"])
                for b in bridge],
        ties=[dict(product=t[0], cls=t[1], fraction=t[2], tied=t[3], won=t[4])
              for t in ties],
        rows=[dict(line=r["line"], order_ref=r["order_ref"],
                   account=r["account"], account_name=ACCOUNTS[r["account"]][2],
                   cls=r["cls"], product=r["product"],
                   product_name=PRODUCT_NAME[r["product"]],
                   ordered=r["ordered"], allocated=r["allocated"],
                   heading=r["heading"], rule=r["rule"],
                   price=str(r["price"]),
                   discount=f"{int(r['discount']*100)}%",
                   value=f"{r['value']:.2f}",
                   share=share.get(r["order_ref"], "") if r["kind"] == "order" else "",
                   ordered_at=r["ordered_at"], note=r["note"], kind=r["kind"],
                   record_id=REC.get(r["line"], ""))
              for r in rows],
        changes=changes,
        passes=[dict(excluded=p[0],
                     offenders=[[str(g), a] for g, a in p[2]])
                for p in passes],
        trace=[dict(product=t[0], cls=t[1], order_ref=t[2], account=t[3],
                    ordered=t[4], share=t[5], allocated=t[6], why=t[7])
               for t in trace],
        subs=[dict(account=s[0], product=s[1], cases=s[2], price=str(s[3]),
                   for_ref=s[4], for_product=s[5], ordered_at=s[6]) for s in subs],
    )

    # per-account message numbers
    msgs = {}
    for a in delivering:
        n = sum(r["allocated"] for r in rows if r["account"] == a)
        m = sum(l[3] for l in LINES if l[1] == a and not l[5])
        msgs[a] = dict(n=n, m=m, window_open=WINDOW_OPEN[a],
                       opted_in=OPTED_IN[a],
                       stop=STOP_REQUESTED.get(a, ""),
                       buyer=BUYER[a][0], email=BUYER[a][1], wa_id=WA_ID[a])
    out["messages"] = msgs

    json.dump(out, open("/workspace/alloc/result.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in
                      ("total", "by_class", "withdrawn", "ties", "changes")},
                     indent=1))
    print("bridge:")
    for b in out["bridge"]:
        print(f"  {b['label']:<62}{b['amount']:>10}  -> {b['running']}")
    print("messages:")
    for a, m in msgs.items():
        print("  ", a, m["n"], "of", m["m"], "window_open", m["window_open"],
              "opted_in", m["opted_in"], m["stop"])


if __name__ == "__main__":
    main()

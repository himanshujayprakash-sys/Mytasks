import json, csv

rec = {}
with open("/workspace/work/records.csv") as f:
    for r in csv.DictReader(f):
        rec[r["runner_id"]] = r

comp = json.load(open("/workspace/work/computed.json"))
runners = {r["runner_id"]: r for r in csv.DictReader(open("/workspace/work/runners.csv"))}

STOP = {"R-2641"}  # STOP text to a hospice number (SC-2)

changes, unchanged = [], []
for rid in sorted(comp):
    c, rr = comp[rid], rec[rid]
    want = {
        "raised_gbp": f'{float(c["raised"]):.2f}',
        "gift_aid_gbp": f'{float(c["gift_aid"]):.2f}',
        "outcome": c["outcome"],
        "amount_due_gbp": f'{float(c["due"]):.2f}',
        "sms_consent": "no" if rid in STOP else runners[rid]["sms_consent_record"],
    }
    delta = {k: (rr[k], v) for k, v in want.items() if rr[k] != v}
    (changes if delta else unchanged).append((rid, delta, want))

print("CORRECT:", len(changes), " LEAVE:", len(unchanged))
for rid, d, w in changes:
    print(rid, runners[rid]["full_name"])
    for k, (was, now) in d.items():
        print(f"    {k}: {was}  ->  {now}")
print("\nUNCHANGED:", ", ".join(r for r, _, _ in unchanged))

json.dump({rid: w for rid, _, w in changes}, open("/workspace/work/to_update.json", "w"), indent=1)
json.dump([rid for rid, _, _ in unchanged], open("/workspace/work/unchanged.json", "w"), indent=1)

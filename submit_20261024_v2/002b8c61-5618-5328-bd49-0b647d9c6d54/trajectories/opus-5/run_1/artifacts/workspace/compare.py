import json
plan = json.load(open("/workspace/plan.json"))

# keyed draft, straight from the loading_plan table (line -> record id, fields)
keyed = {
 "lp-TSF-2201": ("rec0f60b4075234cc", "TSF-2201", "Main", "M2", "Loaded", "204.60"),
 "lp-TSF-2202": ("rec45bb0d297f2510", "TSF-2202", "Upper", "U1", "Loaded", "37.40"),
 "lp-TSF-2203": ("rec41d56370be5b67", "TSF-2203", "Main", "M1", "Loaded", "110.67"),
 "lp-TSF-2204": ("rec31c1df4602e3c7", "TSF-2204", "Upper", "U2", "Loaded", "39.95"),
 "lp-TSF-2205": ("rec14d38d1d8641a1", "TSF-2205", "Main", "M2", "Loaded", "173.60"),
 "lp-TSF-2206": ("rec05198a8834e85b", "TSF-2206", "Main", "M3", "Loaded", "67.20"),
 "lp-TSF-2207": ("rec8a21fad33b4c07", "TSF-2207", "Upper", "U3", "Loaded", "39.10"),
 "lp-TSF-2208": ("rec71368da13a8374", "TSF-2208", "Main", "M2", "Loaded", "34.32"),
 "lp-TSF-2209": ("rec1e3706f523eb36", "TSF-2209", "Upper", "U4", "Loaded", "40.80"),
 "lp-TSF-2210": ("recc891b48ec9baf1", "TSF-2210", "Upper", "U4", "Loaded", "36.55"),
 "lp-TSF-2211": ("rec3eefe80caff918", "TSF-2211", "", "", "Overflow - next sailing", "0.00"),
 "lp-TSF-2212": ("recf7bf8411a12230", "TSF-2212", "Upper", "U4", "Loaded", "41.65"),
 "lp-TSF-2213": ("rec4a0b8ee551d260", "TSF-2213", "Main", "M1", "Loaded", "38.25"),
 "lp-TSF-2214": ("rec8987961bc530b7", "TSF-2214", "Main", "M3", "Loaded", "117.80"),
 "lp-TSF-2215": ("recb756972925f1e5", "TSF-2215", "Main", "M2", "Loaded", "108.81"),
 "lp-TSF-2216": ("rece62f1d343fda72", "TSF-2216", "Main", "M3", "Loaded", "93.00"),
 "lp-TSF-2217": ("recb8575bab87b3b4", "TSF-2217", "Main", "M2", "Loaded", "35.70"),
 "lp-TSF-2218": ("rec0ca7166bf85892", "TSF-2218", "Main", "M2", "Loaded", "39.10"),
 "lp-TSF-2219": ("recd755057e981d98", "TSF-2219", "", "", "Refused - DG declaration not valid", "0.00"),
 "lp-TSF-2220": ("rec6dea435ec85fdb", "TSF-2220", "Main", "M2", "Loaded", "39.95"),
 "lp-TSF-2221": ("rec9885960fccc327", "TSF-2221", "Main", "M2", "Loaded", "39.10"),
 "lp-TSF-2222": ("rec90339d33ae1d94", "TSF-2222", "Upper", "U1", "Loaded", "30.42"),
 "lp-TSF-2223": ("rec8ab6de300cbe3f", "TSF-2223", "Main", "M2", "Loaded", "37.40"),
 "lp-TSF-2224": ("recccd4f783a7e8c4", "TSF-2224", "Main", "M3", "Loaded", "105.40"),
 "lp-TSF-2225": ("rec94fc911a9abd5e", "TSF-2225", "Main", "M2", "Loaded", "40.80"),
 "lp-TSF-2226": ("recfbfccb3f74a528", "TSF-2226", "Main", "M3", "Loaded", "38.25"),
 "lp-TSF-2227": ("rec3ea4d583d0c630", "TSF-2227", "Main", "M3", "Loaded", "124.00"),
 "lp-TSF-2228": ("rec68c6b767cda79c", "TSF-2228", "Main", "M3", "Loaded", "39.10"),
 "lp-TSF-2229": ("rece0fef649fe9988", "TSF-2229", "Main", "M3", "Loaded", "36.55"),
 "lp-TSF-2230": ("rece15b711294e207", "TSF-2230", "Main", "M4", "Loaded", "136.40"),
 "lp-TSF-2231": ("rec740cde7dacc00b", "TSF-2231", "Main", "M3", "Loaded", "39.95"),
 "lp-TSF-2232": ("recb5d2a16a1fb268", "TSF-2232", "Main", "M3", "Loaded", "37.40"),
 "lp-TSF-2233": ("rec99b3c9c7f3bcf3", "TSF-2233", "Main", "M3", "Loaded", "46.80"),
 "lp-TSF-2234": ("rec9c105afeddd7a8", "TSF-2234", "Main", "M4", "Loaded", "39.10"),
 "lp-TSF-2235": ("rec3ae69b6c287d6a", "TSF-2235", "Main", "M4", "Loaded", "38.25"),
 "lp-TSF-2236": ("rec055db388f838b5", "TSF-2236", "", "", "Refused - outside vessel limits", "0.00"),
 "lp-TSF-2237": ("rec1b0ed7eb17fc74", "TSF-2237", "Main", "M4", "Loaded", "40.80"),
 "lp-TSF-2238": ("rec1b5952bfb04803", "TSF-2238", "", "", "Refused - DG declaration not valid", "0.00"),
 "lp-TSF-2239": ("reca0fc8c2d232e0a", "TSF-2239", "Main", "M4", "Loaded", "37.40"),
 "lp-TSF-2240": ("rec0a7c5c5b1f8d6a", "TSF-2240", "", "", "Overflow - next sailing", "0.00"),
 "lp-TSF-2241": ("rec66b2e676bdf7d2", "TSF-2241", "Main", "M5", "Loaded", "39.10"),
 "lp-TSF-2242": ("rec89b62a4806e98a", "TSF-2242", "Main", "M5", "Loaded", "39.95"),
 "lp-TSF-2243": ("rec1d666a4d47867d", "TSF-2243", "Main", "M5", "Loaded", "38.25"),
 "lp-TSF-2244": ("rec2f00cee2e98527", "TSF-2244", "Main", "M5", "Loaded", "39.10"),
 "lp-TSF-2245": ("rec2eb1a015e2bc52", "TSF-2245", "Main", "M5", "Loaded", "38.25"),
 "lp-TSF-2246": ("rec88bcb6e912229a", "TSF-2246", "Main", "M5", "Loaded", "39.95"),
 "lp-TSF-2247": ("rec4e900a0175a56e", "TSF-2247", "Main", "M5", "Loaded", "37.40"),
 "lp-TSF-2248": ("rec093e6854e2e3c1", "TSF-2248", "Main", "M5", "Loaded", "39.10"),
 "lp-TSF-2217b": ("recc4891fad4d1df3", "TSF-2217", "Main", "M2", "Loaded", "35.70"),
}

res = plan["result"]
same, change, add, remove = [], [], [], []

for line, (rid, ref, deck, lane, status, fare) in keyed.items():
    if line == "lp-TSF-2217b":
        remove.append((line, rid, ref, "duplicate second line for TSF-2217 (DLS-4 s5)"))
        continue
    r = res[ref]
    want = (r["deck"] or "", r["lane"] or "", r["status"], r["fare"])
    have = (deck, lane, status, fare)
    if want == have:
        same.append((line, ref, have))
    else:
        change.append((line, rid, ref, have, want))

for ref in res:
    if "lp-" + ref not in keyed:
        add.append((ref, res[ref]))

print("=== CORRECT AS KEYED, LEAVE ALONE (%d) ===" % len(same))
for line, ref, have in same:
    print(" ", line, have)
print("\n=== NEEDS CHANGING (%d) ===" % len(change))
for line, rid, ref, have, want in change:
    print(" ", line, rid)
    print("      was :", have)
    print("      now :", want)
print("\n=== TO ADD (%d) ===" % len(add))
for ref, r in add:
    print(" ", ref, r["status"], r["deck"], r["lane"], r["fare"])
print("\n=== TO REMOVE (%d) ===" % len(remove))
for line, rid, ref, why in remove:
    print(" ", line, rid, why)

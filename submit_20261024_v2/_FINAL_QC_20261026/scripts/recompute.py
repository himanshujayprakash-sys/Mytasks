import json, sys, pathlib, tomllib
root = pathlib.Path(sys.argv[1])
print("uuid8 | polarity | pytest(re) | pytest(rep) | rubric(re judge.toml) | rubric(rep) | combined(re) | report | reward.json | pass_summary | result.json | judge ids==toml | n_crit | guards hit")
for b in sorted(root.iterdir()):
    if not (b / "task.toml").exists(): continue
    run = b / "trajectories/opus-5/run_1"
    tw = json.loads((b / "tests/test_weights.json").read_text())
    tests = (tw.get("components", {}).get("traj_tests", {}) or {}).get("tests") or tw.get("tests")
    pol = tw.get("guard_polarity", "fail_charges")
    st = {t["name"]: t["status"] for t in json.loads((run / "verifier/ctrf.json").read_text())["results"]["tests"]}
    pos = sum(w for w in tests.values() if w > 0)
    earned = sum(w for n, w in tests.items() if w > 0 and st.get(n) == "passed")
    charged, hit = 0, []
    for n, w in tests.items():
        if w < 0:
            s = st.get(n)
            trip = (s == "passed") if pol == "pass_charges" else (s != "passed")
            if trip: charged += -w; hit.append(n)
    p = max(0, (earned - charged) / pos)
    rep = json.loads((run / "report.json").read_text())
    jt = tomllib.loads((b / "tests/reward/rubric/judge.toml").read_text())
    crits = jt.get("criteria") or jt.get("criterion") or []
    wmap = {str(c.get("id")): c for c in crits}
    rr = rep["rubric"]
    tot = sum(abs(float(wmap[str(c["id"])]["weight"])) for c in rr if float(wmap[str(c["id"])]["weight"]) > 0)
    e = sum(abs(float(wmap[str(c["id"])]["weight"])) for c in rr if float(wmap[str(c["id"])]["weight"]) > 0 and c["satisfied"])
    ch = sum(abs(float(wmap[str(c["id"])]["weight"])) for c in rr if float(wmap[str(c["id"])]["weight"]) < 0 and c["satisfied"])
    r = (e - ch) / tot
    comb = 0.5 * p + 0.5 * max(0, r)
    ids_ok = sorted(map(str, wmap)) == sorted(str(c["id"]) for c in rr) and all(abs(float(wmap[str(c["id"])]["weight"])) == abs(c["weight"]) for c in rr)
    rw = json.loads((run / "verifier/reward.json").read_text())["reward"]
    ps = json.loads((b / "trajectories/opus-5/pass_summary.json").read_text())["average_combined_score"]
    rj = json.loads((run / "result.json").read_text())["verifier_result"]["rewards"]["reward"]
    print(b.name[:8], pol, round(p, 4), rep["pytest"]["score"], round(r, 4), rep["rubric_score"], round(comb, 4), rep["final_reward"], rw, ps, rj, ids_ok, len(rr), len(hit), sep=" | ")

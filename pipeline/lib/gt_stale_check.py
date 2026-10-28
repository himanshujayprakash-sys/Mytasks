#!/usr/bin/env python3
"""gt_stale_check.py <task dir> [--jobs DIR ...] [--json OUT]: is solution/gt_env.json stale? Read-only (never
writes in the task). Follows the stage-1 workflow, step 3:

  1. mtimes of solution/gt_env.json, solution/TRUTH.md, solution/solve.py, tests/oracle.json; flag gt_env.json oldest
  2. tests/oracle.json reported.expected (ID -> status), reported.counts, reported.total when present
  3. per expected ID: TRUTH.md status | oracle.json status | gt_env.json status (and amount when TRUTH.md gives one)
  4. TRUTH.md "wrong routes" / "reachable wrong results" section: does gt_env.json match a wrong map instead
  5. the newest fresh oracle end_env.json (harness_mcp_atlas out/jobs/<uuid>*oracle*/*/verifier/, or --jobs dirs)
     diffed against gt_env.json, capture_status ignored: differing leaves + first 20 paths
  verdict STALE / CURRENT with one line of evidence.
Parts 2-4 need the stage-1 shape (reported.expected + a wrong-results section); a task without it says
"not applicable" there and the verdict rests on 1 and 5. With no fresh oracle run either, the verdict is UNKNOWN.
"""
import datetime
import glob
import json
import os
import pathlib
import re
import sys

a = sys.argv[1:]
T = pathlib.Path(a[0]).resolve()
U = T.name
jobs = [a[i + 1] for i, x in enumerate(a) if x == "--jobs"]
# --ran-on PATH: the task folder a matching oracle run must have run on (harbor records it in the trial's
# config.json task.path). Without it a run on any other folder is reported but cannot decide: a cached run of
# another version of the same task (seen 2026-10-28: new_10_20261024 vs submit_20261024) proves nothing here.
ran_on = os.path.realpath(a[a.index("--ran-on") + 1]) if "--ran-on" in a else str(T)
out_json = a[a.index("--json") + 1] if "--json" in a else None
HMA = pathlib.Path(__file__).resolve().parents[2] / "harness_mcp_atlas" / "out" / "jobs"
lines, res = [], {"uuid": U}


def p(s=""):
    lines.append(s)


def load(path):
    try:
        return json.loads(pathlib.Path(path).read_text())
    except Exception:
        return None


# 1. mtimes
files = ["solution/gt_env.json", "solution/TRUTH.md", "solution/solve.py", "tests/oracle.json"]
mt = {f: os.stat(T / f).st_mtime for f in files if (T / f).exists()}
p("## 1. Modification times")
for f in files:
    p("- %-22s %s" % (f, datetime.datetime.fromtimestamp(mt[f]).strftime("%Y-%m-%d %H:%M:%S") if f in mt else "MISSING"))
oldest = min(mt, key=mt.get) if mt else None
gt_oldest = oldest == "solution/gt_env.json" and len(mt) > 1 and mt[oldest] < sorted(mt.values())[1]
res["gt_env_oldest"] = gt_oldest
p("- gt_env.json is the oldest: %s%s" % ("YES (flag)" if gt_oldest else "no", "" if not gt_oldest else
  " (older than %s by %.0f min)" % (sorted(mt, key=mt.get)[1], (sorted(mt.values())[1] - mt[oldest]) / 60)))

oracle = load(T / "tests/oracle.json") or {}
rep = oracle.get("reported") or {}
gt = load(T / "solution/gt_env.json")
truth = (T / "solution/TRUTH.md").read_text(errors="replace") if (T / "solution/TRUTH.md").exists() else ""

# 2. reported.expected / counts / total
p("")
p("## 2. oracle.json reported")
exp = rep.get("expected") if isinstance(rep.get("expected"), dict) else None
p("- expected: %s" % ("%d IDs" % len(exp) if exp else "not present (not applicable)"))
for k in ("counts", "total"):
    if k in rep:
        p("- %s: %s" % (k, json.dumps(rep[k])[:300]))

# helpers to find a record and its status in gt_env
STATUS_KEYS = re.compile(r"^(status|state|outcome|disposition|decision|result|verdict)$", re.I)
AMOUNT_KEYS = re.compile(r"(amount|total|net|fee|charge|value|sum|price|balance)", re.I)


def records(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from records(v)
    elif isinstance(o, list):
        for v in o:
            yield from records(v)


def flat_fields(d):
    f = dict(d)
    if isinstance(d.get("fields"), dict):
        f.update(d["fields"])
    return f


def scalars(o, depth=0):
    if isinstance(o, dict):
        for v in o.values():
            if depth < 3: yield from scalars(v, depth + 1)
    elif isinstance(o, list):
        for v in o:
            if depth < 3: yield from scalars(v, depth + 1)
    elif o is not None:
        yield o


def gt_record(ident):
    """(record, its status field or None, amounts, every scalar in it) for the record an ID names: a dict keyed by
    the ID, or a dict with a field equal to the ID."""
    for d in records(gt):
        if ident in d and isinstance(d[ident], (dict, list)):
            node = d[ident]
        elif any(isinstance(v, str) and v.strip() == ident for v in flat_fields(d).values()):
            node = d
        else:
            continue
        f = flat_fields(node) if isinstance(node, dict) else {}
        st = next((v for k, v in f.items() if STATUS_KEYS.match(str(k)) and isinstance(v, (str, int, float))), None)
        am = [v for k, v in f.items() if AMOUNT_KEYS.search(str(k)) and isinstance(v, (int, float))]
        return node, st, am, [str(x).strip().casefold() for x in scalars(node)]
    return None, None, [], []


def expected_pairs(e):
    """reported.expected as (group, ID, status): either a flat {ID: status} map or {group: {ID: status | [status, ...]}}.
    Placeholders ("<as the records stood ...>": unchanged) and long text values are not statuses and are skipped."""
    def status_of(v):
        while isinstance(v, list) and v:
            v = v[0]
        return v if isinstance(v, (str, int, float, bool)) and not isinstance(v, str) or (isinstance(v, str) and 0 < len(v) <= 40 and not v.startswith("<")) else None
    out = []
    flat = all(not isinstance(v, dict) for v in e.values())
    for g, grp in ([("", e)] if flat else [(k, v) for k, v in e.items() if isinstance(v, dict)]):
        for ident, v in grp.items():
            st = status_of(v)
            if st is not None and len(str(ident)) <= 60:
                out.append((g, str(ident), st))
    return out


def truth_line(ident, statuses):
    for line in truth.splitlines():
        if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(ident), line):
            st = next((s for s in sorted(statuses, key=len, reverse=True) if re.search(r"\b%s\b" % re.escape(str(s)), line, re.I)), None)
            am = [float(x.replace(",", "")) for x in re.findall(r"(?:£|\$|€|GBP |USD |EUR )\s?(-?[\d,]+(?:\.\d+)?)", line)]
            return st, am
    return None, []


# 3. per-ID table
p("")
p("## 3. Per-ID comparison (review evidence)")
fails = 0
pairs = expected_pairs(exp) if exp else []
if pairs and gt is not None:
    statuses = {str(st) for _, _, st in pairs}
    p("| ID | TRUTH.md status | oracle.json status | gt_env.json status | PASS/FAIL |")
    p("|---|---|---|---|---|")
    for g, ident, ost in pairs:
        tst, tam = truth_line(ident, statuses)
        rec, gst, gam, vals = gt_record(ident)
        ok = rec is not None and (str(gst).casefold() == str(ost).casefold() if gst is not None else str(ost).strip().casefold() in vals)
        ok = ok and (tst is None or str(tst).casefold() == str(ost).casefold())
        if ok and tam and gam:
            ok = any(abs(x - y) < 0.005 for x in tam for y in gam)
        located = rec is not None
        fails += located and not ok
        shown = "NOT FOUND" if rec is None else (gst if gst is not None else ("%s present" % ost if str(ost).strip().casefold() in vals else "%s absent" % ost))
        p("| %s%s | %s | %s | %s%s | %s |" % (g + ": " if g else "", ident, tst or "-", ost, shown,
                                           (" (amount %s; TRUTH %s)" % (gam, tam)) if tam else "", "PASS" if ok else "FAIL" if located else "n/a (not located)"))
    p("")
    p("(Evidence to review, not the verdict: the record an ID names and its status field are found by matching, which")
    p("depends on how each app stores records; the verdict below rests on the fresh-oracle diff in section 5.)")
else:
    p("not applicable: %s" % ("no reported.expected in tests/oracle.json" if not exp else
                              "reported.expected has no ID -> status entries" if not pairs else "no gt_env.json"))
res["id_fails"] = fails if pairs else None

# 4. wrong routes
p("")
p("## 4. Wrong routes / reachable wrong results")
m = re.search(r"^(#+) [^\n]*(wrong route|reachable wrong|wrong results?|wrong figures|wrong totals)[^\n]*$", truth, re.I | re.M)
wrong_hits = []
if m and pairs and gt is not None:
    level = len(m.group(1))
    sec = truth[m.end():]
    nxt = re.search(r"^#{1,%d} " % level, sec, re.M)
    sec = sec[: nxt.start()] if nxt else sec
    # a wrong map is a line naming an expected ID with a status different from the truth
    statuses = {str(st) for _, _, st in pairs}
    for line in sec.splitlines():
        for _, ident, ost in pairs:
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(ident), line):
                for s in statuses - {str(ost)}:
                    if re.search(r"\b%s\b" % re.escape(s), line, re.I):
                        _, gst, _, vals = gt_record(ident)
                        if (str(gst).casefold() == s.casefold()) if gst is not None else (s.casefold() in vals and str(ost).casefold() not in vals):
                            wrong_hits.append("%s is %r in gt_env.json, the wrong route's value (%s)" % (ident, gst, line.strip()[:120]))
    p("- section: %s" % m.group(0).strip())
    p("- gt_env.json matches a wrong map: %s" % ("YES" if wrong_hits else "no"))
    for w in wrong_hits[:20]:
        p("  - " + w)
else:
    p("not applicable: %s" % ("no wrong-routes section in TRUTH.md" if not m else "no reported.expected to map IDs"))
res["wrong_route_hits"] = len(wrong_hits)

# 5. fresh oracle diff
p("")
p("## 5. Fresh oracle end_env.json vs gt_env.json")
cands = glob.glob(str(HMA / ("%s*oracle*" % U) / "*" / "verifier" / "end_env.json"))
for j in jobs:
    for pat in ("%s*oracle*" % U, "*-%s-oracle" % U):   # pipeline / QC job names
        cands += glob.glob(os.path.join(j, pat, "*", "verifier", "end_env.json"))
        cands += glob.glob(os.path.join(j, pat, "*", "artifacts", "logs", "artifacts", "atlas", "end_env.json"))
diffs = None
if cands and gt is not None:
    # newest oracle trial; inside it prefer the raw capture (artifacts/.../atlas/end_env.json, what S5-16 reads)
    trial = os.path.dirname(os.path.dirname(max(cands, key=os.path.getmtime)))
    if trial.endswith(os.path.join("artifacts", "logs")):
        trial = os.path.dirname(os.path.dirname(trial))
    tpath = ((load(os.path.join(trial, "config.json")) or {}).get("task") or {}).get("path") or ""
    res["oracle_task_path"] = tpath
    res["oracle_other_folder"] = os.path.realpath(tpath) != ran_on if tpath else True
    raw = os.path.join(trial, "artifacts", "logs", "artifacts", "atlas", "end_env.json")
    newest = raw if os.path.exists(raw) else os.path.join(trial, "verifier", "end_env.json")
    fresh = load(newest)
    # "fresh" = run after the task's last edit; an older oracle ran on other files and proves nothing about these
    task_mtime = max(os.stat(f).st_mtime for f in T.rglob("*") if f.is_file() and "trajectories" not in f.parts)
    oracle_mtime = os.path.getmtime(newest)
    res["oracle_older_than_task"] = oracle_mtime < task_mtime

    def apps(d):   # the per-app snapshot only: test.sh step 2 adds an "apps" copy of every app beside the originals
        if not isinstance(d, dict):
            return d
        top = {k: v for k, v in d.items() if k.startswith("Light")}
        return top or (d.get("apps") if isinstance(d.get("apps"), dict) else d)

    gt_apps, fresh = apps(gt), apps(fresh)

    def flat(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "capture_status":
                    continue
                yield from flat(v, "%s/%s" % (path, k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from flat(v, "%s[%d]" % (path, i))
        else:
            yield path, o

    A, B = dict(flat(gt_apps)), dict(flat(fresh))
    CLOCK = re.compile(r"/(date|internal_date|ts|createdTime|created_at|updated_at|modifiedTime|_canary)$")
    allk = sorted(k for k in set(A) | set(B) if A.get(k) != B.get(k))
    real = [k for k in allk if not CLOCK.search(k)]
    diffs = len(real)
    p("- newest: %s (%s)" % (newest.replace(str(pathlib.Path.home()), "~"),
                              datetime.datetime.fromtimestamp(os.path.getmtime(newest)).strftime("%Y-%m-%d %H:%M")))
    p("- ran on: %s%s" % (tpath or "(unknown)", "" if not res["oracle_other_folder"] else "  <- NOT this task folder"))
    if res["oracle_older_than_task"]:
        p("- WARNING: this oracle run is older than the task's last edit (%s): not fresh" %
          datetime.datetime.fromtimestamp(task_mtime).strftime("%Y-%m-%d %H:%M"))
    p("- differing leaves: %d (plus %d clock/canary-only, not counted)" % (len(real), len(allk) - len(real)))
    for k in real[:20]:
        p("  - %s | gt_env %s | fresh %s" % (k, json.dumps(A.get(k))[:60], json.dumps(B.get(k))[:60]))
else:
    p("not available: %s" % ("no fresh oracle run found" if not cands else "no gt_env.json"))
res["fresh_diff_leaves"] = diffs

# verdict: the fresh oracle diff decides (it is exact); the table and the mtimes are evidence beside it
if diffs is not None and res.get("oracle_other_folder"):
    verdict, ev = "UNKNOWN", "the newest oracle run ran on %s, not on this task folder (%d leaves differ): it may be another version; run the oracle on this one" % (res.get("oracle_task_path") or "an unknown folder", diffs)
elif diffs is not None and res.get("oracle_older_than_task"):
    verdict, ev = "UNKNOWN", "the newest oracle run predates the task's last edit (%d leaves differ from gt_env.json): rerun the oracle" % diffs
elif diffs is not None:
    if diffs:
        verdict, ev = "STALE", "the fresh oracle end state differs from gt_env.json in %d leaves (first: %s)" % (diffs, real[0])
    else:
        verdict, ev = "CURRENT", "the fresh oracle end state equals gt_env.json, clock and canary fields aside%s" % (
            "; gt_env.json is the oldest file, but its content is still the oracle's" if gt_oldest else "")
else:
    verdict, ev = "UNKNOWN", "no fresh oracle run to diff (pipeline gate 1 makes one)%s%s" % (
        "; gt_env.json is the oldest file" if gt_oldest else "",
        "; %d located ID(s) disagree with gt_env.json" % fails if fails else "")
res.update(verdict=verdict, evidence=ev)
p("")
p("## Verdict: %s" % verdict)
p(ev)
print("# gt_env.json staleness: %s\n" % U + "\n".join(lines))
if out_json:
    pathlib.Path(out_json).write_text(json.dumps(res, indent=1))
sys.exit(0 if verdict == "CURRENT" else 1)

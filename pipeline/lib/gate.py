#!/usr/bin/env python3
"""gate.py <qc dir 1_qc/<uuid>> <waivers.txt> <QC_REVIEW mode> <SKILL.md>: gate 1 verdict for one task.

Reads what parts A-C left in the qc dir and writes gate.json + GATE.md:
  PASS     no unwaived BLOCKER/MAJOR from the scripted checks, live runs all ok, review PASS (unless off)
  FAIL     any unwaived BLOCKER/MAJOR, a crashed check, or a review FAIL/PARTIAL
  PENDING  a part has not run yet (live, review)
Only a MAJOR can be waived (waivers.txt: "<ID> <reason>" for the batch, "<uuid8> <ID> <reason>" for one task).
"""
import json
import pathlib
import re
import sys

Q, WAIVERS, MODE, SKILL = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3], pathlib.Path(sys.argv[4])
# Optional 5th arg: the folder of accepted stage-1 bundles (yuji-workspace/trajectories). S1-37 then follows the rule
# the workspace final QC uses: a harness file passes when it matches ANY of them (canary lines aside), and
# environment/state_capture.py is compared without its harness-generated APP_URLS entries (TASK-STRUCTURE.md: "only
# the APP_URLS block changes"). Without it, S1-37 is judged against the Sample alone, as the task-QC text says.
REFS = sorted(p for p in pathlib.Path(sys.argv[5]).glob("*-*-*-*-*") if (p / "tests").is_dir()) if len(sys.argv) > 5 else []
COPY = pathlib.Path("/tmp/qc") / Q.name


def _norm(path, rel):
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return None
    lines = [l for l in lines if "harbor-canary GUID" not in l]
    if rel.endswith("state_capture.py"):
        lines = [l for l in lines if not re.match(r'\s*"Light[A-Za-z0-9]*":\s*os\.environ\.get\(', l)]
    return lines


def s137_match(rel):
    mine = _norm(COPY / rel, rel)
    if mine is None:
        return None
    return next((r.name[:8] for r in REFS if _norm(r / rel, rel) == mine), None)
U = Q.name
SEV = re.compile(r"\b(BLOCKER|MAJOR|MINOR)\b")
table = dict(re.findall(r"^\| (S\d-\d+) \|.*?\| (BLOCKER|MAJOR|MINOR|VERIFY) \|", SKILL.read_text(), re.M))

findings, review_items, notes = [], [], []


def add(cid, sev, text, where):
    findings.append({"id": cid, "sev": sev, "text": text.strip()[:300], "where": where})


def empty(value):
    return value.strip().rstrip(".") in ("", "none", "[]", "{}", "set()")


def scan(path):
    where = path.name
    lines = path.read_text(errors="replace").splitlines()
    for i, l in enumerate(lines):
        if not l.startswith("Traceback (most recent call last)"):
            continue
        frame = next((x for x in lines[i + 1:i + 30] if x.strip().startswith('File "')), "")
        err = next((x for x in lines[i + 1:i + 30] if re.match(r"^\w+(Error|Exception)\b", x)), "?")
        if 'File "<string>"' in frame:   # a python3 -c one-liner: the skill's listings (decisions are checked below)
            review_items.append("%s: a one-line listing could not read this task's data shape (%s); read it by hand" % (where, err[:120]))
        else:                            # one of the skill's checker scripts: its verdict is missing
            add("QC-ERROR", "BLOCKER", "a checker crashed (%s): %s" % (frame.strip()[:80], err[:150]), where)
    for i, line in enumerate(lines):
        m = re.match(r"^(S\d-\d+)\s+(.*)$", line)
        if not m:
            if re.match(r"^INVALID", line):
                add("S1-31", "BLOCKER", line, where)
            elif line.startswith("LEAK "):   # Stage 2 leak scan: a raw string match; the skill makes it a reading
                review_items.append("S2-01 raw hit (the review decides): " + line[:200])   # check (S2-01/S2-02)
            continue
        cid, rest = m.groups()
        if cid == "S2-27":   # prints only what it found, plus the multimodal value
            if rest.startswith("multimodal"):
                if not re.search(r"=\s*False\b", rest):
                    add(cid, table.get(cid, "MAJOR"), "dimensions." + rest, where)
            elif not rest.startswith(("ok", "done")):
                add(cid, table.get(cid, "MAJOR"), rest, where)
            continue
        if rest.startswith("WRONG"):   # raw match of a decoy/wrong figure in the instruction: the review decides
            review_items.append("%s raw hit (the review decides): %s" % (cid, rest[:200]))
            continue
        if rest.startswith("HIT"):
            if cid == "S5-16":   # the Sample's gt_env.json carries _canary too; the oracle snapshot never does
                leaves = [l.split("|")[0].strip() for l in lines[i + 1:i + 21] if l.startswith("    ")]
                if leaves and all(x == "/_canary" for x in leaves):
                    notes.append("S5-16: only /_canary differs (the Sample's gt_env.json has it too): cleared")
                    continue
            s = SEV.search(rest)
            add(cid, s.group(1) if s else table.get(cid, "BLOCKER"), rest[3:], where)
        elif re.match(r"(BLOCKER|MAJOR|MINOR)\b", rest):
            sev, text = rest.split(None, 1) if " " in rest else (rest, "")
            m37 = re.match(r"differs from the Sample: (\S+)", text) if cid == "S1-37" and REFS else None
            if m37 and s137_match(m37.group(1)):
                notes.append("S1-37: %s matches accepted stage-1 bundle %s (final-QC rule)" % (m37.group(1), s137_match(m37.group(1))))
                continue
            parts = [p.split(":", 1)[1] if ":" in p else p for p in text.split(" | ")]
            if ":" in text and all(empty(p) for p in parts):
                continue
            add(cid, sev, text, where)
        elif rest.startswith("VERIFY") or "candidate" in rest.split()[:2]:
            review_items.append(f"{cid} {rest}"[:240])
        elif "reward=" in rest and "expected=" in rest and not rest.rstrip().endswith("ok"):
            add(cid, "BLOCKER", rest, where)
        elif "NOT deducted" in rest:
            add(cid, "BLOCKER", rest, where)
        elif re.search(r"(guards tripped|checks that raised).*:\s*\[.+\]", rest):
            add(cid, "BLOCKER", rest, where)
        elif cid == "S5-15" and "->" in rest and not rest.rstrip().endswith("none"):
            add(cid, "BLOCKER", rest, where)


static = sorted((Q / "static").glob("[0-9]*.log"))
for p in static:
    scan(p)
# one-line checks that decide something must have printed their result (a crash there would hide a finding)
alltext = "\n".join(p.read_text(errors="replace") for p in static)
for marker, cid in (("S1-38 done", "S1-38"), ("S2-27 multimodal", "S2-27"), ("S4-32", "S4-32")):
    if static and marker not in alltext:
        add(cid, "BLOCKER", "check did not print its result (%r missing): it crashed or did not run" % marker, "static")
live = Q / "live" / "readers.log"
if live.exists():
    scan(live)

stale = Q / "live" / "stale.json"
if stale.exists():
    sj = json.loads(stale.read_text())
    if sj.get("verdict") != "CURRENT":
        add("GT-STALE", "BLOCKER", "solution/gt_env.json %s: %s (live/stale.md)" % (sj.get("verdict"), sj.get("evidence")), "stale.json")
elif live.exists():
    add("GT-STALE", "BLOCKER", "staleness check did not run (live/stale.md missing)", "live")

# waivers
batch_w, task_w = {}, {}
if WAIVERS.exists():
    for raw in WAIVERS.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        a, *rest = line.split(None, 2)
        if re.fullmatch(r"[0-9a-f]{8}", a) and rest:
            task_w.setdefault(a, {})[rest[0]] = rest[1] if len(rest) > 1 else ""
        else:
            batch_w[a] = " ".join(rest)
waive = dict(batch_w, **task_w.get(U[:8], {}))
for f in findings:
    if f["id"] in waive and f["sev"] == "MAJOR":
        f["waived"] = waive[f["id"]] or "waived"

blocking = [f for f in findings if f["sev"] in ("BLOCKER", "MAJOR") and not f.get("waived")]

# review
review = {"mode": MODE, "verdict": None, "blocking": []}
rep = Q / "review" / "qc_report.md"
if MODE == "claude" and rep.exists():
    t = rep.read_text()
    m = re.search(r"VERDICT:\s*(PASS|FAIL|PARTIAL)", t)
    review["verdict"] = m.group(1) if m else "UNREADABLE"
    heads = list(re.finditer(r"^### \[([^\]]+)\] ([^\n]*)\n- Severity: (BLOCKER|MAJOR)", t, re.M))
    for h in heads:
        cid = h.group(1)
        if not (h.group(3) == "MAJOR" and cid in waive):
            review["blocking"].append(f"{h.group(3)} {cid} {h.group(2)[:150]}")
    # A review written before a waiver was granted says FAIL; when every BLOCKER/MAJOR it lists is now waived, its
    # verdict is a pass with waivers. PARTIAL (something not checked) never turns into a pass.
    if review["verdict"] == "FAIL" and heads and not review["blocking"]:
        review["verdict"] = "PASS (with waivers: %s)" % ", ".join(sorted({h.group(1) for h in heads}))
elif MODE == "manual" and (Q / "review" / "REVIEW_OK").exists():
    review["verdict"] = "PASS"
    review["note"] = (Q / "review" / "REVIEW_OK").read_text().strip()
elif MODE == "off":
    review["verdict"] = "OFF"

if not static:
    verdict, why = "PENDING", "static checks not run"
elif blocking:
    verdict, why = "FAIL", "%d unwaived BLOCKER/MAJOR finding(s)" % len(blocking)
elif not live.exists():
    verdict, why = "PENDING", "live oracle/nop not run"
elif review["verdict"] in ("FAIL", "PARTIAL", "UNREADABLE") or review["blocking"]:
    verdict, why = "FAIL", "review %s%s" % (review["verdict"], ": " + "; ".join(review["blocking"][:3]) if review["blocking"] else "")
elif review["verdict"] is None:
    verdict, why = "PENDING", "review not done (QC_REVIEW=%s)" % MODE
else:
    verdict, why = "PASS", "scripted checks clean, live oracle/nop ok, review %s" % review["verdict"]

fp = Q / "qc_fingerprint.json"
task_sha = json.loads(fp.read_text())["sha256"] if fp.exists() else None
if verdict == "PASS" and not task_sha:
    verdict, why = "PENDING", "no fingerprint of the checked files (rerun the static checks)"
out = {"uuid": U, "verdict": verdict, "why": why, "task_sha256": task_sha, "findings": findings, "review": review,
       "review_items": review_items, "notes": notes,
       "skill": (Q / "static" / "_blocks.txt").read_text().split()[:2] if (Q / "static" / "_blocks.txt").exists() else None}
(Q / "gate.json").write_text(json.dumps(out, indent=1))
md = ["# Gate 1 (task QC): %s" % verdict, "", "`%s` | %s" % (U, why), "",
      "Checked files: sha256 `%s` (any edit to the task after this makes the verdict CHANGED)." % task_sha, ""]
if findings:
    md += ["| ID | Severity | Finding | Where |", "|---|---|---|---|"]
    md += ["| %s | %s | %s | %s |" % (f["id"], f["sev"] + (" (waived: %s)" % f["waived"] if f.get("waived") else ""),
                                       f["text"].replace("|", "/"), f["where"]) for f in findings]
    md.append("")
if review["blocking"]:
    md += ["Review findings:", *("- " + x for x in review["blocking"]), ""]
if review_items:
    md += ["To read (not blocking by themselves):", *("- " + x for x in review_items), ""]
if notes:
    md += ["Notes:", *("- " + x for x in notes), ""]
(Q / "GATE.md").write_text("\n".join(md))
print("%s %s: %s" % (U[:8], verdict, why))

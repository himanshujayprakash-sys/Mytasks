---
name: structure
stage: static
model: opus
inputs: [.]
gate: block
timeout: 1200
max_turns: 40
---

> `$TASK` is already exported and points at a copy of the task folder. Do not set it again.
> Run the script as written and apply the decision tables to its output.

# STRUCTURE QC — Required files, folder layout, and file integrity

> **Persona:** You are the gatekeeper for the task queue. Nothing downstream (the RUTHLESS
> audit, the build, the oracle/nop gate, pass@k) runs until this check passes. Your job is
> mechanical: run the script against the task folder, record the output verbatim, apply the
> decision tables. Do not judge content quality here. Do not skip a check because the folder
> "looks right".

**Stage:** static, right after the import stage. **Inputs:** the task folder only.
**Gate:** BLOCK. Any BLOCKER row moves the task to `errored/` with this report attached.
**Prereqs:** `python3` 3.11+ (stdlib only), `find`, `du`, `grep`.

---

## Section 0 — Expected layout (the authoring layout the harness builds from)

```
<uuid>/
├── .identity.json                 {uuid, canary (the harbor-canary GUID), instruction_canary,
│                                   imported_from}; minted by the harness, absent on a fresh author drop
├── instruction.md                 the prompt; first line `<!-- instruction-canary <uuid> -->`
├── task.toml                      schema_version, [task] name/description/authors,
│                                   [task.metadata] apps (graded) + mcp_servers (wired) + …;
│                                   harness-owned blocks forbidden
├── environment/Dockerfile         the agent image (required)
├── data/                          files the agent can read, mounted read-only (required, non-empty)
├── world_data/<Server>.json       one seed per wired server, at least 2 (required)
├── solution/
│   ├── solve.py, solve.sh         the oracle replay (solve.py required)
│   ├── gt_env.json                the world after the oracle: {Server: …} flat, or {apps: {…}}
│   └── TRUTH.md                   the answer the oracle states (required)
└── tests/
    ├── test_outputs.py            the graded suite (required); may import claims_lib (harness) and
    │                              a helper module beside it (tests/task_lib.py …)
    ├── test_weights.json          tests map (flat `tests` or `components.traj_tests.tests`),
    │                              threshold, null_floor, guard_polarity (required)
    ├── oracle.json                seed, apps, oracle, reported: the reference run's record (required)
    ├── old_env.json               the untouched seed snapshot (expected)
    └── judge.toml                 the rubric (required; legacy tests/rubric.json accepted)
```

A **built** task (environment/light-servers/, tests/reward/, tests/test.sh) is converted into
this layout by the import stage before this check runs: `light-servers/task_data` → `data/`,
`light-servers/world_data` → `world_data/`, the compiled `tests/reward/rubric/judge.toml` is
decompiled to `tests/judge.toml`, and the harness's own verifier files are dropped. So if any
of those harness files are still present here, the folder was dropped in the wrong shape or
the author shipped them: `tests/test.sh`, `Dockerfile`, `Dockerfile.ecr`, `docker-compose.yaml`,
`.dockerignore`, `evaluate.sh`, `grade.py`, `_judge/`, `reward/`, `ctrf_pytest_plugin.py`,
`claims_lib.py`. The build overwrites every one of them (S1).

---

## Section 1 — Run the checks (once)

```bash
: "${TASK:?TASK is exported by the pipeline}"
python3 - <<'PY'
# static structure QC scripts S1-S4, run with TASK set
import os, json, re, ast, tomllib, collections
from pathlib import Path
T = Path(os.environ["TASK"])
print(f"=== S1 ({T.name})")
REQ_FILES = ["instruction.md", "task.toml", "environment/Dockerfile", "tests/test_outputs.py", "tests/test_weights.json",
             "tests/oracle.json", "solution/solve.py", "solution/gt_env.json", "solution/TRUTH.md"]
REQ_DIRS = ["data", "world_data", "solution", "tests", "environment"]
missing = [f for f in REQ_FILES if not (T / f).is_file()]; empty = [f for f in REQ_FILES if (T / f).is_file() and (T / f).stat().st_size == 0]
nodir = [d for d in REQ_DIRS if not (T / d).is_dir()]
rubric = [p for p in ("tests/judge.toml", "tests/rubric.json") if (T / p).is_file()]
print("missing_files   :", missing or "none"); print("empty_files     :", empty or "none"); print("missing_dirs    :", nodir or "none")
print("rubric_file     :", rubric or "NONE"); print("both_rubrics    :", len(rubric) == 2)
world = sorted(p.stem for p in (T / "world_data").glob("*.json")) if (T / "world_data").is_dir() else []
print(f"world_data_json : {len(world)} files (minimum 2): {world}")
data_n = sum(1 for p in (T / "data").rglob("*") if p.is_file()) if (T / "data").is_dir() else 0
print(f"data_files      : {data_n}"); print("old_env.json    :", (T / "tests/old_env.json").is_file())
helpers = sorted(p.name for p in (T / "tests").glob("*.py") if p.name != "test_outputs.py") if (T / "tests").is_dir() else []
print("helper_modules  :", helpers or "none")
HARNESS = ["test.sh", "Dockerfile", "Dockerfile.ecr", "docker-compose.yaml", ".dockerignore", "evaluate.sh", "grade.py", "_judge", "reward", "ctrf_pytest_plugin.py", "claims_lib.py"]
print("harness_owned_in_tests:", [n for n in HARNESS if (T / "tests" / n).exists()] or "none")

print("=== S2")
bad = []
def chk(rel, loader):
    p = T / rel
    if not p.is_file(): return
    try: loader(p)
    except Exception as e: bad.append(f"{rel}: {type(e).__name__}: {e}")
for rel in ("task.toml", "tests/judge.toml"): chk(rel, lambda p: tomllib.loads(p.read_text()))
for rel in ("tests/rubric.json", "tests/test_weights.json", "tests/oracle.json", "tests/old_env.json", "solution/gt_env.json"): chk(rel, lambda p: json.loads(p.read_text()))
for rel in ["tests/test_outputs.py", "solution/solve.py"] + [f"tests/{h}" for h in helpers]: chk(rel, lambda p: ast.parse(p.read_text()))
for p in sorted((T / "world_data").glob("*.json")) if (T / "world_data").is_dir() else []: chk(f"world_data/{p.name}", lambda q: json.loads(q.read_text()))
print("parse_errors:", "none" if not bad else ""); [print("  ", b) for b in bad]

print("=== S3")
text = (T / "task.toml").read_text(); d = tomllib.loads(text)
OWNED = ["[agent]", "[verifier]", "[verifier.env]", "[verifier.environment]", "[[verifier.collect]]", "[environment]", "[[environment.mcp_servers]]"]
print("harness_owned_blocks:", [b for b in OWNED if any(l.strip() == b for l in text.splitlines())] or "none")
task = d.get("task") or {}; md = task.get("metadata") or {}
print("schema_version      :", d.get("schema_version") or "MISSING"); print("task.name           :", task.get("name") or "MISSING")
print("task.description    :", "present" if task.get("description") else "MISSING"); print("task.authors        :", task.get("authors") or "MISSING")
wired, graded = md.get("mcp_servers") or [], md.get("apps") or []
print("metadata.mcp_servers:", len(wired) or "MISSING"); print("metadata.apps       :", len(graded) or "MISSING")
print("apps_not_wired      :", sorted(set(graded) - set(wired)) if wired and graded else "n/a")
print("wired_without_world :", sorted(set(wired or graded) - set(world)) or "none"); print("world_not_wired     :", sorted(set(world) - set(wired or graded)) or "none")
print("metadata.category   :", md.get("category") or "MISSING"); print("metadata.tags       :", len(md.get("tags") or []) or "MISSING")
print("metadata.gradeable  :", md.get("gradeable"))

print("=== S4a")
w = json.loads((T / "tests/test_weights.json").read_text())
tests = dict(((w.get("components") or {}).get("traj_tests") or {}).get("tests") or {}) or dict(w.get("tests") or {})
body = (T / "tests/test_outputs.py").read_text()
defined = set(re.findall(r"^def (test_\w+)", body, re.M)) | set(re.findall(r"^(test_\w+)\s*=", body, re.M))
dynamic = re.search(r'globals\(\)\s*\[\s*["\']test_', body) is not None
print(f"weight_shape={'components' if 'components' in w else 'flat'} weighted={len(tests)} defined={len(defined)} dynamic_minting={dynamic}")
print("weighted_but_undefined:", sorted(set(tests) - defined) or "none"); print("defined_but_unweighted:", sorted(defined - set(tests)) or "none")
badw = {k: v for k, v in tests.items() if not isinstance(v, (int, float)) or isinstance(v, bool) or v == 0}
print("zero_or_nonnumeric_weights:", badw or "none")
pos = sum(v for v in tests.values() if isinstance(v, (int, float)) and v > 0); neg = sum(-v for v in tests.values() if isinstance(v, (int, float)) and v < 0)
print(f"positive_total={pos} penalty_total={neg} guards={sum(1 for v in tests.values() if isinstance(v, (int, float)) and v < 0)}")
th, nf, gp = w.get("threshold"), w.get("null_floor"), w.get("guard_polarity")
print(f"threshold={th} null_floor={nf} guard_polarity={gp} gate={w.get('gate')}")
print("threshold_ok:", th is None or (isinstance(th, (int, float)) and 0 < th <= 1), "(absent = harness default 0.7)" if th is None else "")
print("null_floor_ok:", isinstance(nf, (int, float)) and 0 <= nf < 1)
print("guard_polarity_ok:", gp in (None, "fail_charges", "pass_charges"), "| guards_without_polarity:", neg > 0 and gp is None)

print("=== S4b")
TARGETS = {"final_answer", "user_facing_message", "trajectory", "state_change"}
IMPORTANCE = {"critically_important": 5, "important": 3, "somewhat_important": 1}
crit = []
if (T / "tests/judge.toml").is_file():
    doc = tomllib.loads((T / "tests/judge.toml").read_text()); shape = "rewardkit" if "judge" in doc or any("name" in c for c in doc.get("criterion") or []) else "authoring"
    for i, c in enumerate(doc.get("criterion") or [], 1):
        ann = c.get("annotations") or {}
        pick = lambda *ks: next((c[k] for k in ks if k in c), next((ann[k] for k in ks if k in ann), None))
        pos = pick("is_positive", "polarity")
        if isinstance(pos, str): pos = {"positive": True, "negative": False}.get(pos.lower())
        wgt = c.get("weight")
        if pos is None and isinstance(wgt, (int, float)): pos = wgt > 0
        crit.append({"id": c.get("id") or c.get("name") or f"#{i}", "number": pick("number") or str(i), "description": c.get("description") or "",
                     "weight": wgt, "is_positive": pos, "target": pick("evaluation_target"), "negate": c.get("negate", False),
                     "scoring": c.get("scoring") or ("binary" if c.get("type") in (None, "binary") else c.get("type"))})
elif (T / "tests/rubric.json").is_file():
    shape = "rubric.json (legacy)"
    for i, c in enumerate(json.loads((T / "tests/rubric.json").read_text()).get("criteria") or [], 1):
        pos = c.get("is_positive", True); wgt = IMPORTANCE.get(str(c.get("importance")), 0)
        crit.append({"id": c.get("id") or str(c.get("number") or i), "number": str(c.get("number") or i), "description": c.get("criterion") or "",
                     "weight": wgt if pos else -wgt, "is_positive": pos, "target": c.get("evaluation_target", "final_answer"), "negate": False, "scoring": "binary"})
else: shape = "NONE"
print(f"shape={shape} criteria={len(crit)}")
if crit:
    ids = [c["id"] for c in crit]; nums = [c["number"] for c in crit]
    print("duplicate_ids:", [k for k, n in collections.Counter(ids).items() if n > 1] or "none"); print("duplicate_numbers:", [k for k, n in collections.Counter(nums).items() if n > 1] or "none")
    print("missing_description:", [c["id"] for c in crit if not c["description"].strip()] or "none")
    print("bad_weight:", [(c["id"], c["weight"]) for c in crit if not isinstance(c["weight"], (int, float)) or isinstance(c["weight"], bool) or c["weight"] == 0] or "none")
    print("no_polarity:", [c["id"] for c in crit if c["is_positive"] is None] or "none")
    print("weight_sign_vs_polarity_mismatch:", [c["id"] for c in crit if isinstance(c["weight"], (int, float)) and c["weight"] != 0 and c["is_positive"] is not None and (c["weight"] > 0) != bool(c["is_positive"])] or "none")
    print("negate_used:", [c["id"] for c in crit if c["negate"]] or "none"); print("non_binary_scoring:", [(c["id"], c["scoring"]) for c in crit if c["scoring"] not in (None, "binary")] or "none")
    print("bad_target:", [(c["id"], c["target"]) for c in crit if c["target"] not in TARGETS] or "none")
    p = sum(c["weight"] for c in crit if isinstance(c["weight"], (int, float)) and c["weight"] > 0); n = sum(-c["weight"] for c in crit if isinstance(c["weight"], (int, float)) and c["weight"] < 0)
    print(f"positive_total={p} penalty_total={n} max_single_positive={max((c['weight'] for c in crit if isinstance(c['weight'], (int, float)) and c['weight'] > 0), default=0)}")
    print("targets:", dict(collections.Counter(str(c["target"]) for c in crit)))

print("=== S4c")
ident = T / ".identity.json"
if ident.is_file():
    idd = json.loads(ident.read_text()); can = idd.get("instruction_canary"); guid = idd.get("canary")
    print("identity:", {k: idd.get(k) for k in ("uuid", "canary", "instruction_canary")})
    print("folder_name_is_uuid:", T.name == idd.get("uuid"))
    found = re.findall(r"instruction-canary\s+([0-9a-fA-F-]{36})", (T / "instruction.md").read_text(errors="ignore"))
    print("instruction_canaries_found:", found or "none (the build stamps one)")
    print("canary_binding_ok:", "n/a (identity records none; the build mints it)" if not can else (not found or can in found) and len(set(found)) <= 1)
    if guid:
        carriers = sorted(str(p.relative_to(T)) for p in T.rglob("*") if p.is_file() and p.suffix in (".py", ".toml", ".json", ".md", ".sh", "") and p.stat().st_size < 50_000_000 and guid in p.read_text(errors="replace"))
        print("harbor_canary_carriers:", carriers)
else:
    print("identity: not minted (a task dropped in the authoring layout; the build mints it)")
gt = json.loads((T / "solution/gt_env.json").read_text())
gt_servers = sorted(gt["apps"]) if isinstance(gt.get("apps"), dict) else sorted(k for k in gt if k.startswith("Light")) if isinstance(gt, dict) else []
print("gt_env_shape    :", "envelope (apps)" if isinstance(gt.get("apps"), dict) else "flat")
print("gt_env_servers  :", gt_servers); print("in_gt_not_world :", sorted(set(gt_servers) - set(world)) or "none"); print("in_world_not_gt :", sorted(set(world) - set(gt_servers)) or "none")
if (T / "tests/old_env.json").is_file():
    oe = json.loads((T / "tests/old_env.json").read_text()); oe_servers = sorted(oe["apps"]) if isinstance(oe.get("apps"), dict) else sorted(k for k in oe if k.startswith("Light"))
    print("old_env_servers :", len(oe_servers), "not in world:", sorted(set(oe_servers) - set(world)) or "none")
PY

# S5 hygiene
find "$TASK" \( -name .DS_Store -o -name __pycache__ -o -name "*.pyc" -o -name "*.swp" \
      -o -name ".ipynb_checkpoints" -o -name node_modules \) -print
du -sh "$TASK"; find "$TASK" -type f -size +20M -exec ls -lh {} \;
grep -rnIE 'sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|"refresh_token"\s*:\s*"[^"]{20,}' \
     "$TASK" --exclude-dir=.git | head -20
basename "$TASK" | grep -qE '^[a-z0-9][a-z0-9._-]*$' && echo "slug ok" || echo "slug BAD"
find "$TASK" -type l -print
```

---

## Section 2 — Decision tables

### S1 — required files and directories

| Output | Verdict |
|---|---|
| any `missing_files`, `missing_dirs`, `empty_files` | **BLOCKER** `S1_MISSING` |
| `rubric_file` NONE | **BLOCKER** `S1_NO_RUBRIC` |
| `both_rubrics` True | **BLOCKER** `S1_TWO_RUBRICS` (the build compiles judge.toml; a foreign one beside the task's rubric.json scored an oracle 0.0 once) |
| `rubric_file` is rubric.json only | **MAJOR** `S1_LEGACY_RUBRIC` |
| `world_data_json` < 2 | **BLOCKER** `S1_EMPTY_WORLD` |
| `data_files` 0 | **BLOCKER** `S1_NO_DATA` (the build refuses an empty evidence folder) |
| `old_env.json` False | **MAJOR** `S1_NO_SEED` (every seed-vs-end comparison in the tests fails closed) |
| `harness_owned_in_tests` non-empty | **MAJOR** `S1_OWNED_FILES` (list them; the build replaces them, so author edits there never run) |
| `helper_modules` non-empty | INFO (name them; the build ships them beside the tests) |

### S2 — every structured file parses

| Output | Verdict |
|---|---|
| any `parse_errors` | **BLOCKER** `S2_PARSE` |

### S3 — task.toml

| Output | Verdict |
|---|---|
| `harness_owned_blocks` non-empty | **BLOCKER** `S3_OWNED_BLOCK` (the harness generates these; an author value here is lost or, worse, kept) |
| `schema_version` MISSING, `task.description` MISSING, or both `mcp_servers` and `apps` MISSING | **BLOCKER** `S3_TOML` (the build refuses the same) |
| `apps_not_wired` non-empty | **BLOCKER** `S3_APP_NOT_WIRED` (a graded app no server serves: every check on it fails) |
| `wired_without_world` non-empty | **MAJOR** `S3_NO_SEED_FOR_SERVER` (the server runs on its stock corpus) |
| `world_not_wired` non-empty | **MINOR** `S3_UNUSED_WORLD` |
| `task.authors`, `metadata.category` or `metadata.tags` MISSING | **MINOR** `S3_METADATA` |

### S4a — test_weights.json ↔ test_outputs.py

| Output | Verdict |
|---|---|
| `weighted_but_undefined` non-empty and `dynamic_minting` False | **BLOCKER** `S4_PHANTOM_TEST` (weight on a test that never runs) |
| `weighted_but_undefined` non-empty and `dynamic_minting` True | **MAJOR** `S4_DYNAMIC_TESTS` (the oracle calibration must collect them) |
| `defined_but_unweighted` non-empty | **BLOCKER** `S4_UNWEIGHTED_TEST` (the build refuses it) |
| `zero_or_nonnumeric_weights` non-empty, `null_floor_ok` False, `threshold_ok` False, `guard_polarity_ok` False | **BLOCKER** `S4_WEIGHTS` |
| `guards_without_polarity` True | **MAJOR** `S4_GUARD_POLARITY` (the harness assumes fail_charges; a suite whose guards assert the misbehaviour needs pass_charges or every clean run is charged every guard) |
| `threshold` None | **MINOR** `S4_THRESHOLD_DEFAULT` (0.7 applies) |
| `penalty_total` ≥ `positive_total` | **MAJOR** `S4_PENALTY_DOMINATES` (RUTHLESS judges the design; here it is a sanity flag) |

### S4b — the rubric

| Output | Verdict |
|---|---|
| `criteria` 0, any `duplicate_ids`, `missing_description`, `bad_weight`, `no_polarity`, `weight_sign_vs_polarity_mismatch`, `negate_used`, `non_binary_scoring`, `bad_target` | **BLOCKER** `S4_CRITERION` (the compiler refuses the same) |
| `duplicate_numbers` | **MAJOR** `S4_CRITERION_NUMBER` |
| `penalty_total` ≥ `positive_total`, or `max_single_positive` > half of `positive_total` | **MAJOR** `S4_RUBRIC_WEIGHTS` |

### S4c — identity, canaries, servers

| Output | Verdict |
|---|---|
| `canary_binding_ok` False | **BLOCKER** `S4_CANARY` (the instruction carries another task's canary, or two canaries: a copied prompt would trace a leak to the wrong task) |
| `folder_name_is_uuid` False | **MAJOR** `S4_FOLDER_NAME` (job and bundle names follow the folder) |
| `in_gt_not_world` non-empty | **MAJOR** `S4_GT_SERVER` (the oracle touched a server with no seeded world) |
| `instruction_canaries_found` none, identity not minted, `in_world_not_gt` non-empty | INFO |

### S5 — hygiene

| Output | Verdict |
|---|---|
| any real credential | **BLOCKER** `S5_SECRET` (never ship it; stop and report) |
| any symlink | **BLOCKER** `S5_SYMLINK` |
| any stray file | **MINOR** `S5_STRAY` |
| a file > 20M or the folder > 500M | **MAJOR** `S5_SIZE` |
| `slug BAD` | **MAJOR** `S5_NAME` |

---

## Section 3 — Report format

Write the report to `REPORT.md`:

```markdown
## VERDICT: PASS | FAIL

| Check | Result | Code | Evidence |
|---|---|---|---|
| S1 required files/dirs | PASS/FAIL | | <missing list or "all present"> |
| S1 rubric file | PASS/FAIL | | judge.toml (<shape>) / rubric.json / none |
| S2 parse | PASS/FAIL | | <errors or "all parse"> |
| S3 task.toml | PASS/FAIL | | <blocks, missing keys, apps vs servers> |
| S4a weights ↔ tests | PASS/FAIL | | weighted=<n> defined=<n> phantom=<n> unweighted=<n> polarity=<…> |
| S4b criteria | PASS/FAIL | | n=<n> dups=<n> polarity=<n> targets=<…> |
| S4c identity / canary / servers | PASS/FAIL | | |
| S5 hygiene | PASS/FAIL | | |

## BLOCKERS
- <code> — <file> — <one line>

## MAJOR
- ...

## MINOR
- ...

## Counts
- files: <n>  size: <du>  data files: <n>  world servers: <n>  tests: <n> (guards <n>)  criteria: <n>
```

## Rules

1. Every row has evidence copied from the script output. No row is filled in from memory.
2. One BLOCKER forces `VERDICT: FAIL`. MAJOR and MINOR never do; they are carried into the
   manifest so the next stage and the author can see them.
3. Do not fix anything. This check reports; the pipeline moves the folder.

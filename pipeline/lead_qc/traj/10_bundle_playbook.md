---
name: bundle_playbook
stage: traj
model: opus
inputs: [.]
gate: block
timeout: 2400
max_turns: 80
---

> `$BUNDLE` is already exported and points at a copy of one packaged bundle. Do not set it
> again. Run every script as written, from your working directory, and quote the real output.

# QC Playbook — mcp-atlas **output bundle**

**Purpose.** Given ONE packaged bundle (`<uuid>/` with `trajectories/<model>/run_<i>/`), answer
six questions about the **shipped artifact only** (no authoring QC: that ran before the build):

1. **Which model** produced each run, and does every file agree? (§1)
2. **Is the score arithmetic honest?** reward, both channels and every aggregate reconcile. (§1.5, §1.6)
3. **Is a failure genuine?** environment vs model/agent, with evidence. (§2)
4. **Is the model's reasoning present** in the trajectory? (§3)
5. **Do the rubric and the pytests score the same thing twice?** (§4)
6. **Are any pytests false or hard-coded?** (§5)

**Prereqs.** `python3` 3.11+ (stdlib only: `json`, `tomllib`, `ast`, `re`), `grep`, `wc`.

---

## Section 0 — Bundle layout and the loader

```
<uuid>/
├── instruction.md, task.toml, environment/, solution/     the built task, as it ran
│   environment/light-servers/world_data/<Server>.json     one per wired server
├── tests/
│   ├── test_outputs.py, test_weights.json, oracle.json, old_env.json, (helper .py)
│   ├── test.sh, Dockerfile, claims_lib.py, ctrf_pytest_plugin.py     the harness verifier
│   └── reward/
│       ├── reward.toml                 weights {pytest = 0.5, rubric = 0.5}
│       ├── pytest/ledger.py            the pytest channel: max(0, (earned - charged) / total positive)
│       └── rubric/judge.toml           THE COMPILED RUBRIC the judge ran: [[criterion]] name, id,
│                                       description "[final answer|trajectory|end state] …", weight
│                                       (normalised, signed), annotations{number, source_weight,
│                                       is_positive, evaluation_target, category, priority}
└── trajectories/<model>/               e.g. opus-5
    ├── pass_summary.json               always: model, scale "0-1", threshold, runs, runs_completed,
    │                                   runs_errored, errored_run_indices, runs_without_rubric,
    │                                   runs_with_state_capture_failed, judge_models, average_*_score,
    │                                   per_run[{run_index, job, trial, pytest_score, rubric_score,
    │                                   combined_score, passed, errored, failure_mode, judge_model}]
    ├── pass@<N>.json, jobs.json        FULL bundles only (passed, pass_rate, mean_reward_per_trial,
    │                                   reward_per_run, failure_mode_histogram, attempts_per_task)
    └── run_<i>/
        ├── config.json                 agent{name, model_name, kwargs.reasoning_effort}, job_id
        ├── result.json                 agent_info{name, version, model_info}, agent_result (tokens,
        │                               cost), verifier_result.rewards{pytest, rubric, reward},
        │                               exception_info
        ├── report.json                 model, model_full, run_index, job, trial, scale, pytest{score,
        │                               passed, failed, guard_polarity, gate, missed[], guards_tripped[],
        │                               tests[{name, weight, passed, tripped, reason, error}]},
        │                               rubric[{id, name, criterion, weight, is_positive,
        │                               evaluation_target, satisfied, justification}], rubric_score,
        │                               judge{ran, model, transport, reason}, final_reward, channels,
        │                               weights, state_capture_failed, errored
        ├── agent/trajectory.json       ATIF (v1.5 to v1.8): agent{name, version}, steps[{step_id,
        │                               source, model_name, message, tool_calls[{function_name,
        │                               arguments, tool_call_id}], observation.results[{content,
        │                               source_call_id}], reasoning_content | thought}], final_metrics
        ├── artifacts/workspace/        the files the agent delivered
        └── verifier/
            ├── reward.json             {pytest, rubric, reward}, or only {reward} in trimmed bundles
            ├── reward-details.json     pytest{score, criteria[1]}, rubric{score, criteria[{id, name,
            │                           value 1|0, raw yes|no, weight, description, reasoning}], judge,
            │                           usage}
            ├── final_message.md        the agent's closing reply as graded
            ├── ctrf.json, junit.xml    raw pytest outcomes
            ├── end_env.json            the apps' end state (absent when the collect hook failed)
            └── FULL bundles also: grade_report.json (the ledger), judge.json, test-stdout.txt,
                pytest-stdout.txt, rewardkit-stdout.txt, server_tool_calls.log, judge_logs/
```

Two layouts ship: the **full** bundle the packager writes, and a **trimmed** delivery copy
(no `pass@N.json`, `jobs.json`, `grade_report.json`, `judge.json`, stdout files or
`server_tool_calls.log`; `reward.json` holds only `reward`). Every check below reads the best
file present and says which it used. A file that is missing in the trimmed layout is never a
finding on its own; a file missing from the **always** set is.

A bundle may hold runs from several harbor jobs (a plan of pass@2 then pass@8 packages as
`run_1..run_10`); `jobs.json`, when shipped, lists them. That is expected, not a reconciliation
failure. Run §1 to §3 for **every** `run_<i>`; §4 and §5 once per bundle.

**Scores are on the 0-1 scale** (`"scale": "0-1"`), never percentages. `reward = 0.5·pytest +
0.5·rubric` (`tests/reward/reward.toml`). A run **passes** when `reward >= threshold`
(`pass_summary.threshold`, from `tests/test_weights.json`, default 0.7) and did not error.

**Save the loader first.** Every script below imports it from your working directory:

```bash
: "${BUNDLE:?exported by the pipeline}"
cat > qc_lib.py <<'PY'
"""qc_lib.py: one mcp-atlas bundle as plain Python values. Stdlib only.

Every loader returns None for a file that is not shipped, so a check can say
"not shipped" instead of crashing. Nothing here writes to the bundle.
"""
import json, os, pathlib, re, tomllib

B = pathlib.Path(os.environ["BUNDLE"]).resolve()
TAG_RE = re.compile(r"^\[(final answer|trajectory|end state)\]\s*")
TARGET_TAG = {"final_answer": "final answer", "user_facing_message": "final answer",
              "trajectory": "trajectory", "state_change": "end state"}


def load(path):
    """JSON file -> value; None when absent; the string 'CORRUPT' when unreadable."""
    p = pathlib.Path(path)
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text())
    except ValueError:
        return "CORRUPT"


def ok(v):
    return v is not None and v != "CORRUPT"


# ---- layout ---------------------------------------------------------------
def model_dirs():
    t = B / "trajectories"
    return sorted(d for d in t.iterdir() if d.is_dir()) if t.is_dir() else []


def runs(model_dir):
    rs = [d for d in model_dir.glob("run_*") if d.is_dir() and d.name[4:].isdigit()]
    return sorted(rs, key=lambda d: int(d.name[4:]))


def run_index(run):
    return int(run.name[4:])


# ---- ground truth shipped at the bundle root -----------------------------
def weights():
    """tests/test_weights.json normalised: {tests: {name: w}, threshold, null_floor,
    guard_polarity, gate, raw}. Both shapes are read: flat `tests` (authoring) and
    `components.traj_tests.tests` (older)."""
    doc = load(B / "tests" / "test_weights.json")
    if not ok(doc):
        return None
    comps = doc.get("components") or {}
    tests = dict(((comps.get("traj_tests") or {}).get("tests") or {}) or doc.get("tests") or {})
    return {"tests": tests, "threshold": doc.get("threshold", 0.7) if doc.get("threshold") is not None else 0.7,
            "null_floor": doc.get("null_floor"), "guard_polarity": doc.get("guard_polarity", "fail_charges"),
            "gate": doc.get("gate"), "raw": doc}


def rubric_source():
    """tests/reward/rubric/judge.toml (the compiled rubric Rewardkit ran) as a list of
    {name, id, number, description (tag stripped), tag, weight (normalised, signed),
    source_weight (the author's, signed), is_positive, target}. None when not shipped."""
    p = B / "tests" / "reward" / "rubric" / "judge.toml"
    if not p.is_file():
        return None
    doc = tomllib.loads(p.read_text())
    out = []
    for c in doc.get("criterion") or []:
        ann = c.get("annotations") or {}
        desc = str(c.get("description") or "")
        m = TAG_RE.match(desc)
        sw = ann.get("source_weight", c.get("weight"))
        pos = ann.get("is_positive")
        if pos is None:
            pos = float(c.get("weight") or 0) > 0
        out.append({"name": c.get("name"), "id": str(c.get("id") or ann.get("number") or ""),
                    "number": str(ann.get("number") or c.get("id") or ""),
                    "description": TAG_RE.sub("", desc), "tag": m.group(1) if m else None,
                    "weight": float(c.get("weight") or 0), "source_weight": sw,
                    "is_positive": bool(pos), "target": ann.get("evaluation_target"),
                    "negate": bool(c.get("negate", False))})
    return out


def reward_policy():
    """tests/reward/reward.toml weights {pytest: 0.5, rubric: 0.5}; None when not shipped."""
    p = B / "tests" / "reward" / "reward.toml"
    if not p.is_file():
        return None
    try:
        return dict(tomllib.loads(p.read_text())["reward"][0]["weights"])
    except (KeyError, IndexError, tomllib.TOMLDecodeError):
        return "CORRUPT"


def test_source():
    p = B / "tests" / "test_outputs.py"
    return p.read_text() if p.is_file() else None


# ---- one run ---------------------------------------------------------------
def report(run):
    return load(run / "report.json")


def result(run):
    return load(run / "result.json")


def config(run):
    return load(run / "config.json")


def reward_json(run):
    return load(run / "verifier" / "reward.json")


def details(run):
    return load(run / "verifier" / "reward-details.json")


def judge_json(run):
    return load(run / "verifier" / "judge.json")


def final_message(run):
    p = run / "verifier" / "final_message.md"
    return p.read_text(errors="replace") if p.is_file() else None


def channels(run):
    """{pytest, rubric, reward} from the best source present, and where each came from.
    reward.json may carry only `reward` (trimmed bundles); report.json.channels and
    result.json.verifier_result.rewards carry the channels too."""
    out, src = {}, {}
    rj = reward_json(run)
    if ok(rj):
        for k in ("pytest", "rubric", "reward"):
            if isinstance(rj.get(k), (int, float)):
                out[k], src[k] = rj[k], "reward.json"
    rp = report(run)
    if ok(rp):
        for k, v in (rp.get("channels") or {}).items():
            if k not in out and isinstance(v, (int, float)):
                out[k], src[k] = v, "report.json.channels"
        if "reward" not in out and isinstance(rp.get("final_reward"), (int, float)):
            out["reward"], src["reward"] = rp["final_reward"], "report.json.final_reward"
    rs = result(run)
    if ok(rs):
        for k, v in (((rs.get("verifier_result") or {}).get("rewards")) or {}).items():
            if k not in out and isinstance(v, (int, float)):
                out[k], src[k] = v, "result.json.verifier_result.rewards"
    return out, src


def ledger(run):
    """The pytest channel per test: {source, rows: [{test, weight, passed, tripped}],
    earned, penalty, total_positive, guard_polarity, gate, missed, guards_tripped}.
    grade_report.json when shipped; else report.json.pytest; else ctrf.json + weights."""
    w = weights() or {"tests": {}, "guard_polarity": "fail_charges"}
    gp = w["guard_polarity"]
    gr = load(run / "verifier" / "grade_report.json")
    if ok(gr):
        rows = [{"test": t.get("test"), "weight": t.get("weight"), "passed": t.get("passed"),
                 "tripped": t.get("tripped"), "reason": t.get("reason"), "error": t.get("error")}
                for t in gr.get("tests") or []]
        return {"source": "grade_report.json", "rows": rows, "earned": gr.get("earned"),
                "penalty": gr.get("penalty"), "total_positive": gr.get("total_positive"),
                "guard_polarity": gr.get("guard_polarity", gp), "gate": gr.get("gate"),
                "missed": gr.get("missed") or [], "guards_tripped": gr.get("guards_tripped") or [],
                "reward": gr.get("reward")}
    rp = report(run)
    if ok(rp) and isinstance(rp.get("pytest"), dict):
        py = rp["pytest"]
        rows = [{"test": t.get("name"), "weight": t.get("weight"), "passed": t.get("passed"),
                 "tripped": t.get("tripped"), "reason": t.get("reason"), "error": t.get("error")}
                for t in py.get("tests") or []]
        return _fill({"source": "report.json.pytest", "rows": rows, "guard_polarity": py.get("guard_polarity", gp),
                      "gate": py.get("gate"), "missed": py.get("missed") or [],
                      "guards_tripped": py.get("guards_tripped") or [], "reward": py.get("score")})
    ct = load(run / "verifier" / "ctrf.json")
    if ok(ct):
        rows = []
        for t in ((ct.get("results") or {}).get("tests")) or []:
            wt = t.get("weight", w["tests"].get(t.get("name")))
            passed = t.get("status") == "passed"
            rows.append({"test": t.get("name"), "weight": wt, "passed": passed,
                         "tripped": (passed if gp == "pass_charges" else not passed) if isinstance(wt, (int, float)) and wt < 0 else None,
                         "reason": None, "error": None})
        return _fill({"source": "ctrf.json + test_weights.json", "rows": rows, "guard_polarity": gp,
                      "gate": None, "missed": None, "guards_tripped": None, "reward": None})
    return None


def _fill(led):
    rows = led["rows"]
    pos = [r for r in rows if isinstance(r["weight"], (int, float)) and r["weight"] > 0]
    gds = [r for r in rows if isinstance(r["weight"], (int, float)) and r["weight"] < 0]
    led["earned"] = sum(r["weight"] for r in pos if r["passed"])
    led["penalty"] = sum(-r["weight"] for r in gds if r["tripped"])
    led["total_positive"] = sum(r["weight"] for r in pos)
    if led["missed"] is None:
        led["missed"] = [r["test"] for r in pos if not r["passed"]]
    if led["guards_tripped"] is None:
        led["guards_tripped"] = [r["test"] for r in gds if r["tripped"]]
    return led


def pytest_from_ledger(led):
    """max(0, (earned - penalty) / total_positive), then the test_weights gate."""
    if not led or not led.get("total_positive"):
        return None
    v = max(0.0, (led["earned"] - led["penalty"]) / led["total_positive"])
    gate = led.get("gate") or (weights() or {}).get("gate") or {}
    if isinstance(gate, dict):
        if gate.get("require_no_guards") and led["guards_tripped"]:
            v = 0.0
        if isinstance(gate.get("floor"), (int, float)) and v < gate["floor"]:
            v = 0.0
    return round(v, 4)


def rubric_graded(run):
    """The rubric channel as judged: {source, score, criteria: [{id, name, value, raw,
    weight, description, reasoning, error}], judge: {...}, usage} or None.
    reward-details.json when shipped; else report.json.rubric (weights re-normalised)."""
    d = details(run)
    if ok(d) and isinstance(d.get("rubric"), dict):
        r = d["rubric"]
        crits = []
        for c in r.get("criteria") or []:
            desc = str(c.get("description") or "")
            crits.append({"id": str(c.get("id") or ""), "name": c.get("name"), "value": c.get("value"),
                          "raw": c.get("raw"), "weight": c.get("weight"), "description": TAG_RE.sub("", desc),
                          "reasoning": c.get("reasoning"), "error": c.get("error")})
        return {"source": "reward-details.json", "score": r.get("score"), "criteria": crits,
                "judge": r.get("judge"), "usage": r.get("usage"), "warnings": r.get("warnings")}
    rp = report(run)
    if ok(rp) and isinstance(rp.get("rubric"), list):
        tot = sum(c["weight"] for c in rp["rubric"] if c.get("is_positive") and isinstance(c.get("weight"), (int, float)))
        crits = []
        for c in rp["rubric"]:
            w = c.get("weight") or 0
            crits.append({"id": str(c.get("id") or ""), "name": c.get("name"),
                          "value": 1.0 if c.get("satisfied") else 0.0, "raw": "yes" if c.get("satisfied") else "no",
                          "weight": (w if c.get("is_positive") else -abs(w)) / tot if tot else None,
                          "description": str(c.get("criterion") or ""), "reasoning": c.get("justification"),
                          "error": c.get("error")})
        return {"source": "report.json.rubric", "score": rp.get("rubric_score"), "criteria": crits,
                "judge": rp.get("judge"), "usage": (rp.get("judge") or {}).get("usage"), "warnings": None}
    return None


def judge_ran(run):
    """(ran: bool|None, reason, model) from judge.json, report.json.judge, pass_summary."""
    j = judge_json(run)
    if ok(j):
        return bool(j.get("ran")), j.get("reason"), j.get("model")
    rp = report(run)
    if ok(rp) and isinstance(rp.get("judge"), dict):
        return bool(rp["judge"].get("ran")), rp["judge"].get("reason"), rp["judge"].get("model")
    rg = rubric_graded(run)
    if rg and rg.get("judge"):
        return True, None, (rg["judge"] or {}).get("model")
    return None, "no judge record shipped", None


def trajectory(run):
    return load(run / "agent" / "trajectory.json")


def agent_steps(traj):
    return [s for s in (traj or {}).get("steps") or [] if s.get("source") == "agent"]


def tool_calls(traj):
    """[(step_id, function_name, arguments)] in order."""
    out = []
    for s in (traj or {}).get("steps") or []:
        for tc in s.get("tool_calls") or []:
            out.append((s.get("step_id"), tc.get("function_name") or "", tc.get("arguments") or {}))
    return out


def observations(traj):
    """[(step_id, source_call_id, content as text)] in order."""
    out = []
    for s in (traj or {}).get("steps") or []:
        for r in ((s.get("observation") or {}).get("results")) or []:
            c = r.get("content")
            if isinstance(c, list):
                c = " ".join(p.get("text") or "" for p in c if isinstance(p, dict))
            out.append((s.get("step_id"), r.get("source_call_id"), c if isinstance(c, str) else json.dumps(c)))
    return out


def split_tool(name):
    """'LightAirtable_update_record' or 'mcp__LightAirtable__update_record' -> (server, verb);
    anything else -> (None, name) (a local tool such as terminal / finish / str_replace_editor)."""
    m = re.match(r"^mcp__([A-Za-z0-9]+)__(.+)$", name)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"^(Light[A-Za-z0-9]+)_(.+)$", name)
    if m:
        return m.group(1), m.group(2)
    return None, name


WRITE_VERBS = re.compile(r"^(create|add|update|set|delete|remove|send|post|reply|upload|move|rename|"
                         r"patch|put|assign|close|resolve|transition|merge|archive|invite|schedule|"
                         r"cancel|approve|reject|publish|write|edit|insert|append|trigger|scale|"
                         r"restart|rollout|apply|comment|label|tag|mark|complete|submit|register|"
                         r"grant|revoke|transfer|pay|refund|issue|revise)", re.I)


def is_write(verb):
    return bool(WRITE_VERBS.match(verb or ""))


def step_text(step):
    m = step.get("message")
    if isinstance(m, list):
        m = " ".join(p.get("text") or "" for p in m if isinstance(p, dict))
    return m if isinstance(m, str) else ""


def reasoning(step):
    """The model's reasoning on a step: ATIF `reasoning_content`, or `thought` (the
    name the bridge agent wrote before 2026-10-26)."""
    for k in ("reasoning_content", "thought"):
        v = step.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


def pass_summary(model_dir):
    return load(model_dir / "pass_summary.json")


def passk(model_dir):
    """pass@N.json when shipped (full bundles only)."""
    files = sorted(model_dir.glob("pass@*.json"))
    return load(files[0]) if files else None


def jobs(model_dir):
    return load(model_dir / "jobs.json")


def short_model(name):
    """'anthropic/claude-opus-5' -> 'opus-5', as the packager names model folders."""
    s = str(name or "").split("/")[-1]
    s = re.sub(r"^claude-", "", s)
    return s


def say(label, value):
    print(f"{label:<34} {value}")
PY
python3 -c "import qc_lib as Q; print(Q.B); print([d.name for d in Q.model_dirs()], [r.name for d in Q.model_dirs() for r in Q.runs(d)])"
```

---

## Section 1 — Identify the model

**Goal.** Every file that names the model agrees, and no second model appears mid-run.
`anthropic/claude-opus-5`, `claude-opus-5` and `opus-5` are the same model (provider prefix
and `claude-` are dropped for folder names); `opus` vs `sonnet`, or two different version
numbers, are not.

```bash
python3 - <<'PY'
# §1 model identity, per run
import qc_lib as Q
ACCEPTED = {f"ATIF-v1.{i}" for i in range(5, 9)}
for md in Q.model_dirs():
    ps = Q.pass_summary(md) or {}
    for run in Q.runs(md):
        cfg, res, tr, rp = Q.config(run), Q.result(run), Q.trajectory(run), Q.report(run)
        names = {
            "folder": md.name,
            "pass_summary.model": ps.get("model"),
            "config.agent.model_name": (cfg or {}).get("agent", {}).get("model_name"),
            "result.agent_info.model_info.name": ((res or {}).get("agent_info") or {}).get("model_info", {}).get("name"),
            "report.model / model_full": f"{(rp or {}).get('model')} / {(rp or {}).get('model_full')}",
            "trajectory.steps[].model_name": sorted({s.get("model_name") for s in Q.agent_steps(tr)} - {None}),
        }
        print(f"== {md.name}/{run.name}")
        for k, v in names.items():
            Q.say(k, v)
        Q.say("agent (config / result / trajectory)",
              f"{(cfg or {}).get('agent', {}).get('name')} / {((res or {}).get('agent_info') or {}).get('name')} "
              f"v{((res or {}).get('agent_info') or {}).get('version')} / {(tr or {}).get('agent')}")
        Q.say("schema_version", f"{(tr or {}).get('schema_version')}  {'ok' if (tr or {}).get('schema_version') in ACCEPTED else 'UNEXPECTED'}")
        Q.say("reasoning_effort (config.agent.kwargs)", ((cfg or {}).get("agent", {}).get("kwargs") or {}).get("reasoning_effort"))
        shorts = {Q.short_model(v) for v in [names["pass_summary.model"], names["config.agent.model_name"],
                  names["result.agent_info.model_info.name"], (rp or {}).get("model_full")] + names["trajectory.steps[].model_name"] if v}
        Q.say("distinct models after normalising", f"{sorted(shorts)}  {'ok' if len(shorts) == 1 else 'MISMATCH'}")
        Q.say("models seen mid-run", f"{len(names['trajectory.steps[].model_name'])}  {'ok' if len(names['trajectory.steps[].model_name']) <= 1 else 'SWAP'}")
PY
```

**Routes that ship under another name.** The harness runs GLM 5.3 on Amazon Bedrock as
`anthropic/glm-5.3-bedrock` (the agent needs the `anthropic/` prefix to reach the bridge) and its
packager relabels the bundle: folder `glm-5.3`, `bedrock/glm-5.3` in config, result, report,
pass_summary and every step (`provider` becomes `bedrock`). `short_model` reduces all of these to
`glm-5.3`, so they are one model; only a harbor **job name** (in jobs.json) keeps the run-time key
`glm-5.3-bedrock`, and a job name is never a model-identity signal. Bedrock trajectories carry the
runner's `ATIF-v1.5` (inside the accepted range) and the model is text-only: an image in the
task's data arrives as a text note, which is not a stale read.

**Decision rule.**

| Signal | Verdict |
|---|---|
| `distinct models after normalising` has one entry and `models seen mid-run` ≤ 1 | ✅ identity confirmed |
| config, result, report or pass_summary name a different model than the trajectory | ❌ **BLOCKER** `MODEL_MISMATCH`: the run did not honour the requested model |
| more than one `model_name` across the agent steps | ❌ **BLOCKER** `MODEL_SWAP` |
| `schema_version` UNEXPECTED (outside ATIF-v1.5 … v1.8) | **MAJOR** `ATIF_VERSION` |
| `agent.version` is `unknown`, `tool_definitions` null | INFO (the bridge agent does not record them) |

---

## Section 1.5 — Score sanity (arithmetic honesty)

**Goal.** The one reward number must be the same in every file and must rebuild from the
per-test ledger and the per-criterion judgments. If it does not, nothing downstream can be
trusted.

```bash
python3 - <<'PY'
# §1.5 score sanity, per run
import qc_lib as Q
W = Q.weights(); SRC = Q.rubric_source(); POL = Q.reward_policy()
print("ground truth:", "test_weights" if W else "NO test_weights.json", "|", f"{len(SRC)} criteria in judge.toml" if SRC else "NO tests/reward/rubric/judge.toml", "| policy", POL)
for md in Q.model_dirs():
    ps = Q.pass_summary(md) or {}
    per_run = {r.get("run_index"): r for r in ps.get("per_run") or []}
    for run in Q.runs(md):
        i = Q.run_index(run); print(f"== {md.name}/{run.name}")
        ch, src = Q.channels(run); Q.say("channels", f"{ch}  from {src}")
        rp, res = Q.report(run) or {}, Q.result(run) or {}
        # a. one reward everywhere
        seen = {"reward.json/channels": ch.get("reward"), "report.final_reward": rp.get("final_reward"),
                "result.verifier_result": ((res.get("verifier_result") or {}).get("rewards") or {}).get("reward"),
                "pass_summary.per_run.combined": (per_run.get(i) or {}).get("combined_score")}
        vals = {k: v for k, v in seen.items() if isinstance(v, (int, float))}
        spread = max(vals.values()) - min(vals.values()) if vals else None
        Q.say("1.5a reward agreement", f"{vals}  spread={spread}  {'ok' if spread is not None and spread <= 0.0001 else 'MISMATCH'}")
        # b. pytest channel from the ledger
        led = Q.ledger(run)
        if led:
            rec = Q.pytest_from_ledger(led)
            Q.say("1.5b pytest ledger", f"source={led['source']} rows={len(led['rows'])} earned={led['earned']} penalty={led['penalty']} total_positive={led['total_positive']} guard_polarity={led['guard_polarity']} gate={led.get('gate')}")
            Q.say("1.5b pytest recompute", f"{rec} vs reported {ch.get('pytest')}  {'ok' if rec is not None and ch.get('pytest') is not None and abs(rec - ch['pytest']) <= 0.0001 else 'MISMATCH'}")
            names = {r["test"] for r in led["rows"]}
            wn = set((W or {}).get("tests") or {})
            Q.say("1.5b weighted tests vs ledger rows", f"weighted={len(wn)} ledger={len(names)} weighted_not_run={sorted(wn - names)[:8]} run_unweighted={sorted(names - wn)[:8]}")
            wrong_w = [r["test"] for r in led["rows"] if r["test"] in wn and r["weight"] != W["tests"][r["test"]]]
            Q.say("1.5b weight drift (ledger vs test_weights)", wrong_w or "none")
            Q.say("1.5b guards tripped / missed", f"{led['guards_tripped']} / {len(led['missed'])} missed")
            errs = [r["test"] for r in led["rows"] if r.get("error")]
            Q.say("1.5b tests that raised", errs or "none")
        else:
            Q.say("1.5b pytest ledger", "NOT SHIPPED (no grade_report.json, report.json.pytest or ctrf.json)")
        # c. rubric channel from the graded criteria
        rg = Q.rubric_graded(run); ran, reason, jmodel = Q.judge_ran(run)
        Q.say("1.5c judge", f"ran={ran} model={jmodel} reason={reason}")
        if rg and rg["criteria"]:
            recr = round(max(0.0, sum((c["weight"] or 0) * (c["value"] or 0) for c in rg["criteria"])), 4)
            Q.say("1.5c rubric recompute", f"{recr} vs reported {rg['score']} / channel {ch.get('rubric')}  {'ok' if ch.get('rubric') is not None and abs(recr - ch['rubric']) <= 0.0001 else 'MISMATCH'}")
            raws = {str(c["raw"]).lower() for c in rg["criteria"]}
            Q.say("1.5c answers", f"n={len(rg['criteria'])} yes={sum(1 for c in rg['criteria'] if c['value'])} no={sum(1 for c in rg['criteria'] if not c['value'])} raw values={sorted(raws)} errors={sum(1 for c in rg['criteria'] if c['error'])}")
            if SRC:
                sids = {c["id"]: c for c in SRC}; gids = {c["id"]: c for c in rg["criteria"]}
                missing, extra = sorted(set(sids) - set(gids)), sorted(set(gids) - set(sids))
                drift = [k for k in set(sids) & set(gids)
                         if abs((sids[k]["weight"] or 0) - (gids[k]["weight"] or 0)) > 1e-6
                         or sids[k]["description"].strip() != gids[k]["description"].strip()]
                Q.say("1.5c judge.toml vs graded", f"missing_in_graded={missing} extra_in_graded={extra} weight_or_text_drift={drift}")
            if rp.get("rubric"):
                Q.say("1.5c report.rubric count", f"{len(rp['rubric'])} ({'ok' if len(rp['rubric']) == len(rg['criteria']) else 'MISMATCH'})")
        elif ran:
            Q.say("1.5c rubric", "judge ran but no graded criteria shipped: MISMATCH")
        else:
            Q.say("1.5c rubric", f"not judged ({reason}); reward must equal pytest: {ch.get('reward')} vs {ch.get('pytest')}")
        # d. polarity in the compiled rubric
        if SRC:
            bad = [c["id"] for c in SRC if (c["weight"] < 0) == c["is_positive"] or c["negate"]]
            Q.say("1.5d polarity mismatches", bad or "none")
            tot_pos = sum(c["source_weight"] for c in SRC if c["is_positive"] and isinstance(c["source_weight"], (int, float)))
            tot_neg = sum(abs(c["source_weight"]) for c in SRC if not c["is_positive"] and isinstance(c["source_weight"], (int, float)))
            Q.say("1.5d source weights", f"positive={tot_pos} penalty={tot_neg} normalised positives sum={round(sum(c['weight'] for c in SRC if c['weight'] > 0), 4)}")
        # e. combination
        wts = rp.get("weights") or POL or {}
        chans = {k: ch[k] for k in wts if k in ch}
        if chans and ch.get("reward") is not None:
            comb = round(sum(ch[k] * wts[k] for k in chans) / sum(wts[k] for k in chans), 4)
            Q.say("1.5e combination", f"weights={wts} -> {comb} vs reward {ch['reward']}  {'ok' if abs(comb - ch['reward']) <= 0.0001 else 'MISMATCH'}")
        # f. the run finished
        tr = Q.trajectory(run); st = Q.agent_steps(tr)
        last = next((Q.step_text(s) for s in reversed(st) if Q.step_text(s).strip()), "")
        fm = Q.final_message(run)
        Q.say("1.5f run", f"exception_info={res.get('exception_info')} errored={rp.get('errored')} state_capture_failed={rp.get('state_capture_failed')} agent_steps={len(st)} last_step_source={(tr or {}).get('steps', [{}])[-1].get('source') if tr else None}")
        Q.say("1.5f final message", f"final_message.md={None if fm is None else len(fm)} chars, last agent text={len(last)} chars, same={'n/a' if fm is None else (fm.strip() == last.strip())}")
        Q.say("1.5f tokens/cost", f"final_metrics={(tr or {}).get('final_metrics')} agent_result={res.get('agent_result')}")
PY
```

**Decision rule.**

| Check | BLOCKER if |
|---|---|
| 1.5a | spread > 0.0001 between reward.json, report.final_reward, result.verifier_result and pass_summary.per_run |
| 1.5b | pytest recompute ≠ reported (±0.0001); a weighted test with no ledger row, or a ledger row with a different weight than test_weights.json |
| 1.5c | rubric recompute ≠ reported; judge ran but no graded criteria; a criterion of judge.toml missing from or extra in the graded set, or its weight/text drifted; `raw` values other than yes/no |
| 1.5d | any polarity mismatch or `negate` in the compiled rubric |
| 1.5e | the channel combination with the stated weights ≠ reward |
| 1.5f | `exception_info` set or `errored` true while the run is counted as completed; the last step is not an agent step with text |
| 1.5c (MAJOR) | judge did not run (`ran=false`) and the bundle is otherwise complete: the rubric channel is missing, reward = pytest alone; name the reason |
| 1.5b (MAJOR) | a test raised (`error` set) rather than passing or failing |
| 1.5f (MAJOR) | final_message.md differs from the last agent text |

If any BLOCKER trips, tag `SIGNOFF_BLOCKED` on the bundle.

---

## Section 1.6 — pass@k and aggregate sanity

**Goal.** `pass_summary.json` (and `pass@N.json` when shipped) must reconcile with the per-run
files and the folders on disk.

```bash
python3 - <<'PY'
# §1.6 pass@k and per-run aggregate sanity, per model folder
import qc_lib as Q, statistics
W = Q.weights() or {}
for md in Q.model_dirs():
    print(f"== {md.name}")
    rs = Q.runs(md); ps = Q.pass_summary(md); pk = Q.passk(md); jb = Q.jobs(md)
    Q.say("run folders", [r.name for r in rs])
    if not Q.ok(ps):
        Q.say("pass_summary.json", "MISSING or CORRUPT: AGGREGATE_MISSING"); continue
    per = ps.get("per_run") or []
    Q.say("1.6a counts", f"runs={ps.get('runs')} completed={ps.get('runs_completed')} errored={ps.get('runs_errored')} per_run={len(per)} folders={len(rs)}  "
          f"{'ok' if ps.get('runs') == len(per) == len(rs) and (ps.get('runs_completed') is None or ps['runs_completed'] + (ps.get('runs_errored') or 0) == ps['runs']) else 'MISMATCH'}")
    th = ps.get("threshold", W.get("threshold")); Q.say("1.6b threshold", f"pass_summary={ps.get('threshold')} test_weights={W.get('threshold')} pass@N={(pk or {}).get('threshold')}  {'ok' if len({x for x in (ps.get('threshold'), W.get('threshold'), (pk or {}).get('threshold')) if x is not None}) <= 1 else 'MISMATCH'}")
    bad_pass, bad_score = [], []
    for r in per:
        run = md / f"run_{r.get('run_index')}"
        ch, _ = Q.channels(run) if run.is_dir() else ({}, {})
        if ch.get("reward") is not None and r.get("combined_score") is not None and abs(ch["reward"] - r["combined_score"]) > 0.0001:
            bad_score.append(r.get("run_index"))
        expect = (not r.get("errored")) and r.get("combined_score") is not None and th is not None and r["combined_score"] >= th
        if bool(r.get("passed")) != bool(expect):
            bad_pass.append((r.get("run_index"), r.get("passed"), r.get("combined_score")))
    Q.say("1.6c per_run.combined == run reward", f"mismatch runs={bad_score or 'none'}")
    Q.say("1.6c pass rule (reward >= threshold, not errored)", f"violations={bad_pass or 'none'}")
    done = [r for r in per if not r.get("errored") and r.get("combined_score") is not None]
    for key, fld in (("average_combined_score", "combined_score"), ("average_pytest_score", "pytest_score"), ("average_rubric_score", "rubric_score")):
        vals = [r[fld] for r in done if r.get(fld) is not None]
        mean = round(statistics.fmean(vals), 4) if vals else None
        Q.say(f"1.6d {key}", f"reported={ps.get(key)} recomputed={mean} over {len(vals)} runs  {'ok' if mean is None or ps.get(key) is None or abs(mean - ps[key]) <= 0.0001 else 'MISMATCH'}")
    Q.say("1.6e flags", f"runs_without_rubric={ps.get('runs_without_rubric')} runs_with_state_capture_failed={ps.get('runs_with_state_capture_failed')} errored_run_indices={ps.get('errored_run_indices')} judge_models={ps.get('judge_models')}")
    if Q.ok(pk):
        c = sum(1 for r in per if r.get("passed")); n = len(per)
        Q.say("1.6f pass@N.json", f"passed={pk.get('passed')} (recomputed {c}) pass_rate={pk.get('pass_rate')} (recomputed {round(c / n, 4) if n else None}) attempts_per_task={pk.get('attempts_per_task')} at={pk.get('at')}")
        rpr = pk.get("reward_per_run") or {}
        drift = [k for k, v in rpr.items() if (per_by := {str(r.get('run_index')): r for r in per}).get(k) is None or abs((per_by[k].get('combined_score') or 0) - v) > 0.0001]
        Q.say("1.6f reward_per_run vs per_run", f"drift={drift or 'none'} mean_reward_per_trial={pk.get('mean_reward_per_trial')} vs {ps.get('average_combined_score')}")
        hist = pk.get("failure_mode_histogram") or {}
        Q.say("1.6f failure_mode_histogram", f"{hist} sum={sum(hist.values())} runs={n}  {'ok' if sum(hist.values()) == n else 'MISMATCH'}")
    else:
        Q.say("1.6f pass@N.json", "not shipped (trimmed bundle): pass_summary.per_run is the aggregate")
    if Q.ok(jb):
        Q.say("1.6g jobs.json", [(j.get("job"), len(j.get("trials") or [])) for j in jb])
    modes = sorted({str(r.get("failure_mode")) for r in per})
    Q.say("1.6h failure modes", modes)
PY
```

**Decision rule.**

| Check | BLOCKER if |
|---|---|
| 1.6a | runs ≠ per_run entries ≠ run folders, or completed + errored ≠ runs |
| 1.6b | thresholds disagree between pass_summary, test_weights and pass@N |
| 1.6c | a per_run combined_score differs from that run's reward, or a `passed` bit disagrees with `reward >= threshold and not errored` |
| 1.6d | any average differs from the recomputed mean over completed runs (±0.0001) |
| 1.6f | pass@N.json `passed`, `pass_rate`, `reward_per_run` or the histogram sum disagree (full bundles only) |
| 1.6e (MAJOR) | a run listed in `runs_with_state_capture_failed` or `runs_without_rubric` that §2 does not explain |

If any BLOCKER trips, tag `AGGREGATE_UNRELIABLE`.

---

## Section 2 — Classify the failure

**Goal.** For every run that did not pass, classify into exactly ONE bucket: **A
(environment)** or **B (model/agent)**, with evidence. A low reward is a result, not a defect;
this section says *why* it is low.

```bash
python3 - <<'PY'
# §2 failure classification, per run
import qc_lib as Q, re, collections
ERR = re.compile(r"connection refused|ECONNREFUSED|Internal Server Error|HTTP/?\s*5\d\d|\"status\":\s*\"error\"|Traceback \(most recent call last\)|\b(AttributeError|KeyError|TypeError|NameError|RuntimeError):|timed out|ReadTimeout|Service Unavailable", re.I)
W = Q.weights() or {}
for md in Q.model_dirs():
    ps = Q.pass_summary(md) or {}; per = {r.get("run_index"): r for r in ps.get("per_run") or []}
    for run in Q.runs(md):
        i = Q.run_index(run); print(f"== {md.name}/{run.name}")
        ch, _ = Q.channels(run); rp = Q.report(run) or {}; res = Q.result(run) or {}
        th = ps.get("threshold", W.get("threshold", 0.7))
        passed = (per.get(i) or {}).get("passed", ch.get("reward") is not None and ch["reward"] >= th)
        Q.say("2.0 passed", f"{passed}  reward={ch.get('reward')} threshold={th} failure_mode={(per.get(i) or {}).get('failure_mode')}")
        # 2.1 environment evidence
        ran, reason, _ = Q.judge_ran(run)
        v = run / "verifier"
        scf = (v / "state_capture_failed.txt").read_text(errors="replace").strip() if (v / "state_capture_failed.txt").is_file() else None
        Q.say("2.1a state capture", f"failed={rp.get('state_capture_failed')} note={scf!r} end_env.json={'shipped' if (v / 'end_env.json').is_file() else 'ABSENT'}")
        Q.say("2.1b trial exception / errored", f"{res.get('exception_info')} / {rp.get('errored')}")
        Q.say("2.1c judge", f"ran={ran} reason={reason} rubric_judge_failed.txt={'present' if (v / 'rubric_judge_failed.txt').is_file() else 'absent'}")
        tr = Q.trajectory(run); calls = Q.tool_calls(tr); obs = Q.observations(tr)
        mcp = [(s, n) for s, n, _ in calls if Q.split_tool(n)[0]]
        Q.say("2.1d tool calls", f"total={len(calls)} mcp={len(mcp)} local={len(calls) - len(mcp)}  {'NO MCP CALLS' if not mcp else 'ok'}")
        bad_obs = [(s, c[:160].replace(chr(10), ' ')) for s, _, c in obs
                   if c and not re.match(r'\s*\{\s*"status"\s*:\s*"ok"', c) and ERR.search(c)]   # a server answer that starts ok is data, whatever it quotes
        Q.say("2.1e tool results that look like server errors", f"{len(bad_obs)}")
        for s, c in bad_obs[:12]:
            print(f"      step {s}: {c}")
        # 2.2 model / agent evidence
        inv = collections.Counter(n for _, n, _ in calls)
        print("   2.2a tool inventory (count, tool):")
        for n, k in inv.most_common(40):
            print(f"      {k:4d}  {n}")
        per_srv = collections.defaultdict(lambda: [0, 0])
        for _, n, _ in calls:
            s, verb = Q.split_tool(n)
            per_srv[s or '(local)'][1 if Q.is_write(verb) else 0] += 1
        Q.say("2.2b per server [reads, writes]", dict(per_srv))
        wired = [p.stem for p in (Q.B / "environment" / "light-servers" / "world_data").glob("*.json")] if (Q.B / "environment" / "light-servers" / "world_data").is_dir() else []
        Q.say("2.2c wired servers never called", sorted(set(wired) - set(per_srv)) or "none")
        led = Q.ledger(run) or {"guards_tripped": [], "missed": []}
        Q.say("2.2d guards tripped", led["guards_tripped"] or "none")
        Q.say("2.2e positive tests missed", f"{len(led['missed'])}: {led['missed'][:12]}")
        fm = Q.final_message(run) or ""
        print("   2.2f final message (first 1200 chars):"); print("      " + fm[:1200].replace("\n", "\n      "))
        rg = Q.rubric_graded(run)
        if rg:
            print("   2.2g criteria judged no (id, weight, description -> reasoning):")
            for c in [c for c in rg["criteria"] if not c["value"]][:20]:
                print(f"      ({c['id']}, {round(c['weight'] or 0, 4)}) {c['description'][:110]}\n          WHY: {(c['reasoning'] or '')[:220]}")
PY
```

### 2.1 Bucket A — environment

Any ONE is sufficient, when it plausibly caused the lost tests or criteria:
- `state_capture_failed` set, `end_env.json` absent: every state check fails closed.
- `exception_info` set, or `errored` true.
- the judge did not run for an infrastructure reason (login, timeout), so the rubric is missing.
- **no MCP calls at all**, or the servers answered errors (2.1e) on calls the task needs
  (a crashing server, `ECONNREFUSED`, a traceback in the result).
- tool results that are empty or malformed for a server the task depends on.

### 2.2 Bucket B — model / agent (default)

Environment healthy but the trajectory shows the model called the wrong tools or never the
required ones, gave up, ignored explicit steps, wrote the wrong value, or tripped a guard.

| Sub-label | Trigger |
|---|---|
| `tool-surface-tunnel-vision` | 2.2c lists wired servers the task needs that were never called, and the final message claims they were unavailable or unnecessary |
| `gave-up-early` | the final message admits stopping without attempting a required write |
| `guard-tripped` | 2.2d non-empty |
| `wrong-value-written` | writes happened but 2.2g shows wrong figures, recipients or records |
| `instruction-ignored` | required steps skipped although the tools were called |
| `stale-read` | the task re-delivers data mid-run and the agent used the early values (2.2e names re-read tests) |

**Decision.** `passed=true` → N/A. Else 2.1 evidence present and explanatory → **A**;
otherwise **B** with one sub-label. State the two or three lines of evidence with paths.

---

## Section 3 — Reasoning presence

**Goal.** Is the model's reasoning carried in the trajectory? The bridge agent copies the
model's reasoning onto each agent step as `reasoning_content` (ATIF's field) or, in bundles
packaged before 2026-10-26, as `thought`. No raw provider stream ships, so signatures cannot be
checked; that is N/A, never a blocker.

```bash
python3 - <<'PY'
# §3 reasoning presence, per run
import qc_lib as Q
for md in Q.model_dirs():
    for run in Q.runs(md):
        tr = Q.trajectory(run); st = Q.agent_steps(tr); cfg = Q.config(run) or {}
        keys = {k for s in st for k in ("reasoning_content", "thought") if s.get(k)}
        n = sum(1 for s in st if Q.reasoning(s)); chars = sum(len(Q.reasoning(s)) for s in st)
        eff = (cfg.get("agent", {}).get("kwargs") or {}).get("reasoning_effort")
        print(f"== {md.name}/{run.name}")
        Q.say("agent steps / with reasoning", f"{len(st)} / {n}  ({chars} chars) field(s) used: {sorted(keys) or 'none'}")
        Q.say("reasoning_effort requested", eff)
        Q.say("per-step metrics present", f"{sum(1 for s in st if s.get('metrics'))} of {len(st)}")
        verdict = "present" if n else ("ABSENT with reasoning_effort set: ESCALATE" if eff else "absent (no effort requested)")
        Q.say("verdict", verdict)
PY
```

| Result | Meaning |
|---|---|
| steps with reasoning > 0 | ✅ present (report the field used and the count) |
| 0 with `reasoning_effort` requested | ❌ **MAJOR** `REASONING_ABSENT`: the harness dropped it; escalate |
| 0 with no effort requested | ✅ expected |
| per-step `metrics` absent | INFO (the bridge agent records totals only, in `final_metrics`) |

---

## Section 4 — Rubric ↔ pytest overlap

**Goal.** Both channels look at the same run by design; the question is whether one outcome
is scored twice as if it were two signals. Pytest names lie, so the matcher uses the literals
each test asserts and its name tokens against the criterion text of the compiled rubric.

```bash
python3 - <<'PY'
# §4 rubric <-> pytest overlap (AST literals + name tokens), per bundle, with lost-weight per run
import qc_lib as Q, ast, re, json
src = Q.test_source(); SRC = Q.rubric_source() or []; W = Q.weights() or {"tests": {}}
tree = ast.parse(src)
STOP = {"the","a","an","of","in","to","is","and","for","that","by","with","on","from","was","were","its","it","as","at","be","or","test","agent"}
def toks(s): return set(re.findall(r"[a-z0-9]+", s.lower().replace("_", " "))) - STOP
def literals(node):
    return [str(n.value) for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, (str, int, float)) and not isinstance(n.value, bool)]
facts = {}
for f in tree.body:
    if isinstance(f, ast.FunctionDef) and f.name.startswith("test_"):
        A = [a for a in ast.walk(f) if isinstance(a, ast.Assert)]
        rets = [r for r in ast.walk(f) if isinstance(r, ast.Return) and r.value is not None]
        lits = {l for n in A + rets for l in literals(n) if len(l) > 1}
        facts[f.name] = {"asserts": len(A), "returns": len(rets), "lits": sorted(lits), "doc": (ast.get_docstring(f) or "")[:160]}
    elif isinstance(f, ast.Assign) and any(isinstance(t, ast.Name) and t.id.startswith("test_") for t in f.targets):
        for t in f.targets:
            if isinstance(t, ast.Name):
                facts[t.id] = {"asserts": 0, "returns": 0, "lits": sorted({l for l in literals(f.value) if len(l) > 1}), "doc": "(bound by assignment)"}
rows = []
for tname, tf in facts.items():
    tt = toks(tname) | toks(tf["doc"]); tl = {l.lower() for l in tf["lits"]}
    best = None
    for c in SRC:
        ct = toks(c["description"]); cl = c["description"].lower()
        s1 = len(tt & ct) / max(1, len(tt | ct))
        s2 = sum(1 for L in tl if L in cl) / max(2, len(tl)) if tl else 0.0   # one shared literal alone never reaches 0.5
        comp = 0.5 * s1 + 0.5 * s2
        if best is None or comp > best[0]:
            best = (comp, s1, s2, c)
    w = W["tests"].get(tname)
    if best is None:
        rows.append(("NO RUBRIC", tname, w, None)); continue
    v = "DOUBLE-COUNTED" if best[0] >= 0.5 else "PARTIAL" if best[0] >= 0.3 else "INDEPENDENT"
    if v == "DOUBLE-COUNTED" and isinstance(w, (int, float)) and w < 0:
        v += " guard" if not best[3]["is_positive"] else " (guard vs positive criterion)"
    rows.append((v, tname, w, best))
rows.sort(key=lambda r: (-(r[3][0] if r[3] else 0), r[1]))
print(f"tests={len(facts)} criteria={len(SRC)}")
print("| verdict | pytest | w | S1 name | S2 literals | crit | criterion (snip) |"); print("|---|---|---|---|---|---|---|")
for v, n, w, b in rows:
    if b: print(f"| {v} | `{n}` | {w} | {b[1]:.2f} | {b[2]:.2f} | {b[3]['id']} ({'+' if b[3]['is_positive'] else '-'}{b[3]['source_weight']}) | {b[3]['description'][:70]} |")
    else: print(f"| {v} | `{n}` | {w} | | | | |")
covered = {b[3]["id"] for _, _, _, b in rows if b and b[0] >= 0.5}
dc = sum(1 for r in rows if r[0].startswith("DOUBLE")); pa = sum(1 for r in rows if r[0] == "PARTIAL")
print(f"\nDOUBLE-COUNTED={dc} PARTIAL={pa} INDEPENDENT={len(rows) - dc - pa} redundancy={dc / max(1, len(rows)):.0%}")
print(f"RUBRIC-ONLY (no test reaches 0.5): {len(SRC) - len(covered)} of {len(SRC)}")
for c in SRC:
    if c["id"] not in covered: print(f"- ({c['id']}, {'+' if c['is_positive'] else '-'}{c['source_weight']}, {c['tag']}) {c['description'][:90]}")
for md in Q.model_dirs():
    for run in Q.runs(md):
        led = Q.ledger(run); rg = Q.rubric_graded(run)
        if led and led["total_positive"]:
            p_lost = sum(r["weight"] for r in led["rows"] if isinstance(r["weight"], (int, float)) and r["weight"] > 0 and not r["passed"])
            print(f"{md.name}/{run.name} pytest positive lost {p_lost}/{led['total_positive']} = {p_lost / led['total_positive']:.1%}; guards charged {led['penalty']}")
        if rg and rg["criteria"]:
            r_tot = sum(c["weight"] for c in rg["criteria"] if (c["weight"] or 0) > 0); r_lost = sum(c["weight"] for c in rg["criteria"] if (c["weight"] or 0) > 0 and not c["value"])
            r_pen = sum(-c["weight"] for c in rg["criteria"] if (c["weight"] or 0) < 0 and c["value"])
            print(f"{md.name}/{run.name} rubric positive lost {r_lost:.4f}/{r_tot:.4f} = {r_lost / r_tot:.1%}; penalties charged {r_pen:.4f}")
PY
```

| Composite | Verdict |
|---|---|
| ≥ 0.5, both positive | **DOUBLE-COUNTED positive**: the same outcome scored twice |
| ≥ 0.5, test is a guard | **DOUBLE-COUNTED guard** (penalty twins are intentional distractor design: note, do not fail) |
| 0.3 – 0.5 | **PARTIAL**: read both and decide |
| < 0.3 | **INDEPENDENT** |
| criterion with no test ≥ 0.5 | **RUBRIC-ONLY** (what the judge alone grades: prose, explanation, provenance) |

Report redundancy (% of tests double-counted), the lost-weight ratios per channel, and a
recommendation (`keep both` / `dedupe positives` / `drop guard twin`). §4 findings are
**MAJOR at most**: the same files were audited before the run by the RUTHLESS check.

---

## Section 5 — False / hard-coded pytest detection

**Goal.** Flag tests that pass by construction rather than by verifying the agent. Tests in
this harness are return-style (`return <bool>`) or assert-style; a guard under
`guard_polarity = pass_charges` **passes when the misbehaviour is detected** and is charged
for it, so a guard that "asserts the wrong behaviour" is correct design.

```bash
python3 - <<'PY'
# §5 false / hardcoded pytest detection (AST), per bundle; pass bits from the ledger of each run
import qc_lib as Q, ast, re
src = Q.test_source(); SRC = Q.rubric_source() or []; W = Q.weights() or {"tests": {}}
tree = ast.parse(src)
funcs = {f.name: f for f in tree.body if isinstance(f, ast.FunctionDef)}
EVIDENCE = re.compile(r"ATLAS_TRAJECTORY|ATLAS_END_ENV|ATLAS_OUTPUT_ROOTS|end_env|agent_trajectory|final_message|_end\(|_steps\(|_calls\(|_writes\(|_final\(|workspace|"
                      r"L\.(?!(has|norm|as_float|near|numbers_in|fmt|words_to_number|cosine|tokens|index|score_claim|install_skip_fixture|split_tool|load_fixture|sentences)\b)\w+\(", re.I)
FIXTURE = re.compile(r"ATLAS_ORACLE|ATLAS_OLD_ENV|oracle\.json|old_env\.json|_oracle\(|_seed\(|_reported\(|gt_env|ground_truth", re.I)
ALIASES = set()           # module-level names bound to claims_lib helpers: _steps = L.steps
ASSIGNS = {}              # module-level assignments by name: _PROJ = {...}
for n in tree.body:
    if isinstance(n, ast.Assign):
        for t in n.targets:
            if isinstance(t, ast.Name):
                ASSIGNS[t.id] = n.value
                if isinstance(n.value, ast.Attribute) and isinstance(n.value.value, ast.Name) and n.value.value.id == "L":
                    ALIASES.add(t.id)
REGISTRY = {}             # registry dict name -> functions a decorator registers into it (@projection("x") -> _PROJ[name] = fn)
for dec in funcs.values():
    for reg in re.findall(r"^\s*(\w+)\[[^\]]+\]\s*=\s*\w+\s*$", ast.unparse(dec), re.M):
        for f in funcs.values():
            if any((isinstance(d, ast.Call) and ast.unparse(d.func) == dec.name) or (isinstance(d, ast.Name) and d.id == dec.name) for d in f.decorator_list):
                REGISTRY.setdefault(reg, set()).add(f.name)
def names_in(node):
    return {x.id for x in ast.walk(node) if isinstance(x, ast.Name)} | {x.attr for x in ast.walk(node) if isinstance(x, ast.Attribute)}
def reaches(node, pat, seen=None):
    """True when the function (or value) matches the pattern itself, names an alias of a
    claims_lib helper, or references, transitively, a module function / value that does."""
    seen = seen if seen is not None else set()
    key = node.name if isinstance(node, ast.FunctionDef) else id(node)
    if key in seen: return False
    seen.add(key)
    if pat.search(ast.unparse(node)): return True
    names = names_in(node)
    if pat is EVIDENCE and names & ALIASES: return True
    for nm in names:
        if nm in funcs and funcs[nm] is not node and reaches(funcs[nm], pat, seen): return True
        if nm in ASSIGNS and ASSIGNS[nm] is not node and reaches(ASSIGNS[nm], pat, seen): return True
        if nm in REGISTRY and any(reaches(funcs[g], pat, seen) for g in REGISTRY[nm] if funcs[g] is not node): return True
    return False
ANSWER = set()
for c in SRC:
    ANSWER |= set(re.findall(r"\b\d[\d,]*\.?\d*\b", c["description"]))
ANSWER = {a.replace(",", "") for a in ANSWER if len(a.replace(",", "")) >= 3}
def bool_const(a): return isinstance(a.test, ast.Constant) and a.test.value is True   # `assert False, msg` is a deliberate failure, not a constant pass
def self_compare(a): return isinstance(a.test, ast.Compare) and len(a.test.comparators) == 1 and ast.dump(a.test.left) == ast.dump(a.test.comparators[0])
def or_true(fn): return any(isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or) and any(isinstance(v, ast.Constant) and v.value is True for v in n.values) for n in ast.walk(fn))
def swallows(fn):
    for n in ast.walk(fn):
        if isinstance(n, ast.Try):
            for h in n.handlers:
                if h.type is None or (isinstance(h.type, ast.Name) and h.type.id == "Exception"):
                    body = "\n".join(ast.dump(s) for s in h.body)
                    if "Assert" not in body and "Raise" not in body: return True
    return False
def returns_true_const(fn):
    rets = [r for r in ast.walk(fn) if isinstance(r, ast.Return) and r.value is not None]
    return bool(rets) and all(isinstance(r.value, ast.Constant) and r.value.value is True for r in rets)
def wildcard_in(fn):
    for a in ast.walk(fn):
        if isinstance(a, ast.Compare) and any(isinstance(o, ast.In) for o in a.ops) and isinstance(a.left, ast.Constant) and a.left.value in ("", 0, None): return True
    return False
def literal_hits(fn):
    lits = {str(n.value).replace(",", "") for n in ast.walk(fn) if isinstance(n, ast.Constant) and isinstance(n.value, (str, int, float)) and not isinstance(n.value, bool)}
    return sorted(lits & ANSWER)
leds = {f"{md.name}/{run.name}": Q.ledger(run) for md in Q.model_dirs() for run in Q.runs(md)}
rows = []
for name, fn in funcs.items():
    if not name.startswith("test_"): continue
    A = [a for a in ast.walk(fn) if isinstance(a, ast.Assert)]
    rets = [r for r in ast.walk(fn) if isinstance(r, ast.Return) and r.value is not None]
    flags = []
    raises = [r for r in ast.walk(fn) if isinstance(r, ast.Raise)] + [c for c in ast.walk(fn) if isinstance(c, ast.Call) and ast.unparse(c.func).endswith("fail")]
    if not A and not rets and not raises: flags.append("NO_VERDICT")
    if any(bool_const(a) for a in A) or (not A and not raises and returns_true_const(fn)): flags.append("CONST_VERDICT")
    if any(self_compare(a) for a in A): flags.append("SELF_COMPARE")
    if or_true(fn): flags.append("OR_TRUE")
    if wildcard_in(fn): flags.append("WILDCARD_IN")
    if swallows(fn): flags.append("SWALLOWED_EXCEPT")
    if not reaches(fn, EVIDENCE): flags.append("NO_AGENT_EVIDENCE" if reaches(fn, FIXTURE) else "NO_EVIDENCE_READ")
    hits = literal_hits(fn)
    if hits: flags.append("ANSWER_LITERAL:" + ",".join(hits[:4]))
    w = W["tests"].get(name)
    passes = {k: next((r["passed"] for r in (l or {}).get("rows", []) if r["test"] == name), None) for k, l in leds.items()}
    if isinstance(w, (int, float)) and w > 0 and any(passes.values()) and any(f in flags for f in ("NO_VERDICT", "CONST_VERDICT", "SELF_COMPARE", "OR_TRUE")):
        flags.append("PASSED_TRIVIALLY")
    rows.append((name, w, passes, flags))
print("| pytest | w | passed per run | flags |"); print("|---|---|---|---|")
for n, w, p, fl in rows:
    print(f"| {'FLAG' if fl else 'ok'} `{n}` | {w} | {p} | {', '.join(fl) or '-'} |")
print(f"\n{sum(1 for r in rows if r[3])}/{len(rows)} tests carry a flag; BLOCKER flags: {sum(1 for r in rows if any(f in r[3] for f in ('NO_VERDICT','CONST_VERDICT','SELF_COMPARE','OR_TRUE','PASSED_TRIVIALLY')))}")
print("\n5.2 assert/return lines carrying a rubric figure:")
seen_lines = set()
for i, line in enumerate(src.splitlines(), 1):
    hits = [a for a in ANSWER if a in line]
    if hits and ("assert" in line or "return" in line) and i not in seen_lines:
        seen_lines.add(i); print(f"  L{i} {sorted(hits, key=len, reverse=True)[:3]}: {line.strip()[:140]}")
PY
```

| Flag | What it means | Severity |
|---|---|---|
| `NO_VERDICT` | no assert, no return value, no raise: cannot fail | **BLOCKER** |
| `CONST_VERDICT` | `assert True`, or every return is `return True` with no assert or raise | **BLOCKER** |
| `SELF_COMPARE` | `assert x == x` | **BLOCKER** |
| `OR_TRUE` | `cond or True` | **BLOCKER** |
| `PASSED_TRIVIALLY` | a positive test with one of the above that passed in a run | **BLOCKER** |
| `SWALLOWED_EXCEPT` | `except: pass` around the verdict | **MAJOR** |
| `WILDCARD_IN` | `"" in body` | **MAJOR** |
| `NO_AGENT_EVIDENCE` | reads oracle / seed only, never the tool log, end state, files or final message (transitively through helpers) | **MAJOR** |
| `NO_EVIDENCE_READ` | reads nothing at all | **MAJOR** |
| `ANSWER_LITERAL:<n>` | asserts a figure the rubric also grades: likely double-counted (§4) and a drift hazard if not read from oracle.json | **MINOR** |

§5 BLOCKER flags are reported as **MAJOR** here (the RUTHLESS check owns the authoring verdict);
they still go in the report with the line numbers.

---

## Section 6 — Report format

Write the report to `REPORT.md`:

```markdown
# QC Report — <uuid>   layout: full | trimmed   runs: <n>   model(s): <…>

## §1 Model
- per run: config / result / report / trajectory agree → ✅ | ❌ (BLOCKER)
- ATIF version(s), agent version

## §1.5 Score sanity (per run)
- reward agreement spread, pytest recompute, rubric recompute, judge ran, polarity, combination, run completion

## §1.6 Aggregates
- counts, threshold, pass bits, averages, pass@N (or "not shipped")

## §2 Failure classification (per run)
- passed / reward vs threshold / bucket / sub-label / evidence (2-3 lines with paths)

## §3 Reasoning
- steps with reasoning / field / effort / verdict

## §4 Overlap
- tests, criteria, double-counted, partial, rubric-only, redundancy, lost-weight ratios, recommendation

## §5 False pytests
- scanned, flagged, blocker-class flags (as MAJOR), list with line numbers

## Verdict
- SIGNED | REVIEW | BLOCKED, with the section ids that decided it
```

**Verdict mapping.** Any §1, §1.5 or §1.6 BLOCKER → `"verdict": "FAIL"`. §2 is a
classification, never a failure. §3, §4 and §5 findings are `major` / `minor` only.

---

## Section 7 — Reference: verified against `5b10675f-e16b-5f22-ae7f-d8040f6324c4` (trimmed layout, 2026-10-26)

| Section | Result |
|---|---|
| §1 | `opus-5` everywhere (`anthropic/claude-opus-5` in config and steps, `claude-opus-5` in result), openhands-sdk v1.58.0, ATIF-v1.5, effort high ✅ |
| §1.5 | reward 0.2529 in all four files; pytest 0.3182 = (14 − 0)/44 from `report.json.pytest` (no grade_report.json shipped), 12 missed, no guard tripped; rubric 0.1875 = Σ weight·value over 35 criteria (20 yes), judge gpt-5.6-sol; 0.5·0.3182 + 0.5·0.1875 = 0.2529 ✅ |
| §1.6 | 1 run, threshold 0.7, passed false, averages match; pass@N.json not shipped ✅ |
| §2 | failed, `partial`; end_env shipped, judge ran, 84 calls (74 MCP), no server errors → **Bucket B**, `stale-read` (missed `test_ingest_counts_were_read_after_the_redelivery`, `test_late_counts_were_read_before_the_ticket_was_closed`, `test_source_owners_were_read_after_the_handover`); LightAmplitude, LightGithub, LightMixpanel wired but never called (decoys) |
| §3 | 30 of 85 agent steps carry `thought` (17 381 chars) ✅ present |
| §4 | 33 tests vs 35 criteria: 0 double-counted, 4 partial, 29 independent; 35 criteria rubric-only ✅ |
| §5 | 0 of 33 flagged ✅ |

# RUTHLESS QC — Rubric & Pytest Correctness Audit

> **Persona:** You are a 20-year industry veteran QA architect. You have seen careers end over
> sloppy eval design. Your job is to ruthlessly critique the correctness of the **rubric** and the
> **pytest** suite for this task. Assume the author's CTO will personally review your findings —
> **if anything is wrong and you miss it, someone gets fired.** Be paranoid. Be specific. Cite
> line numbers and exact code. "Looks fine" is not an acceptable verdict unless you have proven it.

---

## 0. Inputs Under Audit

| Artifact | What it is |
|---|---|
| `pytest` file(s) | Standalone test suite that grades the agent's **behavior** (tool calls) |
| Rubric | Human/model-graded criteria for the same task |
| Task prompt | The source of truth for what is and is not "defined in the prompt" |

Read **all three** in full before writing a single finding. Every verdict below must be justified
against the actual text of these artifacts, not your assumptions.

---

## 1. Hard Constraint Checks (Automatic FAIL if violated)

Go through **every single test case, assertion, fixture, and helper** in the pytest file(s) and
check each of the following. For each constraint, list every violating line. If there are zero
violations, state explicitly: "Checked all N test cases — no violations."

### ❌ C1. No file-content checks
- Does **any** test case open, read, parse, hash, diff, or otherwise inspect the **content** of a
  file produced by the agent?
- This includes sneaky variants: `open(...).read()`, `Path.read_text()`, `json.load()`,
  `csv.reader`, `pandas.read_*`, regex over file bytes, checksum/hash comparison, image pixel
  inspection, PDF text extraction, snapshot comparison.
- **Any of the above = FAIL.** The pytest layer must not grade file content.

### ❌ C2. No hardcoded file names or extensions (unless defined in the prompt)
- Does any test assert on a specific file name (e.g., `report.csv`, `output.png`) or a specific
  extension (`.endswith(".xlsx")`, glob patterns like `*.pdf`)?
- **Exception:** the name/extension is **explicitly stated in the task prompt**. Quote the exact
  prompt sentence that defines it. No quote → no exception → FAIL.
- Watch for indirect hardcoding: constants at the top of the file, fixtures that build paths,
  string interpolation that reconstructs a fixed name.

### ❌ C3. No file-size or file-dimension checks
- Does any test assert on byte size (`os.path.getsize`, `stat().st_size`, `len(data)`),
  image dimensions (width/height), page counts, row/column counts, duration, resolution, or any
  other size/dimension property of an output file?
- **These must never be tested. Any occurrence = FAIL.**

### ✅ C4. Pytest grades tool-call behavior — and ONLY that
- Confirm the pytest layer grades exactly two things:
  1. The **correct/required tool calls were made** (right tools, and where the prompt demands it,
     right order / right arguments as defined by the prompt).
  2. The **forbidden tool calls were avoided**.
- Verify the mechanism: tests should inspect a tool-call log/transcript/recorder — not the
  filesystem, not the environment state, not the answer.
- Flag any required tool that is **not** asserted, and any forbidden tool that is **not** checked
  for absence. Missing coverage here is a correctness bug too.
- **Read/write balance — count them.** Tally how many positive-weight tests assert **write/mutating
  tool calls** (create, update, delete, send, upload, post) versus **read-only calls** (get, list,
  open, search). If fewer than **5** tests assert write calls, **flag it**: read calls are
  near-free reward — any agent that pokes around the environment satisfies them without doing the
  actual work. The graded signal must be dominated by the writes the prompt demands. (If the
  prompt genuinely demands fewer than 5 distinct writes, say so explicitly and show the tally —
  the check is on missing write coverage, not on inventing writes the prompt never asked for.)

### ❌ C5. No grading of file content, state, or the numeric answer
- Beyond C1: does any test grade the **final numeric answer**, computed values, environment
  state (created dirs, env vars, DB rows, side effects), or agent message text as a proxy for
  the answer?
- Asserting on the *result* instead of the *behavior* = FAIL at the pytest layer. That is the
  rubric's job, not pytest's.

---

## 2. Rubric ↔ Pytest Overlap Check (Automatic FAIL if violated)

Build an explicit cross-reference table:

| Rubric item | What it grades | Nearest pytest test | Overlap? (Y/N) | Evidence |
|---|---|---|---|---|

- **No rubric item may grade the same thing as any test case, and vice versa.**
- Overlap = double-jeopardy grading. One mistake gets punished twice; graders disagree; scores
  become garbage. **Any overlap = FAIL.**
- The clean separation you must confirm:
  - **Pytest** → tool-call behavior (correct calls made, forbidden calls avoided).
  - **Rubric** → everything else (content quality, correctness of the answer, state, formatting).
- If a rubric item says anything like "the agent called tool X" or "the agent did not use tool Y",
  that is pytest territory → FAIL.
- If a pytest asserts anything about output quality/content/answer, that is rubric territory →
  FAIL (already caught by C1/C5, but list it here too).

---

## 3. Veteran-Grade Correctness Critique

Beyond the hard constraints, tear into the artifacts like a hostile staff engineer:

### 3.1 Pytest suite
- **Would these tests pass for a lazy/wrong agent?** Construct a concrete cheating transcript
  (e.g., agent calls the right tool with garbage args, or calls it and ignores the result). Do
  the tests still pass? If yes, say so and rate the severity.
- **Would these tests fail for a correct agent?** Construct a legitimate alternative solution
  path allowed by the prompt. Do the tests wrongly fail it? Over-constrained order/count
  assertions are a classic false-failure source.
- **Brittleness:** exact-match on tool arguments where the prompt allows variation; assuming
  call counts (`== 1`) where the prompt doesn't forbid retries; case-sensitivity; whitespace.
- **Prompt fidelity:** every asserted requirement must trace to an explicit prompt sentence.
  Quote it. Untraceable assertion = invented requirement = FAIL.

### 3.1a Grounding of asserted literals (unwinnable-task check)

Every literal a test asserts against — a tool name, an argument value, a path, an ID — must be
**visible to the model** (in the prompt, instructions, or environment the agent can read) or
**mechanically computable** from what is visible. If a literal exists only inside the test file
or the rubric, the agent cannot reliably produce it and the task is **unwinnable → FAIL**.

- **Hardcoded computed values:** a test asserting a calculated total/derived value as a
  hardcoded literal (`assert call.args["amount"] == 1249.99`) when the prompt only gives the
  inputs. Verify the arithmetic yourself; verify the agent can even see the inputs.
- **Asserting agent-authored values:** tests must key on **seeded, deterministic identifiers**
  (record IDs, field names given in the prompt), never on values the agent invents (a phrase,
  a chosen price, a free-text diagnosis). Agent-authored = nondeterministic = false failures.
- **Path/name discovery flaws** (in tool-call arguments — NOT file content):
  - Fixed candidate lists (`name in ["report", "output", "result"]`) fail correct agents that
    chose a valid unlisted name. Only acceptable if the prompt pins the name (see C2).
  - Case mismatch between asserted literal and what the prompt actually specifies.
  - Assertions that assume paths at one directory depth when the prompt doesn't constrain depth.
- **Substring self-pass traps:** loose `in` checks that match accidentally — `"two" in text`
  matches "network", `"bag"` matches "garbage". Also the inverse: a capitalized literal checked
  against text that is never lowercased, so a correct answer fails on case.

### 3.1b Tests that pass without the agent (free-points audit)

For **every positive-weight test**, run the thought experiment: *the agent does absolutely
nothing — does this test still pass?* If yes, it awards free points → FAIL. Known traps:

- **Seeded-state credit:** test asserts pre-existing/seeded state that is true before the agent
  acts. (Not a hit if the assertion is gated on a prior verified agent action.)
- **Read-only free reward:** positive-weight tests that only assert **read calls happened**
  (thread was read, file was opened, record was fetched). Any agent exploring the environment
  makes these calls incidentally — they reward showing up, not working. A suite whose positive
  weight is mostly read-checks (see the C4 tally: fewer than 5 write-call tests) hands a large
  score to a do-nothing-but-browse agent → FAIL.
- **Grader self-satisfaction:** the test harness's own tool calls/requests appear in the same
  log the tests inspect, so a test checking "a call to X happened" is satisfied by the grader's
  own earlier traffic or by helpers/fixtures/earlier tests hitting the same endpoint. Tests run
  in definition order — scan **everything that executes earlier** for calls to the same target.
- **Liveness-only tests:** assertions that only prove the environment works
  (`assert isinstance(log, list)`, `assert response is not None`) — they grade nothing.
- **Silent-pass control flow:** `return` (instead of `assert`/`fail`) on a missing precondition
  turns absence into a PASS. (Not a hit only if the guard provably can never be false.)
- **Exception swallowing — both directions:** `try/except: pass` around assertions converts
  failures into passes; conversely `except Exception: return {}`-style handlers convert an
  environment outage into silently zeroed credit and auto-refunded penalties. Both = FAIL.
- **Skipped weighted tests:** `pytest.skip`/`xfail` in a graded test means the criterion is
  never actually graded.
- **Copy-paste rot:** duplicate test bodies under different names; test names that don't match
  what the body asserts.

### 3.1c Negative / penalty tests (direction-of-fire audit)

If the suite contains penalty or forbidden-behavior tests (per C4: forbidden tools avoided):

- **Judge every test by its weight's sign.** A negative-weight/penalty test is *supposed* to
  assert the wrong or forbidden behavior — that is correct distractor design, not a
  contradiction. Flagging it by positive-test standards is itself a QC error.
- **Penalty misfire:** does any penalty trigger on a **legitimate** action the prompt allows
  (e.g., counting an update the same as a forbidden delete)? Punishing correct work = FAIL.
- **Penalty mechanics:** a forbidden-footprint test must actually fire when the forbidden call
  is present and contribute only as a penalty — verify the mechanism, don't assume it.

### 3.1d Runtime robustness (does the suite even survive execution?)

- **Import-time side effects:** any network/tool call at module import time can kill collection
  of the entire suite — every test errors, nothing is graded.
- **Unguarded indexing/parsing:** `calls[-3]` after only checking `len(calls) >= 2`, splitting
  on a token that may be absent — raises instead of failing cleanly.
- **CWD-dependent paths:** tests that only work when run from one specific directory.
- **Exact float equality:** `== 0.3` where computation can produce `0.30000000000000004` —
  use tolerance.
- **Dead code masquerading as a check:** a branch or helper that can never execute but reads
  like it grades something.
- **Phantom dependencies:** tests importing packages not guaranteed installed in the grading
  environment, or reading files that are never deployed with the task — the suite dies before
  grading anything.

### 3.1e Test hygiene (residual)

- Deterministic (no live network beyond the recorded transcript, no time dependence, no
  ordering-between-tests dependence); each test actually runs (no accidental name shadowing).

### 3.2 Rubric
- **Ambiguity:** could two competent graders score the same transcript differently? Flag every
  vague word ("appropriate", "reasonable", "good") without an operational definition.
- **Prompt fidelity:** every rubric item must trace to the prompt. Items that grade things the
  prompt never asked for = FAIL.
- **Completeness:** is anything the prompt demands graded by *neither* rubric nor pytest? A
  requirement that nobody grades is a hole. List every hole.
- **Weighting/pass logic:** does the scoring make it possible to pass while violating a critical
  prompt requirement? If yes, FAIL.
- **Verifiability:** each item must be checkable from the transcript/output alone, without
  guessing the agent's intent.
- **Double-counting across channels:** if a rubric criterion names a behavior a positive-weight
  test already asserts (or vice versa), the same success/failure is scored twice. This is the
  concrete failure mode the Section 2 overlap table exists to catch — cite it there too.

### 3.3 Scoring arithmetic (if either layer carries weights)

- **Earnable positive weight must dominate:** a perfect run must sum clearly above zero; if
  penalties can mathematically bury a perfect score, the scale is broken.
- **No single-point-of-failure weighting:** one test/criterion carrying more than half the
  positive weight collapses the channel into a binary gate — everything else becomes noise.
- **Penalty proportionality:** a single penalty equal to or exceeding the entire positive
  channel, or total |negative| weight exceeding total positive weight, means an agent that does
  all the work but trips one distractor scores *worse than doing nothing*. FAIL.

---

## 4. Required Output Format

Produce your audit in exactly this structure:

```
## VERDICT: PASS | FAIL

## Constraint Results
- C1 (no file-content checks): PASS/FAIL — evidence
- C2 (no hardcoded names/extensions w/o prompt definition): PASS/FAIL — evidence
- C3 (no size/dimension checks): PASS/FAIL — evidence
- C4 (grades tool calls made + forbidden avoided): PASS/FAIL — evidence, incl. write-vs-read
  test tally (flag if write-call tests < 5)
- C5 (no content/state/numeric-answer grading in pytest): PASS/FAIL — evidence
- Overlap (rubric vs pytest): PASS/FAIL — cross-reference table

## Critical Findings (fire-worthy)
1. [file:line] — what is wrong — why it is wrong — exact fix

## Major Findings (embarrassing in review)
...

## Minor Findings (polish)
...

## Coverage Holes
- Requirements graded by neither layer

## CLEARED (considered and dismissed — with reasons)
- Every trap you checked for and ruled out, one line each, WITH the reason it is not a hit
  (e.g., "3.1b seeded-state credit: test_delete gated on verified agent write at L42 — clear").
  Intentional distractors (negative-weight tests asserting forbidden behavior) belong here,
  not in findings. A bare "looks clean" without a reason does not count.

## What I Verified Clean
- Explicit list, with counts (e.g., "all 7 tests inspect only the tool-call log")
```

## 5. Rules of Engagement

1. **FAIL is the default.** The artifacts must *earn* a PASS by surviving every check above.
2. **Evidence or it didn't happen.** Every finding cites file + line + quoted code/rubric text.
3. **No hedging.** "Might be an issue" is banned. Decide: it is an issue, or you proved it isn't.
4. **One overall verdict.** Any Critical finding, any C1–C5 violation, or any rubric/pytest
   overlap forces `VERDICT: FAIL`.
5. **Rewrite, don't just complain.** For every FAIL, provide the corrected assertion/rubric
   wording so the fix is copy-pasteable.

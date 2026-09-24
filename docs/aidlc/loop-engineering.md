# Harness and loop engineering

> **If you read nothing else:** write the acceptance criteria first, give
> the assistant a check it can run, demand the evidence rather than a claim,
> and stop after two failed corrections. Everything below is detail on those
> four sentences.

> **Agent = model + harness.** You cannot change the model. Every bit of
> engineering leverage you have is in the *harness*: the guides you put in
> front of the model and the checks you put behind it.
>
> So here is the course's central claim, and the thing your sprint grade
> actually measures: **the deliverable is not the AI's output — it is the
> loop that verifies it.** Anyone can generate a document. Your engineering
> contribution is the harness that makes a wrong document fail loudly in
> under a minute.

Companion to [`hitl-gates.md`](hitl-gates.md) (which gate catches what) and
[`prompt-library.md`](prompt-library.md) (what to type). This file is about
*building the machinery* and *running the loop*.

---

## 1. What a harness is

Two directions, two kinds of check:

| | **Guides** — steer *before* it acts | **Sensors** — detect *after* it acts |
|---|---|---|
| **Deterministic** (milliseconds, same answer every time) | typed interfaces, project scaffolds, issue/PR templates, `CLAUDE.md` | tests, type checker, linters, link checker, schema validators, build exit code, the repo harness |
| **Inferential** (an LLM does the checking; slow, non-deterministic) | the spec, acceptance criteria, worked examples | a reviewer prompt in a fresh session, LLM-as-judge |

**Prefer deterministic over inferential, and sensors over prompts.** A rule
written in `CLAUDE.md` is *advisory* — the model complies probabilistically.
A rule in CI is *enforced*. When you catch yourself writing "please always
remember to…" in a prompt, that is a sign the rule belongs in the harness
instead.

## 2. What to build, in order of payoff

You have one semester and a small team. Build in this order; the first five
cost an afternoon and catch most AI-specific defects.

| # | Check | Why it earns its keep against LLM output |
|---|---|---|
| 1 | **Type check** (`tsc --noEmit`, `mypy`) | kills hallucinated APIs and wrong signatures at essentially zero cost — the most AI-specific defect class there is |
| 2 | **Build / compile exit code** | "it compiles" is the floor, and it is free |
| 3 | **Dependency existence + lockfile review** | models invent package names at scale, and attackers register the popular hallucinations ("slopsquatting"). Never install a package the model suggested without checking it exists and is the one you meant |
| 4 | **Link + reference checker** | AI-written documents cite plausible URLs and file paths that do not exist (this repo's gates G3/G4) |
| 5 | **Lint + format** | stops style churn from inflating diffs, so reviewers see the real change |
| 6 | **Golden-file / snapshot diff** for your prototype's core output | gives the *model* something to self-check against, which is what stops "looks done" |
| 7 | **3–8 acceptance tests, one per acceptance criterion** | these *are* the spec, executable |
| 8 | **Schema validation** of structured artifacts (front-matter, config, API contracts) | models invent fields |
| 9 | **One end-to-end smoke run** (`make demo` exits 0) | catches integration lies that unit tests miss |
| 10 | **Secret scanning / SAST** (free on GitHub) | roughly *half* of AI-generated code samples in published testing introduced a common security flaw, and that rate has stayed flat while models got better at syntax |

Two properties matter more than the list:

- **The local command and the CI command must be the same command.**
  Divergence is where teams burn whole afternoons on "works on my machine."
  In this repo that command is:
  ```bash
  python .github/scripts/check_repo.py
  ```
- **Success silent, failure verbose.** A gate that prints nothing when it
  passes and the full error when it fails keeps both your attention and the
  model's context clean.

## 3. The ratchet: every rule earns its place

Keep [`harness-log.md`](harness-log.md) — one line per rule, naming the
failure that caused it. A rule with no failure behind it is superstition; a
failure with no rule behind it will happen again.

This is also the best evidence of learning you can hand me at a sprint
review: *"here is what went wrong, and here is the check that makes it
impossible now."*

## 4. Running the loop

```
        ┌── spec / acceptance criteria (yours, written first) ──┐
        │                                                       │
        ▼                                                       │
   prompt ──▶ generate ──▶ HARNESS ──▶ green? ──▶ evidence ──▶ PR
                             │  red                            │
                             ▼                                 │
                    fix once, fix twice ─── still red? ────────┘
                             │
                             └──▶ STOP. New session, or fix the spec.
```

**Test-first, with the red commit.** The strongest pattern available to you:

1. Write the tests from the acceptance criteria.
2. Run them; confirm they fail for the right reason.
3. **Commit the failing tests.**
4. Implement, with the instruction *do not modify the tests*.
5. Iterate to green.

That committed red state is cheap, and it is proof that you owned the
specification before any code existed. It also makes any later weakening of
the test visible in the diff.

**Iteration budget: two.** After two failed corrections on the same problem,
stop correcting. Start a clean session with a better first prompt that
includes what you learned. A fresh session with a good prompt beats a long
session full of dead ends, because failed attempts stay in the context and
degrade everything after them.

**Four tells that the *specification* is the problem, not the prompt:**

1. Two independent sessions, both with clean context, fail the same way.
2. The output satisfies every criterion you wrote and is still wrong —
   the defining symptom of incomplete criteria.
3. You cannot write the failing test without inventing a new requirement.
4. Two teammates disagree about whether the PR is correct.

The fix is to edit the spec and re-run from a clean session — never to pile
more clarifications onto a polluted conversation.

**Restart the session when:** two corrections failed · the model re-reads
files it already read · it reintroduces a bug you already fixed · you switch
stories · you have been iterating more than about thirty minutes with no
gate turning green.

**Keep durable state in files, not in the chat.** The spec, the plan, the
issue, the harness log — those survive. A conversation does not.

## 5. Don't let the check get gamed

The cheapest way to make a check pass is to weaken the check. Treat these as
blocking, no discussion:

- **Tests are append-only while implementing.** If an implementation PR
  touches a test file, the PR body must say why.
- **Any change that weakens CI is an automatic block** — deleted or skipped
  tests, lowered coverage thresholds, `continue-on-error`, narrowed
  workflow triggers.
- **Ask of every new test: would this fail if I reintroduced the bug?** If
  not, it asserts nothing. Tests that only exercise mocks are the classic
  AI-generated test pathology.
- **Never let the author of a change be its approver.** GitHub enforces this
  for you once approvals are required — keep it that way.

Benchmarks that hold out hidden tests show frontier models saturating the
*visible* tests while the hidden ones still fail, and the gap grows with the
size of the change. Passing your own tests is necessary, not sufficient.

## 6. Reviewing in ten minutes (the realistic protocol)

Order matters — CI changes first, source last:

| Minute | Do this |
|---|---|
| 0–2 | scan the file list; classify what kind of change this is |
| 2–3 | **read workflow/test/config changes first** — weakening CI is the one thing you must never wave through |
| 3–5 | grep for an existing helper that already does what the new code does (agents re-implement rather than reuse) |
| 5–8 | trace **one** critical path by hand, and require a test that would fail on the old behavior |
| 8–9 | check the security boundary: input validation, permissions, anything touching secrets |
| 9–10 | confirm the evidence line is real and specific |

**Ask for a split when** more than ~5 unrelated files changed, the purpose
is not statable in one sentence, or CI is failing with only test files
touched. Asking for a split is a reviewer's right, not a favor.

## 7. Disclosure and accountability

Human accountability does not change because a model wrote the draft. In
this course:

- Disclose in the PR body (our template asks tool, what it drafted, what you
  checked, what remains unverified).
- Add a git trailer on AI-assisted commits:
  ```
  Assisted-by: Claude (claude-sonnet-4.6)
  ```
  `Assisted-by:` is the convention most open-source projects have settled on
  for this. Note that there is *no* industry-wide standard yet — projects
  disagree, and one major project banned AI contributions outright before
  partially reversing. We use `Assisted-by:`.
- Never sign off work you have not verified. "The model wrote it" is not a
  defense at a code review, in a job interview, or in this class.

## 8. Two numbers to watch (and report at the sprint review)

- **Iterations to green per PR** — how many correction rounds before CI
  passed. Falling over the semester means your specs and harness are getting
  better.
- **Harness rules added per week** — from your harness log. Rising early,
  flattening later, is exactly the right shape.

A team whose iterations-to-green falls while its harness grows is learning
the thing this course is actually about. That is the same measurement idea
as Lecture 4's benchmarks-and-ROI discussion, at team scale.

Consider a **rotating "harness owner"** each sprint — one person responsible
for the gates and the log. The published study of AI use in capstone courses
found team-level governance roles to be one of the few interventions that
reliably helped.

---

## Where the evidence for all this lives

Every claim in this file — the perception gap, AI as an amplifier, the
maintainability drift, hidden-test gaming, hallucinated packages — is sourced
in [`evidence.md`](evidence.md), along with the primary documentation worth
reading yourself.

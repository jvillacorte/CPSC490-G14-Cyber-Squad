# The seven gates — how we keep LLM output honest

> **If you read nothing else:** the seven gates are (0) write the criteria,
> (1) prompt from shared context, (2) read it and run the harness yourself,
> (3) CI, (4) a teammate who did not write it approves, (5) protected merge,
> (6) sprint review. Gate 2 is the one that catches the most, and it is
> entirely yours.

> **AIDLC, human-in-the-loop (HITL).** You may use any LLM for any part of
> this project. What you may *not* do is let its output reach `main` without
> passing through gates that a human controls. This file explains every gate:
> what it checks, **which specific LLM failure mode it catches**, what you
> do there, and what evidence it leaves behind.
>
> The contrast worth understanding (Lecture 1): a *human-out-of-the-loop*
> system replaces the human at these gates with machinery. In this course
> **you are the gate** — the machinery only makes your checking fast.

An LLM fails in a small number of recognizable ways. Every gate below is
aimed at one of them:

| Failure mode | What it looks like |
|---|---|
| **Fabrication** | citations, APIs, file paths, issue numbers, benchmark figures that do not exist |
| **Plausible-but-wrong** | code or prose that reads perfectly and is subtly incorrect |
| **Requirement drift** | the answer solves a slightly easier problem than the one you asked |
| **Scope creep** | extra "helpful" changes you never asked for |
| **Unverified claim** | "this now works" with nothing run |
| **Check-gaming** | the test/criterion gets weakened until it passes |

---

## Gate 0 — Frame: acceptance criteria before the prompt

**You do:** write the story and its acceptance criteria in the issue *first*,
in your own words. Only then open the LLM.

**Catches: requirement drift.** A model cannot drift from a target that
exists in writing; it absolutely will drift from a vague ask. This is also
the cheapest gate — thirty seconds here saves an hour at review.

**Evidence:** the issue itself — story text, acceptance criteria checklist,
owner, sprint, priority, points.

**Red flag:** you are prompting to find out what you want. Stop and write the
criteria.

---

## Gate 1 — Prompt: shared context, one story at a time

**You do:** work from `CLAUDE.md` (shared project context) and a template
from [`prompt-library.md`](prompt-library.md). Paste the acceptance criteria
**verbatim**. Ask for a plan first on anything non-trivial.

**Catches: requirement drift and scope creep.** Explicit scope plus "do not
change anything else" is the difference between a reviewable diff and an
archaeology session. Shared context also stops five teammates getting five
different answers about the same project.

**Evidence:** the prompt you used (keep notable ones in the issue thread —
they are as reusable as code).

**Red flag:** a prompt that says "improve the document."

---

## Gate 2 — Self-verify: you read it, then you run it

**You do:** before *anything* leaves your machine —

1. **Read every line** the model produced. If you cannot explain a line to a
   teammate, it does not ship. (You will be asked in the sprint meeting.)
2. **Check each claim that can be checked**: does the cited paper exist and
   say that? does that function exist in the library's docs? does that file
   path exist? does the API return that shape?
3. **Run the harness locally** — seconds, no install:
   ```bash
   python .github/scripts/check_repo.py
   ```
4. **Run the prototype / its tests** if you touched code.

**Catches: fabrication, plausible-but-wrong, unverified claims.** This is
the highest-yield gate in the whole chain, and it is entirely yours — CI
cannot check whether a citation actually supports the sentence.

**Evidence:** the verification line you will paste into the PR ("ran the
harness — green; opened the two cited papers; ran `npm test` — 4 passing").

**Red flag:** "it looked right" is not verification.

---

## Gate 3 — CI harness: the automated gates

Pushing a branch and opening a PR runs `.github/workflows/ci.yml`. Each
check is small on purpose so a red run tells you exactly what is wrong.

### G1 · template structure
Checks `proposal/proposal.md` still has all 11 template headings, in order.
**Catches fabrication/drift:** asked to "clean up the proposal," a model will
happily rename *Problem Statements* to *Problem Statement*, merge
*Related Work* into the introduction, or drop *AI Usage*. The template is a
course requirement, not a suggestion.
**Fix:** restore the heading exactly as the template spells it.

### G2 · traceability
Every file in `docs/specs/` and `docs/design/` must name its issue(s) in the
first lines (`> Epic: #1 · Stories: #2, #3`).
**Catches scope creep:** documents nobody planned. Work that traces to no
objective scores nothing on *Relevance* at the sprint review — and this gate
tells you before the instructor does.
**Fix:** add the header, or file the issue the document actually serves.

### G3 · issue references exist
Every `#123` cited in your documents is looked up against the real issue
list.
**Catches fabrication:** models invent issue numbers with total confidence.
A reference that resolves to nothing breaks the audit trail that your
*Traceability* score depends on.
**Fix:** cite the real number, or create the issue you meant.

### G4 · links resolve
Every relative Markdown link must point at a file that exists.
**Catches fabrication:** confident references to `docs/design/architecture.md`
when nobody wrote it, and paths left behind by a rename.
**Fix:** create the file or correct the path.

### G5 · secrets
Scans for AWS/GitHub/OpenAI/Anthropic/Google key shapes, private-key blocks,
and hardcoded credentials.
**Catches plausible-but-wrong help:** "just put the key in the config for
now" is a normal-looking suggestion and a permanent mistake in a public repo.
**Fix:** remove it, rotate the key, use an environment variable or a GitHub
Actions secret. Never "fix" it by deleting only the latest commit — the key
stays in history; rotate it.
**Test fixtures and examples:** a fake password in a test is not a secret, so
add `# pragma: allowlist secret` on that line (the prototype's test file shows
one). The marker is deliberate and greppable — `grep -rn "allowlist secret" .`
lists every exemption, so a reviewer can audit them. Never use it to silence
a real credential.

### G6 · placeholders *(warning, not a failure)*
Reports leftover `〈…〉`, `TODO`, `FIXME`, lorem ipsum outside template files.
**Catches unverified claims:** half-finished sections marked done.
It is advisory because templates *should* have brackets — this example
repository reports a few by design. In your repo the count should fall to
zero as you fill things in; reviewers read this list at Gate 4.

### G7 · every design document has a diagram
Each of your own files in `docs/design/` must contain a ```mermaid block or
an exported image.
**Catches design-by-prose:** asked for a design document, an assistant
writes four confident paragraphs about layers. Paragraphs hide the questions
a picture forces you to answer — what calls what, and with what data.
**Fix:** draw it. [`../design/DIAGRAMS.md`](../design/DIAGRAMS.md) says which
diagram answers which question.

### G8 · every issue is linked from the right proposal section
Epics and user stories must be linked from proposal §2; every other work
item — feature, enhancement, bug, task, sub-task — from §4.
**Catches the document and the board drifting apart:** work the proposal
never mentions is work your reader cannot see, and a proposal listing issues
nobody filed is fiction. Both cost you *Traceability*.
**Fix:** add the `#n` to the right section, or close the issue if it is not
real work. While §2 or §4 is still the untouched skeleton the gate says so
once instead of listing every issue.

### G9 · every specification and design document is indexed in §4
Proposal §4 is the index of your specifications and design documents.
**Catches detail nobody can find:** a good specification that no reader of
the proposal is ever pointed at may as well not exist — and §4 is the
section that has to carry it.
**Fix:** list the document under §4 with a one-line description.

### G10 · every non-epic issue names a parent
The chain is epic → user story → feature / enhancement / bug → task /
sub-task, and nothing floats off it. Link a child with GitHub's
**sub-issues** (*Create sub-issue* → *Add existing issue*) or name the
parent's number under the issue's `## Epic` / `## Parent` heading.
**Catches work nobody traced to an objective:** the whole reason for the
chain is that a reader can open §2, pick a goal, and walk down to the
smallest piece of work being done about it. One unparented issue breaks that
walk, and it is usually a task somebody filed without asking which objective
it serves.
**Fix:** parent it. If nothing above it fits, that is the gate telling you
something real — either the objective is missing from §2, or the issue is
not project work.

**G8, G9 and G10 are advisory on `feature → develop` and blocking into
`main`.** Filing an issue mid-sprint and parenting or linking it an hour
later costs you nothing; shipping a release whose document and board
disagree is what they stop.

### Plus two job-level gates
- **prototype** — installs and tests `prototype/` (Node or Python,
  auto-detected). *Catches plausible-but-wrong code: it either runs or it
  does not.* A prototype with no tests gets a warning; add one by Sprint 2.
- **pr-discipline** — your PR body must link a story (`Closes #12`),
  disclose AI use, keep no template placeholders, and state what you
  verified. *Catches unverified claims* — the one thing reviewers cannot
  reconstruct later.

**Read the failure, not the vibe.** A red harness names the file and the
line. Pasting the red log back into the LLM is fine — but you decide whether
its proposed fix addresses the cause or just silences the check.

---

## Gate 4 — Peer review: a human who did not write it

**You do (as reviewer):** GitHub will not let the author approve their own
PR, so this is structurally a second person. Reviewing AI-assisted work is
*not* the same as reviewing a classmate's hand-written work — the prose is
always fluent, so fluency tells you nothing.

**Read the changes in this order: workflow/test/config first, source last.**
The one change you must never wave through is one that weakens the harness
itself. Then check:

- [ ] **Does it satisfy the acceptance criteria as written?** Open the issue
      and compare, line by line. Do not accept a reworded criterion.
- [ ] **Were the criteria themselves changed in this PR?** That is a scope
      decision and needs its own discussion, not a silent edit.
- [ ] **Spot-check two facts.** Pick the two most load-bearing claims — a
      citation, an API call, a performance number — and verify them
      yourself. Fabrications cluster in exactly the places that are tedious
      to check.
- [ ] **Does the code actually do what the prose says?** Read the diff, not
      the summary.
- [ ] **Do the tests assert anything?** `expect(true).toBe(true)`,
      tests that never call the code, and deleted assertions are the classic
      tells of a model making a check pass.
- [ ] **Was any test weakened, skipped, or deleted?** Tests are append-only
      while implementing; a test change inside an implementation PR needs a
      stated reason.
- [ ] **Does this re-implement something the repo already has?** Assistants
      re-invent helpers instead of reusing them — grep before approving.
- [ ] **Is anything here unrelated to the story?** Unasked-for refactors,
      reformatting, dependency bumps → ask for them to be split out. Asking
      for a split is your right, not a favor: use it when more than ~5
      unrelated files changed or the purpose is not statable in one
      sentence.
- [ ] **Is the AI-use disclosure honest and the verification specific?**
      "Used AI, verified everything" is not specific.

**Catches: everything the automation cannot** — especially
plausible-but-wrong content and check-gaming.

**Evidence:** your review comments and the approval itself. Approving means
*you* now vouch for it; the sprint grade for *Separation of duties* reads
this history.

**Red flag (reviewer):** approving within seconds of the PR opening. **Red
flag (author):** a PR so large nobody can review it — split the story.

---

## Gate 5 — Merge: branch protection

**The machine does:** refuses the merge unless CI is green, one approval
exists, the branch is current with `develop`, and conversations are
resolved. Configuration is in
[`../git-workflow.md`](../git-workflow.md) §6.

**Catches: process bypass.** Good intentions decay under deadline; a rule
that is enforced does not. This is also the line that makes the course
claim literally true: an LLM can write the whole change, but it cannot
approve it and it cannot merge past a red harness.

**Evidence:** the merge itself — green checks plus a named approver, visible
forever in the PR.

---

## Gate 6 — Sprint review: did it serve the goal?

**You do:** at each sprint boundary, write
`docs/sprint-reviews/sprint-N.md` — planned vs. completed points, what
carried over **and why**, what the prototype can now do.

**Catches: the failure no line-level gate can see** — a sprint of merged,
green, well-reviewed work that moved no goal forward. (This is the
*Relevance* metric, and in industry it is the expensive one.)

**Evidence:** the sprint review file, the board's sprint history, and the
velocity trend.

---

## The loop, in one picture

```
   Gate 0 frame ──▶ Gate 1 prompt ──▶ Gate 2 self-verify ──┐
        ▲                                                  │ fails?
        │                                                  ▼
        └──── rethink the SPEC after ~3 rounds ◀── iterate (fix + re-run)
                                │ passes
                                ▼
              Gate 3 CI harness ──▶ Gate 4 peer review ──▶ Gate 5 merge
                                                               │
                                                               ▼
                                                    Gate 6 sprint review
```

**The stopping rule.** After **two** failed corrections on the same problem,
stop correcting — start a clean session with a better first prompt that
includes what you learned (failed attempts stay in the context and drag down
everything after them). After **three** failed attempts at the story, the
*specification* is the problem, not the prompt. The four tells, and what to
do about each, are in
[`loop-engineering.md` §4](loop-engineering.md#4-running-the-loop). Take it
to the team, split the story (`sp: 8` means split it), or fix the criteria
deliberately in their own PR.

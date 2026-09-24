# Project context for AI assistants

**Copy this file into your repository and edit the 〈brackets〉.** Every
teammate's AI session then starts from the same facts, so you get consistent
output instead of five people re-explaining the project five different ways.

Claude Code reads `CLAUDE.md` automatically. `AGENTS.md` is the same idea as
a cross-tool convention; GitHub Copilot reads
`.github/copilot-instructions.md`, Cursor `.cursor/rules/`, Gemini CLI
`GEMINI.md`. Keep **one** real file and copy it for whatever your team uses;
never let two versions drift.

**Keep this file under about two pages.** For every line ask: *would removing
this cause a mistake?* If not, cut it. A bloated context file gets ignored —
including the rules you care about — and emphasizing every line emphasizes
none of them. Rules that MUST hold (formatting, no direct pushes, lint before
commit) belong in CI or a git hook where they are enforced rather than
merely suggested; see `docs/aidlc/loop-engineering.md`.

> **You are the engineer. The assistant drafts; you decide and you verify.**
> This course is **human-in-the-loop (HITL)**: nothing reaches `main` that a
> human did not read, verify against acceptance criteria, and approve.

---

## The project

- **Course:** CPSC 490 Undergraduate Seminar, Fall 2026 (proposal + prototype
  semester; full implementation happens in CPSC 491).
- **Team:** Group 〈N〉 〈name〉 — members in `README.md`.
- **Project:** 〈one or two sentences a stranger understands〉
- **Sponsor:** 〈RTX-3 / EL-1 / SNX-n / independent〉
- **Source of truth:** `proposal/proposal.md`. Specs in `docs/specs/`,
  designs in `docs/design/`, proof-of-concept code in `prototype/`.
- **Stack (prototype):** 〈languages, frameworks, services〉

## How we work

- Work is tracked as GitHub issues: **epic = goal**, **user story =
  objective**; every story carries assignee, sprint milestone, `priority:`,
  and a `sp:` story-point label.
- Four 2-week sprints (`Sprint 1`–`Sprint 4`).
- Every change lands through a **pull request** that says `Closes #<story>`
  and is **approved by a teammate who is not the author**. CI must be green.
- A story is done only when its acceptance criteria are checked off and its
  PR is merged.

## What the assistant may and may not do

**May draft:** proposal and document prose, spec/design sections, prototype
code, tests, diagrams, commit messages, PR descriptions, review comments,
alternatives and trade-off analyses.

**Must NOT decide (a human decides):**
- whether a story is **done** — acceptance criteria are judged by a person;
- **scope**: adding, dropping, or reinterpreting a goal, objective, or
  acceptance criterion;
- **design trade-offs** that outlive the sprint (architecture, data model,
  third-party dependencies);
- anything that touches the **sponsor relationship** or course deliverables.

**Never:**
- weaken or reword an acceptance criterion so the current output passes —
  if the criterion is wrong, a human changes it deliberately, in its own PR;
- invent citations, benchmark numbers, sponsor requirements, or API behavior;
  cite what can be checked, and say plainly what you could not verify;
- claim something works without naming the evidence (command run, test
  passed, page opened);
- commit secrets, API keys, `.env` files, or anything student-identifying
  beyond the team's own names.

## House rules for output

1. **Quote the requirement verbatim** before working on it (story text or
   acceptance criterion). Do not paraphrase it into something easier.
2. **Verify what you can, name what you cannot.** End substantial work with
   what was checked and what remains unverified.
3. **Small steps.** One story at a time; if it cannot be finished in one
   pass, say so and propose a split instead of half-doing it.
4. **Match the existing document or code style** in this repo rather than
   introducing a new one.
5. **Cite file paths and issue numbers** so a reviewer can follow the trail
   (`docs/specs/x.md §2`, `#12`).

## Conventions

- Markdown documents, one topic per file; every doc's first lines name its
  epic and stories (`> Epic: #1 · Stories: #2, #4`).
- Branches: `<issue-number>-short-slug` (e.g. `12-login-spec`).
- Commit subject: imperative, under ~72 chars; body explains *why*.
- Disclose AI use in each PR (see `.github/PULL_REQUEST_TEMPLATE.md`) and in
  the proposal's **AI Usage** section.

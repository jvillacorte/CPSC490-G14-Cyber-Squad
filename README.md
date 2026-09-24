# CPSC 490 — Group Repository Setup Guide

**Fall 2026 · Prof. Kyoung Shin · Department of Computer Science, CSUF**

Author: **Kyoung Shin** · <kshin@fullerton.edu> · © 2026 — original course
work, **all rights reserved** ([`LICENSE`](LICENSE)). Enrolled CPSC 490/491
students may copy and build on this for their coursework; any other use,
including adoption for another course, needs written permission — just ask.
Instructors: see [`FOR_INSTRUCTORS.md`](FOR_INSTRUCTORS.md).

**Project board (live example): <https://github.com/users/kyoungshin/projects/1>**
· **Field Guide: <https://kyoungshin.github.io/CPSC490/aidlc/AIDLC-Field-Guide.html>**
· **Start here: [`QUICKSTART.md`](QUICKSTART.md)**

> **This repository is itself the example.** It is laid out exactly the way
> your group repository should be — the folders, the issue templates, the
> labels, the `Sprint 1`–`Sprint 4` milestones, the sample issues, the
> runnable `prototype/`, the worked
> [specification](docs/specs/example-spec.md) and
> [design document](docs/design/example-design.md), and the
> [project board](https://github.com/users/kyoungshin/projects/1) — so build
> yours the same way.
>
> `scripts/bootstrap.sh` does the whole labels/milestones/branches/board
> setup in one command, and `scripts/sprint_report.py` measures story points
> committed versus closed each sprint.
>
> **The syllabus governs grades and deadlines.** Repository work is assessed
> under the syllabus's **20% Prototype & repository practice — 5% per
> sprint**, and what earns it is **progress on the proposal and the
> prototype**, evidenced in the repo. This guide adds no requirements of its
> own.

---

## 1. Create the repository

All of this is [`QUICKSTART.md`](QUICKSTART.md) steps 1–4, and
`scripts/bootstrap.sh` does most of it in one command. In short: the leader
creates one **private** repo named `CPSC490-G<number>-<groupname>`, adds every
teammate **and `kyoungshin`** as collaborators, copies this example's
scaffolding in, then runs the bootstrap script for labels, milestones,
`develop`, branch protection and the board. Post the repo URL where the
course asks for it.

**Every member commits in every sprint.** The contributor graph is part of how
individual participation is seen.

---

## 2. Repository layout

```
CPSC490-G03-California/
├── README.md               ← team + project one-pager (below)
├── proposal/
│   └── proposal.md         ← THE proposal, template §3 (single source of truth)
├── CLAUDE.md               ← shared AI context (§7)
├── docs/
│   ├── specs/              ← specification documents (one .md per epic)
│   ├── design/             ← design documents + diagrams/ (§3, DIAGRAMS.md)
│   ├── sprint-reviews/     ← one file per sprint boundary (§6 ritual)
│   ├── git-workflow.md     ← Gitflow + CI/CD (§7)
│   ├── development-plan.md ← team charter (quantified triggers) + risk register
│   ├── checklists.md       ← what reviewers review against (§8)
│   └── aidlc/              ← the seven gates, prompt library, harness log, lectures (§7)
├── prototype/              ← prototype v0: running proof-of-concept (due Sep 27)
│   └── README.md           ← how to build/run it
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── epic.md         ← §5
    │   ├── user-story.md   ← §5
    │   ├── task.md         ← §5
    │   └── bug.md          ← §5
    └── PULL_REQUEST_TEMPLATE.md
```

**README.md** must contain: project title · sponsor code (e.g. RTX-3) if
sponsored · member table (name, GitHub username, role) · leader/contact ·
link to `proposal/proposal.md` · **link to your Project board** (the way the
[example board](https://github.com/users/kyoungshin/projects/1) is linked
from this guide). **Start from
[`README_TEMPLATE.md`](README_TEMPLATE.md) in the example repository** —
copy it to your repo as `README.md` and fill in the 〈brackets〉.

---

## 3. The proposal (`proposal/proposal.md`)

`proposal/proposal.md` **is the proposal document, not a README.** Write
continuous academic prose — no task lists, no emoji, no repo jargon — with
the section numbers and titles of the course Word template, exactly. **Each
section in the skeleton opens with the template's own guidance text** in a
quote block; delete those blocks as you write.

| § | Section |
|---|---|
| 0 | Abstract |
| 1 | Introduction |
| 1.1 | Related Work |
| 1.2 | Problem Statements |
| 2 | **Goals and Objectives** ← drives your issue board (§4) |
| 3 | Proposed Approaches |
| 4 | Required Environment, Resources, and Planned Activities ← **diagrams go here** |
| 5 | Project Outcomes |
| 6 | Project Timeline ← **next semester's implementation plan** |
| 7 | AI Usage |
| 8 | References |

CI gate G1 checks these headings and their numbering, because the numbering
is what makes the file convert cleanly into the Word template.

**Getting it into Word for Canvas.** The template numbers its headings
automatically (a multilevel list: top-level sections at level 1, *Related
Work* and *Problem Statements* at level 2), so do not end up with both its
numbers and the ones typed in the Markdown. Most teams should simply **open
the course template and paste their prose in section by section** — ten
minutes, no surprises. If you prefer to convert, `pandoc` works
(`winget install pandoc`):

```
pandoc proposal/proposal.md -o proposal.docx --reference-doc="CPSC 490 Project Proposal Template Fall 2026.docx"
```

…then in Word delete the typed `0.`/`1.`/`1.1` prefixes and set *Related
Work* and *Problem Statements* to the template's level-2 heading. Either way,
keep the Markdown copy current — it is what peer review and CI can read.

**Formatting requirements for the submitted Word document** (graded
explicitly): **Times New Roman, 11-point · 1.5 line spacing · 1.0-inch
margins** on all sides — the template's **cover page used unchanged** (fill
its fields, keep its layout) — and the template's **section format, numbering
and indentation followed exactly** (its styles set all of this; paste with
*Keep Text Only* so they apply, and verify after a pandoc conversion). **The Final
Project Proposal Paper (due Sun Dec 20) must exceed 50 pages** under this
formatting; the fixed font/spacing/margins are what make that page count mean
the same thing for every team. Full details sit at the top of
`proposal/proposal.md`.

Six sections need particular care:

- **1.1 Related Work** — a **comparative analysis**, not a list of summaries.
  Compare the existing ideas/products/papers against each other on the
  dimensions that matter, with honest pros and cons in a table, then argue in
  prose what your project does differently and why that is worth doing.
  "Nothing like this exists" reads as a missing survey.
- **1.2 Problem Statements** — **concise** (a few sentences each; no
  background, no solution) and **traceable both ways**: every problem must be
  addressed by a goal in §2, and every goal in §2 must trace back to a
  problem here. The skeleton includes a small mapping table for that check —
  it is what your final report is graded against.

- **2 Goals and Objectives** — each *goal* is an **Epic** issue, each
  *objective* under it a **User Story** issue (§4). **Every epic and user
  story is linked from this section**, so the goals in the document and the
  work on the board cannot drift apart.
- **3 Proposed Approaches** — **clear and concise**: the strategy you chose,
  the alternatives, and the reasoning. This is the argument, not the manual —
  all the detail (tooling, platforms, frameworks, DBMS, environment,
  diagrams, work breakdown) goes in §4. If a sentence here names a version
  number or a library, it belongs in §4.
- **4 Required Environment, Resources, and Planned Activities** — this is
  where all the concrete detail lives, and it has three inventories.
  **Literally every specification and design document** the team writes is
  listed here with the objective it serves (gate G9), so §3 stays the
  argument and §4 is the index of everything buildable. Also your
  **diagrams**: high-level architecture and
  system/context at minimum, plus ER/EER and data-flow views where they earn
  their place. Keep the authoritative copies in `docs/design/` (editable
  source *and* exported image) and reference them here — tools and
  conventions in [`docs/design/DIAGRAMS.md`](docs/design/DIAGRAMS.md).
  And the **planned-activities inventory**: this section links every
  *other* work item — **feature, enhancement, bug, task, sub-task** — each
  traceable to the objective it serves (epics and stories themselves are
  linked from §2). Together the two sections give a reader every planned
  activity in one place. Gate G8 fails if an issue of either kind exists that
  its section does not link.
- **5 Project Outcomes** — one or two paragraphs of prose explaining the
  outcome overall (not a checklist): what will exist when the project is
  done, the deliverables named inside those paragraphs, and briefly what
  prototype v0 demonstrates today and how to run it.
- **6 Project Timeline** — this is the plan for **CPSC 491 next semester**:
  how the system actually gets built, in what order, with which milestones.
  It is *not* this semester's four proposal sprints — those live on the
  project board and in `docs/sprint-reviews/`.

The Word document you submit and `proposal.md` must say the same thing — the
repo copy is the living version you keep improving all semester, and the
Preview and Final Project Proposal Papers grow out of it.

---

## 4. Epics and user stories on the issue board

CPSC 490 uses **GitHub Issues + one GitHub Projects board** — everything
lives in the repository, so there is no second tool to keep in step.

**Epic = a Goal.** One issue per goal from *Goals and Objectives*.
Label `epic`. An epic's body lists its user stories as a task list
(`- [ ] #12`) so progress is visible automatically.

**User story = an Objective.** One issue per objective, and **title it with
the objective itself, in the words proposal §2 uses** — an action word plus
what gets completed. Someone reading §2 beside your board has to see the same
sentence in both places; that one-to-one match *is* the traceability the
rubric looks for, and it disappears the moment a title is a paraphrase.

The classic user-story sentence — *"As a 〈who〉, I want 〈what〉, so that
〈why〉."* — earns its keep on objectives that deliver a user-facing
capability, because naming the *who* and the *why* is what makes acceptance
criteria writeable. Put it in the issue **body** when it helps, and leave it
out when there is no user in the objective: *"Achieve ≥ 90% precision on the
held-out set"* is a perfectly good objective, and *"as a user, I want 90%
precision"* is a worse version of it. The label stays `user-story` either
way — that is the agile category for an objective, whatever its prose.

**What a good objective looks like.** These came through this course in real
proposals, lightly trimmed — action word first, and a number wherever a
number is possible:

- *Create a 3-act system, including setup, confrontation, and resolution.*
- *Design a clean home layout with large, colourful buttons that let children
  express needs and feelings quickly.*
- *Integrate multilayered safety protocols, including account verification,
  reporting tools, and trust scoring.*
- *Maintain traversal times of ~2 minutes between points of interest.*
- *Include at least two encounter types per zone.*
- *Classify updates as breaking, potentially breaking or informational, with
  roughly 75–80% accuracy.*
- *Aim for 10–15 minutes from source change to internal processing.*

Note how many of them carry a figure — *3 acts*, *~2 minutes*, *at least
two*, *75–80%*, *10–15 minutes*. That is the "measurable" half of the
template's instruction, and it is what makes the objective checkable at the
end of CPSC 491 rather than arguable.

The two ways objectives go wrong, both of which I have actually received: a
goal written as **a paragraph of prose with no objectives enumerated under
it** — nothing to file as an issue, nothing to measure at the end — and
objectives that are **feature names rather than completions**. "The voting
system" is not an objective; *"Implement one-vote-per-user-per-song with
rate limiting"* is.

Every story must have, from the moment it enters a sprint:

| Field | How | Values |
|---|---|---|
| **Owner** | GitHub **Assignee** (exactly one) | a team member |
| **Sprint** | **Milestone** on the issue | `Sprint 1` … `Sprint 4` |
| **Priority** | label | `priority: high / medium / low` |
| **Story points** | `sp: N` label | 1, 2, 3, 5, 8 — and `sp: 8` means *too big, split it* |
| **Acceptance criteria** | issue body checklist | what "done" means, checkable |

**The full agile work-item taxonomy.** Epics and user stories are the two
types this course *requires*; the rest of the standard agile categories are
there when your work needs them (the labels exist in the example repo):

| Type label | What it is | Typical CPSC 490 use |
|---|---|---|
| `epic` | A **goal** — container of user stories | one per Goal in the proposal |
| `user-story` | An **objective** from proposal §2 | one per Objective |
| `feature` | A new capability that delivers (part of) a story | prototype capabilities |
| `enhancement` | Improvement to something that already works | polish after check feedback |
| `bug` | Defect — built behavior ≠ spec | prototype defects |
| `task` | Concrete unit of work under a story/feature | "draft spec §3", "set up repo CI" |
| `sub-task` | Breakdown of a task — smallest tracked unit | child checklist items |

### The chain, and nothing off it

Every item hangs off the one above it:

```
epic  (a goal, from proposal §2)
 └─ user story  (an objective, from proposal §2)
     └─ feature / enhancement / bug
         └─ task
             └─ sub-task
```

That chain is the whole point: a reader opens proposal §2, picks a goal, and
walks down to the smallest piece of work being done about it. The example
repository is wired exactly that way, so you can click straight through it —
[#1 goal](https://github.com/kyoungshin/CPSC490/issues/1) → [#3 objective](https://github.com/kyoungshin/CPSC490/issues/3) → [#6 feature](https://github.com/kyoungshin/CPSC490/issues/6) →
[#5 task](https://github.com/kyoungshin/CPSC490/issues/5) → [#7 sub-task](https://github.com/kyoungshin/CPSC490/issues/7).

Link a child to its parent with GitHub's **sub-issues**: open the parent
issue, *Create sub-issue* → *Add existing issue*. The board then gives you a
**Parent issue** column and a **Sub-issues progress** bar for nothing — both
are built-in fields, so there is no extra field to keep in step. The issue
templates also ask for the parent's number under a `## Epic` or `## Parent`
heading, and either one satisfies the gate.

**Gate G10 blocks a merge into `main` while any non-epic issue has no
parent**, because an unparented item is work nobody traced back to an
objective — and it is exactly what goes missing when a reader tries to
follow a goal down to the code. On `feature → develop` it is only a warning,
so filing something mid-sprint and parenting it an hour later costs nothing.

`feature` / `enhancement` / `bug` also describe *what kind* of change an item
is, so one item can carry two labels (`task` + `bug`). In CPSC 490 most of
your board is goals, objectives and tasks; enhancements and bugs become the
daily vocabulary in CPSC 491.

### Where the story points go: on the objective, once

| Item | `sp:` label? | Why |
|---|---|---|
| `epic` (a goal) | no | spans sprints; its size is the sum of its objectives |
| `user-story` (an objective) | **yes** | this is the thing committed to a sprint |
| everything below it | no | already inside that objective's estimate |

Point an objective *and* its tasks and you have counted the same work twice
— a sprint that reads as 15 points of capacity when the team committed to 8,
which makes every velocity figure after it wrong.
`scripts/sprint_report.py` catches that, reading both the `- [ ] #12`
checklists and GitHub's native sub-issues, counting the work once at the
objective and naming the labels to fix. The habit is simply: **estimate the
objective, break it down, do not re-estimate the pieces.**

**Board:** create one Project (*Projects → New project → Board*) with
columns **Backlog → Sprint To-Do → In Progress → In Review → Done**. Add
every epic and story to it. It needs **no custom fields**: the `Status`
column field GitHub gives you is the whole board configuration.

> 📋 **The example board is live — open it and copy what you see:**
> **<https://github.com/users/kyoungshin/projects/1>**
> (issues #1–#5 placed across the columns with their Status set, and the
> three views described below.) Put **your** board's URL in your team
> `README.md`.

**Every fact about an issue lives in exactly one place**, which is why the
board carries no fields of its own:

| Fact | Lives in | Not in |
|---|---|---|
| which sprint | the issue's **milestone** | ~~a board Sprint field~~ |
| how big | the issue's **`sp: N` label** | ~~a board Story Points field~~ |
| where in its life | the board's **Status** column | — |

Earlier drafts of this course had the sprint and the points in two places
each — on the issue *and* on the board — and the two copies drifted apart
within a sprint. One copy cannot disagree with itself.

`bash scripts/bootstrap.sh` creates the board and its Status columns for you.

### Running a sprint on the board

Two things confuse people at first, so to be explicit: **the Status columns
are not sprints.** Columns are *where a card is in its life*; the
**milestone** is *which fortnight it belongs to*. A card moves across the
columns within one sprint.

**Set up three views once** (view tabs at the top of the board — the API
cannot create these, so do it by hand; the
[example board](https://github.com/users/kyoungshin/projects/1) has all three
to copy):

| View | Layout | How | What it is for |
|---|---|---|---|
| **Sprint Board** | Board | column field = `Status`; turn on `Milestone` and `Labels` so the sprint and the `sp:` points show on the cards | daily work |
| **Current Sprint** | Board | same, plus filter `milestone:"Sprint 1"` — move it on at each sprint boundary | the only view you need most days — it hides the other three sprints |
| **Sprint Plan** | Table | show `Milestone`, `Status`, `Labels`, `Assignees`; **group by `Milestone`** | planning and the sprint review |

**At sprint planning** — pull work from `Backlog` into `Sprint To-Do`, and
for each card set **assignee, milestone, priority and story points
*now***, not later. Sum the points you pulled: that is your plan.

**During the sprint** — one card per person in `In Progress` is the ideal;
move a card yourself when you branch, and to `In Review` when you open the
pull request. **Nothing reaches `Done` except by a merged PR** — dragging a
card to Done is not how work finishes, and a Done column full of unmerged
cards is the fastest way to undercut the *transparency* evidence behind
that 20%.

**Seeing the story-point totals per sprint.** GitHub's milestone pages count
issues, not points, and the board has no points field to sum — so one
command does it:

```bash
python scripts/sprint_report.py            # or --markdown for the review
```

It prints, per sprint, the points the sprint **started** with, the points
that **closed** inside it, what carried over, what scope was **added after
the sprint began**, and the completion percentage — then reads your own
history back to you: *"completed 8, 11, 9 → commit about 9 next sprint."*

It reads the `sp:` labels and the `Sprint N` milestones straight off the
issues, never the board, so `.github/workflows/sprint-report.yml` runs it
weekly on GitHub's own token — no Projects permission, no personal access
token, no setup. That answer — your team's real capacity — is the number
worth knowing by Sprint 3.

**At the sprint boundary** — read the `Sprint N` group: points planned versus
points actually in `Done`. That ratio is your velocity; it goes in
`docs/sprint-reviews/sprint-N.md` with anything that carried over and why.
Then plan the next sprint from the same view, using the report's suggested
commitment rather than optimism.

**Epics stay on the board but carry no Sprint** — they span sprints, and
their progress shows through the task list of stories in the epic body.

**What "done" means in CPSC 490:** stories come in two kinds and both are
first-class. *Document stories* deliver a section of the proposal or a
spec/design document; *prototype stories* deliver working proof-of-concept
code in `prototype/` (a feature spike, an integration with the sponsor's
data, a demo path for the in-class check). Either kind is Done when its
change is **merged through a reviewed pull request** and its acceptance
criteria are checked off. What waits for CPSC 491 is production-depth
implementation — not coding itself.

---

## 5. Traceability: issues ↔ documents ↔ pull requests

The single habit that most affects your sprint grade:

1. **Every spec/design document names its issues.** Top of each file in
   `docs/`:
   `> Epic: #1 · Stories: #2, #3, #5`
2. **Every story links its document.** In the issue body:
   `Deliverable: docs/specs/account-management.md §2`
3. **Every change lands by pull request**, and the PR body says
   `Closes #12` so the story closes automatically on merge.
4. **Author ≠ reviewer.** A different team member approves each PR before
   merge. Rotate reviewers; don't let one person approve everything.

Issue templates live in `.github/ISSUE_TEMPLATE/` — the example ships
`epic.md`, `user-story.md`, `task.md`, `bug.md` and
`PULL_REQUEST_TEMPLATE.md`, already wired for the fields above. Copy the
folder; you do not need to write them.

---

## 6. The four sprints

Four 2-week sprints between the proposal submission and the Preview Paper
(dates may be adjusted in class — Canvas announcements win):

Each sprint carries **5%** of the course grade (the syllabus's 20%
*Prototype & repository practice*, split evenly across the four), assessed
on the repository at that sprint's boundary.

| Sprint | Dates (planned) | Focus | Syllabus anchor |
|---|---|---|---|
| **Sprint 1** | Sep 28 – Oct 11 | Epics + stories filed from Goals & Objectives; board running; specs started; **prototype v0 → v1 demo path** for the in-class check | ends right before the **Week-8 in-class prototype check** (Oct 13 §01 / Oct 15 §05) |
| **Sprint 2** | Oct 12 – Oct 25 | Specification documents per epic; proposed approach firmed; **prototype reworked from check feedback** | — |
| **Sprint 3** | Oct 26 – Nov 8 | Design documents **with diagrams** (architecture, system context, ER/EER, DFD); **prototype proves the riskiest design choice**; spring timeline drafted | **report draft #1 due Nov 1** (mid-sprint) |
| **Sprint 4** | Nov 9 – Nov 22 | Integration: proposal/report polished end-to-end; **prototype stable + demoable, README run instructions verified** | **report draft #2 due Nov 29** (the sprint's output) |

Plan a healthy mix each sprint — document stories AND prototype stories.
A sprint that is all writing or all code is usually a planning smell.

Before Sprint 1 begins, two things are already due **Sep 27** per the
syllabus: the **project proposal** (HW#4) and **prototype v0 — a running
proof-of-concept committed to this repository**. Keep prototype code in a
`prototype/` folder with a README that says how to run it; prototype work
is issue-tracked like everything else.

Sprint ritual (30 minutes at each boundary, leader drives) — **write it down
in `docs/sprint-reviews/sprint-N.md`** (template in the example repo), and
**revisit [`docs/development-plan.md`](docs/development-plan.md)**: the team
charter, the QA/harness owner rotation, and the risk register all change as
the project does. A charter nobody revises is a charter nobody uses.

Due with the proposal: the **development plan** — a team charter whose
accountability rules carry *quantified triggers and real consequences*
("misses 20% of meetings in a sprint → …"), a QA owner per sprint, your
team's own AI rules, and a risk register. The numbers matter: when something
goes wrong, nobody has to find the courage to accuse a teammate — they point
at the rule everyone agreed to.

- **Close out:** move finished stories to Done (via merged PRs — not by
  dragging cards); carry over or re-scope what didn't finish, with a
  one-line note on why.
- **Plan:** pull next stories from Backlog into the new sprint's milestone;
  every pulled story gets owner, priority, and story points *at
  planning time*, not retroactively.
- Points planned vs. completed per sprint = your velocity; I look at the
  trend, not the absolute number.

---

## 7. Working with an LLM: AIDLC, human-in-the-loop

You may use any LLM (Claude, ChatGPT, Copilot, Gemini) for any part of this
project — that is encouraged, and it is what the AIDLC lectures are about.
The discipline is **human-in-the-loop**: the assistant drafts, *you* verify,
and a *second human* approves. Nothing reaches `main` otherwise.

Four documents in the example repo make that real — copy them and read them
when the table in `QUICKSTART.md` says to:

1. **[`CLAUDE.md`](CLAUDE.md) — standardized context.** One file naming the
   project, conventions, what the assistant may draft, and what only a human
   decides. Every teammate's session starts from the same facts, so you stop
   getting five different answers about your own project. (Copilot reads
   `.github/copilot-instructions.md`, Cursor reads `.cursor/rules/` — keep
   one real file and copy it.)
2. **[`docs/aidlc/prompt-library.md`](docs/aidlc/prompt-library.md) —
   standardized prompts** for the jobs you actually do: draft a spec section
   from a story, write code from acceptance criteria, review a diff, write
   tests, survey related work. Each template ends by requiring the model to
   separate what it verified from what it could not.
3. **[`docs/aidlc/hitl-gates.md`](docs/aidlc/hitl-gates.md) — the seven
   gates.** Read this one carefully. It names the six ways LLMs fail
   (fabrication, plausible-but-wrong, requirement drift, scope creep,
   unverified claims, check-gaming) and, gate by gate, what catches each:
   framing criteria before prompting → your own verification → the CI
   harness → peer review → protected merge → sprint review.

4. **[`docs/aidlc/loop-engineering.md`](docs/aidlc/loop-engineering.md) —
   the harness and the loop.** What a harness is (guides that steer before,
   sensors that detect after), which checks to build first for the best
   payoff, test-first with a committed failing test, the two-correction
   stopping rule, how to tell the *spec* is at fault rather than the prompt,
   how to stop a check from being gamed, and a ten-minute review protocol.
   Teams keep a [harness log](docs/aidlc/harness-log.md) where every rule
   names the failure that caused it — bring it to the sprint review.

**The harness** is the automated half — run it in one second before you push:

```bash
python .github/scripts/check_repo.py
```

It checks template structure, document↔issue traceability, that cited issue
numbers really exist, that links resolve, that no secrets are committed, and
flags leftover placeholders. GitHub Actions runs the same script on every
pull request, plus your prototype's tests and a check that your PR links a
story, discloses AI use, and says what you verified.

**Loop engineering** in one line: frame the criteria, prompt once, verify
against the harness, iterate — two failed corrections mean start a clean
session, three failed attempts mean the specification is the problem, not
the prompt. Keep the local command and the CI command identical, and
disclose AI-assisted commits with an `Assisted-by:` trailer.

**Git workflow and CI/CD:** standard Gitflow
(`main` / `develop` / `feature/*` / `release/*` / `hotfix/*`), branch
protection requiring green CI plus one non-author approval, releases tagged
on `main` — all in
[`docs/git-workflow.md`](docs/git-workflow.md).

**Course AIDLC materials** are in the repository so everything lives in one
place: [`docs/aidlc/lectures/`](docs/aidlc/lectures/) (Lecture 1 From SDLC to
AIDLC / HITL vs HOTL · Lecture 2 Prompt Engineering · Lecture 3 Harness Loop
Engineering · Lecture 4 Benchmarks, Quality and ROI) and the **AIDLC Field
Guide**, which reads in your browser here:
**<https://kyoungshin.github.io/CPSC490/aidlc/AIDLC-Field-Guide.html>**
(the [file in the repo](docs/aidlc/AIDLC-Field-Guide.html) is the same
document as source).

## 8. What I look at in your repository

> **Where this lands in your grade.** The syllabus allocates **20% to
> Prototype & repository practice**, assessed **5% per sprint across the four
> sprints**. That is the only grade item this page feeds — nothing here adds
> an item, changes a weight, or creates a requirement the syllabus does not
> have. It tells you *what I read in the repository* at each checkpoint, so
> the evidence is visible to you before it is visible to me. The syllabus
> governs.
>
> Practically: each sprint is worth the same 5%, assessed at that sprint's
> **boundary** — not retroactively at the end of term. A sprint you let slide
> is 5% you cannot earn back by working twice as hard in the next one. What
> earns it is **progress on the proposal and the prototype**, evidenced in
> the repository so it can be seen and attributed.

**What is actually measured each sprint: progress.** Did the **proposal**
move — new or improved sections, specifications, designs with diagrams — and
did the **prototype** move — something it can do now that it could not at the
start of the sprint? That is the substance, judged against the rubrics for
those deliverables (§3 for the proposal, the checklists in
[`docs/checklists.md`](docs/checklists.md) for specs, designs and code).

The five lenses below are **how the repository evidences that progress** —
they are not a substitute for it. A spotless board, perfect labels and a
current sprint review, with a proposal and prototype that did not advance,
does not earn the sprint's 5%. Equally, real progress that leaves no trail —
no issues, no linked documents, one person's commits, nothing merged — cannot
be assessed as a team's work even when the artifact is good. You need both:
the movement, and the evidence of who moved it.

At each sprint checkpoint I read the repository through five lenses (the same
ones that carry into CPSC 491's implementation sprints):

| Metric | What I look for in YOUR repo |
|---|---|
| **Accountability** | Every story has exactly one assignee; every member owns stories and has commits/PRs each sprint |
| **Traceability** | Story ↔ document ↔ PR links resolve both ways (§5); epics' task lists reflect reality |
| **Transparency** | Board matches the truth — statuses current, carry-overs annotated, no "Done" without a merged PR |
| **Separation of duties** | PRs reviewed by a non-author; review rotation; work distribution isn't one person's repo |
| **Relevance** | Sprint work maps to the proposal's Goals & Objectives — no orphan busywork, no goals with zero movement |

What makes the work hard to see — and therefore hard to credit:
unassigned or field-less issues, documents with no linked issue, one member
with all the commits, a board updated only the night before review, and
"Done" columns full of unmerged work.

**Working agreements your team sets for itself.** These are *not* course
rules and carry no separate grade; they are the defaults recommended in
[`docs/development-plan.md`](docs/development-plan.md) and
[`CONTRIBUTING.md`](CONTRIBUTING.md) because they make the five lenses above
easy to satisfy. Adopt, adjust, or replace them in your charter:

- at least **2 merged contributions per member per sprint**, so the project
  is a team's and not one person's with spectators;
- pull requests under about **10 files / 500 lines**, because a PR nobody can
  review is a PR nobody reviews;
- treat **unmerged work as unfinished** — if it is not merged by the sprint
  boundary it carries over, with a reason, in the sprint review.

**What I read at each sprint review**, beyond the board and the diffs:
your `docs/sprint-reviews/sprint-N.md` — velocity, carry-overs *with
reasons*, the **feedback-response table** (every item of feedback and what
you changed; "we decided not to, because…" is a legitimate row), and the
**contribution snapshot** (three metrics of your choosing, per member). The
snapshot is not a grade; it is an early warning the team can act on itself.
Research on capstone teams finds contribution is unequal in essentially
every team and does not by itself predict quality — what matters is whether
the team noticed and did something.

**Reviewing counts as real work in this course** — it is part of the
*separation of duties* lens above, not a separate grade item. Review against
[`docs/checklists.md`](docs/checklists.md) and name the items you checked in
the PR. "LGTM" is a ceremony, not a review; across published capstone
research, how often teams performed agile ceremonies did not separate strong
teams from weak ones — only how deeply they used them did.

---

## 9. AI usage

AI tools (Claude, Copilot, ChatGPT, …) are **encouraged** for drafting,
reviewing, and organizing — and their use must be disclosed in the
proposal's **AI Usage** section (what tools, for what, and how you verified
the output). AI-assisted work is your work; unverified AI output submitted
as fact is not.

---

## 10. Sponsored projects and your industry mentor

Nine projects from three companies — Edwards Lifesciences, RTX, and SonarX —
are on offer this year, each with a named industry mentor who is your team's
technical contact for both semesters.

**→ [Sponsored projects: titles, summaries, and mentors](docs/sponsored-projects.md)**

That page carries a condensed summary of every project (`EL-1`, `RTX-1`…
`SNX-4`), the mentor and contact address for each company, what each sponsor
says success looks like, and the etiquette for emailing a mentor — one voice
per team, the instructor copied, questions batched, and **no sponsor data in
the repository**. Read the original sponsor document in Canvas before you
write proposal §1; the summary is a starting point, not a requirement set.

---

*Questions or a blocker with GitHub setup? Post in the course channel or
bring it to the project meeting — do not lose sprint days to tooling.*

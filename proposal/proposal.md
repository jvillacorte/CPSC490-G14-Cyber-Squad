# Project Proposal — 〈Project Title〉

**Department of Computer Science**
**CPSC 490 Undergraduate Seminar in Computer Science — Proposal for Capstone Project**

**Group 〈N〉 — 〈Group Name〉** · Sponsor: 〈RTX-3 / EL-1 / SNX-n / independent〉
Authors: 〈Last, First (GitHub username)〉, 〈…〉
Date: 〈YYYY-MM-DD〉

> **This file is the proposal document, not a README.** Its section numbers,
> titles, and guidance are copied from the course Word template, so it
> converts cleanly for Canvas submission. Write continuous academic prose —
> no task lists, no emoji, no repo jargon.
>
> Each section below opens with the template's own guidance in a quote block.
> **Delete the quote blocks and every 〈bracket〉 before submitting.**
>
> **Getting this into the Word template for Canvas.** The template numbers
> its headings **automatically** (a multilevel list: top-level sections at
> level 1, *Related Work* and *Problem Statements* at level 2). The numbers
> typed below exist so the repo copy is readable and checkable — so when you
> move the text into Word, do not end up with both sets.
>
> The reliable route, and the one most teams should use: **open the course
> template and paste your prose section by section**, leaving Word's own
> numbering to do the numbering. Ten minutes, no surprises.
>
> If you prefer to convert, `pandoc` can do it (install with
> `winget install pandoc`):
>
>     pandoc proposal/proposal.md -o proposal.docx --reference-doc="CPSC 490 Project Proposal Template Fall 2026.docx"
>
> Then in Word: delete the typed `0.` / `1.` / `1.1` prefixes (Word re-adds
> them from the list), and set *Related Work* and *Problem Statements* to the
> template's level-2 heading so they number as 1.1 and 1.2. Check figure
> placement, then submit.
>
> **Formatting requirements — the submitted Word document is graded against
> these, explicitly:**
>
> - **Cover page: use the template's cover page, unchanged in layout.** Fill
>   in only its fields — project title, group number and name, sponsor,
>   authors, date — and keep the template's own placement, fonts and spacing
>   for it. The header block at the top of this file carries the same fields
>   so the paste is a transcription, not a redesign.
> - **Font: Times New Roman, 11-point.** Body text, headings and captions
>   take their size and style from the template's own styles — do not
>   restyle anything by hand.
> - **Line spacing: 1.5.** **Margins: 1.0 inch** on all four sides.
> - **Section format, numbering and indentation must match the Word template
>   exactly** — the multilevel-list numbering, heading levels, and paragraph
>   indentation are the template's, not yours. If your document's §1.1 looks
>   different from the template's §1.1, fix yours.
> - **Length: the Final Project Proposal Paper (due Sun Dec 20) must exceed
>   50 pages** under exactly this formatting — font, spacing and margins are
>   fixed above precisely so page count means the same thing for every team.
>   The Preview paper (due Sun Nov 29) is the same document part-way; it has
>   no minimum, but it is graded on the same formatting.
>
> A paste into the template inherits all of this automatically **if you paste
> as text and let Word's styles apply** (Home → Paste → *Keep Text Only*, or
> apply the template's styles after pasting). A pandoc conversion with
> `--reference-doc` inherits it too — but verify font, spacing and margins
> afterward rather than assuming.
>
> Either way, keep this Markdown copy current — it is what peer review and CI
> can actually read. If your team writes in Word instead, commit the `.docx`
> here as well.

---

## 0. Abstract

> The primary purpose of abstract is to help the reader understand the main
> message of current document (proposal in this case) without reading the
> entire document. Therefore an abstract should include at least one or two
> paragraph of background (or motivation) information for the project, a
> brief description of the problem you are trying to solve in this proposal,
> a proposed ideas or solutions, the significance of your proposed idea
> elaborating why the proposed idea is non-trivial, significant, or
> beneficial in one or two paragraphs, the project goals and outcomes in one
> paragraph, and a brief description of what you will discuss in this
> proposal, giving a brief outline of this document in 1-2 sentences in one
> paragraph. Abstract should not exceed one page. Any abstract exceeded
> one-page limit must be shortened.

〈Your abstract. Write it last.〉

## 1. Introduction

> Describe the necessary background on the project field to help the reader
> understand the field. Assume the reader has B.S. degree in computer science
> but not necessary knowledgeable in the selected area. You may also briefly
> describe motivation of the project if any.
>
> Specify the problem identified and to be solved in this project, the
> importance or usefulness of the problem solving or project. Further
> describes what makes your proposal different from existing ones.

〈Your introduction.〉

### 1.1 Related Work

> Describe the related or existing work in detail. This section is like a
> survey on the selected problem or topic.

〈Your survey. Cite with bracketed numbers matching §8 — every reference must
be a source your team has actually read.〉

**Do a comparative analysis, not a list of summaries.** Find the existing
ideas, products, papers, or tools that attack the same problem and compare
them against each other on the dimensions that matter for your project, with
honest pros and cons. Then say plainly what your project does differently and
why that difference is worth the effort.

| Existing approach | What it does | Pros | Cons | Why ours differs |
|---|---|---|---|---|
| 〈product / paper [1]〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |
| 〈product / paper [2]〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |
| 〈product / paper [3]〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |

〈Discuss the table in prose — the table is evidence, the paragraph is the
argument. "Nothing like this exists" is almost never true and reads as a
missing survey; if a close competitor exists, say so and explain why you are
still building this.〉

### 1.2 Problem Statements

> Briefly state the problem to solve in this project.

〈Your problem statement(s), **concise** — a few sentences each, no
background (that was §1) and no solution (that is §3). Number them P1, P2, …
so later sections can refer back.〉

**Every problem here must connect to the goals and objectives in §2, and
every goal in §2 must trace back to a problem here.** A goal with no problem
behind it is scope you invented; a problem with no goal is a problem you are
not actually solving. Check both directions before you submit — this mapping
is what the final project report is graded against.

| Problem | Addressed by |
|---|---|
| P1 〈one line〉 | 〈Goal 1 (#n)〉 |
| P2 〈one line〉 | 〈Goal 2 (#n)〉 |

## 2. Goals and Objectives

> Describe goals and objectives. Goals are general statements of what you are
> trying to accomplish with the project or problems to solve. Objectives are
> specific, measurable statements of what you want to complete to reach the
> project goals. Most projects have 2-3 goals.
>
> List the objectives for each goal. To write objectives, look at the goal
> statement and list what you need to complete using action words like use
> case names in order to meet the goal.
>
> Note that the goals and objectives in a proposal will be an important
> metric to evaluate whether or not you successfully finished your project
> when you turn in your final project report.

Each **goal** is tracked as an **Epic** issue and each **objective** as a
**User Story** issue in the team repository (see the setup guide's *Epics and user stories* section).
**Every epic and user story in the repository is linked from this section** —
CI gate G8 fails if one exists that this section does not link. That is what
keeps the goals in this document and the work on the board from drifting
apart.

Write each objective the way the guidance above asks — **an action word plus
the measure that says it is done**, not a role-play sentence:

- **Goal 1: 〈e.g. Secure account management〉** (Epic #〈n〉)
  - Objective 1.1: 〈Implement member registration and login with hashed
    credentials, session expiry, and rejection of malformed input.〉 (#〈n〉)
  - Objective 1.2: 〈Demonstrate the login round-trip in a runnable prototype
    at the Week-8 in-class check.〉 (#〈n〉)
- **Goal 2: 〈your second goal〉** (Epic #〈n〉)
  - Objective 2.1: 〈Action word + what you will complete + how it will be
    measured〉 (#〈n〉)

〈Replace the brackets with your own 2–3 goals and their objectives, and put
the **real issue numbers** in as you file them — gate G8 checks that every
epic and story in your repository is linked from this section. A fully worked
version of this, with live issues and a populated board, is in the course
example repository.〉

## 3. Proposed Approaches

> Describe your proposed approach to solve the problem, specifying how you
> will achieve the stated goals. List some possible strategies.

〈Your approach — **clear and concise**. State the strategy you chose, the
alternatives you considered, and the reasoning that decided between them.
Think of this as the argument, not the manual: a reader should finish this
section understanding *what* you will do and *why that* rather than the
alternatives.〉

**Keep the details out of this section.** Tooling, platforms, frameworks,
DBMS choices, environment setup, diagrams, and the work breakdown all belong
in §4 (Required Environment, Resources, and Planned Activities). If a
sentence here names a version number, a library, or a configuration, it
probably belongs in §4 — leave a pointer instead ("the implementation stack
is detailed in §4").

〈A few paragraphs, or a short list of candidate strategies with one line of
trade-off each. If it runs past a page, you are writing §4.〉

## 4. Required Environment, Resources, and Planned Activities

> Review the required and available resources and environment to complete
> your project. For example, server, platform, software tools, operating
> systems, DBMS, or any required skills.
>
> Describe the expected activities to achieve the stated goals, e.g.,
> software development process.

〈Your environment, resources, and planned activities.〉

**Diagrams belong in this section.** Include at minimum a high-level
architecture diagram and a system (context) diagram; add the ER/EER model and
a data-flow diagram where they help the reader understand what you are
building and what it depends on. Draw them with any graphical tool
(Lucidchart, draw.io, Miro, Mermaid, ERDPlus, Figma), keep the authoritative
copies in `docs/design/` with both editable source and exported image, and
reference them here.

〈Number every figure, caption it, and point at it from the prose — "Figure 1
shows the three deployment tiers and the trust boundary between them." A
figure the text never mentions is decoration. See `docs/design/DIAGRAMS.md`
for tools, conventions, and the rule that every box and arrow must be
verified against reality.〉

### Specification and design documents

**Every specification and design document the team writes is listed here**
with the objective it serves. This section is the index of the project's
technical detail: §3 holds the argument, §4 holds the documents that make it
buildable. CI gate G9 fails if a document exists in `docs/specs/` or
`docs/design/` that this section does not link.

| Document | Kind | Covers | Issues |
|---|---|---|---|
| 〈docs/specs/account-management.md〉 | specification | 〈account management requirements〉 | 〈#n, #n〉 |
| 〈docs/design/architecture.md〉 | design | 〈system architecture + data model〉 | 〈#n〉 |

〈The scaffold ships `docs/specs/example-spec.md` and
`docs/design/example-design.md` as worked examples — read them, then delete
them once you have your own, and list yours here.〉

〈Replace these rows with your own. Each document names its epic and stories
in its own first lines too (gate G2), so the trail runs both ways.〉

### Planned activities — the work items

The goals and objectives live in §2 as epics and user stories. **This section
links every *other* work item: features, enhancements, bugs, tasks, and
sub-tasks** — the concrete activities that deliver those objectives. CI gate
G8 fails if such an issue exists that this section does not link.

| Issue | Type | Activity | Parent | Owner | Sprint |
|---|---|---|---|---|---|
| 〈#n〉 | 〈task〉 | 〈stand up the prototype login endpoint〉 | 〈#story〉 | 〈owner〉 | 〈Sprint 1〉 |
| 〈#n〉 | 〈feature/enhancement/bug/task/sub-task〉 | 〈…〉 | 〈#story〉 | 〈…〉 | 〈…〉 |

〈Replace these rows with your own, and keep the table current as you file new
issues — with §2 it gives a reader every planned activity in one place, each
traceable to the objective it serves.〉

## 5. Project Outcomes

> Describe the outcomes or deliverables, e.g., final project report, user
> manuals, source code, data or database files, etc.
>
> Note: the deliverables always include the team GitHub repository, which
> must already contain prototype v0 (a thin end-to-end proof-of-concept,
> however small, running when this proposal is submitted). Briefly describe
> what your v0 demonstrates and how to run it.

〈**One or two paragraphs** explaining the project outcome overall — what will
exist when the project is finished, and what it will let someone do. Keep it
prose, not a checklist; name the deliverables inside the paragraphs, and say
briefly what prototype v0 demonstrates today and how to run it.〉

## 6. Project Timeline

> Identifies tasks (project objectives) to be performed, milestones to be
> met, and the estimated number of hours for each task.

〈**This is the plan for CPSC 491 next semester — the implementation timeline,
not this semester's proposal work.** Identify the tasks (your objectives from
§2), the milestones, and the estimated hours for each, in the order they will
be built. State the assumptions it rests on (sponsor availability, data
access, hardware).〉

| Task (objective) | Milestone | Owner | Est. hours | Spring phase |
|---|---|---|---|---|
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |

〈Do **not** put this fall's four proposal sprints here — those live on the
project board and in `docs/sprint-reviews/`. This section answers "how does
the system actually get built next semester?"〉

## 7. AI Usage

> Per the course AI policy (see the syllabus, Use of AI Tools), disclose the
> AI tools used in preparing this proposal and the prototype: which tools,
> for what tasks (e.g., code generation, test writing, debugging,
> diagramming), and approximately what fraction of each artifact was
> AI-assisted.
>
> Reminder: the prose of this proposal must be your own writing. You remain
> fully responsible for the correctness of all AI-assisted work, including
> the prototype code.

〈Your disclosure. Naming the tool is not disclosure — name what it drafted,
what fraction of each artifact was AI-assisted, and how you verified it.〉

## 8. References

> [1] Burges, C. J. C. Tutorial on Support Vector Machines for Pattern
> Recognition. Kluwer Academic Publishers, 1998.
> [2] Chen, P., Fan, R., and Lin, C. A study on SMO-type decomposition
> methods for support vector machines. IEEE Transactions on Neural Networks,
> 2006.
> [3] For Wikipedia, specify the URL here
> [4] For a web source, specify the URL here plus date accessed

〈Number references in the order first cited and cite them in the text as
[1], [2]. Every entry must be a source a team member has actually read and
can produce on request.〉

# Sprint 1 review — Oct 1 – Oct 14, 2026

> One file per sprint, written at the sprint boundary (the setup guide's
> *The four sprints* section). This file, the board, and the merged PRs are
> what the sprint's **5%** (of the syllabus's 20% *Prototype & repository
> practice*) is assessed on — as they stand at the boundary.
>
> **Written late.** This review was reconstructed on Nov 11, 2026 from the
> repository, the issue board, the sprint report and the instructor's
> readiness page, because no review was written at the Oct 14 boundary. Every
> number below comes from that evidence; anything that was not recorded is
> stated as not recorded.

## Progress this sprint — the substance

**Proposal moved:** Very little in the repository. The HW#4 proposal was
submitted on Canvas before the sprint, but `proposal/proposal.md` was still
the course template at the boundary, and the README described a different
project (an AI-assisted security operations platform) from the proposal (the
Cyber Sandbox). The instructor's Oct 15 readiness card recorded both
problems.

| Section | What changed | Where |
|---|---|---|
| Repository workflow | CODEOWNERS added so pull requests request reviewers automatically | PR #5 (#4) |
| Course tooling | Instructor's sprint-report update merged (writing tasks carry story points) | PR #11 (#10) |

**Prototype moved:** No change. `prototype/` held only the course's example
`login.py`.

The sprint was thin, and the reason is plain: the team had not yet moved the
proposal into the repository or agreed which project the repository
described, so there were no goals to file as epics and stories. Both were
fixed at the start of Sprint 2.

## Velocity

| | Story points | Issues |
|---|---|---|
| Planned | 2 | 2 |
| Completed on time | 0 | 0 |
| Closed late | 2 | 2 |

From the Sprint report workflow: both Sprint 1 issues were finished in
merged pull requests but their issues were closed on Oct 16, two days after
the boundary, so the report counts them as late.

## Completed (merged PRs)

| Issue | Owner | Points | PR |
|---|---|---|---|
| #4 Add CODEOWNERS for automatic review routing | @alexgoodson-1991 | 1 | #5 (merged Oct 1; issue closed Oct 16) |
| #6 Sync develop with main to fix G4 harness failure | @alexgoodson-1991 | 1 | #7 (merged Sep 24, before the sprint; issue closed Oct 16) |
| #10 Instructor: sprint report flags writing tasks | instructor | — | #11 (merged Oct 1) |

## Carried over — and why

| Issue | Owner | Why not finished | Decision |
|---|---|---|---|
| #4, #6 | @alexgoodson-1991 | Work was merged, but the issues were not closed until Oct 16 | Closed in Sprint 2; counted as late in the sprint report |
| §2 Goals and Objectives, epics and stories | team | The proposal had not been committed to `proposal.md`, so there was nothing to file | Done at the start of Sprint 2: §2 written and epics #22, #23 with stories #24–#41 filed on Oct 15–16 |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | Not tracked |
| Harness rules added (rows in the harness log) | 0 |

Requirements were not yet written in the repository, so there was nothing to
measure spec-writing against.

## Prototype increment

None. The prototype folder contained only the course example.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Writing tasks should carry story points (instructor issue, Oct 1) | Merged the instructor's sprint-report update | #10 / PR #11 |
| The sprint report counts the last day of a sprint as late (instructor issue, Oct 1) | Not acted on in Sprint 1; the instructor PR was closed as superseded. Fixed in Sprint 3 by running the course-update script | #15 / PR #76 |
| Harness G10 should let a writing task stand alone (instructor issue, Oct 6) | Not acted on in Sprint 1; fixed in Sprint 3 by the course update | #17 / PR #76 |
| One-command Word export of `proposal.md` (instructor issue, Oct 9) | Merged in Sprint 2 | #19 / PR #42 |
| Epics and stories do not match HW#5 §2; the only epic was an unrelated web scanner (instructor issue and readiness card, Oct 12–15) | Filed Goal 1 and Goal 2 as epics and one story per objective, closed the web scanner epic, wrote the issue numbers into §2 | #21 / #22, #23, #24–#41 |
| README and proposal describe different projects; `proposal.md` is still the template (readiness card, Oct 11–15) | README rewritten for the Cyber Sandbox and the proposal committed to `proposal.md` in Sprint 2 | #13 |
| Stop pushing straight to `main`/`develop`; turn on branch protection (readiness card) | Not done in Sprint 1; direct pushes continued into Sprint 2 and 3 | — |
| Replace the PR template text and add `Closes #N` (readiness card) | Not done in Sprint 1; adopted from Sprint 2 onward | — |

## Contribution snapshot

From merged pull requests, submitted reviews and closed issues in the sprint
window. Meeting attendance was not recorded in Sprint 1.

| Member | Meetings attended | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @jvillacorte | Not recorded | 0 | 0 | 2 |
| @danjobo | Not recorded | 0 | 0 | 0 |
| @NguyenVGH | Not recorded | 0 | 0 | 0 |
| @alexgoodson-1991 | Not recorded | 1 | 0 | 0 |
| @Jake-P-N | Not recorded | 0 | 0 | 0 |

The numbers show a sprint in which almost no project work reached the
repository; most activity was setting up the repository itself. Three
members had no recorded contribution. The team's response was to move the
proposal into the repository and file the full issue board at the start of
Sprint 2, so that everyone had assigned work.

## What we change next sprint

- Commit the proposal and §2 to `proposal.md` and file one epic per goal and
  one story per objective before planning anything else.
- Close issues when their pull request merges, not days later.
- Write the sprint review at the boundary instead of reconstructing it.

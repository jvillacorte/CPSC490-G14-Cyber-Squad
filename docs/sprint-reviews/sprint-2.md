# Sprint 2 review — Oct 15 – Oct 28, 2026

> One file per sprint, written at the sprint boundary (the setup guide's
> *The four sprints* section). This file, the board, and the merged PRs are
> what the sprint's **5%** (of the syllabus's 20% *Prototype & repository
> practice*) is assessed on — as they stand at the boundary.
>
> **Written late.** This review was reconstructed on Nov 11, 2026 from the
> repository, the issue board, the sprint report and the instructor's
> readiness page, because no review was written at the Oct 28 boundary.
> Attendance comes from the two team meetings recorded as issues #44 and #45;
> the content of the Oct 15 Sprint 1 review meeting was not recorded and is
> stated as such.

## Progress this sprint — the substance

**Proposal moved:** Sprint 2 turned the repository into the Cyber Sandbox
project. The proposal moved into `proposal.md` with its goals and objectives,
each goal and objective was filed as an epic or story, both specifications
were written, and four of the six design diagrams were merged.

| Section | What changed | Where |
|---|---|---|
| §2 Goals and Objectives | Goals and objectives written into `proposal.md` and linked to epics #22, #23 and stories #24–#41 | Direct commits to `develop` (Oct 15, Oct 28) |
| README | Rewritten to describe the Cyber Sandbox project | #13 |
| `docs/specs/training-environment.md` | New specification for Goal 1 (epic #22) | PR #48 (#46) |
| `docs/specs/ai-scenarios.md` | New specification for Goal 2 (epic #23) | PR #51 (#47) |
| §3 Proposed Approaches | Written | #61, direct commits to `develop` |
| §4 Environment and resources | Written, with a reason for each choice | #59, direct commits to `develop` |
| Figure 3, data flow diagram | `docs/design/data-flow.md` and exported image | PR #64 (#55) |
| Figure 4, ER diagram | `docs/design/data-model.md` and exported image | PR #65 (#56) |
| Figure 6, user flow diagram | `docs/design/user-flow.md` and exported image | PR #67 (#58) |
| Figure 1, high-level architecture | `docs/design/architecture.md` with design decisions and exported image | PR #69 (#53) |
| Word export | The instructor's one-command Word export of `proposal.md` | PR #42 (#19) |

**Prototype moved:** No change. The Sprint 2 checklist asked for a
prototype skeleton with the chosen stack, and none was built; `prototype/`
still held the course example at the boundary. The skeleton task (#60)
carried over.

Two team meetings near the end of the sprint drove the work. On Oct 26
(#44) the team split the architecture planning into tasks and assigned the
requirements lists, the ER diagram and the data flow diagram. On Oct 27
(#45) the team agreed on the project scope and made the sprint's main
technical decision: to build the desktop with Python and PySide6 instead of
Unity, trading raw performance for faster development with ready-made window
components and easier integration with the LLM tooling, all in Python.

The proposal side moved a long way, but nearly all of it landed in the last
two days of the sprint, and some of it (§2, §3 and §4 environment) was pushed
directly to `develop` instead of through pull requests. The prototype did not
move at all.

## Velocity

| | Story points | Issues |
|---|---|---|
| Planned | 23 | 8 |
| Completed on time | 21 | 7 |
| Closed late | 2 | 1 |

From the Sprint report workflow. All 23 points were **added after the sprint
began**: the Sprint 2 issues were filed and pointed on Oct 28, the last day,
after the instructor's Oct 24 readiness card asked for story points and
milestones. The two Goal requirement tasks (#46, #47, 2 points each) were
completed in this sprint but have no milestone, so they are not counted.

## Completed (merged PRs)

| Issue | Owner | Points | PR |
|---|---|---|---|
| #53 High-level architecture diagram | @danjobo | 5 | #69 |
| #55 Data flow diagram for scenario generation and evaluation | @alexgoodson-1991 | 5 | #64 |
| #56 ER diagram for scenario schema and action logs | @NguyenVGH | 3 | #65 |
| #58 User flow diagram for game loop and desktop screens | @jvillacorte | 3 | #67 |
| #59 Write proposal §4 environment and resources | @NguyenVGH | 2 | Direct commits to `develop` (committed by @jvillacorte) |
| #61 Write proposal §3 proposed approaches | @jvillacorte | 2 | Direct commits to `develop` |
| #62 Backfill Sprint 2 story metadata and typed refs | @jvillacorte | 1 | Direct commits to `develop` |
| #46 Create requirements list for Goal 1 (no milestone) | @jvillacorte | 2 | #48 |
| #47 Create requirements list for Goal 2 (no milestone) | @jvillacorte | 2 | #51 |

## Carried over — and why

| Issue | Owner | Why not finished | Decision |
|---|---|---|---|
| #57 UML sequence diagram for critical scenario flow | @Jake-P-N | Merged on Oct 29, one day after the boundary | Closed early in Sprint 3 (PR #77); counted as late |
| #54 System context diagram | @NguyenVGH | Not started in Sprint 2 | Moved to Sprint 3 |
| #60 Prototype skeleton and smoke run | @Jake-P-N | Not started; the team focused on documents | Moved to Sprint 3 |
| Stories #24–#41 | team | Filed without a Sprint milestone or story points | Planning gap; stories still unmilestoned at the end of Sprint 3 |
| #44, #45 (meeting records) | team | Filed with the Task template, `sp: 1` and no milestone instead of the team-meeting template, so they look like tasks on the board and in proposal §4 | Use the team-meeting template for future meetings |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | Not tracked |
| Harness rules added (rows in the harness log) | 0 |

Spec-writing improved: both goals now have a specification with functional
and non-functional requirements traced to stories. Several requirements
(malware behaviors, network fields, completion rules) were left as open
questions, which the architecture work at the end of the sprint began to
answer.

## Prototype increment

None. The prototype skeleton (#60) was not started.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Sprint 1 review meeting (instructor, Oct 15) | Content not recorded | — |
| Give stories `sp:` and a Sprint milestone; Sprint 2 is empty (readiness card, Oct 24) | Sprint 2 tasks filed with `sp:` and the Sprint 2 milestone on Oct 28; stories #24–#41 still have no milestone | #53–#62 |
| Link every issue from `proposal.md` as a typed reference (readiness card, Oct 24) | Backfilled typed references in §2 and the §4 tables | #62 |
| Fill in §4 with the other work items (readiness card, Oct 24) | §4 environment, specification table and planned-activities table added | #59, #62 |
| Python/PySide6 setup has no task; learner outcome evaluation has no objective (readiness card, Oct 24) | Prototype skeleton task filed; no objective added for learner outcomes | #60 |
| Stop pushing straight to `main`/`develop`; turn on branch protection (readiness card, Oct 24) | Not done; §2, §3 and §4 were pushed directly in this sprint | — |
| Every PR replaces the template text and says `Closes #N` (readiness card, Oct 24) | Adopted for the diagram PRs (#64, #65, #67, #69) | — |
| Sprint 2 must deliver specs, a design with diagrams, environment choices and a prototype skeleton (readiness page, Oct 26) | Specs, environment and four diagrams done; system context and sequence diagrams and the skeleton carried over | #54, #57, #60 |

## Contribution snapshot

From merged pull requests, submitted reviews and closed issues (as assignee)
in the sprint window, and the attendance recorded in the two team meetings
(#44 on Oct 26, #45 on Oct 27).

| Member | Meetings attended | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @jvillacorte | 2 of 2 | 6 (plus 2 Copilot PRs he assigned: #48, #51) | 7 | 6 |
| @danjobo | 2 of 2 | 2 | 3 | 6 |
| @NguyenVGH | 1 of 2 | 0 | 4 | 2 |
| @alexgoodson-1991 | 2 of 2 | 2 | 5 | 0 |
| @Jake-P-N | 1 of 2 | 0 | 2 | 0 |

Merged PR counts include release and sync PRs (#43, #52, #63, #66, #68),
which carry other members' work. The numbers hide that NguyenVGH's ER
diagram (#56) was merged in a PR authored by alexgoodson-1991 (#65), and that
§2–§4 were written in direct commits by jvillacorte that no PR counts.
Jake-P-N had no merged work in the sprint and missed the Oct 26 planning
meeting; his sequence diagram merged one day after the boundary. Only two
meetings were recorded, both in the final three days, so attendance earlier
in the sprint is unknown. The issues-closed counts include #44 and #45, which
are meeting records assigned to all five members.

## What we change next sprint

- Plan the sprint at its start, so issues count as committed rather than
  added mid-sprint.
- Every change goes through a pull request; turn on branch protection for
  `main` and `develop`.
- Start the prototype skeleton (#60) in the first week of Sprint 3.

# Sprint 3 review — Oct 29 – Nov 11, 2026

> One file per sprint, written at the sprint boundary (the setup guide's
> *The four sprints* section). This file, the board, and the merged PRs are
> what the sprint's **5%** (of the syllabus's 20% *Prototype & repository
> practice*) is assessed on — as they stand at the boundary.
>
> Written on Nov 11, 2026, the last day of the sprint, from the repository,
> the issue board, the Sprint report workflow and the instructor's readiness
> page and Nov 2 email.

## Progress this sprint — the substance

**Proposal moved:** Sprint 3 finished the design set and began turning §4
into the prose paper the instructor asked for. All six required diagram types
are now merged, two components (the virtual file system and the network
activity viewer) have full specifications and design documents, the §4
tables were rewritten as paragraphs, and on the last day the first runnable
prototype slice merged.

| Section | What changed | Where |
|---|---|---|
| Course files | Sprint report and harness fixes from the instructor's course-update script | PR #76 (#15, #17) |
| Figure 5, UML sequence diagram | `docs/design/scenario-sequence.md` | PR #77 (#57) |
| Figure 2, system context diagram | `docs/design/system-context.md`, embedded in §4 | PR #75, PR #118 (#54) |
| Design alignment | Data model, data flow and both specs aligned with the architecture decisions | PR #74 (#70, #72, #73) |
| §4 Environment and traceability | Environment table explained in prose; issue references aligned | PR #96 (#93) |
| §4 Planned activities | Rewritten from a table into paragraphs by purpose and sprint | PR #95 (#94) |
| Figures 4 and 5 in §4 | ER and sequence diagrams embedded with captions and explanations | PR #116 (#111) |
| Figures 7 and 8, virtual file system | `docs/design/virtual-file-system.md` for Objective 1.2 | PR #100 (#99) |
| Network activity viewer specification | Fields, protocols and states; 16 detailed requirements; acceptance criteria with verification methods; §4 summary | PR #117, PR #119 (#101–#104) |
| Figures 9–11, network activity viewer design | `docs/design/network-activity-viewer.md`: components, connection lifecycle, wireframe, seven key decisions, open items; §4 summary and figures | PR #121 (#105–#110) |
| §1 Introduction and §1.1 Related Work | Sourced comparison with existing training simulators, expanded into prose | PR #120 (#113) |
| Word export | Updated converter and paragraph formatting for the Word submission | PR #98 (#97) |
| Proposal traceability | Issue references completed and statuses refreshed across the proposal | PR #122 (#113) |
| Prototype slice and §4 prototype text | PySide6 start menu, one Pydantic-validated sample scenario, in-memory file explorer, 20 tests; §4 updated to describe it | PR #123 (#60) |
| Team communication | Discord server set up and documented | PR #90 (#86) |
| Release | `develop` released to `main` | PR #71, PR #89 |

**Prototype moved:** For the first time, on the last day. Until Nov 11 the
prototype was only a README and a placeholder Dockerfile (PR #87). PR #123,
merged at 7:51 pm on Nov 11, added the first runnable slice: `python
start_simulation.py` opens a PySide6 start menu, loads one sample scenario
after validating it with a Pydantic schema, and shows an in-memory file
explorer where the student can browse folders, inspect, create and delete
simulated files, and restart the scenario. It adds 20 tests (scenario
validation, simulation and offscreen UI), all passing; CI runs the 15
scenario and simulation tests and skips the UI tests on runners without Qt's
graphics libraries. The folders follow the architecture's layers: `ui/` is
the presentation layer, `sim/` the simulation core and `scenario/` the
schema and validation from the AI integration layer, with a local sample in
place of NRP.ai.

The slice proves the desktop and validation path, but not the riskiest
design choices: there is no AI generation and no host-isolation test yet, so
#79 stays open. The proposal was the strongest part of the sprint; the
prototype arrived late, merged hours before the boundary rather than early
enough to be reviewed and iterated on.

## Velocity

| | Story points | Issues |
|---|---|---|
| Planned | 38 | 17 |
| Completed on time | 17 | 10 |
| Carried over | 21 | 7 |

From the Sprint report workflow, run on Nov 11. Only 5 of the 38 points (the
alignment tasks #70, #72, #73) were in the milestone when the sprint began;
33 were added during it. The remaining issues in the milestone (#101–#110,
the network viewer features and tasks) carry no points of their own, because
their parent story #28 holds the estimate. #85, this task, is not counted by
the report.

## Completed (merged PRs)

| Issue | Owner | Points | PR |
|---|---|---|---|
| #70 Align data-model.md with architecture decisions | @danjobo | 2 | #74 |
| #72 Align data-flow.md with architecture decisions | @danjobo | 2 | #74 |
| #73 Mark spec open questions answered by architecture decisions | @danjobo | 1 | #74 |
| #83 Make proposal §4 work-item references complete | @Jake-P-N | 2 | #96 |
| #86 Create a Discord server for group communication | @NguyenVGH | 2 | #90 |
| #93 Rewrite §4 environment and resources in paragraph format | @danjobo | 2 | #96 |
| #94 Rewrite §4 planned activities in paragraph format | @alexgoodson-1991 | 3 | #95 |
| #97 Update proposal Word export and paragraph formatting | @jvillacorte | 1 | #98 |
| #99 Virtual file system design doc and Figures 7–8 | @alexgoodson-1991 | 1 | #100 |
| #111 Embed the data-model and sequence diagrams in §4 | @alexgoodson-1991 | 1 | #116 |
| #101–#104 Specify the network activity viewer (under story #28) | @danjobo | — | #117, #119 |
| #105–#110 Design the network activity viewer (under story #28) | @danjobo | — | #121 |

## Carried over — and why

| Issue | Owner | Why not finished | Decision |
|---|---|---|---|
| #60 Prototype skeleton and smoke run | @Jake-P-N | Delivered by PR #123 (authored by @jvillacorte with Copilot) on the last day; the issue was not closed because merges into `develop` do not close issues | Close; the deliverable is merged |
| #79 Prototype the riskiest design choice | team | The slice in PR #123 proves the desktop and validation path, but not AI generation or host isolation | Moved to Sprint 4; choose which risk to prove at the Sprint 4 planning meeting |
| #54 System context diagram | @NguyenVGH | The diagram merged (PR #75, fixed in PR #118) but the issue was not closed | Close; the deliverable is merged |
| #80 Draft the spring implementation timeline | team | Not started | Moved to Sprint 4 |
| #81 Prepare report draft #1 | team | Not started | Moved to Sprint 4 |
| #82 Complete proposal outcomes and AI disclosure | unassigned | Not started; no owner | Moved to Sprint 4; assign an owner |
| #84 Complete the project development plan | unassigned | Not started; no owner | Moved to Sprint 4; assign an owner |
| #85 Complete sprint review records | @danjobo | Completed on the last day of the sprint with this file | Close when this pull request merges |
| #28 Objective 1.5: network activity viewer (no milestone) | @danjobo | Specification (#101) and design (#105) completed this sprint; AC1–AC6 require a working viewer, which is outside this semester's prototype slice | Implementation moved to CPSC 491; story stays open in Backlog |

## Loop health (docs/aidlc/loop-engineering.md §8)

| | This sprint |
|---|---|
| Iterations to green, average per PR | Not tracked |
| Harness rules added (rows in the harness log) | 0 |

Spec-writing is improving. The network activity viewer went from three
general requirements to a specification with defined fields, sixteen
detailed requirements and testable acceptance criteria before any design
began, and the design was written against it. Two process failures repeated
from earlier sprints: the system context diagram merged with invalid Mermaid
and an unembedded image and had to be fixed in a second PR, and a draft pull
request (#117) was merged before it was finished.

## Prototype increment

From nothing runnable to a working slice (PR #123). Demonstrated by
following `prototype/README.md` from a clean environment: create a virtual
environment outside the repository, `pip install -r requirements.txt pytest`,
run `python start_simulation.py` to open the start menu and file explorer,
and run `python -m pytest -q` for 20 passing tests. The placeholder
Dockerfile was removed.

## Feedback we received, and what we did about it

| Feedback (source) | What we changed | Issue / PR |
|---|---|---|
| Sprint 2 review meeting (instructor, Oct 29) | Content not recorded | — |
| Build the prototype skeleton with PySide6 and Pydantic, a smoke run and tests (readiness card, Oct 29; email, Nov 2; readiness card, Nov 10) | Done on the last day: runnable start menu, validated sample scenario, file explorer and 20 tests merged into `develop`; not yet released to `main` | #60 / PR #87, PR #123 |
| Reviewer feedback on the prototype PR: keep the course's `check_repo.py` and `ci.yml` unedited so future course updates still reach them (danjobo, review on PR #123) | Virtual environment moved outside the repository in the README; UI tests skip when Qt's graphics libraries are missing instead of changing CI; both course files left unedited | PR #123 |
| Merge the system context diagram and fix it (readiness card, Oct 29) | Merged and fixed; issue still open | #54 / PR #75, PR #118 |
| Write the sequence diagram or remove the dead §4 link (readiness card, Oct 29) | Sequence diagram merged | #57 / PR #77 |
| Finish aligning the data model, data flow and spec questions with the architecture (readiness card, Oct 29) | Done | #70, #72, #73 / PR #74 |
| Break every story into features, tasks and sub-tasks as sub-issues; points on stories only (email, Nov 2; readiness card, Nov 10) | Done for story #28 (2 features, 8 tasks); the other 17 stories still have no child issues, and the Sprint 3 tasks hang off the epics | #101–#110 |
| The proposal must stand alone as a 50-page technical paper; write §4 in full paragraphs that end with their issue references (email, Nov 2) | §4 environment and planned activities rewritten as prose; network viewer and virtual file system summarized in §4 with explained figures | PR #95, PR #96, PR #100, PR #119, PR #121 |
| Embed Figures 2, 4 and 5 with captions and explanations (readiness card, Nov 10) | Done | #111 / PR #116, PR #118 |
| Summarize spec requirements and acceptance criteria inside §4 (readiness card, Nov 10) | Done for the network activity viewer; not yet for the rest of the two specs | PR #119 |
| Add a §4 implementation-details section (readiness card, Nov 10) | Started: §4 now describes the prototype slice; a full implementation-details section is still to write | PR #123 |
| Expand §1 and §1.1 into prose arguing how the project differs (readiness card, Nov 10) | Done | #113 / PR #120 |
| Stop direct commits to `main` (readiness card, Nov 10) | Not done; branch protection is still off | — |

## Contribution snapshot

From merged pull requests, submitted reviews and closed issues (as assignee)
in the sprint window, and the attendance recorded in the two Sprint 3 meeting
issues (#91 on Nov 2, #92 on Nov 4).

| Member | Meetings attended | Merged PRs | Issues closed | Reviews given |
|---|---|---|---|---|
| @jvillacorte | 0 of 2 | 7 | 1 | 11 |
| @danjobo | 2 of 2 | 6 | 15 | 8 |
| @NguyenVGH | 2 of 2 | 2 | 1 | 2 |
| @alexgoodson-1991 | 2 of 2 | 3 | 3 | 1 |
| @Jake-P-N | 1 of 2 | 2 | 2 | 2 |

The numbers hide some things. Most of danjobo's closed issues are the ten
network viewer features and tasks, which are small by design. jvillacorte
missed both recorded meetings but gave the most reviews and merged the
release, proposal-formatting and prototype work, much of it drafted with
GitHub Copilot. alexgoodson-1991 gave one review across Sprints 2 and 3. The
prototype skeleton (#60) was assigned to Jake-P-N but delivered in a pull
request by jvillacorte, so the merged-PR column does not show who owned the
task.
Velocity reflects the Sprint report after closing #54 and #60, whose deliverables merged in #118 and #123.

## What we change next sprint

- Build on the merged prototype slice early in Sprint 4 instead of on the
  last day, and choose which risk to prove next (#79) at the planning
  meeting: AI generation and validation, or host isolation.
- Give every story in Sprint 4 child issues and a Sprint milestone at
  planning time, not mid-sprint.
- Turn on branch protection for `main` and `develop`, and stop merging draft
  pull requests.
- Rotate reviews so every member reviews at least one pull request per week.

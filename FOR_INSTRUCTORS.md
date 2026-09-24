# For instructors adopting this scaffold

This repository is the working scaffold for **CPSC 490 Undergraduate Seminar**
(the proposal semester) at CSU Fullerton, Fall 2026. Student teams copy it and
run their capstone proposal like a real software project: issues and a board,
four 2-week sprints, Gitflow, GitHub Actions as an automated harness, and an
explicitly **human-in-the-loop** AI policy.

**Author and copyright:** Kyoung Shin, Department of Computer Science,
California State University, Fullerton — <kshin@fullerton.edu>. This
curriculum, the AIDLC lecture series, and the harness are his original course
work.

**Terms: all rights reserved — please ask first.** The repository is public
so that enrolled students can copy it and so colleagues can evaluate the
approach, but publication grants no licence (see [`LICENSE`](LICENSE)).
If you would like to use or adapt any of it for your own course, write to
<kshin@fullerton.edu>. Requests from fellow instructors are welcome and
normally granted — the point is simply that the author knows who is using
the material and that authorship stays clear. Once granted, please cite:

> Shin, K. (2026). *CPSC 490 AIDLC course scaffold: human-in-the-loop
> AI-driven development for undergraduate capstone projects.* Department of
> Computer Science, California State University, Fullerton. Used with
> permission. https://github.com/kyoungshin/CPSC490

---

## What is here

| Piece | What it does |
|---|---|
| [`QUICKSTART.md`](QUICKSTART.md) | the student entry point: whole setup in ~1 hour of numbered steps |
| [`README.md`](README.md) | the full reference guide (repo layout, proposal rules, board conventions, sprint cadence, grading metrics) |
| [`scripts/bootstrap.sh`](scripts/bootstrap.sh) | one command creates the 15 labels, 4 sprint milestones, `develop`, branch protection, and a project board with its Status columns |
| [`.github/scripts/check_repo.py`](.github/scripts/check_repo.py) | the harness: 10 gates, standard library only, same command locally and in CI |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | runs the harness, the prototype's tests, and a PR-discipline check |
| [`docs/aidlc/`](docs/aidlc/) | the AI-use curriculum: the seven gates, a prompt library, harness/loop engineering, a harness log, four lecture decks, and a sourced evidence appendix |
| [AIDLC Field Guide](https://kyoungshin.github.io/CPSC490/aidlc/AIDLC-Field-Guide.html) | the four-week course companion, served via GitHub Pages (`docs/.nojekyll` keeps Jekyll from mangling the `{{…}}` prompt placeholders) |
| [`docs/design/DIAGRAMS.md`](docs/design/DIAGRAMS.md) | which diagram answers which question, tools, and file conventions |
| [`proposal/proposal.md`](proposal/proposal.md) | proposal skeleton matching our Word template section-for-section |
| `docs/specs/`, `docs/design/`, `prototype/` | worked examples, not stubs — a real specification, a design doc with three Mermaid diagrams, and a runnable prototype with tests |

## The ten gates, in one line each

The harness exists because LLM output fails in recognizable ways. Each gate
targets one; `docs/aidlc/hitl-gates.md` explains them to students.

| Gate | Checks | Catches |
|---|---|---|
| G1 | proposal has the template's sections, with its numbering | the assistant "improving" required structure |
| G2 | every spec/design doc names its issues | orphan documents nobody asked for |
| G3 | cited issue numbers exist | invented references |
| G4 | relative links resolve | confident links to files that were never written |
| G5 | no committed credentials (with an auditable `allowlist secret` marker) | "just hardcode it for now" |
| G6 | leftover placeholders *(warning)* | sections marked done that are not |
| G7 | every design document contains a diagram | design-by-prose |
| G8 | epics/stories linked from proposal §2; other work items from §4 | the document and the board drifting apart |
| G9 | every specification and design document indexed in proposal §4 | technical detail a reader cannot find |
| G10 | every non-epic issue names a parent | work nobody traced back to an objective |

G8, G9 and G10 are advisory on `feature → develop` and blocking into `main`,
so a mid-sprint issue nobody has linked yet cannot redden an unrelated PR.

## What to change for your course

Search-and-replace, roughly in order of importance:

1. **Instructor username** — `kyoungshin` appears in `QUICKSTART.md` (add as
   collaborator) and in the board URL. Replace with yours.
2. **Course number and title** — `CPSC 490` throughout; `CPSC 491` is
   referenced as "next semester, the implementation course".
3. **Sprint dates** — four 2-week sprints. They appear in
   `scripts/bootstrap.sh` (milestone due dates and the iteration
   configuration), `README.md` §6, and `QUICKSTART.md`.
4. **Proposal sections** — `REQUIRED_PROPOSAL_SECTIONS` in
   `.github/scripts/check_repo.py` encodes our template's headings and
   numbering (0 Abstract; 1 Introduction with 1.1–1.2; 2 Goals and
   Objectives; … 8 References). Swap in your own and G1 enforces it.
   `proposal/proposal.md` quotes our template's guidance text under each
   heading — replace with yours.
5. **Deliverable dates** — prototype v0, the in-class prototype check, and
   the two report drafts are named in `README.md` §6 and the proposal
   skeleton.
6. **Grading metrics** — `README.md` §8 uses five per-sprint metrics
   (accountability, traceability, transparency, separation of duties,
   relevance). Adjust the wording to your rubric; the harness already
   produces the evidence each one reads.
7. **Repo naming convention** — `CPSC490-G<number>-<groupname>`.

Nothing in the harness is course-specific beyond those constants; it is
plain Python with no dependencies, so it runs on any runner.

## Notes from building it

- **A gate that silently passes is worse than no gate.** Our CI reported
  "tests passed" for a while without running them, because the step gated on
  a shell glob. It now reads pytest's exit code. Check your gates actually
  fire before you trust them.
- **Re-running setup must be safe.** An early version of `bootstrap.sh`
  replaced the board's Status options on every run, which rotates their IDs
  and silently clears every card's status. It now compares first.
- **The harness log is the best learning artifact.** Every rule cites the
  failure that produced it (`docs/aidlc/harness-log.md`). Students bring it
  to the sprint review; it shows *learning*, not just output.
- **Scope the content gates to student deliverables.** Ours initially
  flagged the course documents that *explain* issue numbers.
- The two numbers worth tracking per team are **iterations-to-green per PR**
  and **harness rules added per week** (`docs/aidlc/loop-engineering.md` §8).

## Known gaps, honestly

- The prototype example is Python; a Node example would serve teams that pick
  JavaScript (CI already auto-detects and runs either).
- The sample issues are all assigned to one account, so the example does not
  model work distribution across a team.
- This repository's own history does not model the pull-request flow, because
  a single maintainer cannot approve their own PR.
- Reading load is ~90 minutes in total. The **required** subset is ~17
  minutes and named at the top of `QUICKSTART.md`; everything else is
  reference. If your students will not read that much, cut
  `loop-engineering.md` and the evidence appendix first.

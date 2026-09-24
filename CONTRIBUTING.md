# Contributing — how this team works

The short version. Details are linked from each line.

1. **Pick up work as an issue.** Every change starts from an issue with an
   assignee, a sprint milestone, `priority:`, a `sp:` story-point label, and
   acceptance criteria — see the setup guide §4.
2. **Branch per issue:** `feature/<issue>-<slug>` off `develop`
   ([`docs/git-workflow.md`](docs/git-workflow.md)).
3. **Write the acceptance criteria before you prompt an assistant**, and keep
   yourself in the loop — the seven gates are in
   [`docs/aidlc/hitl-gates.md`](docs/aidlc/hitl-gates.md), the standard
   prompts in [`docs/aidlc/prompt-library.md`](docs/aidlc/prompt-library.md).
4. **Run the harness before you push:**
   `python .github/scripts/check_repo.py`
5. **Open a pull request into `develop`**, fill in the template: link the
   story (`Closes #n`), say what you verified, disclose AI use.
6. **A teammate who is not the author reviews it** against
   [`docs/checklists.md`](docs/checklists.md) and names the items they
   checked — reviewing is real work here, not a rubber stamp.
7. **Green CI + one approval → squash merge**, branch deleted.

## Working agreements we hold ourselves to

*(Our team's own rules, not course requirements — the syllabus governs
grades. We keep them because they make our work visible and reviewable.)*

- At least **2 merged contributions per member per sprint**.
- Pull requests under **10 files / 500 lines**, except by agreement — a PR
  nobody can review is a PR nobody reviews.
- **We treat unmerged work as unfinished.** If it is not merged by the
  sprint boundary it carries over, with a reason, in the sprint review —
  each sprint is assessed on what the repository shows at its boundary.
- **Tests are append-only** while implementing; weakening CI is a blocker.
- Nobody merges work they cannot explain out loud.

## Every sprint boundary

Close out the board, plan the next sprint, and write
`docs/sprint-reviews/sprint-N.md` — velocity, carry-overs with reasons, the
feedback-response table, and the contribution snapshot. Revisit
[`docs/development-plan.md`](docs/development-plan.md) and change what is not
working.

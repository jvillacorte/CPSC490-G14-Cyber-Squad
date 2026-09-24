# Quick start — one hour, start to finished setup

**Read this page first.** It is the whole setup, in order, as commands and
clicks. Everything else in this repository is reference material you read
when you need it (map at the bottom).

Do steps 1–4 together as a team in one sitting. One person drives; everyone
watches, because everyone has to work in this repo.

---

## 1. Leader: create the repository (5 min)

1. GitHub → **New repository**
2. Name: `CPSC490-G<number>-<groupname>` — e.g. `CPSC490-G03-California`
3. **Visibility — read this before you pick:**
   - **Public** — branch protection works on the free plan, so "green CI + one
     approval before merge" is actually *enforced*. Your proposal and
     prototype are visible to anyone. Recommended unless your sponsor has
     told you the work is confidential.
   - **Private** — GitHub does **not** allow branch protection on private
     repositories on the free plan, so the merge rule becomes honour-based
     unless someone on the team activates **GitHub Pro/Team free through
     [GitHub Education](https://education.github.com)** (a few minutes with a
     `.edu` address). If your sponsor requires private, do that.
4. Check **Add a README file**, and create it.

## 2. Leader: add your team and the instructor (2 min)

**Settings → Collaborators → Add people** — add every teammate's GitHub
username, then add **`kyoungshin`** (required, so your work can be graded).

## 3. Leader: copy the scaffolding from this example repo (10 min)

**Copy it with the command below, not by dragging files.** `.github/` is a
*hidden* folder: unzip-and-drag silently leaves it behind, and without it you
get no CI, no harness, and no issue templates — with nothing to tell you they
are missing. (This is not hypothetical; it happened to a team in 2026.)

From inside your new, empty repository:

```bash
git clone --depth 1 https://github.com/kyoungshin/CPSC490.git ../cpsc490-scaffold
(cd ../cpsc490-scaffold && git archive HEAD) | tar -x -C .
rm -rf ../cpsc490-scaffold

# VERIFY before you commit — all four must print
ls -d .github .gitignore docs scripts
```

If `ls` cannot find `.github`, your copy is incomplete — re-run the three
lines above. `git archive` includes hidden files and excludes the example
repo's own git history, which is what you want.

What you just copied:

| Copy this | To | What it is |
|---|---|---|
| `README_TEMPLATE.md` | rename to your `README.md` | your team's front page — fill in the 〈brackets〉 |
| `CLAUDE.md` | `CLAUDE.md` | shared AI context — fill in the 〈brackets〉 |
| `proposal/proposal.md` | `proposal/proposal.md` | the proposal skeleton (already matches the Word template) |
| `.github/` (whole folder) | `.github/` | issue + PR templates, CI workflow, the harness script — **hidden; the command above is the only reliable way to get it** |
| `docs/` (whole folder) | `docs/` | reference docs, diagram guide, sprint-review template |
| `scripts/` (whole folder) | `scripts/` | the setup script and the sprint story-point report |
| `prototype/` | `prototype/` | the runnable starter — replace the code with yours |

```bash
git add -A && git commit -m "chore: course scaffolding" && git push
```

The two `example-*` documents in `docs/specs/` and `docs/design/` are worked
examples to read and then delete once you have your own — the harness treats
them as reference material, so they will not fail your CI while they sit
there.

## 4. Leader: set up branches, labels, milestones, board (1 command)

Everything in this step is automated. From inside your repository:

```bash
gh auth login                       # once, if you have not
gh auth refresh -s project,repo     # lets it create the board
bash scripts/bootstrap.sh
```

That creates all 15 labels, the four sprint milestones with dates, the
`develop` branch, branch protection on `main` and `develop`, and the project
board with its Status columns. It is safe to re-run —
it skips whatever already exists — and it prints what is left for you.

**One thing you must add by hand** (GitHub's API cannot create board views):
three view tabs on the board — a **Sprint Board**, a **Current Sprint** board
filtered to `milestone:"Sprint 1"`, and a **Sprint Plan** table grouped by
`Milestone`. Two minutes, and it is what makes the board usable during a sprint.
The recipe is in the setup guide §4 ("Running a sprint on the board"), and the
[example board](https://github.com/users/kyoungshin/projects/1) has all three
set up to copy.

<details>
<summary>Or do it by hand (click-by-click, ~20 minutes)</summary>

**Branches** — create `develop` and protect both:

```bash
git switch -c develop && git push -u origin develop
```

Then **Settings → Branches → Add branch ruleset**, once for `main` and once
for `develop`:
- Require a pull request before merging
- Require approvals: **1**
- Dismiss stale approvals when new commits are pushed
- Require status checks: `Repository harness`, `Prototype build & tests`, `PR links an issue and discloses AI use`
- Require branches to be up to date before merging
- Block force pushes

**Labels** — Issues → Labels → New label. Add these 15 (GitHub pre-creates a
few of its own such as `documentation` and `question`, so your total will be
higher — leaving them alone is harmless):

```
epic  user-story  feature  enhancement  bug  task  sub-task
priority: high   priority: medium   priority: low
sp: 1   sp: 2   sp: 3   sp: 5   sp: 8
```

**Milestones** — Issues → Milestones → New milestone: `Sprint 1` … `Sprint 4`
with the due dates from the setup guide §6.

**Board** — Projects → New project → **Board**:
- Status column values: `Backlog`, `Sprint To-Do`, `In Progress`, `In Review`, `Done`
- no custom fields — the sprint is the issue's milestone and the size is its
  `sp:` label, so the board never holds a second copy of either
- paste the board URL into your README

</details>

## 5. Everyone: file your goals and objectives as issues (30 min)

From your proposal's *Goals and Objectives*:

- one **epic** issue per goal (label `epic`)
- one **user-story** issue per objective (label `user-story`), each with
  **assignee, milestone, `priority:`, a `sp:` story-point label, and
  acceptance criteria** — filled in when the story enters a sprint, not later
- list the story numbers in the epic body as `- [ ] #12` so progress shows
- link every epic and story from proposal §2, and every task/bug/feature
  from proposal §4

Also in week one: fill in [`docs/development-plan.md`](docs/development-plan.md)
together — the team charter's accountability rules need **numbers**
("misses 20% of meetings in a sprint → …"), because that is what lets anyone
raise a problem later without it being personal.

## 6. Everyone: make your first real pull request (15 min)

```bash
git switch develop && git pull
git switch -c feature/<issue-number>-<short-slug>
# ...do the work...
python .github/scripts/check_repo.py        # the harness — must be green
git push -u origin HEAD
```

Open the PR against `develop`, fill in the template (link the story, say
what you verified, disclose AI use), and have **a teammate who is not the
author** approve it. Green CI + one approval → squash merge.

That is the loop you will repeat all semester.

---

## What to read, and when

**Required reading, whole team, before Sprint 1 — about 17 minutes:** this
page (4 min) + [`docs/aidlc/hitl-gates.md`](docs/aidlc/hitl-gates.md) (9 min)
+ [`README.md`](README.md) §3, the proposal rules (4 min). That is the
mandatory set. **Everything else below is reference** — look it up when the
right-hand column applies to what you are doing today. Nobody is expected to
read it all at once.

| When | Read |
|---|---|
| Before Sprint 1, everyone | [`docs/aidlc/hitl-gates.md`](docs/aidlc/hitl-gates.md) — the seven gates and the LLM failure each one catches |
| Before you first use an LLM on this project | [`docs/aidlc/prompt-library.md`](docs/aidlc/prompt-library.md) — the standard prompts |
| Before your first PR | [`docs/git-workflow.md`](docs/git-workflow.md) — Gitflow, CI, releases |
| When writing the proposal | [`README.md`](README.md) §3 and the skeleton in `proposal/proposal.md` |
| When you start design work | [`docs/design/DIAGRAMS.md`](docs/design/DIAGRAMS.md) — which diagram, which tool, where it lives |
| When something keeps going wrong | [`docs/aidlc/loop-engineering.md`](docs/aidlc/loop-engineering.md) — harness building and the stopping rules |
| At every sprint boundary | [`docs/sprint-reviews/sprint-1.md`](docs/sprint-reviews/sprint-1.md) — copy it for the new sprint |
| Before your first review of someone's PR | [`docs/checklists.md`](docs/checklists.md) — what you review against, and name |
| With the proposal, then every sprint | [`docs/development-plan.md`](docs/development-plan.md) — team charter with real triggers, QA owner, risk register |
| The full reference | [`README.md`](README.md) — the complete setup guide |
| When you want the research behind a rule | [`docs/aidlc/evidence.md`](docs/aidlc/evidence.md) — sources and measured failure rates |
| At planning, to decide how much to commit | `python scripts/sprint_report.py` — points committed vs closed per sprint, and your real capacity |

Stuck on tooling for more than 20 minutes? Ask in the course channel or at
the project meeting. Do not lose sprint days to setup.

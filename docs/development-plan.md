# Development plan — Group 〈N〉 〈Group Name〉

> Due with the proposal. Revisit it at **every sprint review** and change what
> is not working — a plan nobody revises is a plan nobody uses.

## 1. Team charter

### External goals

〈What does this team want out of the project beyond a grade? A portfolio
piece, a sponsor reference, a conference submission, a skill each member
wants? Say it plainly — it is what you will trade against when time runs
short.〉

### Attendance

| | Our rule |
|---|---|
| Expected meetings | 〈e.g. Tuesdays 4pm, plus the project meeting〉 |
| Acceptable excuse | 〈e.g. illness, work shift, family — told in the group chat before the meeting〉 |
| Unacceptable | 〈e.g. silent no-show〉 |
| In an emergency | 〈who to tell, and how work gets handed over〉 |

### Accountability — with numbers

**Write a quantified trigger and a real consequence for each row.** A vague
charter ("we will all do our share") is useless at the moment you need it.
The point of numbers is that nobody has to muster the courage to accuse a
teammate — they point at the rule everyone already agreed to.

| Concern | Trigger (measurable) | Consequence |
|---|---|---|
| Missing meetings | 〈misses 20% of team meetings in a sprint〉 | 〈brings coffee; second occurrence → the team raises it at the project meeting〉 |
| Not contributing code/docs | 〈fewer than 5% of the team's merged PRs by the prototype-v0 deadline〉 | 〈meeting with the instructor〉 |
| Work quality | 〈a PR reopened twice for the same missed acceptance criterion〉 | 〈pairs with a teammate on the next story〉 |
| Not reviewing | 〈reviews no PR in a sprint〉 | 〈takes the reviewer rotation for the next sprint〉 |
| Going dark | 〈no response in the group chat for 3 days〉 | 〈team lead calls; then the instructor is told〉 |

### Quality assurance

〈Name the person — rotating by sprint — responsible each sprint for the
harness being green, the board matching reality, and the sprint review being
written. See the "harness owner" idea in `docs/aidlc/loop-engineering.md` §8.〉

| Sprint | QA / harness owner |
|---|---|
| 1 | 〈name〉 |
| 2 | 〈name〉 |
| 3 | 〈name〉 |
| 4 | 〈name〉 |

### Decision making

〈How do you decide when you disagree — consensus, majority, lead decides
after hearing everyone? And how long may a decision stay open before someone
just calls it?〉

## 2. Workflow

- Branching, PRs, review and CI: [`git-workflow.md`](git-workflow.md).
- Issues, labels, sprints and the board: setup guide §4.
- **Working agreements we set for ourselves** (recommended defaults, not
  course requirements — see setup guide §8): every member
  makes at least **2 merged contributions per sprint**; pull requests stay
  under **10 files / 500 lines** except by agreement; and we treat
  **unmerged work as unfinished** — if it is not merged by the sprint
  boundary it carries over.

## 3. Use of AI and LLMs

〈How will this team use assistants — for which parts of the proposal, the
documents, and the prototype? Which rules will you hold each other to beyond
the course minimum?〉

The course rules are in [`aidlc/hitl-gates.md`](aidlc/hitl-gates.md); the
prompts are in [`aidlc/prompt-library.md`](aidlc/prompt-library.md). Every
deliverable carries a disclosure, and every PR says what was verified.

〈Name your team's own additions, e.g. "nobody merges generated code they
cannot explain in the sprint meeting"; "the reviewer always spot-checks two
facts".〉

## 4. Risk register

Review and update at every sprint boundary. Likelihood and impact: H / M / L.

| # | Risk | L | I | Early warning sign | What we will do about it | Owner |
|---|---|---|---|---|---|---|
| R1 | 〈sponsor data arrives late〉 | 〈M〉 | 〈H〉 | 〈no reply to two emails〉 | 〈build against synthetic data; ask at the project meeting〉 | 〈name〉 |
| R2 | 〈the chosen framework cannot do X〉 | 〈L〉 | 〈H〉 | 〈spike does not work in one day〉 | 〈prototype the risky part first — that is what v0 is for〉 | 〈name〉 |
| R3 | 〈a member drops the course〉 | 〈L〉 | 〈H〉 | 〈missed meetings, per the charter triggers〉 | 〈re-scope to the objectives, tell the instructor early〉 | 〈name〉 |
| R4 | 〈…〉 | | | | | |

〈Risks whose early warning sign has already appeared are not risks any more —
they are problems. Move them to an issue.〉

## 5. Technology and environment

〈Languages, frameworks, services, accounts needed, and who owns each setup.
The detail belongs in the proposal §4; this is the working list.〉

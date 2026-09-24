# Review checklists

Reviewing is real work in this course, not a favour. These are the lists you
review *against* — name the items you actually checked in your PR review, the
way the pull-request template asks. (No separate grade attaches to these
checklists; the syllabus governs grades. They exist because a review that
names what it checked is worth something to the author, and a "LGTM" is not.)

Why it matters: across capstone research, how *often* teams performed agile
ceremonies did not separate high from low performers — only how *deeply* they
used them did. A review that says "LGTM" is a ceremony. A review that says
"checked C3, C5 and D2; C5 fails because the diagram still shows the old
service" is depth.

---

## Code review (C)

- [ ] **C1** The change satisfies the linked story's acceptance criteria **as
      written** — I opened the issue and compared, not the PR summary.
- [ ] **C2** Nothing outside the story's scope changed (no drive-by
      refactors, reformatting, or dependency bumps).
- [ ] **C3** No test was weakened, skipped or deleted; if a test file changed
      in an implementation PR, the body explains why.
- [ ] **C4** Each new test would **fail if the bug were reintroduced** — it
      asserts behaviour, not mocks.
- [ ] **C5** Every import, API call and file path referenced actually exists
      in the versions we pin (I checked the two most load-bearing).
- [ ] **C6** No credential, key or token is committed (and any
      `allowlist secret` marker is genuinely a fixture).
- [ ] **C7** I can explain what this code does; if I cannot, I asked rather
      than approving.
- [ ] **C8** The PR is reviewable: under ~10 files and ~500 lines, or split.

## Specification review (S)

- [ ] **S1** Names its epic and stories in the first lines.
- [ ] **S2** Every requirement is written so it can become a test ("when …,
      the system shall …") — no requirement that cannot fail.
- [ ] **S3** **Out of scope** is stated explicitly, not left implied.
- [ ] **S4** Requirements trace to the objectives in the proposal §2; nothing
      here serves a goal we never stated.
- [ ] **S5** Non-functional requirements say *why* each one exists.
- [ ] **S6** Open questions are recorded as open, not silently answered.
- [ ] **S7** No invented requirement IDs, numbers, or sponsor statements.

## Design review (D)

- [ ] **D1** Names its epic and stories; links its specification.
- [ ] **D2** Contains at least one diagram, and the diagram matches the
      prose (when they disagree, the diagram is usually stale).
- [ ] **D3** **Every box is something that exists or that we have decided to
      build**; every arrow is a real call or data movement.
- [ ] **D4** Entities and attributes match our actual or intended schema —
      not a generic textbook model.
- [ ] **D5** Key decisions record the options considered and why one won.
- [ ] **D6** What is *not* designed yet is stated.
- [ ] **D7** Figures are numbered, captioned, and referenced from the text.

## Writing review (W)

- [ ] **W1** A reader with a CS degree but no knowledge of this area can
      follow it.
- [ ] **W2** Claims are supported: citations exist, and someone on the team
      has actually read them.
- [ ] **W3** No placeholder brackets, TODOs, or half-finished sections.
- [ ] **W4** Section headings and numbering match the course template.
- [ ] **W5** It reads as one document, not as four voices stitched together.

## Getting-started review (G) — run this once, on someone else's machine

- [ ] **G1** `git clone`, then the README's steps, and the prototype runs —
      on a machine that has never seen this project.
- [ ] **G2** `python .github/scripts/check_repo.py` is green.
- [ ] **G3** The prototype's tests run and pass.
- [ ] **G4** Nothing required is missing from the instructions (no "oh, you
      also need…" moments).

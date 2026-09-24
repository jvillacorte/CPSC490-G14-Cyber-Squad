# Git workflow — Gitflow + CI/CD with GitHub Actions

Standard **Gitflow** (Driessen model), mapped onto this course's four
sprints, with GitHub Actions as the gate. Read this once as a team before
Sprint 1 and follow it for the rest of 490 and all of 491.

---

## 1. The branches

| Branch | Lives | Holds | Who merges into it |
|---|---|---|---|
| `main` | forever | **released** work only — what you showed the sponsor / submitted | release and hotfix branches |
| `develop` | forever | the **integration** branch — everything finished but not yet released | feature branches |
| `feature/<issue>-<slug>` | days | one story or task | you, from `develop` |
| `release/<version>` | days | stabilizing a deliverable (report draft, demo build) | cut from `develop` |
| `hotfix/<version>` | hours | urgent fix to something already released | cut from `main` |

```
main     ──●─────────────────●────────────●──────▶   tags: v0.1, v0.2, …
            \               /            /
release      \        ●───●─ release/0.1 /  (stabilize, no new scope)
              \      /                  /
develop  ──●───●────●──────●───────●───●─────────▶   integration
             \     /        \     /
feature       ●───●          ●───●                   feature/12-login-spec
```

**Naming.** Always lead with the issue number so the branch, the issue, and
the PR are one trail: `feature/12-login-spec`, `feature/27-prototype-auth`,
`hotfix/0.1.1-broken-link`. Versions are `MAJOR.MINOR.PATCH` (semver):
`v0.1` = proposal + prototype v0 (Sep 27), `v0.2` = the Week-8 demo build,
`v0.3` = report draft #1, `v1.0` = final submission.

> **Note on this example repository.** It ships with `main` only, because it
> is a template you copy — a second identical branch here would just be
> noise. **Your** repository needs `develop`, and
> `bash scripts/bootstrap.sh` creates and protects it for you (QUICKSTART
> step 4).

## 2. The everyday loop (feature → develop)

```bash
git switch develop && git pull                 # always start current
git switch -c feature/12-login-spec            # branch per issue
# ... work in small commits ...
git push -u origin feature/12-login-spec
gh pr create --base develop --fill             # or the GitHub web UI
```

Then: **CI must be green** and **a teammate who is not the author must
approve**. Merge with *squash* so `develop` keeps one clean commit per
story, then delete the branch. Closing the PR with `Closes #12` in its body
closes the story automatically.

Rules that keep this sane:
- One story per branch. If you find unrelated work, file an issue and branch
  again — do not smuggle it in.
- Rebase (or merge `develop` in) before asking for review, so the reviewer
  sees your change and not someone else's conflict.
- Never commit straight to `develop` or `main`. Branch protection will
  refuse it anyway.

## 3. Releasing a deliverable (develop → release → main)

Cut a release branch when a course deliverable is due:

```bash
git switch develop && git pull
git switch -c release/0.2
# only stabilization here: fixes, formatting, version bump, report polish
gh pr create --base main --title "Release 0.2 — Week-8 demo build"
# after approval + green CI and merge:
git tag -a v0.2 -m "Week-8 demo build" && git push origin v0.2
git switch develop && git merge --no-ff main   # carry the fixes back
```

**No new scope on a release branch.** New ideas go back to `develop` as
issues for the next sprint. The release branch exists so one person can
polish while everyone else keeps working.

## 4. Hotfix (main → hotfix → main + develop)

Something you already submitted or demoed is broken:

```bash
git switch main && git pull
git switch -c hotfix/0.2.1-dead-links
# smallest possible fix
gh pr create --base main --title "Hotfix 0.2.1 — repair dead spec links"
# merge, tag v0.2.1, then merge main back into develop
```

A hotfix that takes more than a day is not a hotfix — it is a story.

## 5. CI/CD with GitHub Actions

`.github/workflows/ci.yml` runs on every PR into `main`, `develop`,
`release/*`, `hotfix/*` and on every push to `develop`/`main`. Three jobs,
each a gate you can reason about:

| Job | What it does | What it catches |
|---|---|---|
| **harness** | runs `.github/scripts/check_repo.py` — every gate | template drift, orphan documents, invented issue numbers, dead links, committed secrets |
| **prototype** | installs and tests `prototype/` (Node or Python, auto-detected) | code that looks right but does not run; missing tests |
| **pr-discipline** | reads the PR body | PRs with no linked story, no AI disclosure, no statement of what was verified |

Run the same harness locally *before* you push — that is the whole point of
a harness:

```bash
python .github/scripts/check_repo.py          # seconds, no install
```

**CD in this course** means publishing the deliverable, not deploying a
service: tag the release on `main`, attach the built artifact (report PDF,
demo build) to a GitHub Release, and note the tag in your sprint review. If
your prototype does deploy somewhere (Pages, a container, a cloud function),
add a second workflow triggered on `push: tags: ['v*']` so only tagged,
reviewed, green code can ever ship.

## 6. Branch protection (leader sets this once)

*Settings → Branches → Add branch ruleset* (or classic protection) for
`main` **and** `develop`:

- ✅ Require a pull request before merging
- ✅ Require approvals: **1** — GitHub will not let you approve your own PR,
  so this is what guarantees a second pair of human eyes
- ✅ Dismiss stale approvals when new commits are pushed
- ✅ Require status checks to pass: `Repository harness`,
  `Prototype build & tests`, `PR links an issue and discloses AI use`
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ❌ Do **not** allow force pushes or deletions

Everything above is deliberate: it is what makes "human in the loop"
structural instead of a promise. An AI can write the whole change — but it
cannot approve it, and it cannot merge past a red harness.

> **Plan caveat, verified the hard way.** GitHub does **not** allow branch
> protection on a **private** repository on the free plan — `bootstrap.sh`
> will tell you so rather than pretending it worked. Either make the
> repository **public**, or activate **GitHub Pro/Team free via
> [GitHub Education](https://education.github.com)** and re-run the script.
> Without one of those, the merge rule is honour-based: you still open pull
> requests and still get a non-author approval, but nothing stops a merge.

## 7. Commit provenance for AI-assisted work

Add a trailer to any commit an assistant helped write:

```
fix: correct token refresh on session timeout

The refresh call used the expired token, so the retry failed too.

Assisted-by: Claude (claude-sonnet-4.6)
```

`Assisted-by:` is the convention most open-source projects have converged on
(the Linux kernel, Fedora and LLVM among them). There is no industry-wide
standard yet, so **this course uses `Assisted-by:`**. Never add
`Signed-off-by` on a model's behalf — sign-off is a statement of human
accountability, and accountability does not transfer to a tool.

## 8. Quick reference

```bash
git switch develop && git pull                     # start clean
git switch -c feature/<issue>-<slug>               # new work
python .github/scripts/check_repo.py               # local gate
git push -u origin HEAD && gh pr create --base develop
# green CI + 1 approval → squash merge → branch deleted
```

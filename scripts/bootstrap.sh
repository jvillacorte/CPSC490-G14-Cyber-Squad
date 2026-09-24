#!/usr/bin/env bash
# CPSC 490 — one-command repository setup.
#
# Creates everything QUICKSTART step 4 asks for: labels, Sprint 1-4
# milestones, the develop branch, branch protection on main and develop, and
# a project board with its Status columns.
#
# Run it ONCE, from inside your own repository:
#
#     bash scripts/bootstrap.sh
#
# Requirements:
#   - GitHub CLI installed      https://cli.github.com   (winget install GitHub.cli)
#   - Signed in with project scope:
#         gh auth login
#         gh auth refresh -s project,repo
#
# Safe to re-run: every step checks for what already exists and skips it.
set -uo pipefail

ok()   { printf '  \033[32mok\033[0m    %s\n' "$*"; }
skip() { printf '  --    %s (already there)\n' "$*"; }
warn() { printf '  \033[33mwarn\033[0m  %s\n' "$*"; }
die()  { printf '\n\033[31mstopped:\033[0m %s\n' "$*" >&2; exit 1; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ---------------------------------------------------------------- preflight
step "Checking your setup"
command -v gh >/dev/null || die "GitHub CLI not found. Install it: https://cli.github.com"
# Check that the API actually works rather than the exit code of
# 'gh auth status' - that command also fails for a merely missing optional
# scope, which would stop a setup that would otherwise work fine.
WHOAMI=$(gh api user -q .login 2>/dev/null)   || die "Not signed in (or the token cannot reach the API). Run: gh auth login"
git rev-parse --git-dir >/dev/null 2>&1 || die "Run this from inside your repository."
ok "signed in as $WHOAMI"

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null) \
  || die "Could not identify the repository. Is 'origin' set to your GitHub repo?"
OWNER=${REPO%%/*}
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
ok "repository: $REPO (default branch: $DEFAULT_BRANCH)"

AUTH_OUT=$(gh auth status 2>&1 || true)
if grep -q "'project'" <<<"$AUTH_OUT"; then
  HAVE_PROJECT_SCOPE=1; ok "token has 'project' scope"
else
  HAVE_PROJECT_SCOPE=0
  warn "token lacks 'project' scope — the board step will be skipped."
  warn "to include it:  gh auth refresh -s project,repo   then re-run"
fi

# ---------------------------------------------------------------- labels
step "Creating labels"
add_label() {  # name, colour, description
  if gh label list --repo "$REPO" --limit 100 --json name -q '.[].name' | grep -qxF "$1"; then
    skip "label $1"
  else
    gh label create "$1" --repo "$REPO" --color "$2" --description "$3" >/dev/null 2>&1 \
      && ok "label $1" || warn "label $1 could not be created"
  fi
}
add_label "epic"              "5319e7" "A project goal from Goals & Objectives"
add_label "user-story"        "1d76db" "An objective under a goal"
add_label "feature"           "0052cc" "New capability delivering a user story"
add_label "enhancement"       "a2eeef" "Improvement to something that already works"
add_label "bug"               "d73a4a" "Built behavior does not match the specification"
add_label "task"              "bfdadc" "Concrete unit of work under a story/feature"
add_label "sub-task"          "d4e5f7" "Breakdown of a task; smallest tracked unit"
add_label "priority: high"    "d93f0b" ""
add_label "priority: medium"  "fbca04" ""
add_label "priority: low"     "0e8a16" ""
for sp in 1 2 3 5; do add_label "sp: $sp" "ededed" "story points"; done
add_label "sp: 8"             "ededed" "story points - too big, split it"

# ---------------------------------------------------------------- milestones
step "Creating Sprint 1-4 milestones"
EXISTING_MS=$(gh api "repos/$REPO/milestones?state=all&per_page=100" -q '.[].title' 2>/dev/null)
add_milestone() {  # title, due (YYYY-MM-DD), description
  if grep -qxF "$1" <<<"$EXISTING_MS"; then skip "milestone $1"; return; fi
  gh api -X POST "repos/$REPO/milestones" -f title="$1" -f due_on="${2}T06:59:00Z" \
    -f description="$3" >/dev/null 2>&1 && ok "milestone $1 (due $2)" \
    || warn "milestone $1 could not be created"
}
add_milestone "Sprint 1" "2026-10-11" "Sep 28 - Oct 11 - board running, specs started, prototype demo path"
add_milestone "Sprint 2" "2026-10-25" "Oct 12 - Oct 25 - specs per epic, prototype reworked from check feedback"
add_milestone "Sprint 3" "2026-11-08" "Oct 26 - Nov 8 - design docs with diagrams (report draft #1 Nov 1)"
add_milestone "Sprint 4" "2026-11-22" "Nov 9 - Nov 22 - integration, prototype stable (report draft #2 Nov 29)"

# ---------------------------------------------------------------- develop
step "Creating the develop branch"
if gh api "repos/$REPO/branches/develop" >/dev/null 2>&1; then
  skip "branch develop"
else
  SHA=$(gh api "repos/$REPO/git/ref/heads/$DEFAULT_BRANCH" -q .object.sha)
  gh api -X POST "repos/$REPO/git/refs" -f ref="refs/heads/develop" -f sha="$SHA" \
    >/dev/null 2>&1 && ok "branch develop" || warn "develop could not be created"
fi

# ---------------------------------------------------------------- protection
step "Protecting $DEFAULT_BRANCH and develop"
PROTECT_JSON=$(mktemp)
cat > "$PROTECT_JSON" <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Repository harness", "Prototype build & tests", "PR links an issue and discloses AI use"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

protect() {
  if gh api -X PUT "repos/$REPO/branches/$1/protection" --input "$PROTECT_JSON" >/dev/null 2>&1; then
    ok "protected $1 (1 approval + 3 required checks)"
  else
    warn "could not protect $1 - GitHub does not allow branch protection on a PRIVATE repo on the free plan."
    warn "  Pick one: make the repository PUBLIC, or get GitHub Pro/Team free through"
    warn "  GitHub Education (https://education.github.com), then re-run this script."
    warn "  Until then the review rule is honour-based: still open PRs, still get a"
    warn "  non-author approval - it just is not enforced by the platform."
  fi
}
protect "$DEFAULT_BRANCH"
gh api "repos/$REPO/branches/develop" >/dev/null 2>&1 && protect develop

# ---------------------------------------------------------------- board
step "Creating the project board"
if [ "$HAVE_PROJECT_SCOPE" -eq 0 ]; then
  warn "skipped (no project scope). Create it by hand per QUICKSTART step 4, or run:"
  warn "  gh auth refresh -s project,repo && bash scripts/bootstrap.sh"
else
  TITLE="${REPO##*/}"
  # GraphQL rather than 'gh project list': the CLI's --owner flag needs the
  # read:org scope even for a personal account, and otherwise fails with
  # "unknown owner type".
  OWNER_ID=$(gh api graphql -f query="{ user(login: \"$OWNER\") { id } }" -q .data.user.id 2>/dev/null)
  EXISTING=$(gh api graphql -f query="{ user(login: \"$OWNER\") { projectsV2(first: 50) { nodes { id title url } } } }" 2>/dev/null)
  PID=$(jq -r --arg t "$TITLE" '.data.user.projectsV2.nodes[]? | select(.title==$t) | .id' <<<"$EXISTING" | head -1)
  BOARD_URL=$(jq -r --arg t "$TITLE" '.data.user.projectsV2.nodes[]? | select(.title==$t) | .url' <<<"$EXISTING" | head -1)

  if [ -n "${PID:-}" ]; then
    skip "board $TITLE"
  elif [ -n "${OWNER_ID:-}" ]; then
    CREATED=$(gh api graphql -f query="mutation { createProjectV2(input: {ownerId: \"$OWNER_ID\", title: \"$TITLE\"}) { projectV2 { id url } } }" 2>/dev/null)
    PID=$(jq -r '.data.createProjectV2.projectV2.id // empty' <<<"$CREATED")
    BOARD_URL=$(jq -r '.data.createProjectV2.projectV2.url // empty' <<<"$CREATED")
    if [ -n "$PID" ]; then ok "board $TITLE"; else warn "board could not be created"; fi
  else
    warn "could not resolve the owner account for the board"
  fi

  if [ -n "${PID:-}" ]; then
    FIELDS=$(gh api graphql -f query="{ node(id: \"$PID\") { ... on ProjectV2 { fields(first: 30) { nodes { ... on ProjectV2FieldCommon { id name } } } } } }" 2>/dev/null)
    field_id() { jq -r --arg n "$1" '.data.node.fields.nodes[]? | select(.name==$n) | .id' <<<"$FIELDS" | head -1; }

    SF=$(field_id "Status")
    WANT="Backlog Sprint To-Do In Progress In Review Done"
    HAVE=$(gh api graphql -f query="{ node(id: \"$PID\") { ... on ProjectV2 { fields(first: 30) { nodes { ... on ProjectV2SingleSelectField { name options { name } } } } } } }" 2>/dev/null            | jq -r '[.data.node.fields.nodes[]? | select(.name=="Status") | .options[]?.name] | join(" ")')
    if [ -z "$SF" ]; then
      warn "no Status field on the board"
    elif [ "$HAVE" = "$WANT" ]; then
      skip "Status columns"
    else
      # Replacing the options assigns NEW option ids, which clears the Status
      # of every card already on the board - so only do it when they differ.
      gh api graphql -f query="mutation { updateProjectV2Field(input: {fieldId: \"$SF\", singleSelectOptions: [{name: \"Backlog\", color: GRAY, description: \"\"}, {name: \"Sprint To-Do\", color: BLUE, description: \"\"}, {name: \"In Progress\", color: YELLOW, description: \"\"}, {name: \"In Review\", color: ORANGE, description: \"\"}, {name: \"Done\", color: GREEN, description: \"\"}]}) { projectV2Field { ... on ProjectV2SingleSelectField { id } } } }" >/dev/null 2>&1         && ok "Status columns: Backlog / Sprint To-Do / In Progress / In Review / Done"         || warn "could not set the Status columns"
      ITEMS=$(gh api graphql -f query="{ node(id: \"$PID\") { ... on ProjectV2 { items(first: 1) { totalCount } } } }"               -q '.data.node.items.totalCount' 2>/dev/null)
      if [ -n "$HAVE" ] && [ "${ITEMS:-0}" -gt 0 ]; then
        warn "cards already on the board lost their Status (option ids changed) - re-set them once"
      fi
    fi

  fi
fi

# ---------------------------------------------------------------- summary
step "Done. What is left for you:"
cat <<EOS
  1. Put your team into README.md (start from README_TEMPLATE.md) and fill in
     CLAUDE.md.
  2. Paste your board URL into README.md${BOARD_URL:+   ->  $BOARD_URL}
  3. Add every teammate AND 'kyoungshin' under Settings -> Collaborators.
  4. File your goals as 'epic' issues and objectives as 'user-story' issues,
     each with assignee, milestone and priority. Story points go on the
     user stories only - not on epics, not on a story's own tasks.
  5. Run the harness before your first push:
        python .github/scripts/check_repo.py

  Full walkthrough: QUICKSTART.md      Reference: README.md
EOS

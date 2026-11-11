#!/usr/bin/env bash
# CPSC 490 — bring the latest course files into your repository.
#
# The course repository (kyoungshin/CPSC490) keeps improving: examples, the
# Word export, issue templates, the harness, the guides. Run this from inside
# your own repository, on an up-to-date develop, whenever you want them:
#
#     git switch develop && git pull
#     bash scripts/update-course-files.sh
#
# What it does:
#   - downloads the course repository's main branch (the same files the
#     QUICKSTART copy gave you; course-only pages stay out);
#   - updates every course file you have NOT edited, and adds new ones;
#   - never touches a file you edited: it lists those so you can compare;
#   - never touches your README.md: the course guide arrives as
#     COURSE_README.md instead;
#   - never brings back the example spec/design you deleted, the prototype
#     starter, or the sprint-review template;
#   - commits the result on a new branch, course-update-YYYY-MM-DD, and
#     prints the issue + pull request steps. Nothing is pushed.
#
# Safe to re-run: when nothing changed upstream it says so and stops.
set -uo pipefail

COURSE_URL=https://github.com/kyoungshin/CPSC490.git
REF=refs/course/main

ok()   { printf '  \033[32mok\033[0m    %s\n' "$*"; }
warn() { printf '  \033[33mwarn\033[0m  %s\n' "$*"; }
die()  { printf '\n\033[31mstopped:\033[0m %s\n' "$*" >&2; exit 1; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ---------------------------------------------------------------- preflight
step "Checking your repository"
git rev-parse --git-dir >/dev/null 2>&1 || die "Run this from inside your repository."
cd "$(git rev-parse --show-toplevel)" || die "Could not find the repository root."
[ -z "$(git status --porcelain)" ] || die "You have uncommitted changes. Commit or stash them first."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
[ "$BRANCH" = develop ] || warn "you are on '$BRANCH', not develop; the update branch starts from here."
NEW="course-update-$(date +%Y-%m-%d)"
git show-ref --verify --quiet "refs/heads/$NEW" \
  && die "Branch $NEW already exists. Push it and open its pull request (or delete it: git branch -D $NEW), then re-run."
ok "on $BRANCH, working tree clean"

# ---------------------------------------------------------------- download
step "Downloading the latest course files"
git fetch --quiet --no-tags "$COURSE_URL" "+main:$REF" || die "Could not download $COURSE_URL"
ok "course main is $(git rev-parse --short "$REF")"
TMP=$(mktemp -d) || die "Could not make a temporary folder."
trap 'rm -rf "$TMP"' EXIT
git archive "$REF" | tar -x -C "$TMP" || die "Could not unpack the course files."

# Files you own: never added back when missing (README.md is handled below).
no_readd() {
  case "$1" in
    prototype/*|docs/sprint-reviews/*) return 0 ;;
    docs/specs/example-spec.md|docs/design/example-design.md) return 0 ;;
  esac
  return 1
}

# True when your copy of $2 is byte-for-byte some past version of course file $1.
unedited() {
  local mine; mine=$(git hash-object -- "$2") || return 1
  git log --no-abbrev --format= --raw "$REF" -- "$1" | awk '{print $4}' | grep -qxF "$mine"
}

# ---------------------------------------------------------------- update
step "Updating course files"
updated=() added=() kept=()
while IFS= read -r -d '' f; do
  src=${f#./}
  dest=$src
  [ "$src" = README.md ] && dest=COURSE_README.md
  if [ -e "$dest" ]; then
    if cmp -s "$TMP/$src" "$dest"; then
      # same as the course's, but maybe never committed (git-ignored)
      git ls-files --error-unmatch -- "$dest" >/dev/null 2>&1 || added+=("$dest")
      continue
    fi
    if unedited "$src" "$dest"; then
      cp "$TMP/$src" "$dest" && updated+=("$dest")
    else
      kept+=("$dest")
    fi
  else
    no_readd "$src" && continue
    mkdir -p "$(dirname "$dest")" && cp "$TMP/$src" "$dest" && added+=("$dest")
  fi
done < <(cd "$TMP" && find . -type f -print0)

for f in "${updated[@]}"; do ok "updated  $f"; done
for f in "${added[@]}";   do ok "added    $f"; done
for f in "${kept[@]}";    do warn "yours, left alone: $f   (compare: git diff $REF:${f/#COURSE_README.md/README.md} -- $f)"; done

changed=("${updated[@]}" "${added[@]}")
if [ ${#changed[@]} -eq 0 ]; then
  step "Already up to date with the course repository."
  exit 0
fi

# ---------------------------------------------------------------- commit
step "Committing on a new branch"
if ! git switch --quiet -c "$NEW"; then
  git checkout --quiet -- .; rm -f -- "${added[@]}"
  die "Could not create branch $NEW. Nothing was changed."
fi
undo() {
  git reset --quiet --hard; rm -f -- "${added[@]}"
  git switch --quiet - && git branch --quiet -D "$NEW"
  die "$1 Nothing was changed."
}
# -f: course files are meant to be tracked even if your .gitignore would skip
# them (e.g. proposal/reference.docx under a proposal/*.docx rule).
git add -f -- "${changed[@]}" || undo "git add failed."
git commit --quiet -m "chore: latest course files from kyoungshin/CPSC490 $(git rev-parse --short "$REF")" \
  || undo "git commit failed."
ok "committed ${#changed[@]} file(s) on $NEW"

cat <<EOF

Next (the usual document-first flow):
  1. Open an issue: "Update course files to CPSC490 $(git rev-parse --short "$REF")".
  2. git push -u origin $NEW
  3. Open a pull request into develop whose body says "Closes #<that issue>"
     and has an "## AI use" section ("None" is fine).
EOF

#!/usr/bin/env python3
"""CPSC 490 repository harness — the automated gates that check AI (and human)
output before a pull request can merge.

Each gate below exists because of a specific, observed LLM failure mode. Read
`docs/aidlc/hitl-gates.md` for the why; this file is the what.

    python .github/scripts/check_repo.py            # run all gates
    python .github/scripts/check_repo.py --strict   # warnings fail too

Standard library only, so it runs anywhere with Python 3.9+ and needs no
install step. GITHUB_TOKEN (provided automatically in Actions) enables the
issue-existence check; without it that gate is skipped, not failed.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# The sections of the CPSC 490 proposal template, with the template's own
# numbering (0 Abstract; 1 Introduction with 1.1-1.2; 2 onward). Headings in
# proposal.md must match these so the document converts into the Word
# template for Canvas submission.
REQUIRED_PROPOSAL_SECTIONS = [
    ("0", "Abstract"),
    ("1", "Introduction"),
    ("1.1", "Related Work"),
    ("1.2", "Problem Statements"),
    ("2", "Goals and Objectives"),
    ("3", "Proposed Approaches"),
    ("4", "Required Environment, Resources, and Planned Activities"),
    ("5", "Project Outcomes"),
    ("6", "Project Timeline"),
    ("7", "AI Usage"),
    ("8", "References"),
]

# Files that are meant to contain 〈placeholders〉 — templates and examples.
TEMPLATE_GLOBS = [
    "README_TEMPLATE.md",
    "CLAUDE.md",                     # copy-and-edit template
    ".github/**/*.md",
    "docs/aidlc/*.md",               # course reference material
    "docs/**/example-*.md",
    "docs/sprint-reviews/sprint-*.md",
    "proposal/proposal.md",
]

SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{50,}", "GitHub fine-grained token"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style secret key"),
    (r"sk-ant-[A-Za-z0-9\-_]{20,}", "Anthropic API key"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API key"),
    (r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----", "private key block"),
    (r"(?i)(password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", "hardcoded credential"),
]

# Fenced code blocks: links inside them are documented examples, not links.
FENCE_RE = re.compile('^ {0,3}(?:`{3,}|~{3,}).*?^ {0,3}(?:`{3,}|~{3,})', re.S | re.M)

PLACEHOLDER_PATTERNS = [r"〈[^〉]{0,80}〉", r"\bTODO\b", r"\bFIXME\b", r"(?i)lorem ipsum"]

failures: list[str] = []
warnings: list[str] = []


def fail(gate: str, msg: str) -> None:
    failures.append(f"{gate}: {msg}")


def warn(gate: str, msg: str) -> None:
    warnings.append(f"{gate}: {msg}")


def inventory_issue(gate: str, msg: str) -> None:
    """Inventory gates (G8, G9, G10) are advisory during a sprint and blocking
    on the way to main.

    Rationale: an issue filed mid-sprint that nobody has added to the
    proposal yet should not redden an unrelated pull request - that teaches
    people to resent the harness. But a release must not reach main with the
    document and the board out of step. So: warn on feature -> develop, fail
    on anything -> main (and whenever --strict is passed).
    """
    enforcing = ("--strict" in sys.argv
                 or os.environ.get("GITHUB_BASE_REF") == "main"
                 or os.environ.get("GITHUB_REF") == "refs/heads/main")
    (fail if enforcing else warn)(gate, msg + ("" if enforcing else
                                 "  [advisory now; blocks the merge into main]"))


def md_files() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        out.append(p)
    return sorted(out)


def is_deliverable(path: Path) -> bool:
    """True for files the TEAM authors as project work.

    Course scaffolding — docs/aidlc/, docs/git-workflow.md, README*,
    CLAUDE.md, .github/ — is reference material. It legitimately contains
    example issue numbers and placeholders, so the content gates below would
    otherwise flag the very documents that explain them.
    """
    rel = path.relative_to(ROOT).as_posix()
    if path.name.startswith("example-"):
        return False    # worked examples ship with the scaffold; their issue
                        # numbers belong to the example repo, not to yours
    if rel.startswith(("proposal/", "docs/specs/", "docs/sprint-reviews/")):
        return True
    if rel.startswith("docs/design/"):
        return not path.stem.isupper()   # DIAGRAMS.md is reference material
    return False


def is_template(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return any(rel.match(g) or rel.as_posix().startswith(g.split("**")[0].rstrip("/") + "/")
               and rel.match(g) for g in TEMPLATE_GLOBS) or any(rel.match(g) for g in TEMPLATE_GLOBS)


# ---------------------------------------------------------------- gate 1
def gate_proposal_structure() -> None:
    """G1 — the proposal still follows the course template.

    Catches: the assistant helpfully 'improving' the structure — renaming,
    merging, or dropping template sections. The template is the requirement.
    """
    g = "G1 template-structure"
    p = ROOT / "proposal" / "proposal.md"
    if not p.exists():
        fail(g, "proposal/proposal.md is missing")
        return
    text = p.read_text(encoding="utf-8", errors="replace")
    headings = [re.sub(r"\s+", " ", m.group(1)).strip()
                for m in re.finditer(r"^#{1,3}\s+(.+?)\s*$", text, re.M)]
    lowered = [h.lower() for h in headings]
    found, missing = [], []
    for num, title in REQUIRED_PROPOSAL_SECTIONS:
        accepted = (f"{num} {title}".lower(), f"{num}. {title}".lower())
        if num == "0":   # the Word template leaves Abstract unnumbered
            accepted += (title.lower(),)
        hit = next((h for h in lowered if h in accepted), None)
        if hit is None:
            missing.append(f"{num}. {title}")
        else:
            found.append(lowered.index(hit))
    if missing:
        fail(g, "proposal is missing section(s), numbered exactly as the Word "
                "template does: " + "; ".join(missing))
    if found != sorted(found):
        warn(g, "proposal sections are out of template order")
    if not missing:
        print(f"  {g}: all {len(REQUIRED_PROPOSAL_SECTIONS)} template sections "
              f"present with template numbering")


# ---------------------------------------------------------------- gate 2
def gate_traceability() -> None:
    """G2 — every spec/design document names the issue(s) it serves.

    Catches: orphan documents. An assistant asked to 'write the design doc'
    will happily produce work nobody planned, which then counts for nothing
    at the sprint review.
    """
    g = "G2 traceability"
    docs = [p for p in (ROOT / "docs").rglob("*.md")
            if p.parent.name in ("specs", "design") and is_deliverable(p)
            ] if (ROOT / "docs").exists() else []
    if not docs:
        warn(g, "no specification or design documents of your own yet - the "
                "example-* files that ship with the scaffold are reference, "
                "not deliverables")
        return
    for p in docs:
        head = "\n".join(p.read_text(encoding="utf-8", errors="replace").splitlines()[:8])
        if not re.search(r"#\d+", head):
            fail(g, f"{p.relative_to(ROOT).as_posix()} does not name an issue in its first 8 lines "
                    f"(expected a line like '> Epic: #1 · Stories: #2, #3')")
    print(f"  {g}: checked {len(docs)} document(s)")


# ---------------------------------------------------------------- gate 3
def gate_issue_refs_exist() -> None:
    """G3 — issue numbers cited in documents actually exist.

    Catches: invented issue numbers. Models produce plausible-looking
    references (#42) with no hesitation; a citation that resolves to nothing
    is worse than no citation.
    """
    g = "G3 issue-refs"
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not (repo and token):
        print(f"  {g}: skipped (no GITHUB_REPOSITORY/GITHUB_TOKEN — runs in CI)")
        return
    refs: dict[int, set[str]] = {}
    for p in md_files():
        if not is_deliverable(p):
            continue
        rel = p.relative_to(ROOT).as_posix()
        for m in re.finditer(r"(?<![\w/])#(\d{1,5})\b", p.read_text(encoding="utf-8", errors="replace")):
            refs.setdefault(int(m.group(1)), set()).add(rel)
    if not refs:
        print(f"  {g}: no issue references found")
        return
    bad: list[str] = []
    for num, where in sorted(refs.items()):
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/issues/{num}",
            headers={"Authorization": f"Bearer {token}", "User-Agent": "cpsc490-harness",
                     "Accept": "application/vnd.github+json"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                bad.append(f"#{num} (cited in {', '.join(sorted(where))})")
            else:
                warn(g, f"could not verify #{num}: HTTP {e.code}")
        except Exception as e:  # network trouble must not fail the build
            warn(g, f"could not verify #{num}: {e}")
    for b in bad:
        fail(g, f"cited issue does not exist: {b}")
    print(f"  {g}: verified {len(refs)} distinct issue reference(s)")


# ---------------------------------------------------------------- gate 4
def gate_links() -> None:
    """G4 — relative links point at files that exist.

    Catches: confident references to files the assistant never created, and
    paths that drifted after a rename.
    """
    g = "G4 links"
    broken = 0
    for p in md_files():
        text = p.read_text(encoding="utf-8", errors="replace")
        # strip fenced code blocks: links inside them are examples, not links
        text = re.sub(FENCE_RE, "", text)
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = m.group(1).strip()
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = (p.parent / target.split("#")[0]).resolve()
            if not str(path).startswith(str(ROOT)):
                continue
            if not path.exists():
                fail(g, f"{p.relative_to(ROOT).as_posix()} links to missing '{target}'")
                broken += 1
    if not broken:
        print(f"  {g}: all relative links resolve")


# ---------------------------------------------------------------- gate 5
def gate_secrets() -> None:
    """G5 — no credentials committed.

    Catches: the assistant pasting a working key into an example, and the
    classic 'just hardcode it for now'.
    """
    g = "G5 secrets"
    hits = 0
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT).as_posix()
        if not p.is_file() or rel.startswith((".git/", "node_modules/")):
            continue
        if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".pptx", ".docx", ".xlsx", ".zip"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, text):
                if "check_repo.py" in rel:  # this file lists the patterns
                    continue
                # Explicit, greppable escape hatch for test fixtures and
                # documentation examples. Audit every use with:
                #   grep -rn "allowlist secret" .
                line_no = text.count(chr(10), 0, m.start())
                line = text.splitlines()[line_no]
                if "allowlist secret" in line:
                    continue
                fail(g, f"possible {label} in {rel} (line {text[:m.start()].count(chr(10)) + 1})")
                hits += 1
    if not hits:
        print(f"  {g}: no credential patterns found")


# ---------------------------------------------------------------- gate 6
def gate_placeholders() -> None:
    """G6 — unfilled placeholders (warning).

    Not a hard failure: templates and examples are supposed to have them.
    But a document you claim is finished should not still say 〈…〉 or TODO,
    and reviewers use this list at the review gate.
    """
    g = "G6 placeholders"
    total = 0
    for p in md_files():
        if not is_deliverable(p) or is_template(p):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        n = sum(len(re.findall(pat, text)) for pat in PLACEHOLDER_PATTERNS)
        if n:
            warn(g, f"{p.relative_to(ROOT).as_posix()} has {n} unfilled placeholder(s)/TODO(s)")
            total += n
    if not total:
        print(f"  {g}: no stray placeholders outside templates")


# ---------------------------------------------------------------- gate 7
def gate_diagrams() -> None:
    """G7 - every design document contains a diagram.

    Catches: design-by-prose. A design nobody drew is a design nobody
    checked; structure is the thing readers cannot reconstruct from
    paragraphs. See docs/design/DIAGRAMS.md.
    """
    g = "G7 diagrams"
    d = ROOT / "docs" / "design"
    docs = [p for p in d.glob("*.md") if is_deliverable(p)] if d.exists() else []
    if not docs:
        warn(g, "no design documents of your own yet (expected by Sprint 3; the "
                "shipped example-design.md is reference)")
        return
    for p in docs:
        text = p.read_text(encoding="utf-8", errors="replace")
        has_mermaid = "```mermaid" in text
        has_image = re.search(r"!\[[^\]]*\]\([^)]+\)", text) is not None
        if not (has_mermaid or has_image):
            fail(g, f"{p.relative_to(ROOT).as_posix()} has no diagram - embed a "
                    f"```mermaid block or an exported image (docs/design/DIAGRAMS.md)")
    print(f"  {g}: checked {len(docs)} design document(s)")


# ---------------------------------------------------------------- gate 8
SECTION_FOR_LABEL = {
    # section number in proposal.md -> issue labels that must be linked there
    "2": ("epic", "user-story"),
    "4": ("feature", "enhancement", "bug", "task", "sub-task"),
}
SECTION_TITLE = {"2": "Goals and Objectives",
                 "4": "Required Environment, Resources, and Planned Activities"}


def _proposal_section(text: str, num: str) -> str | None:
    """Return the body of '## <num>. <title>' up to the next '## ' heading."""
    pat = r"^##\s+" + re.escape(num) + r"\.?\s+.*?$(.*?)(?=^##\s|\Z)"
    m = re.search(pat, text, re.M | re.S)
    return m.group(1) if m else None


def gate_activities_linked() -> None:
    """G8 - every issue is linked from the right proposal section.

    Section 2 (Goals and Objectives) carries the epics and user stories -
    the what. Section 4 (Required Environment, Resources, and Planned
    Activities) carries every other work item - feature, enhancement, bug,
    task, sub-task - the how.

    Catches: the board and the document drifting apart. An issue the proposal
    never mentions is work the reader cannot see; a proposal listing work
    nobody filed is fiction.
    """
    g = "G8 activities-linked"
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    prop = ROOT / "proposal" / "proposal.md"
    if not (repo and token):
        print(f"  {g}: skipped (no GITHUB_REPOSITORY/GITHUB_TOKEN - runs in CI)")
        return
    if not prop.exists():
        return  # G1 already reported it
    text = prop.read_text(encoding="utf-8", errors="replace")
    total_links = 0
    unlinked = 0
    for num, labels in SECTION_FOR_LABEL.items():
        section = _proposal_section(text, num)
        if section is None:
            fail(g, f"could not find section {num} ({SECTION_TITLE[num]}) in "
                    f"proposal/proposal.md")
            continue
        if "〈" in section:
            # Still the untouched skeleton (angle-bracket placeholders). Say so
            # once, gently, instead of listing every issue in the repository -
            # a team on day one has not written this section yet.
            warn(g, f"proposal section {num} ({SECTION_TITLE[num]}) is still the "
                    f"skeleton - list your real issue numbers there as you file them")
            continue
        linked = {int(n) for n in re.findall(r"#(\d{1,5})", section)}
        linked |= {int(n) for n in re.findall(r"/issues/(\d{1,5})", section)}
        total_links += len(linked)
        for label in labels:
            url = (f"https://api.github.com/repos/{repo}/issues"
                   f"?state=open&labels={label}&per_page=100")
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {token}", "User-Agent": "cpsc490-harness",
                "Accept": "application/vnd.github+json"})
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    issues = json.load(r)
            except Exception as e:
                warn(g, f"could not list '{label}' issues: {e}")
                continue
            for issue in issues:
                if "pull_request" in issue:
                    continue
                if issue["number"] not in linked:
                    unlinked += 1
                    inventory_issue(g, f'#{issue["number"]} ({label}) '
                                       f'"{issue["title"][:45]}" is not linked from '
                                       f'proposal section {num} ({SECTION_TITLE[num]})')
    if not unlinked:
        print(f"  {g}: {total_links} issue link(s) across sections 2 and 4, "
              f"nothing unlinked")


# ---------------------------------------------------------------- gate 9
def gate_documents_linked() -> None:
    """G9 - every specification and design document is listed in proposal
    section 4 (Required Environment, Resources, and Planned Activities).

    Catches: technical detail that exists but that no reader of the proposal
    can find. Section 4 is the index of the project's specifications and
    designs; a document missing from it is invisible work.
    """
    g = "G9 documents-linked"
    prop = ROOT / "proposal" / "proposal.md"
    if not prop.exists():
        return  # G1 already reported it
    docs = [p for p in (ROOT / "docs").rglob("*.md")
            if p.parent.name in ("specs", "design") and is_deliverable(p)
            ] if (ROOT / "docs").exists() else []
    if not docs:
        warn(g, "nothing to index in section 4 yet - no specification or design "
                "documents of your own")
        return
    section = _proposal_section(prop.read_text(encoding="utf-8", errors="replace"), "4")
    if section is None:
        fail(g, "could not find section 4 in proposal/proposal.md")
        return
    for d in docs:
        rel = d.relative_to(ROOT).as_posix()
        if rel not in section and d.name not in section:
            inventory_issue(g, f"{rel} is not listed in proposal section 4 "
                               f"(Specification and design documents)")
    print(f"  {g}: checked {len(docs)} document(s) against proposal section 4")


# ---------------------------------------------------------------- gate 10
NEEDS_PARENT = ("user-story", "feature", "enhancement", "bug", "task", "sub-task")
# `## Epic` / `## Parent` followed by a #n - the shape the issue templates ask for.
PARENT_HEADING_RE = re.compile(r"^#{2,}\s*(?:epic|parent)\b[^\n]*\n+[^\n]*?#(\d{1,5})",
                               re.I | re.M)


def _gh_json(repo: str, token: str, path: str):
    """One GET against the issues API, parsed. Raises on failure."""
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}{path}",
                                 headers={"Authorization": f"Bearer {token}",
                                          "User-Agent": "cpsc490-harness",
                                          "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def gate_hierarchy() -> None:
    """G10 - the work breakdown is one unbroken chain.

    epic (goal) -> user story (objective) -> feature / enhancement / bug ->
    task / sub-task. The whole point is that a reader can start at a goal in
    proposal section 2 and walk all the way down to the smallest piece of
    work. An item with no parent breaks that walk, and it is usually a sign
    of work nobody traced back to an objective.

    Parents are found by asking every issue for its CHILDREN
    (/issues/N/sub_issues) - GitHub does not put a parent pointer on the
    issue payload - and by the `#n` under a `## Epic` / `## Parent` heading,
    which is what the issue templates ask for.

    Advisory during a sprint, blocking into main, like G8 and G9: an item
    filed mid-sprint that nobody has parented yet should not redden an
    unrelated pull request.
    """
    g = "G10 hierarchy"
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not (repo and token):
        print(f"  {g}: skipped (no GITHUB_REPOSITORY/GITHUB_TOKEN - runs in CI)")
        return
    try:
        issues = [i for i in _gh_json(repo, token, "/issues?state=open&per_page=100")
                  if "pull_request" not in i]
    except Exception as e:
        warn(g, f"could not list issues: {e}")
        return
    if not issues:
        print(f"  {g}: no open issues yet")
        return

    parented = set()
    for i in issues:
        try:
            kids = _gh_json(repo, token,
                            f"/issues/{i['number']}/sub_issues?per_page=100")
        except Exception:
            kids = []               # sub-issues unavailable; body refs still count
        if isinstance(kids, list):
            parented |= {k["number"] for k in kids
                         if isinstance(k, dict) and "number" in k}
        if PARENT_HEADING_RE.search(i.get("body") or ""):
            parented.add(i["number"])

    orphans = 0
    for i in issues:
        labels = [l["name"] for l in i.get("labels", [])]
        if "epic" in labels:
            continue                # an epic is the top of the chain by definition
        kind = next((l for l in NEEDS_PARENT if l in labels), None)
        if kind is None:
            continue                # untyped issue: G8's business, not this gate
        if i["number"] not in parented:
            orphans += 1
            inventory_issue(g, f'#{i["number"]} ({kind}) "{i["title"][:42]}" names no '
                               f"parent - put it under the item it belongs to "
                               f"(epic -> user story -> feature/enhancement/bug -> "
                               f"task/sub-task)")
    if not orphans:
        print(f"  {g}: all {len(issues)} open issue(s) sit on the chain")



def main() -> int:
    strict = "--strict" in sys.argv
    print("CPSC 490 repository harness\n" + "=" * 34)
    for gate in (gate_proposal_structure, gate_traceability, gate_issue_refs_exist,
                 gate_links, gate_secrets, gate_diagrams, gate_activities_linked,
                 gate_documents_linked, gate_hierarchy, gate_placeholders):
        gate()
    print()
    for w in warnings:
        print(f"WARN  {w}")
    for f in failures:
        print(f"FAIL  {f}")
    print()
    if failures or (strict and warnings):
        print(f"HARNESS RED — {len(failures)} failure(s), {len(warnings)} warning(s).")
        print("Fix the cause, re-run, and say in your PR what you verified.")
        return 1
    print(f"HARNESS GREEN — 0 failures, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

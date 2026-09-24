#!/usr/bin/env python3
"""Sprint story-point report — committed vs completed, and your real capacity.

Answers, per sprint, without anyone counting by hand:

  * how many story points the sprint STARTED with (what you committed to),
  * how many it CLOSED with (what actually finished),
  * what carried over, and what scope was added after the sprint began,
  * and, from that history, what an honest commitment for the next sprint is.

    python scripts/sprint_report.py                 # table for humans
    python scripts/sprint_report.py --markdown       # paste into a sprint review
    python scripts/sprint_report.py --sprint 2       # one sprint only

Reads **`sp: N` labels** and **`Sprint N` milestones** through the plain REST
API, so it runs with the token GitHub Actions already gives you — no Projects
permission, no extra setup, no dependencies beyond the standard library.

Needs GITHUB_REPOSITORY and GITHUB_TOKEN (both automatic inside Actions).
Locally:  GITHUB_REPOSITORY=owner/repo GITHUB_TOKEN=$(gh auth token) python scripts/sprint_report.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"
SPRINT_DAYS = 14
SP_LABEL = re.compile(r"^sp:\s*(\d+)$", re.I)
# `- [ ] #12` - the task-list checklist the setup guide uses to make an
# epic name its stories and a story name its tasks.
TASK_CHILD_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s*[^\n]*?#(\d+)", re.M)


def api(path: str) -> list | dict:
    """GET one API path, following pagination."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not (repo and token):
        sys.exit("Set GITHUB_REPOSITORY and GITHUB_TOKEN (both are automatic in Actions).")
    out: list = []
    url = f"{API}/repos/{repo}{path}"
    while url:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "cpsc490-sprint-report",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = json.load(r)
                link = r.headers.get("Link", "")
        except urllib.error.HTTPError as e:
            sys.exit(f"GitHub API {e.code} on {url}: {e.reason}")
        if isinstance(body, dict):
            return body
        out.extend(body)
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if m else None
    return out


def points(issue: dict) -> int:
    """Story points from the issue's `sp: N` label (0 if unpointed)."""
    for lab in issue.get("labels", []):
        m = SP_LABEL.match(lab["name"] if isinstance(lab, dict) else str(lab))
        if m:
            return int(m.group(1))
    return 0


def task_children(body: str | None) -> set:
    """Issue numbers this issue lists as task-list children (`- [ ] #12`)."""
    return {int(n) for n in TASK_CHILD_RE.findall(body or "")}


def sub_issue_children(number: int) -> set:
    """Issue numbers GitHub records as native sub-issues of this issue.

    The "Create sub-issue" button in the GitHub UI makes a real relationship
    rather than a checklist line, so both have to be read or a team using the
    button would double-count without being told. Access can fail harmlessly
    (older API, restricted token); task lists still cover that case.
    """
    try:
        kids = api(f"/issues/{number}/sub_issues?per_page=100")
    except SystemExit:
        return set()
    if not isinstance(kids, list):
        return set()
    return {k["number"] for k in kids if isinstance(k, dict) and "number" in k}


def when(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def milestone_added_at(number: int) -> datetime | None:
    """When this issue was put into its milestone (best effort).

    Used to separate work you committed to at planning from work that
    appeared mid-sprint. Timeline access can fail harmlessly; then we treat
    the issue as committed at planning.
    """
    try:
        events = api(f"/issues/{number}/timeline?per_page=100")
    except SystemExit:
        return None
    stamps = [when(e.get("created_at")) for e in events
              if isinstance(e, dict) and e.get("event") == "milestoned"]
    return max([s for s in stamps if s], default=None)


def collect(only: int | None, trace_scope: bool) -> list[dict]:
    milestones = [m for m in api("/milestones?state=all&per_page=100")
                  if re.match(r"^Sprint \d+$", m["title"])]
    milestones.sort(key=lambda m: int(m["title"].split()[-1]))
    rows = []
    for i, ms in enumerate(milestones):
        num = int(ms["title"].split()[-1])
        if only and num != only:
            continue
        end = when(ms.get("due_on"))
        prev_end = when(milestones[i - 1].get("due_on")) if i else None
        start = prev_end or (end - timedelta(days=SPRINT_DAYS) if end else None)

        issues = [x for x in api(f"/issues?milestone={ms['number']}&state=all&per_page=100")
                  if "pull_request" not in x]

        # Points belong to the item the team COMMITS to the sprint - normally
        # the user story. If a pointed story also has pointed children, a
        # plain sum counts the same work twice, so children of a pointed
        # parent are rolled up into it and reported as a labelling fix.
        # Hierarchy is read BOTH ways teams express it: `- [ ] #12` task
        # lists and GitHub's native sub-issues.
        rolled_up = set()
        for x in issues:
            if points(x) > 0:
                rolled_up |= task_children(x.get("body"))
                rolled_up |= sub_issue_children(x["number"])

        r = {"sprint": num, "title": ms["title"], "start": start, "end": end,
             "committed": 0, "completed": 0, "late": 0, "carried": 0,
             "added_mid": 0, "unpointed": 0, "n": len(issues), "epics": 0,
             "double_pointed": 0}
        for x in issues:
            names = [l["name"] for l in x.get("labels", [])]
            if "epic" in names:          # epics span sprints; not capacity
                r["epics"] += 1
                continue
            p = points(x)
            if p == 0:
                # Only an objective is meant to carry points. A feature, task
                # or sub-task without an `sp:` label is correct, not missing -
                # its parent objective holds the estimate - so saying otherwise
                # would scold every team that followed the rule.
                if "user-story" in names:
                    r["unpointed"] += 1
                continue
            if x["number"] in rolled_up:
                r["double_pointed"] += p     # its parent already carries these
                continue
            mid = False
            if trace_scope and start:
                added = milestone_added_at(x["number"])
                mid = bool(added and added > start)
            if mid:
                r["added_mid"] += p
            else:
                r["committed"] += p
            closed = when(x.get("closed_at"))
            if closed and (end is None or closed <= end):
                r["completed"] += p
            elif closed:
                r["late"] += p
            else:
                r["carried"] += p       # still open: in flight, or carried
                                        # over, depending on whether the
                                        # sprint has ended (see the header)
        rows.append(r)
    return rows


def advise(rows: list[dict]) -> list[str]:
    """Turn the history into a recommendation, honestly hedged."""
    # Labelling problems are reported FIRST and regardless of whether a sprint
    # has ended - a board that measures itself wrongly is worth fixing in week
    # one, not after the sprint it spoiled.
    quality = []
    dbl = sum(r["double_pointed"] for r in rows)
    if dbl:
        quality.append(f"{dbl} point(s) sit on sub-issues whose parent story is "
                       "pointed too. They are counted once, at the parent, so "
                       "these totals are right — but fix the labels: point the "
                       "user story, not its tasks (setup guide §4).")
    unpointed = sum(r["unpointed"] for r in rows)
    if unpointed:
        quality.append(f"{unpointed} user story/stories carry no `sp:` label, so "
                       "they are invisible to this report. Point every objective "
                       "at planning time. (Features, tasks and sub-tasks are "
                       "*meant* to be unpointed - their objective holds the "
                       "estimate.)")

    done = [r for r in rows if r["end"] and r["end"] < datetime.now(timezone.utc)
            and (r["committed"] + r["added_mid"]) > 0]
    if not done:
        return quality + ["No completed sprint yet — after Sprint 1 this section "
                          "will suggest a commitment based on what you actually "
                          "finished."]
    vel = [r["completed"] for r in done]
    avg = sum(vel) / len(vel)
    last3 = vel[-3:]
    lines = [f"Completed per sprint so far: {', '.join(str(v) for v in vel)} "
             f"(average {avg:.1f} points)."]
    if len(vel) >= 2:
        lines.append(f"Recent average (last {len(last3)}): "
                     f"{sum(last3)/len(last3):.1f} points.")
        lines.append(f"**Commit about {round(sum(last3)/len(last3))} points next sprint.** "
                     "Planning much above what you have ever finished is how carry-over "
                     "becomes permanent.")
    else:
        lines.append(f"**One data point only — commit about {round(avg)} points next "
                     "sprint and re-read this after Sprint 2.**")
    for r in done:
        total = r["committed"] + r["added_mid"]
        if total and r["completed"] / total < 0.6:
            lines.append(f"{r['title']}: finished {r['completed']} of {total} points "
                         f"({r['completed']/total:.0%}). Either the stories were too big "
                         "(`sp: 8` means split it) or the commitment was optimistic.")
        if r["added_mid"] > max(3, 0.25 * max(total, 1)):
            lines.append(f"{r['title']}: {r['added_mid']} points were added *after* the "
                         "sprint began. Mid-sprint scope is the usual reason a plan misses.")
    return lines + quality


def main() -> int:
    md = "--markdown" in sys.argv
    trace = "--no-scope-trace" not in sys.argv
    only = None
    if "--sprint" in sys.argv:
        only = int(sys.argv[sys.argv.index("--sprint") + 1])
    rows = collect(only, trace)
    if not rows:
        print("No `Sprint N` milestones found — run scripts/bootstrap.sh first.")
        return 0

    head = ["Sprint", "Window", "Committed", "Added mid", "Completed",
            "Open/carried", "Closed late", "Done %"]
    body = []
    for r in rows:
        total = r["committed"] + r["added_mid"]
        pct = f"{r['completed']/total:.0%}" if total else "—"
        window = (f"{r['start']:%b %d} – {r['end']:%b %d}"
                  if r["start"] and r["end"] else "dates not set")
        body.append([r["title"], window, r["committed"], r["added_mid"],
                     r["completed"], r["carried"], r["late"], pct])

    if md:
        print("### Story points by sprint\n")
        print("| " + " | ".join(head) + " |")
        print("|" + "---|" * len(head))
        for row in body:
            print("| " + " | ".join(str(c) for c in row) + " |")
        print("\n*Open/carried* is work still open: in flight while the sprint "
              "runs, carried over once it has ended.\n")
        print("\n### What this says\n")
        for line in advise(rows):
            print(f"- {line}")
        print("\n<sub>Generated by `scripts/sprint_report.py` from `sp:` labels and "
              "`Sprint N` milestones.</sub>")
    else:
        widths = [max(len(str(x)) for x in [head[i]] + [r[i] for r in body])
                  for i in range(len(head))]
        line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(head))
        print(line)
        print("-" * len(line))
        for row in body:
            print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(row)))
        print()
        for l in advise(rows):
            print("* " + re.sub(r"\*\*", "", l))
    return 0


if __name__ == "__main__":
    sys.exit(main())

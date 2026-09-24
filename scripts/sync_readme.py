#!/usr/bin/env python3
"""Rebuild README.md from the course guide, preserving the author block.

The README is the course setup guide with a repository-specific banner on
top. This script is the single place that assembles it, so an edit to the
banner can never again silently drop the attribution (it did once).
"""
import io
import re
import sys
from pathlib import Path

GUIDE = Path(sys.argv[1] if len(sys.argv) > 1 else
             r"C:/Users/kshin/OneDrive/Documents/CSUF/2026_Fall/CPSC490_Group_Repo_Guide.md")
OUT = Path(__file__).resolve().parents[1] / "README.md"

BANNER = """# CPSC 490 — Group Repository Setup Guide

**Fall 2026 · Prof. Kyoung Shin · Department of Computer Science, CSUF**

Author: **Kyoung Shin** · <kshin@fullerton.edu> · © 2026 — original course
work, **all rights reserved** ([`LICENSE`](LICENSE)). Enrolled CPSC 490/491
students may copy and build on this for their coursework; any other use,
including adoption for another course, needs written permission — just ask.
Instructors: see [`FOR_INSTRUCTORS.md`](FOR_INSTRUCTORS.md).

**Project board (live example): <https://github.com/users/kyoungshin/projects/1>**
· **Field Guide: <https://kyoungshin.github.io/CPSC490/aidlc/AIDLC-Field-Guide.html>**
· **Start here: [`QUICKSTART.md`](QUICKSTART.md)**

> **This repository is itself the example.** It is laid out exactly the way
> your group repository should be — the folders, the issue templates, the
> labels, the `Sprint 1`–`Sprint 4` milestones, the sample issues, the
> runnable `prototype/`, the worked
> [specification](docs/specs/example-spec.md) and
> [design document](docs/design/example-design.md), and the
> [project board](https://github.com/users/kyoungshin/projects/1) — so build
> yours the same way.
>
> `scripts/bootstrap.sh` does the whole labels/milestones/branches/board
> setup in one command, and `scripts/sprint_report.py` measures story points
> committed versus closed each sprint.
>
> **The syllabus governs grades and deadlines.** Repository work is assessed
> under the syllabus's **20% Prototype & repository practice — 5% per
> sprint**, and what earns it is **progress on the proposal and the
> prototype**, evidenced in the repo. This guide adds no requirements of its
> own.

"""

body = io.open(GUIDE, encoding="utf-8").read()
# drop the guide's own title/author/intro preamble; keep from the first rule
m = re.search(r"^---\n\n## 1\.", body, re.M)
if not m:
    sys.exit("guide structure changed: could not find the '## 1.' section")
out = BANNER + body[m.start():]

for required in ("kshin@fullerton.edu", "LICENSE", "QUICKSTART.md",
                 "projects/1", "## 1."):
    if required not in out:
        sys.exit(f"refusing to write README.md: '{required}' missing")

io.open(OUT, "w", encoding="utf-8", newline="\n").write(out)
print(f"README.md rebuilt ({len(out.split())} words) — attribution present")

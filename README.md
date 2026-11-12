# CPSC 490 — Group 14 Cyber Squad

**Project title:** Cyber Sandbox
**Sponsor:** Independent
**Section:** 05 (Thu)

## Team

| Name | GitHub | Role | Leader |
|---|---|---|---|
| Villacorte, Joseph | @jvillacorte | docs lead | ✅ |
| Boynton, Daniel | @danjobo | Developer / Scrum Master | |
| Vanna Nguyen | @NguyenVGH | Frontend Lead | |
| Alex Goodson | @alexgoodson-1991 | Security & Testing Lead | |
| Jake Nellesen | @Jake-P-N | DevOps | |

**Contact person:** Joseph Villacorte — josephvillacorte@gmail.com

## Links

- **Proposal:** [`proposal/proposal.md`](proposal/proposal.md)
- **Project board:** https://github.com/users/jvillacorte/projects/1
- **Specifications:** [`docs/specs/`](docs/specs/) · **Designs:** [`docs/design/`](docs/design/)
- **Prototype:** [`prototype/`](prototype/) — run instructions in its README
- **Sprint reviews:** [`docs/sprint-reviews/`](docs/sprint-reviews/)

## Export the proposal to Word

From the repository root, with GitHub CLI authenticated and Pandoc installed:

```bash
gh issue list --state all --limit 1000 --json number,title > proposal/issues.json
pandoc proposal/proposal.md -o proposal/proposal.docx --reference-doc=proposal/reference.docx --lua-filter=proposal/to-word.lua --resource-path=proposal
```

Refresh `issues.json` before each export so the appendix uses current issue titles. Both generated files are ignored by Git. Check the exported cover, figures, section formatting, and appendix in Word; fill in the cover emails and replace the remaining proposal placeholders before submission.

## Project summary

Cyber Sandbox is a proposed AI-assisted cybersecurity training environment using an in-memory simulated desktop, not a virtual machine. Users will eventually investigate simulated files, processes, logs, and network activity and practice incident response. The current offline prototype supports inspecting and deleting simulated files; AI generation and malware behaviors are not yet implemented. Python, PySide6, and Pydantic support the prototype, while a future LLM integration is intended to provide scenario variation and feedback.

## How we work

- Sprints: four 2-week sprints (`Sprint 1`–`Sprint 4` milestones).
  Sprint boundary ritual every other 〈day〉.
- Every change lands by pull request; **the author never approves their own PR**.
- Every issue carries: assignee (owner), milestone (sprint), `priority:`,
  and a `sp:` story-point label.
- AI tools are used and disclosed — see the proposal's *AI Usage* section.

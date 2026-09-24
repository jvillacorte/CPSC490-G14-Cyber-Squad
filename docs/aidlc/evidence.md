# Appendix — the evidence, and where to read more

Everything the AIDLC documents assert about how LLM-assisted development
actually behaves, with sources. You do not need this to do the work; read it
when you want to know *why* a rule exists, or when you are arguing about
tooling with someone.

Lecture 4 (Benchmarks, Quality and ROI) goes deeper on measurement.

---

## What the research says

**Your sense of speedup is unreliable.** In a randomized trial, 16
experienced open-source developers were about **19% slower** on real tasks in
their own repositories when allowed AI tools — while estimating beforehand
that they would be 24% faster and reporting afterwards that they had been 20%
faster. Small, expert, familiar-code study with early-2025 tooling, so the
effect size does not transfer to you; the *perception gap* is the durable
finding, and it is why this course asks for measured velocity instead of
impressions. (METR, metr.org + arXiv:2507.09089; METR later judged its own
follow-up data unreliable, which is worth knowing too.)

**AI amplifies whatever your process already is.** The 2025 DORA research
found throughput *up* with AI adoption and instability *also* up — more
change failures, more rework. Read that as: discipline matters more, not
less. (dora.dev/insights/balancing-ai-tensions)

**Maintainability is drifting industry-wide.** Across hundreds of millions of
changed lines, duplicated code blocks rose sharply while refactoring fell to a
small fraction of changed lines. The authors attribute it to workflow
incentives — accept the suggestion and move on — rather than to models being
incapable. (GitClear, "The Maintainability Gap")

**Passing your own tests is necessary, not sufficient.** Benchmarks that hold
back hidden tests show frontier models saturating the *visible* tests while
the held-out ones still fail, and the gap grows with the size of the change.
Documented gaming includes returning expected values directly, special-casing
inputs, and deleting failing tests. (SpecBench, arXiv:2605.21384)

**Invented package names are a live supply-chain risk.** A large study of
generated code found roughly a fifth of samples referenced packages that do
not exist, with many hallucinated names recurring across repeated runs —
which makes them registrable by attackers ("slopsquatting"). Frontier models
have improved but not to zero. Check that a dependency exists *and* is the one
you meant. (USENIX Security 2025)

**Generated code is not secure by default.** In one large evaluation about
**45%** of AI-generated samples introduced a common (OWASP Top-10) weakness,
and that rate stayed roughly flat across model generations even as syntactic
correctness rose sharply. (Veracode GenAI Code Security report — vendor-run,
methodology stated)

**Citations are the least trustworthy output.** A peer-reviewed study of
ChatGPT-generated bibliographies found a large share of references
fabricated, and the fakes carry real author names and well-formed DOIs, so
they survive a glance. This is why the course rule is: *you* find the
sources, the assistant helps you synthesize them. (Nature *Scientific
Reports*, s41598-023-41032-5)

**Review is the gate that is actually missing in practice.** In a study of
900k+ AI-generated pull requests, the majority had *no* recorded human review
activity. A matched comparison of agent vs. human PRs found agent PRs merged
at close to human rates **where review did happen**. The gate is what makes
the difference — which is the whole reason this course requires a non-author
approval. (arXiv:2605.02273; arXiv:2509.14745)

---

## Primary sources worth reading yourself

Vendor guidance changes with each model generation, so prefer these over blog
summaries:

- Anthropic, *Claude prompting best practices* —
  platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic, *Claude Code best practices* — code.claude.com/docs/en/best-practices
  (verification loops, explore→plan→code→commit, the named failure patterns,
  context-file include/exclude guidance)
- Anthropic, *Effective context engineering for AI agents* —
  anthropic.com/engineering/effective-context-engineering-for-ai-agents
  ("context rot"; smallest set of high-signal tokens)
- OpenAI, *Prompt engineering guide* and the *GPT-5 / GPT-5.2 prompting
  guides* — developers.openai.com (reference-text grounding, citation
  tactics, the cost of contradictory instructions)
- Google, *Prompt design strategies* — ai.google.dev/gemini-api/docs/prompting-strategies
- GitHub, *Prompt engineering for Copilot Chat* and *repository custom
  instructions* — docs.github.com/en/copilot (including the ~2-page limit on
  instruction files)
- GitHub, *How to review agent pull requests* — github.blog, and
  *Reviewing AI-generated code* — docs.github.com/en/copilot/tutorials/review-ai-generated-code
  (the five red flags and the ten-minute review protocol this course uses)
- Martin Fowler, *Harness engineering* —
  martinfowler.com/articles/harness-engineering.html (the guides/sensors model)
- Addy Osmani, *Agent harness engineering* — addyosmani.com/blog/agent-harness-engineering/
  (the ratcheting principle behind our harness log)
- GitHub, *spec-kit* — github.com/github/spec-kit (EARS-style acceptance
  criteria; spec → plan → tasks)
- Simon Willison, *Using LLMs for code* and *Coding agent tips* —
  simonwillison.net (the clearest practitioner statement of
  human-in-the-loop discipline)
- *AGENTS.md* — agents.md (the cross-tool context-file convention)
- On disclosure: the `Assisted-by:` trailer discussion —
  allthingsopen.org and lwn.net/Articles/1049830/ (and note that no
  industry-wide standard exists yet)

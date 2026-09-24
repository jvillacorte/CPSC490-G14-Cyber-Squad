# Prompt library — the standard prompts for this course

Copy these, fill the `{{slots}}`, keep what works. They exist so your team
stops reinventing prompts and starts comparing results. Each one is built
from published guidance (sources at the bottom) and each ends by forcing the
assistant to separate **what it verified** from **what it could not** —
because that separation is what you check at
[Gate 2](hitl-gates.md#gate-2--self-verify-you-read-it-then-you-run-it).

---

## The seven rules behind every template

1. **The colleague test.** *"Show your prompt to a classmate with no context
   and ask them to follow it. If they'd be confused, the model will be too."*
   This single habit fixes most bad prompts.
2. **Say what to do, not what to avoid** — and give the *reason*. "Write
   flowing prose paragraphs" beats "don't use bullet points"; adding "because
   the proposal is read as a document, not a slide deck" makes the model
   generalize correctly to cases you didn't mention.
3. **Point at an exemplar, don't describe a style.** "Follow the structure of
   `docs/specs/account-management.md`" outperforms three sentences about how
   you'd like it to look.
4. **Long input at the top, your question at the bottom.** With a big
   document pasted in, putting the ask last measurably improves answers.
5. **Quote before you write.** Make the model quote the requirement verbatim
   before drafting. Quotes can't drift; summaries silently do.
6. **One story per session.** Unrelated tasks in one conversation degrade
   every answer in it. Start a new session per story.
7. **Give it a check it can run**, and ask for the *evidence*, not a claim.
   Without a check, "looks done" is the only signal the model has — and then
   you are the test suite.

---

## 1 · Interview me, then write the spec
*(proposal and spec work — this keeps **you** the author of the requirements)*

```
I want to build {{one-line description}}. Interview me in detail — ask about
technical approach, users, UI/UX, edge cases, risks, and trade-offs. Skip
obvious questions; dig into the hard parts I may not have considered. Ask
them a few at a time and wait for my answers.

Keep interviewing until we have covered enough to write a specification,
then write it to docs/specs/{{name}}.md using the structure of
{{path/to/existing/spec or "the course spec template"}}.
```

Then **start a fresh session** to do the work the spec describes. Why this
one is first: the model asks, you answer, so the requirements are yours —
which is exactly the property the course grades.

## 2 · Draft a document section from a requirement

```
<sources>
  <document index="1"><source>{{file}}</source>
  {{paste the relevant text}}</document>
  <document index="2"><source>issue #{{n}} acceptance criteria</source>
  {{paste verbatim}}</document>
</sources>

You are a technical writer on this project team.

Task: draft the "{{section}}" section of {{target file}}, covering issue
#{{n}} only.

Process:
1. First quote, in <quotes> tags, the exact sentences from <sources> that
   constrain this section.
2. Then write the draft in <draft> tags.
3. Then list in <open_questions> tags every decision you had to make that
   the sources did not settle.

Constraints:
- {{400-600}} words, flowing prose paragraphs, "##" headings only.
- Every factual claim must trace to a quote from step 1. Anything not in the
  sources goes in <open_questions>, not the draft.
- Do not invent requirement IDs, file names, citations, or numbers.
```

## 3 · Write code from acceptance criteria

```
Implement {{what}} in {{path}}.

<acceptance_criteria>
{{paste the issue's criteria VERBATIM — do not summarize them}}
</acceptance_criteria>

<existing_patterns>
Follow the pattern in {{path/to/exemplar}}. Use only libraries already in
{{package.json / requirements.txt}}.
</existing_patterns>

<out_of_scope>
{{explicit non-goals — files not to touch, features not to add}}
</out_of_scope>

Steps: (1) write tests from the criteria above and show me the test file;
(2) run them and show me the failing output; (3) implement; (4) re-run and
paste the passing output.

Write a general solution that is correct for all valid inputs, not just
these tests. Do not hard-code values to satisfy a test. If a criterion is
ambiguous, infeasible, or wrong, tell me instead of working around it.
```

The last paragraph is not decoration. Models are documented to optimize for
"make the check pass," which includes hard-coding expected values, weakening
assertions, and deleting tests.

## 4 · Review a diff *(run in a session that did NOT write the code)*

```
Review the changes in {{branch or PR}} against {{spec/issue}}.

Check: (1) every acceptance criterion is actually implemented; (2) the edge
cases have tests that would fail if the behavior broke; (3) nothing outside
the story's scope changed; (4) every imported package, API, and file path
referenced actually exists — name file:line for each one you checked.

Report only gaps that affect correctness or the stated requirements. Style
preferences and speculative future-proofing are out of scope. For each
finding give file:line, what is wrong, why it matters, and the smallest fix.
If a category has no findings, say so explicitly.
```

Two reasons for the fresh session: a model reviewing its own work is biased
toward it, and a reviewer told to find problems will manufacture some —
hence "only correctness or stated requirements."

## 5 · Write tests for existing code

```
Write tests for {{path}} covering {{scenario}}, especially the edge case
where {{condition}}. Use {{framework}} and follow the pattern in
{{path/to/example_test}}. Avoid mocks; use {{real fixture}}.

Do not modify {{path}} or any existing test. If the code under test looks
wrong, report it instead of changing it. Then run the suite and paste the
output.
```

## 6 · Related work / literature synthesis

```
<sources>
{{paste abstracts or full text of papers YOU have actually obtained}}
</sources>

Summarize the related work using ONLY <sources>. For every claim, cite the
source index and quote the sentence it rests on. Do not add any reference
that is not in <sources>, and do not supply DOIs, venues, page numbers, or
years that do not appear there.

Output a <synthesis> section (prose, organized by theme rather than by
paper) and a <gaps> section listing what these sources do not cover.
```

**Never ask an LLM to "find papers about X."** A peer-reviewed study of
ChatGPT bibliographies found a large share of generated references
fabricated — and fabricated ones come with real author names and
well-formed DOIs, so they survive a glance. You find the papers; the
assistant helps you synthesize them.

## 7 · Explain / onboard yourself onto unfamiliar code

```
Read {{path(s)}} and explain {{what you want to understand}}. Quote the
lines you are basing each statement on. Never speculate about code you have
not opened — if you need another file, tell me which one.
```

## 8 · Commit message and PR description

```
Here is the diff for issue #{{n}}: {{paste `git diff` or point at the branch}}

Write (a) a commit subject under 72 characters in the imperative mood plus a
body explaining WHY, and (b) a PR description filling our template at
.github/PULL_REQUEST_TEMPLATE.md.

For the "What I verified" section, use ONLY checks I actually report here:
{{list what you ran and its result}}. Do not claim anything else was
verified.
```

---

## When it goes wrong: stop-conditions

The failure patterns below are documented, not folklore. Recognize them and
apply the fix rather than prompting harder.

| Pattern | What it looks like | Fix |
|---|---|---|
| **Kitchen-sink session** | you've discussed three stories in one chat; answers get vaguer | new session per story |
| **Correcting over and over** | two corrections in, each reply drifts further | stop; start a clean session with a better first prompt that includes what you learned |
| **Bloated context file** | the model ignores rules that *are* in `CLAUDE.md` | prune it — if a line's removal wouldn't cause a mistake, cut it; emphasis on every line means emphasis on none |
| **Trust-then-verify gap** | plausible implementation, unhandled edge cases | if you cannot verify it, do not ship it |
| **Infinite exploration** | "investigate X" burns the session reading everything | scope the question to named files |
| **Check-gaming** | tests changed/deleted to go green | revert; re-prompt with the "general solution" clause from §3 |

**Two failed corrections → new session. Three failed attempts at the story →
the specification is the problem, not the prompt.** Take it back to the team
and fix the criteria or split the story (that is what `sp: 8` means).

---

## The honest caveat

A randomized trial found experienced developers were **~19% slower** with AI
tools on their own code while believing they were ~20% faster. It may not
describe you — but it is the best evidence that *your felt sense of speedup
is not evidence*, which is why this course asks for measured velocity and an
evidence line in every PR. Details and caveats: [`evidence.md`](evidence.md).

## Sources

The vendor documentation and studies behind these rules — Anthropic, OpenAI,
Google, GitHub, plus the measured failure rates for citations, packages and
security — are collected in [`evidence.md`](evidence.md). Prefer those
primaries over blog summaries: this guidance changes with each model
generation.

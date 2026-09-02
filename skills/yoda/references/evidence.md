# Evidence behind yoda's rules

Every rule in `SKILL.md` traces to something measured or specified. Read a row when you need to
justify a rule, defend it under challenge, or decide whether a particular case warrants breaking
it. A rule with a weak source is marked as such — knowing which rules are soft is the point of
this file.

## Contents

- [The 250-character cap](#the-250-character-cap)
- [The description contract is contested](#the-description-contract-is-contested)
- [Position and length](#position-and-length)
- [Simultaneous constraints](#simultaneous-constraints)
- [Net-negative skills and self-assessment](#net-negative-skills-and-self-assessment)
- [Failure rates in the wild](#failure-rates-in-the-wild)
- [Structural rules](#structural-rules)
- [What reading cannot establish](#what-reading-cannot-establish)
- [What the spec does not cover](#what-the-spec-does-not-cover)

---

## The 250-character cap

Claude Code changelog v2.1.86: "Skill descriptions in the `/skills` listing are now capped at
250 characters to reduce context usage." This appears in no documentation page; it is recorded
in `anthropics/claude-code` issue #40121, which also establishes that `SLASH_COMMAND_TOOL_CHAR_BUDGET`
adjusts the *aggregate* metadata budget across skills (dynamically 2% of the context window,
fallback 16,000 characters) and does **not** lift the per-description cap.

The Agent Skills specification permits `description` up to 1024 characters. Both are true: a
description can be spec-valid and still be truncated to under a quarter of its length at the
point where it decides whether the skill loads.

**Confidence: high.** First-party changelog and issue tracker. **Caveat:** it is a version-specific
behavior of one implementation and could change; re-check the changelog if a description that
should fire reliably doesn't.

## The description contract is contested

Two authoritative sources give opposed instructions. Neither has refuted the other, and yoda
does not resolve it — it asks the author to choose deliberately.

**Trigger-only** (obra/superpowers, `anthropic-best-practices.md`): the description states when
to use the skill, in third person, and never summarizes the process. Stated reason, from their
own testing: a description summarizing a workflow becomes a shortcut the model follows *instead
of* reading the body. The reported instance — a description reading "code review between tasks"
produced one review where the skill's flowchart specified two; removing the summary restored the
two-stage behavior.

**Both, and push** (Anthropic, `skill-creator/SKILL.md`): "include both what the skill does AND
specific contexts for when to use it. All 'when to use' info goes here, not in the body." It
further states Claude "has a tendency to 'undertrigger' skills — to not use them when they'd be
useful. To combat this, please make the skill descriptions a little bit 'pushy'," with a worked
example appending "Make sure to use this skill whenever the user mentions dashboards, data
visualization, internal metrics, or wants to display any kind of company data, even if they
don't explicitly ask for a 'dashboard.'"

**Reconciliation (inference, not stated by either source):** they target opposite failures.
Trigger-only optimizes against shortcutting; pushy optimizes against under-triggering. Which
dominates depends on the skill — a rarely-relevant reference skill fails by never firing, a
multi-step discipline skill fails by being summarized away. No source tests both failure modes
against each other, so treat this as a way to choose, not as a finding.

Both agree on: the description is the triggering mechanism, and vagueness is fatal.

## Position and length

**Lost in the Middle** (Liu et al., TACL 2023): across multi-document QA and key-value retrieval,
accuracy is highest when the relevant content sits at the very start or end of the context and
degrades sharply — often toward random — in the middle. The U-shaped curve persists in models
built specifically for long contexts.

**Found in the Middle** supplies the mechanism: a measurable U-shaped *attention* bias, where
start and end tokens receive disproportionate attention regardless of relevance, recoverable by
calibration without retraining. So this is an attention-allocation property, not a quirk of one
benchmark.

Independently, issue #40121 reaches "front-load the most important trigger words" from a pure
truncation argument. Two unrelated lines of reasoning converge on the same authoring rule, which
is the strongest form of support available here.

**Confidence: high for the effect. Medium for the ~500-line body threshold** — that number comes
from Anthropic's `skill-creator` and obra's best-practices as guidance ("under 500 lines ideal"),
not from a measurement of where compliance drops. Treat 500 as a convention with a real mechanism
behind it, not a measured cliff.

## Simultaneous constraints

Per-constraint compliance degrades gradually as instructions accumulate, but satisfying **all**
of them collapses nonlinearly: a model passing individual constraints about 41% of the time
satisfies all eight simultaneous constraints only 5.7% of the time. Reliable compliance breaks
down past roughly five or six for most models tested. Structural constraints — those requiring
sustained tracking across the output — lose about twice as much capability per added constraint
as lexical or binary ones.

This is what turns "keep skills focused" from taste into arithmetic, and it is the argument for
splitting rather than lengthening.

**Confidence: medium-high.** Peer-reviewed measurement, but the specific numbers are model- and
benchmark-dependent; the shape of the curve is the transferable part, not 5.7%.

## Net-negative skills and self-assessment

A controlled three-way experiment — vanilla, a monolithic 8-phase SKILL.md, and modular per-phase
scripts — across three coding tasks. Modular scripts scored 0.92. On the large task the
**monolithic skill scored 0.55 against vanilla's 0.77**, and produced **zero unit tests where
vanilla produced 30**, despite explicitly instructing "write tests."

The author's diagnosis is "attention budget depletion": roughly 2,300 tokens of protocol in one
file buried the testing instruction as "paragraph 12 in a wall of text" — exactly what the
position research predicts.

The second result is the one that matters for verification: **the skill self-scored 0.92 on the
zero-test output.** A skill grading its own compliance reported success on the output that proved
its failure. This is why a paired run is the test and self-assessment is not.

**Confidence: medium.** A single practitioner experiment, not peer-reviewed, n=3 tasks. The
direction is corroborated by the position research; treat the specific scores as illustrative
rather than as effect sizes.

## Failure rates in the wild

A tool-scored audit of 214 community skills: 73% scored below 60/100 on the author's activation
threshold; 68% had vague descriptions with no quoted trigger phrases; 41% had descriptions under
20 words; 55% lacked code examples; 62% were missing version metadata; 12 skill-conflict pairs
were detected. Two skills with 4–5 word descriptions scored 8/100 and 22/100 and reportedly never
fired.

The mechanism it names is the organizing fact for this whole skill: "Claude Code skills fail
silently. A bad `SKILL.md` doesn't throw an error — it just never gets invoked."

**Confidence: low-to-medium, and read the caveat.** The piece is promotional for the author's own
tool, and its "14 weighted criteria" are presented as drawn from Anthropic's documentation. The
*weights* (description length 20%, trigger phrases 25%, body 15%…) are the tool author's design;
no Anthropic document publishes weights. Treat the percentages as a real measurement of that
rubric applied to 214 skills — not as measured non-compliance with an Anthropic standard. Its
third-person/trigger-phrase finding does independently corroborate obra.

## Structural rules

From Anthropic's `skill-creator` and obra's `anthropic-best-practices`, which agree on all of
these:

| Rule | Source | Note |
| ---- | ------ | ---- |
| Body under 500 lines | both | Guidance, not measured |
| Reference chains exactly one level deep | obra | Stated reason: agents read nested chains incompletely |
| Table of contents on long reference files | both | Anthropic says >300 lines, obra says >100 |
| `scripts/` `references/` `assets/` layout | Anthropic | `scripts/` for deterministic code, `references/` for docs loaded as needed, `assets/` for files used in output |
| Directory name = frontmatter `name` | spec | 1–64 chars, lowercase and hyphens |
| Organize multi-domain skills by variant under `references/` | Anthropic | So only the relevant file is read |
| Imperative form; explain why rather than stacking MUSTs | Anthropic | "explain to the model why things are important in lieu of heavy-handed musty MUSTs" |
| Forward slashes in paths, never backslashes | obra | |
| One default with an escape hatch, not several equal options | obra | |

**On the baseline discipline specifically:** Anthropic's `skill-creator` specifies it mechanically
— save 2–3 realistic prompts to `evals/evals.json`, then "For each test case, spawn two subagents
in the same turn — one with the skill, one without. This is important: don't spawn the with-skill
runs first and then come back for baselines later." Anthropic's engineering write-up states the
same ordering as internal practice: start from an evaluation that exposes a capability gap
*before* writing the skill. obra arrives at it from a TDD framing. Three independent routes to
the same rule.

## What reading cannot establish

Unicode Tag codepoints can be embedded in a `SKILL.md` — invisible to a human reviewer and to a
diff — and read by the model as instructions. A demonstrated payload sat on line 5 of an
otherwise legitimate security skill and forced the model to run `curl … | bash`. Manual review
and diffing both fail; detection requires tooling that scans for consecutive Unicode Tag runs
(ASCII Smuggler, or the demonstrator's `aid` scanner). An agent able to modify its own
configuration makes such an injection persistent.

At ecosystem scale: an audit of 3,984 published skills found 36.82% carrying security flaws, 76
with confirmed malicious payloads, and 341 typosquatting skills, alongside CVE-2025-59536 (CVSS
8.7). Three format-specific attack patterns are documented: natural-language injection in skill
prose, invisible Unicode injection, and malicious `.claude/settings.json` injection.

**The bound this places on an audit:** a review that reads a skill can assess quality but cannot
establish safety, because the dangerous content is by construction invisible to reading. Report
them as separate operations.

## What the spec does not cover

The Agent Skills specification scopes its reference validator to checking "that your SKILL.md
frontmatter is valid and follows all naming conventions" — frontmatter and naming, nothing else.
Every failure mode in this document except a missing `name` passes validation.

The gap between *valid* and *works* is structural rather than an oversight: most of these
failures are observable only in a transcript or a paired run, not in the file. This is the entire
reason yoda exists as prose discipline rather than a linter.

The newer packaging layer repeats the omission — Agent Plugins 1.0 (August 2026), which wraps
skills and MCP config in a cross-vendor `plugin.json`, deliberately excludes security,
sandboxing, marketplace and trust mechanisms, leaving them platform-specific.

**Portability note:** the packaging is portable; triggering behavior is not. Gemini CLI activates
skills through an explicit consented `activate_skill` tool call rather than Claude Code's implicit
selection. A skill authored once loads in both; the conditions under which it fires differ.

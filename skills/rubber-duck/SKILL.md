---
name: rubber-duck
description: Gets a second opinion from a different vendor's model and records it verbatim to docs/rubber-duck — Codex (GPT-6 Astra, high reasoning) when running in Claude Code, Claude (Fable 5.1) when running in Codex.
when_to_use: Use when stuck, before committing to an approach that is hard to reverse, or when asked to rubber duck, sanity check, red-team, challenge, or get a second opinion on something. Also when you notice you may be agreeing with yourself, or when a plan has felt right for a suspiciously long time.
---

# Rubber Duck

## Overview

**Another instance of yourself is not a second opinion.** Spawning subagents gives you more
opinions from the same weights, the same training, and the same blind spots — correlated
answers that feel like consensus. If your first instinct was wrong, they inherit the error and
confirm it back to you with more confidence than you started with.

**Core principle:** independence comes from a different model, not from more copies of this one.
This skill asks the other vendor's frontier model, and records what it said without softening it.

**Measured:** an agent asked for "the most genuinely independent perspective" on a design
question spawned six same-model perspective subagents and never once considered another vendor's
model. That is the default this skill exists to override.

## 1. Pick the duck — it is always the other vendor

| You are running in | Ask | Model |
| ------------------ | --- | ----- |
| **Claude Code** | Codex CLI | `gpt-6-astra`, reasoning effort `high` |
| **Codex** | Claude Code CLI | `claude-fable-5-1` |

You know which one you are. Route on that, and **never** substitute a same-vendor subagent
because the other CLI is missing or slow — that silently returns you to the failure above.
If the CLI is unavailable, **stop and say so**; a missing duck is a reportable outcome, not
something to paper over.

Verify first:

```bash
command -v codex    # from Claude Code
command -v claude   # from Codex
```

## 2. Brief the duck — it has none of your context

This is where the consult actually succeeds or fails. The duck has no conversation history, no
memory of what you tried, and no idea what constraints are real. An underspecified prompt returns
generic advice you will correctly ignore, which then reads as "the duck was useless" when the
brief was the problem.

Write a self-contained brief containing all five:

1. **The situation** — enough that a stranger could reason about it. Name the repo, the files,
   the constraint that makes this non-obvious.
2. **What you are leaning toward**, stated plainly. Do not hide it; you want it attacked, and a
   hidden position cannot be.
3. **What you have already tried or ruled out**, and why. Otherwise you get your own rejected
   options back.
4. **The specific question.** "Is this a good idea?" invites agreement. "What breaks in six
   months if I do this?" invites analysis.
5. **Explicit license to disagree.** Say that you want the position challenged and that agreeing
   is only useful if it survives an honest attempt to break it.

**Never ask a leading question.** "Don't you think X is right?" gets you X back and teaches you
nothing. If you would be annoyed by the answer "yes," the question is leading.

The duck can read the repo — it runs in the working directory with read access — so point it at
real files rather than pasting long excerpts.

## 3. Run the consult

**From Claude Code**, ask Codex. `-s read-only` keeps it advisory; it can read the repo but
cannot change anything:

```bash
codex exec -m gpt-6-astra -c model_reasoning_effort=high -s read-only \
  "<the five-part brief>" 2>&1 | tail -n +2
```

**From Codex**, ask Claude:

```bash
claude -p --model claude-fable-5-1 "<the five-part brief>"
```

High reasoning effort takes minutes on a real question. Allow a generous timeout and do not kill
it and retry with a thinner prompt — a truncated consult is worse than none, because you will
weigh it as though it were complete.

## 4. Record it verbatim

Write the duck's answer to `docs/rubber-duck/` **in the repo you are working in**, byte for byte:

```
docs/rubber-duck/YYYY-MM-DD-<short-slug>.md
```

Capture stdout directly rather than retyping or summarizing. Add a short header of your own —
date, model consulted, the question asked — then the duck's response **unedited beneath it**.

**Summarizing here is the failure mode.** You have just paid for an opinion specifically because
it is not yours; compressing it through your own judgement is how the disagreement quietly
disappears. If the duck said something you think is wrong, record it and then say you think it is
wrong. Both parts.

Do not edit the report later to match what you ended up doing. It is a record of what was said at
the time, and its value is that it can contradict you.

## 5. Report what came back, especially if it stings

Lead with **where the duck disagreed** — that is the entire return on the consult. Agreement is
worth one line; disagreement is worth the detail.

For each substantive point: what the duck said, whether you think it is right, and what you are
changing. "The duck raised X, and I still disagree because Y" is a fine outcome and an honest
one. "The duck agreed with me" as a whole summary usually means the brief was leading — check
step 2 before believing it.

Link the report path so the raw answer is one click away.

## Signals to Watch For

| Signal | Instead |
| ------ | ------- |
| Reaching for a subagent, perspective pass, or "let me think about this differently" | Those are all you. Route to the other vendor. |
| "The other CLI isn't set up, I'll approximate it" | You cannot approximate a different model. Stop and report. |
| Writing a brief that assumes context the duck cannot have | It has none. All five parts, self-contained. |
| Phrasing the question so agreement is the natural answer | If "yes" would annoy you, the question is leading |
| Summarizing the response into your own words | Verbatim. The point is that it is not your words. |
| Reporting only the parts that matched your view | Lead with the disagreement — it is what you paid for |
| Editing an old report to match what you shipped | It is a record, not a justification |
| Treating the duck as an authority | It is one more opinion, from a model with different blind spots — not fewer |

## What this is not

The duck is not a reviewer, an approver, or a tiebreaker. It has less context than you and no
stake in the outcome. A disagreement is a prompt to think again, not a verdict — and if you
consult it on something you have already decided, you will find a way to read the answer as
agreement.

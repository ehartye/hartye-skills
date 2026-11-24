---
name: challenge
description: Takes a fresh look at an idea, concept or course of action, asks whether it is being thought about the right way and what is missing, and offers a blind subagent evaluation.
when_to_use: Use when the user says "challenge this", "sanity check", "red-team this", "poke holes", "push back on this", "are we thinking about this right", or "what are we missing". Not for line-by-line review of code or a document.
---

# Challenge

Step back and look at the idea fresh. The aim is a sanity check on the thinking, so stay broad.

## 1. Challenge the thinking

- **Restate it.** In one or two sentences, say what is proposed and what problem it is meant to solve.
- **Are we thinking about this right?** Test the premise: is this the real problem, does the idea
  act on its cause, and which assumption, if wrong, sinks it?
- **What are we missing?** Look for what nobody has raised, such as another way to see the problem,
  a person affected, a cost, or a way it fails. Give the few points that matter.
- **Verdict.** Say one of: it holds up, it holds up with changes, or it needs rethinking. Name what
  would change your mind.

"It holds up" is a complete answer. Do not invent concerns to have something to say, and do not
fill the space with execution tips. Say where a better direction lies in a sentence, and leave the
replacement plan until the user asks for it.

## 2. Offer a blind evaluation

Your challenge comes from inside this conversation. Say so, and end by offering a blind evaluation
from a fresh subagent. Wait for the answer; do not launch it unasked.

On a yes, start one new subagent, never a fork of this conversation.

- **Give it** the idea in the user's own words, the facts and constraints it needs, and read-only
  access to whatever the idea concerns.
- **Withhold** your verdict, your points, and any question that hints at them.
- **Ask it** the two questions above, openly, and tell it "it holds up" is a valid result.

Run one pass, with no debate. Report where it disagrees with you and with the user, what it raised
that you missed, and where you still differ. The user decides.

It is the same model with the same training, so agreement between you is weak evidence. For a
different vendor's model, the user can run hartye-skills:other-guy.

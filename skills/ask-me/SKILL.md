---
name: ask-me
description: Interviews the user about pending decisions and approvals, with context and recommendations. Use when the user says "ask me", "what do you need from me", "I have a moment", or "what's blocked on me".
when_to_use: Use when the user says "ask me", "what do you need from me", "I have a moment", "anything you are waiting on", or "what's blocked on me". Also when you notice you parked a decision, made an assumption, took a detour or paused for lack of an answer, and the user is now available.
---

# Ask Me

The user has a moment. Spend it on the questions that unblock the most work, asked so each one
can be answered in a few seconds.

## 1. Gather

Take stock from your own awareness of this session. There is no fixed list of places to look:
decisions you parked, assumptions you made and carried on with, detours you took because an
answer was missing, approvals you are waiting on, and things you would like confirmed before
going further.

Drop anything the conversation has already answered. Merge duplicates.

If nothing is waiting, say so in one line and stop. Do not invent questions to fill the time.

## 2. Ask

Use a structured-question tool available in the current mode. Put related items in the same
batch, up to four questions or fewer if the tool requires it. Obey its option limits too. Keep
the complete pending set when it needs several batches. In Codex, read
[question controls and waiting](references/codex.md) before choosing the tool. For each question:

- Put the context in the question itself: what you were doing, what stopped you, and what you did
  in the meantime, so the user does not have to scroll back.
- Offer two to four options within the tool's limits, each with its trade-off in a few words.
- Put the option you recommend first and mark it as recommended.

When several choices may apply, use native multi-select if supported. Otherwise explain the
limit and ask for all chosen option labels in free text. If the tool cannot accept that answer,
use plain text. Do not force a multiple-answer question into a single-choice control.

With no suitable structured-question tool, use the same shape in plain text: numbered questions,
lettered options, the recommendation first and marked, in batches of up to four.

## 3. Wait for submission

Let the user complete and submit the interview. An asynchronous tool's acknowledgement only
means the questions were accepted for display; answers arrive separately. Use the host's
supported waiting mechanism to keep the interview open. Do not cancel or replace an unanswered
dialog, or send a final response that dismisses it. If the host cannot keep it open while
awaiting input, explain that limit and use the plain-text interview instead.

Track submission per question: retain each actual answer, including every selected value.
One answered question does not complete the other questions in the batch. Keep waiting for
each unanswered item until it is submitted or explicitly skipped, or the interview is canceled.

Preselected options, silence and wait timeouts are not answers. Continue only independent work
while waiting, and resume waiting after a timeout. Act on a decision only after its answer
arrives. Send the next batch only after every question in the current batch is answered or
explicitly skipped. If the user cancels or skips, leave unanswered decisions pending; do not
choose defaults or reopen the dialog automatically.

## 4. Act

After the answers, state in one line each what happens next, then do it within the user's
authorization and the active mode's permissions. Where an answer invalidates an assumption you
already built on, say what you will redo.

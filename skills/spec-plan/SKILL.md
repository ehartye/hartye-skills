---
name: spec-plan
description: Turns a request into a wiki-grounded spec saved on the project roadmap, shaped so plan mode converts it into a question-free plan that runs on approval with parallel subagents.
when_to_use: Use when asked to spec, scope or write up a feature, change or spike before building it; to turn open roadmap items into something buildable; or when told "/plan the spec" or to plan or execute from a saved spec.
---

# Spec, Plan, Execute

An unspecified request produces a plan full of guesses. This skill moves every question to the
front: it interviews you, grounds the work in the project wiki, and saves a spec as a backlog item
on the roadmap. The spec is written so the planner can turn it into a plan with no questions in
it, and approving that plan is the go signal. It assumes wiki-master is installed; without it,
say so and stop. Not for one-line changes, release notes or docs write-ups.

## Mode check

Stage 1 writes: discover and ingest clip sources, and the spec is saved. It cannot run in
read-only planning mode. If planning mode is active, **save nothing**, say the spec must be saved
before planning, ask the user to leave planning mode, and stop. Stages 2 and 3 run in planning
mode and in execution.

## Stage 1: Spec

1. **Size gate.** If the change can be described as one diff in one sentence, say so, skip the
   spec and just plan it. Otherwise keep the spec lightweight: pad no section, and omit a
   section that has nothing to say.
2. **Interview before you draft.** Ask in small batches, **two to four questions each, never
   five or more**: if you have more, ask the ones that change the spec most and hold the rest for
   the next batch. Give each a recommended default, using your structured-question tool if one exists. Cover: goal and the
   outcome a user can see; scope and non-goals; hard constraints; how acceptance is checked;
   build or spike; and which outward-facing actions are pre-authorized and which are not. Draft
   nothing until the first batch is answered. If the user says to decide for them, record your
   defaults as assumptions. Find the project from the repository through the overview's `repo:`
   field; if that fails, ask for the project slug.
3. **Search the wiki.** Dispatch a subagent to search it (**REQUIRED:** Use wiki-master:wiki-search) for the
   topic and the project's backlog. Report what coverage it found and what is missing, not just
   a list of pages.
4. **Offer discover and ingest when coverage is light.** Say what is missing and offer
   wiki-master:wiki-discover and wiki-master:wiki-ingest for it. Do not decline on the user's behalf.
5. **Settle overlapping roadmap items** the search found. The user decides each one in the
   interview: name the item, recommend a default, and ask. If their answers did not cover it,
   ask in a further batch; never settle it yourself. The outcomes:
   - One matching item: adopt it and spec it in place.
   - Related items that serve the same goal: group them as work packages.
   - Related but out of scope: list them under Non-goals as links.
   - Grouping that yields more than one independent goal: that is two specs.
   - An item that contradicts the goal is a conflict: ask which wins and record it as a Decision.

   An absorbed item stays on the roadmap with one line, `Specced in [[<spec>]] (WP-n)`, and its
   status moves with its work package.
6. **Explore the code read-only through subagents.** Find the real files, commands and
   existing behavior. Put findings in the spec only if the planner could not discover them
   itself. Questions the search or exploration raise go to the user in a further small batch.
7. **Spike when only an experiment can answer.** A request to find out whether something can
   work is a spike spec, not an answer: do not research it yourself and reply. Use the template's
   spike variant: each question as Given/When/Then with an observable result, ordered by risk;
   a verdict of validated, partial or invalidated, each with a deliverable and promote-or-discard
   criteria. State an effort budget only if the user gave one; otherwise write "no timebox;
   stops at the first met exit criterion".
8. **Open-decision gate.** The agent will not notice its own gaps, so list them. Every unknown
   becomes a question you ask now, a stated assumption, or a spike work package. The saved spec
   contains no question marks, no TBD or TODO, no "open questions" section, and no options left
   for the planner to pick between.
9. **Save it.** **REQUIRED:** Use wiki-master:wiki-author and the
   [spec template](references/spec-template.md). The spec is a backlog item at
   `wiki/authored/<project>/backlog/<slug>.md` with `kind: backlog-item` and
   `backlog-status: planned`, so the roadmap lists it with no extra step. Write acceptance as a
   runnable command with its expected output, or an observation anyone can repeat. Write
   at the altitude of outcomes and design; the planner chooses the technical steps.
10. **Close the interview** with exactly: "When you're ready, tell me `/plan the spec`." That
    line is the last thing the reply says: nothing follows it, no summary, no assumptions list, no
    wiki commands. Put anything the user should see before it.

## Stage 2: Plan (planning mode)

1. **Find the spec** from the conversation. Failing that, take the project's most recently updated
   backlog item that has a `## For the planner` section and status planned or in-progress. The
   plan's first line states which spec it chose.
2. **One work package is one plan step.** Keep the spec's parallel groups and carry each brief
   verbatim, with its owned files and done-when. Add the spec's Setup and Verification steps as
   its For the planner section directs, and add no step the spec does not contain.
3. **No questions, and no options.** The plan asks nothing, presents no alternatives and carries
   no ceremonial phases. If you find a gap, say which section has it and return to Stage 1.
4. **Carry the execution rules into the plan.** Its closing lines restate, so they survive
   approval: a fresh verifier, never the builder, runs the acceptance commands; one repair
   attempt by a fresh subagent, then record the failure and stop; at most three subagents at
   once; each report at most 150 words.
5. **Close with** "Approving this plan starts execution."

## Stage 3: Execute

1. Approval is the go signal. Set the item's `backlog-status` to in-progress, and move each
   absorbed item's status as its work package starts and finishes.
2. **Dispatch each parallel group** as concurrent subagents, one per work package, each given
   its self-contained brief and told to return at most 150 words, at most three at once. A package whose
   dependencies are unmet waits. Two packages never own the same file.
3. **The orchestrator keeps only the short reports** (files changed, the done-when output, any
   problem), not the files the subagents read. At each group boundary, restate the remaining
   plan so a long run does not drift.
4. **An independent verifier runs the acceptance commands**, a fresh subagent that is never
   the builder. It runs the full suite, and the negative tests the spec names. Only the
   verifier's result marks a criterion passed; nobody but the user edits the criteria.
5. **One repair attempt** by a fresh subagent per failure. If it still fails, record the failure
   in Results and stop; do not report the work complete. Continue only with packages that do
   not depend on the failed one.
6. **Write Results** in the spec as the progress log: what ran, each acceptance command and its
   output, decisions made, failures. A fresh session must be able to restart from the spec alone.
7. Leave `backlog-status` at in-progress until the user accepts the change. For a spike, stop at
   the first met exit criterion, record the verdict, and recommend promote or discard.
8. **No subagent facility?** Run the same work packages one after another in group order, keep
   each report just as short, and run verification last, against the acceptance criteria rather
   than your own notes.

## Red flags

| Signal | Instead |
| ------ | ------- |
| Drafting before the user has answered anything | Interview first, in small batches with defaults |
| A TBD, a `?` or an "open questions" section in the spec | Ask now, state an assumption, or make it a spike work package |
| A spike with no exit criteria, or an invented timebox | Verdicts with deliverables; a budget only if the user gave one |
| A duplicate item when the roadmap already has one | Adopt it, group it, or link it as a non-goal |
| Coverage light and no offer to discover and ingest | Offer it, naming the gap |
| Planning mode active and you saved or drafted anyway | Save nothing; ask the user to leave planning mode |
| A question or an options table in the plan | Gap means back to Stage 1; the plan only sequences |
| The orchestrator reading files a subagent should read | Delegate; keep the reports |
| The builder grading its own work | A fresh verifier runs the acceptance commands |
| Work packages that overlap on files, or need a long chat to understand | One owner per file; a brief that stands alone |

## Evidence

The rules come from the wiki synthesis *Specs and Plans for Coding Agents* (section 9). Read it
when a rule is challenged or the skill needs revising.

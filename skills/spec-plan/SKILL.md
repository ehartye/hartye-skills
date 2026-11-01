---
name: spec-plan
description: Turns a request into a wiki-grounded spec saved on the project roadmap, shaped so plan mode converts it into a question-free plan that runs on approval with parallel subagents.
when_to_use: Use when asked to spec, scope or write up a feature, change or spike before building it; to turn open roadmap items into something buildable; or when told "/plan the spec" or to plan or execute from a saved spec.
argument-hint: "[mode=standard|enhanced] [request]"
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

## Review mode

The arguments may carry `mode=standard` or `mode=enhanced` anywhere; the rest is the request.
With neither, the first interview batch asks which, standard recommended. **Standard** is the
skill as written elsewhere. **Enhanced** adds three independent reviews: spec review, package
review and final review. Each can also be adopted alone in a standard spec.

**Independent** means a fresh subagent started for that review alone: never continued by message,
never the author or builder of what it reviews, never the orchestrator, never reused. The final
reviewer is also distinct from the orchestrator, every builder, every package reviewer and the
verifier. It is given the
artifacts and the spec's relevant parts, never the builder's report or reasoning.

A reviewer does three jobs. **Code review:** correctness, regressions, and the style the spec
names. **Spec adherence:** it does what the brief and criteria say and no more, stays inside the
owned files, and respects the non-goals. **Independent testing:** it runs the done-when command
and at least one check of its own that the builder did not specify, including a negative one. A
reviewer edits nothing in the artifact.

A reviewer returns at most 150 words: PASS or FAIL, then each finding with evidence, a file and
line or a command and its output. A finding without evidence does not block; it goes into Results
as advisory. Reviewers count toward the cap of three subagents at once, and only the verifier
marks criteria. With no subagent facility, say in one line, before the spec review is dispatched or, when none is in force, before step 10
closes the interview, that enhanced cannot run independently, and record standard.

## Stage 1: Spec

1. **Size gate.** If the change can be described as one diff in one sentence, say so, skip the
   spec and just plan it. Otherwise keep the spec lightweight: pad no section, and omit a
   section that has nothing to say.
2. **Interview before you draft.** Ask in small batches, **two to four questions each, never
   five or more**: if you have more, ask the ones that change the spec most and hold the rest for
   the next batch. Give each a recommended default, using your structured-question tool if one exists. When no
   mode was given, the mode question (see Review mode) joins the first batch. Cover: goal and the
   outcome a user can see; scope and non-goals; hard constraints; how acceptance is checked;
   build or spike; the project's release and repo procedure (branch, pull request, merge method,
   tag, downstream pins) and which of those steps are pre-authorized; and which other
   outward-facing actions are pre-authorized and which are not. Draft
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

   The exploration subagent also reads the skills and plugins visible to the session, the
   project's enabled set, and the wiki's notes on the project's tooling if there are any, and
   returns the tools that fit the work. Propose every tool that fits, not only the best one, as
   ONE structured question (a multi-select with a recommended default), each tool with a
   one-line reason and the packages that use it; the user confirms or trims the list in one
   answer. It counts as one question in the interview batch (still two to four questions, never
   five or more). Record only confirmed tools. When none fits, say nothing about tools.

   After exploration, and before the spec review is dispatched or, when none is in force, before
   step 10 closes the interview, for each part that is especially high risk or complex,
   suggest the fitting review element in one structured question that names each qualifying
   package with the element suggested for it, with a recommendation for each. The parts that qualify: an action hard to reverse or outward-facing
   (delivery, deletion, migration, publishing); security, permission or data-handling changes; a
   shared contract many things depend on (public interface, schema, config format); a package
   spanning many files or needing care over order or concurrency; a spike whose verdict gates a
   larger build; a package resting on an assumption the user did not confirm. When nothing
   qualifies, say nothing. Record a declined suggestion as declined and do not ask again.
7. **Spike when only an experiment can answer.** A request to find out whether something can
   work is a spike spec, not an answer: do not research it yourself and reply. Use the template's
   spike variant: each question as Given/When/Then with an observable result, ordered by risk;
   a verdict of validated, partial or invalidated, each with a deliverable and promote-or-discard
   criteria. State an effort budget only if the user gave one; otherwise write "no timebox;
   stops at the first met exit criterion".
8. **Open-decision gate.** The agent will not notice its own gaps, so list them. Every unknown
   becomes a question you ask now, a stated assumption, or a spike work package. The saved spec
   contains no question marks, no TBD or TODO, no "open questions" section, and no options left
   for the planner to pick between. **Check each criterion against its artifact.** When a
   criterion asserts the content of a page, table or file, open that artifact or its template
   first and phrase the criterion at a level it can hold. Before saving, list each acceptance
   criterion with the artifact it reads and one line on what that artifact holds, learned by
   opening it or its template. A criterion with no such line is rewritten at a level the
   artifact can hold, or removed.
9. **Save it.** **REQUIRED:** Use wiki-master:wiki-author and the
   [spec template](references/spec-template.md). The spec is a backlog item at
   `wiki/authored/<project>/backlog/<slug>.md` with `kind: backlog-item` and
   `backlog-status: planned`, so the roadmap lists it with no extra step. Write acceptance as a
   runnable command with its expected output, or an observation anyone can repeat. Write
   at the altitude of outcomes and design; the planner chooses the technical steps. Record the
   release and repo procedure from the interview as a final delivery work package that depends on
   every other package, so merge, tag and pins are in the plan rather than left outside it. The saved spec has a Review
   mode section holding the mode, the elements in force, any declined, and the spec review
   outcome. It has a Recommended tools section when any tool was confirmed, and a Tools line on
   each package that uses one.

   **Settle review and tools before the review.** Before the spec review is dispatched or, when
   none is in force, before step 10 closes the interview, check whether each of two things has
   already been put to the user for this spec: the review-element suggestion and the
   recommended-tools proposal from step 6. Put each one that has not, whether or not step 6 has
   run, in one interview batch of two to four questions (never five or more) with a recommended
   default each. The review suggestion is ONE question, and the recommended-tools proposal is
   ONE structured question listing every tool that fits the work, not only the best one, each
   with its one-line reason and the packages that use it, so the user confirms or trims the
   list in one answer; each counts as one question toward the batch limit. Never put one a second time, including one the user
   declined. Record an accepted element under Review mode, a declined one as declined, and a
   confirmed tool under Recommended tools. A part that does not qualify, or a tool that does not
   fit, is not put to the user and is not recorded. Where the answers change an already saved
   spec, amend the saved page.

   **Spec review**, when in force, runs after the save and before step 10. Save the draft to the
   wiki at its final path first and review it in place; a draft in the wiki during review is
   acceptable. A fresh reviewer receives the user's request, the interview questions and answers,
   and the path of the saved draft. Its brief names the three jobs by the labels under Review
   mode. **Code review:** check the spec's claims about the codebase against the code. **Spec
   adherence:** check that every user decision is present and none is contradicted or invented.
   **Independent testing:** run the acceptance commands that can run before the build, confirming
   each baseline fails for the stated reason and each other command is runnable. The author fixes
   confirmed findings, a fresh reviewer re-checks once, and anything still open becomes a
   question in a further batch. The saved spec records that spec review ran and its outcome.
10. **Close the interview** with exactly: "When you're ready, tell me `/plan the spec`." That
    line is the last thing the reply says: nothing follows it, no summary, no assumptions list, no
    wiki commands. Put anything the user should see before it, and when other specs are queued
    (Stage 2 step 1), say how many.

## Stage 2: Plan (planning mode)

1. **Find the spec.** A queued spec is a backlog item with a `## For the planner` section and
   status planned or in-progress. If the user names a spec, use it. If exactly one is queued, use
   it. If several are, before writing the plan ask a multi-select question with your
   structured-question tool, offering the four most recently updated and letting the user name
   another. Picked specs run in the order picked, one after another, each with its own parallel
   groups. The plan's first line names the specs in order, each with its review elements. Before
   the plan is written, if reading the spec shows a risk its Review mode section does not mention,
   make the suggestion once more in the same shape (Stage 1 step 6); an accepted element is
   carried in the plan and recorded by the Setup step.
2. **One work package is one plan step.** Keep the spec's parallel groups and carry each brief
   verbatim, with its owned files, done-when and Tools line. Add the spec's Setup and Verification steps as
   its For the planner section directs, and add no step the spec does not contain. A reviewed package's plan step carries "then
   reviewed" as part of that step. When in force, Final review is its own step between
   Verification and delivery.
3. **No questions, and no options.** The plan asks nothing, presents no alternatives and carries
   no ceremonial phases. This governs the plan's content; the step 1 picker and suggestion run before the plan
   exists. If you find a gap, say which section has it and return to Stage 1.
4. **Carry the execution rules into the plan.** Its closing lines restate, so they survive
   approval: a fresh verifier, never the builder, runs the acceptance commands; one repair
   attempt by a fresh subagent, then record the failure and stop; at most three subagents at
   once; each report at most 150 words. Whenever any review element is in force, also restate that
   reviewers are fresh subagents that never review their own work, that a failed review gets one
   repair by a fresh subagent and a fresh re-review, and that a second failure is recorded and
   stops.
5. **Close with** "Approving this plan starts execution."

## Stage 3: Execute

1. Approval is the go signal. Set the item's `backlog-status` to in-progress, and move each
   absorbed item's status as its work package starts and finishes.
2. **Dispatch each parallel group** as concurrent subagents, one per work package, each given
   its self-contained brief and told to return at most 150 words, at most three at once. A package whose
   dependencies are unmet waits. Two packages never own the same file. The dispatch brief carries
   the package's Tools line. A tool is advisory: the subagent uses it where it fits, may skip it
   with a one-line reason in its report, and proceeds without it, saying so, if it is not
   available when the run starts. Pass or fail rests on the acceptance and done-when commands
   alone. A reviewer brief may carry tools the same way.

   **Package review**, when in force: after a package's builder reports and before any package
   that depends on it starts, a fresh reviewer reviews it, except the delivery package. Packages
   of one group may be reviewed together within the cap. A FAIL with evidence gets one repair
   attempt by a fresh subagent given the findings, not the original builder, and a fresh
   re-review. A second failure is recorded in Results; the package and its dependents stop, and
   independent packages continue.
3. **The orchestrator keeps only the short reports** (files changed, the done-when output, any
   problem), not the files the subagents read. At each group boundary, restate the remaining
   plan so a long run does not drift.
4. **An independent verifier runs the acceptance commands**, a fresh subagent that is never
   the builder. It runs the full suite, and the negative tests the spec names. Only the
   verifier's result marks a criterion passed; nobody but the user edits the criteria.

   **Final review**, when in force: after every non-delivery package has passed review and the
   verifier has passed, and before the delivery package starts, a fresh final reviewer, whose dispatch
   states that it is distinct from the orchestrator, every builder, every package reviewer and
   the verifier, reviews the whole result against the Goal, Scope and non-goals, and the acceptance criteria: how the
   packages fit together, files changed outside any owner, the diff staying confined. A failure
   gets one repair per finding by a fresh subagent and a fresh final reviewer. A second failure is
   recorded in Results, delivery does not start, and the work is not reported complete. For a
   spike, package review covers the exploratory packages and the final review checks the verdict
   against the recorded evidence and the exit criteria.
5. **One repair attempt** by a fresh subagent per failure. If it still fails, record the failure
   in Results and stop; do not report the work complete. Continue only with packages that do
   not depend on the failed one.
6. **Write Results** in the spec as the progress log: what ran, each acceptance command and its
   output, decisions made, failures. A fresh session must be able to restart from the spec alone.
7. Leave `backlog-status` at in-progress until the user accepts the change. For a spike, stop at
   the first met exit criterion, record the verdict, and recommend promote or discard.
8. **No subagent facility?** Run the same work packages one after another in group order, keep
   each report just as short, and run verification last, against the acceptance criteria rather
   than your own notes. Review elements are not run.
9. **End with an interview over what is still outstanding.** Use a structured-question tool: give
   each item its context, its options and a recommendation where there is one, so the user
   decides in the moment. Do not close with a list of follow-ups. With no question tool, ask in
   plain text in the same shape.

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
| The builder or orchestrator reviewing its own work, or a reviewer given the builder's report | A fresh reviewer, given the artifacts |
| Work packages that overlap on files, or need a long chat to understand | One owner per file; a brief that stands alone |
| Ending an execution with a list of follow-ups | Ask about each outstanding item, with options and a recommendation |

## Evidence

The rules come from the wiki synthesis *Specs and Plans for Coding Agents* (section 9). Read it
when a rule is challenged or the skill needs revising.

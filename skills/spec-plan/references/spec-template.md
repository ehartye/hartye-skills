# Spec template

Save as `wiki/authored/<project>/backlog/<slug>.md`. Each section's note says what belongs and what
to leave out; delete the note, and any section with nothing to say. The finished spec has no
questions, no TBD, no TODO and no NEEDS CLARIFICATION.

```markdown
---
type: authored
created: <date>
updated: <date>
status: draft
sources: []
ai-generated: true
project: <project>
kind: backlog-item
backlog-status: planned
---
# <Imperative title: what changes for the user>

## Goal
Open here: the goal and the outcome a user can see, in a few sentences. State the spec's level
and lifetime (written before building and discarded after, kept alongside the code, or the
standing source of truth) and mark what is existing behavior and what is new. Leave out history.

## Review mode
The mode and the review elements in force, any element the user declined, and the outcome of the
spec review. Omit the section for a standard spec with no elements.

Mode: <standard | enhanced>
Review elements: <spec review, package review (every package except delivery, or the WP ids), final review; or none>
Declined: <elements the user declined, or none>
Spec review: <ran, with its outcome | not in force>

## Context
Only what the planner cannot discover from the code or the wiki: the evidence pages, the
decision that makes this non-obvious, links to related notes. Leave out orientation it can read
for itself.

## Scope and non-goals
In scope as a short list, then non-goals. Related items that are out of scope go here as links.
Leave out anything nobody would plausibly assume is in scope.

## Absorbed and related items
Each roadmap item the work absorbs, as a link with the one line `Specced in [[<this spec>]]
(WP-n)`; each related item left alone, with a reason. Omit if there are none.

## Decisions
Numbered, each with the choice made and the reason in a clause. These are settled; the planner
does not reopen them. Leave out options that were considered and dropped.

## Assumptions
Things taken as true because the user gave no answer, each stated so the user can correct it
before planning. Leave out anything the user actually decided; that is a Decision.

## Constraints and pre-authorized actions
Hard, checkable constraints only: the commands to build, test and run; the project structure the
work must respect; one real code snippet showing the style to match; and Always, Ask first and
Never boundaries. Name which outward-facing actions are pre-authorized and which are not. Name
the delivery steps that apply (branch, pull request, merge method, tag, downstream pins) and which
are pre-authorized, taking the details from the project's own guidelines.

## Recommended tools
The plugins and skills available in the project that fit the work, confirmed by the user, each as
`<name as the project lists it> - <one-line reason>; used by <WP ids>`. Tools are advisory: a
package may do without them. Omit the section when none fits.

## Acceptance criteria
Numbered. Each is a runnable command with its expected output, or an observation anyone can
repeat, per milestone where there are several. Include at least one negative test and name the
full suite. Leave out adjectives ("clean", "fast") with no check behind them. Only the independent
verifier marks a criterion passed; the executor does not edit the criteria.

## Work packages
Group by context boundary, not by role. One loop of work each, independently verifiable, with a
stop-and-fix rule: if the done-when fails, repair once and stop. Each file has exactly one owner,
and a package is self-contained, readable without the rest of the spec. Start with one agent for
a small change, and plan no more than three at once. Leave out granular technical steps the
planner can choose better than the spec can.

### Group A (independent, run together)
**WP1: <name>.** Depends on: <none | WP ids>. Owns: <files or directories>.
Brief: <everything the subagent needs, with the goal, inputs, constraints and what to return>.
Done when: <a command and its expected output>.
Tools: <names from Recommended tools, or none>. (optional line)

A package marked for review has its plan step carry "then reviewed".

### Group B (after group A)
**WP2: <name>.** Depends on: WP1. Owns: <files>.
Brief: <...>. Done when: <...>.

### Final group (delivery, after every other package)
**WP-last: Deliver.** Depends on: every other WP. Owns: <none beyond the delivery steps>.
Brief: the delivery steps from Constraints that apply, in order, running only those
pre-authorized. Done when: <a command and its expected output>.

## Verification
How a fresh session runs everything end to end: the acceptance commands in order, and where each
command and its output are recorded. State that a failure not fixed is recorded as failing, and the
work is not reported complete while a named criterion fails. A verifier subagent runs this, never
the builder.

## For the planner
Plan hooks, as a short list: one plan step per work package plus Setup, in the groups above, with
briefs carried verbatim; which step sets the status and which runs Verification; when the final review is in force, a Final
review step between Verification and delivery; that approval
of the plan is the go signal; that a blocked package is recorded in Results and the rest continue;
that the orchestrator keeps only the subagents' short reports.

## Results
Not started. Execution turns this into the progress and decision log: what ran, each command
and its output, decisions made, failures, and the link to the delivered change.
```

## Spike variant

Use when only an experiment can answer an unknown. A spike spec keeps Goal, Review mode, Context,
Scope and non-goals, Assumptions, Constraints, Recommended tools, Verification, For the planner and
Results, and replaces the middle:

```markdown
## Question
Each unknown as Given / When / Then with an observable result, ordered by risk, riskiest first.

## Budget
Only an effort budget the user gave, in their words. Otherwise: "no timebox; stops at the first
met exit criterion". Do not invent one.

## Exploratory work packages
The same fields as above. Throwaway code lives somewhere that is never delivered, and each
package says where. Leave out production-quality work.

## Exit criteria
- **Validated:** the observable result held. Deliverable: <the finding and the evidence>.
  Promote when <criterion>: it becomes a build spec.
- **Partial:** some held. Deliverable: <what held, what did not, the smallest next experiment>.
  Promote or discard by <criterion>.
- **Invalidated:** the result did not hold. Deliverable: <the evidence and the options that
  remain>. Discard the experiment.
```

Execution stops at the first met exit criterion, records the verdict in Results, and recommends
promote or discard.

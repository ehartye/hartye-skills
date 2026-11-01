# Spec template

Save as `wiki/authored/<project>/backlog/<slug>.md`. Replace guidance with settled content,
keeping the sections that help a fresh planner understand the goal and make a concrete plan.
Before handoff, settle decisions about scope, behavior, interfaces, dependencies, acceptance
and authorization, and record them as statements. Replace placeholders and open questions with
settled choices; leave routine implementation details within those choices to the implementer.
For multiple goals, save one spec per goal in the same backlog. Each spec retains its own
decisions, rigor and acceptance criteria so it can be planned alone or in a selected set.

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
State the goal and the user-visible outcome. Distinguish existing behavior from the change.
State the spec's intended lifetime: a planning input, a maintained companion to the code,
or the standing source of truth.

## Rigor
Rigor: <standard | enhanced>
Spec review: <selected | not selected>; outcome: <pending | passed, with evidence>
Planned work-package review: <all packages | selected WP ids | not selected>
Stage-specific choices: <accepted or declined enhancements and the user's reason, if any>

Enhanced selects both enhancements. Record the actual spec-review outcome before handoff;
the plan carries work-package reviews as future review steps.

## Context
Record relevant evidence and non-obvious design context, with source links, so the planner
can distinguish established facts from assumptions.

## Scope and non-goals
State the included outcomes and plausible adjacent work outside this change. Link related
roadmap items that remain separate.

## Absorbed and related items
Link absorbed items to their work packages. Each absorbed roadmap entry points here with
`Specced in [[<this spec>]] (WP-n)` so it remains discoverable.

## Decisions
List each settled choice with its reason. These decisions let planning focus on concrete steps.

## Dependencies
Link prerequisite specs and name the required outcomes or settled interface contracts. Identify
already verified prerequisite results where applicable. Include this section when dependencies
exist. Findings from an unresolved spike inform a later build spec and plan after its verdict.

## Assumptions
Record user-delegated choices explicitly so the user can correct them before the plan depends
on them. Resolve execution-informing decisions through the interview or a defined spike.

## Constraints and authorization
Record checkable constraints, relevant commands, interfaces, project conventions and a real
code-style example where useful. Carry forward the project's delivery procedure and the
user's authorization boundaries so the plan can accurately describe any delivery package.

## Recommended tools
List user-confirmed tools as `<name> — <reason>; used by <WP ids>`. These inform the plan's
package briefs. Include this section when tools have been selected.

## Acceptance criteria
Number observable outcomes, each with a runnable command and expected output or a repeatable
observation. Identify the artifact each criterion reads and what it can show. Distinguish
existing baseline checks from checks requiring future work. Include relevant failure cases
and the appropriate project validation commands.

## Work packages
Group by context boundary. Give each package a self-contained brief, explicit dependencies,
file ownership and a checkable result. Independent packages with disjoint ownership can be
planned in parallel; shared-file changes need an explicit sequence.

### Group A — independent
**WP1: <name>.** Depends on: <none | WP ids>. Owns: <files or directories>.
Brief: <goal, inputs, interfaces, constraints and expected artifacts>.
Done when: <command and expected output, or repeatable observation>.
Tools: <confirmed tools, when applicable>.

### Group B — after its dependencies
**WP2: <name>.** Depends on: WP1. Owns: <files or directories>.
Brief: <self-contained brief>. Done when: <observable result>.

### Delivery — when required by the scope
**WP-last: Deliver.** Depends on: <required WP ids>.
Brief: <project-specific delivery requirements and authorization boundaries>.
Done when: <observable delivery outcome>.

## Verification
Describe how the eventual result will be checked against acceptance, including integration
checks and relevant negative cases. This is input to the plan's verification steps.

## For the planner
Carry the package briefs, ownership, dependencies, done-when checks and confirmed tools into
the plan. Default to subagents for parallel independent work and context preservation, with
concise reports to the orchestrator; state the reason for any exception. Add the selected
fresh-agent work-package reviews after package work and before dependent work (before the
outward-facing action for delivery). Apply the same decision-completeness check to the plan
before handoff so a fresh agent can begin every package with those decisions settled.
When selected with other specs, retain this spec's rigor and acceptance criteria in its own
section of the combined plan. Qualify package IDs as `<spec-slug>/WP-n`, reconcile dependencies
and shared interfaces across the set, and sequence specs in dependency-compatible selection
order, with parallel groups inside each spec. Recheck readiness from the saved content and
review outcome against the current repository when planning begins.
```

## Spike variant

Keep the same grounding, Rigor, dependencies and planner handoff sections. Replace build outcomes and work
packages with the following experimental design, so planning has a defined decision to support.

```markdown
## Questions to investigate
State each unknown as Given / When / Then with an observable result, ordered by risk.

## Budget
Use the user's stated effort budget. Otherwise: "no timebox; stops at the first met exit criterion".

## Exploratory work packages
Use the same brief, dependency, ownership and done-when fields. Name the disposable experiment
artifacts, the settled experimental method and the evidence each package should produce.

## Exit criteria
- **Validated:** <observable result>; deliverable: <finding and evidence>; promote when <criterion>.
- **Partial:** <what held and what remains>; deliverable: <evidence and smallest next experiment>;
  promote or discard according to <criterion>.
- **Invalidated:** <observable result>; deliverable: <evidence and remaining possibilities>;
  discard according to <criterion>.
```

Specify which observable condition ends the experiment and how its verdict informs the next
decision. Investigatory questions belong in the spike; its method, observable outcomes and
exit criteria are settled before handoff. When findings determine a later build decision,
plan the spike first and complete the affected build plan after its verdict. The spike spec
and its plan are the deliverables of this skill.

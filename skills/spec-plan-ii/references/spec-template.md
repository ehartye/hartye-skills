# Spec template

Save each spec as `wiki/authored/<project>/backlog/<slug>.md`, one spec per independent goal.
Replace the guidance with settled content and keep the sections that help a fresh planner
understand the goal and plan it. Before handoff, record decisions about scope, behavior,
interfaces, dependencies, acceptance and authorization as statements, not open questions. Leave
routine implementation details to the implementer.

The spec carries no hardening round count. That is a planning argument.

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
State the goal and the user-visible outcome. Label existing behavior and the change separately.
State the spec's intended lifetime: a planning input, a maintained companion to the code, or the
standing source of truth.

## Review
Pending.

Keep this section at "Pending." until the sanity check returns, so the checker never reads the
self-review. Fill it in after the sanity check returns, at triage:

Self-review (<date>): <outcome of the four checks: decisions settled, acceptance observable,
existing and new behavior labeled, each package startable from its brief; what was fixed>
Sanity check (<date>, fresh agent): <"No concerns", or the points returned>
- Adopted: <point; the change made to this spec>
- Disputed: <point; the reviewer's position; ours; the recommendation given to the user>
User decisions: <for each disputed point, what the user decided and when>

A spec is ready for planning only when all three lines are filled in and no disputed point is
waiting for the user.

## Context
Record evidence and non-obvious design context with source links, so the planner can tell
established facts from assumptions. Note the wiki coverage, the gaps, and any research round that
filled them.

## Scope and non-goals
State the included outcomes and plausible adjacent work that is out of scope. Link related
roadmap items that stay separate.

## Absorbed and related items
Link absorbed items to their work packages. Each absorbed item carries
`specced-in: ["[[<this spec>|WPn]]"]` in its frontmatter, so it stays discoverable.

## Decisions
List each settled choice with its reason.

## Dependencies
Link prerequisite specs and name the required outcome or settled interface contract. Include
this section when dependencies exist.

## Assumptions
Record choices the user delegated, so the user can correct them before the plan depends on them.

## Constraints and authorization
Record checkable constraints, commands, interfaces, and the project's implementation and quality
rules, which hardening reviewers check against. Carry forward the delivery procedure and the
user's authorization boundaries. Record any delegated-planning authority separately from
execution authority.

## Recommended tools
List user-confirmed tools as `<name> — <reason>; used by <WP ids>`. Include this section when
tools were selected.

## Acceptance criteria
Number observable outcomes, each with a runnable command and expected output or a repeatable
observation. Name the artifact each criterion reads. Separate checks that pass today from checks
that need the future work. Include relevant failure cases and the project's validation commands.

## Work packages
Group by context boundary. Independent packages with disjoint ownership can run in parallel;
shared-file changes need an explicit sequence.

### Group A — independent
**WP1: <name>.** Depends on: <none | WP ids>. Owns: <files or directories>.
Brief: <goal, inputs, interfaces, constraints and expected artifacts>.
Done when: <command and expected output, or repeatable observation>.
Tools: <confirmed tools, when applicable>.

### Group B — after its dependencies
**WP2: <name>.** Depends on: WP1. Owns: <files or directories>.
Brief: <self-contained brief>. Done when: <observable result>.

### Delivery — when the scope requires it
**WP-last: Deliver.** Depends on: <required WP ids>.
Brief: <delivery requirements and authorization boundaries>.
Done when: <observable delivery outcome>.

## Verification
Describe how the result will be checked against acceptance, including integration checks and
negative cases.

## For the planner
Carry each package's brief, ownership, dependencies, done-when and tools into the plan. Plan each
development task as a TDD, dev and certification triple under one developer agent. Plan the
hardening rounds after the development packages are certified and before delivery. Use subagents
for independent work with disjoint ownership. Planned with other specs, keep this spec's own
section, qualify package IDs as `<spec-slug>/WPn`, and reconcile shared interfaces. Use Plan mode
unless delegated planning outside it is explicitly authorized.
```

## Spike variant

Keep the Goal, Review, Context, Dependencies, Constraints and For the planner sections. Replace the
build outcomes and work packages with the experiment below. A spike gets the self-review and the
sanity check, but no TDD, certification or hardening: its deliverable is a verdict with evidence.

```markdown
## Questions to investigate
State each unknown as Given / When / Then with an observable result, ordered by risk.

## Budget
The user's stated effort budget. Otherwise: "no timebox; stops at the first met exit criterion".

## Exploratory work packages
Use the same brief, dependency, ownership and done-when fields. Name the disposable experiment
artifacts, the settled method and the evidence each package produces.

## Exit criteria
- **Validated:** <observable result>; deliverable: <finding and evidence>; promote when <criterion>.
- **Partial:** <what held and what remains>; deliverable: <evidence and the smallest next
  experiment>; promote or discard according to <criterion>.
- **Invalidated:** <observable result>; deliverable: <evidence and remaining possibilities>;
  discard according to <criterion>.
```

Settle the method, the observable outcomes and the exit criteria before handoff. When the verdict
decides a later build, plan the spike first; promoted work gets its own build spec.

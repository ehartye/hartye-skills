# Delegated planning validation

Date: 2026-11-03. Baseline: `36e6b4cf01b7527b60a5177cc684dbd88e5b02f4` (0.9.6).
This is process-documentation validation, not a live implementation or host integration test.
The [fixture](spec-plan-delegated-scenario.md) supplies wiki and repository evidence; it does
not contact a real wiki, run product tests, implement CSV export, or create a product PR.

## Method and pre-edit evidence

Started separate fresh agents in the same turn with the fixture, one without spec-plan and
one with the unmodified skill. Both wrote their actual proposed plans before the edit.
The no-skill run produced a plan with acceptance and review steps but omitted separate
immediately preceding TDD tasks, same-developer pairs, and the expected-failure dependency.
Verbatim excerpts from that output:

> Serialize typed `Transaction[]` with the settled header, escaping, ordering, and empty-input behavior. Cover commas, quotes, CR/LF, and empty rows with explicit expected outputs.

> In the real task, begin the implementation phase by recording the workspace baseline and preparing safe branch/worktree isolation, then implement WP1 and obtain its independent review.

The current-skill baseline succeeded by applying user-instruction precedence despite the
skill's absolute mode prerequisite. Its explicit explanation was:

> Planning is complete in Default mode using regular Markdown todos, as explicitly authorized. That instruction overrides the skill's Plan-mode prerequisite.

It preserved enhanced TDD/review requirements and prior execution authority. Thus this run
does **not** demonstrate that the old skill always blocked delegated planning. The change
codifies the authorized exception and its persistence/tracking contract; it does not claim
to fix a demonstrated model inability to recognize user precedence.

## Forward scenarios

Fresh agents received the modified skill and fixture, without baseline outputs or the author's
expected answers. Normal mode ran separately; authorization/blocker variants shared one test
agent, and delegated/todo variants shared another. Each variant was treated as a separate
simulation. Inspect the actual generated plan or response against these observable contracts:

| Scenario and changed fixture inputs | Observed result |
| --- | --- |
| Default mode; original fixture with explicit planning and later implementation/draft-PR authority; simulated todo UI | PASS: saved complete plan with host mode, authority, assumptions, briefs, acceptance and a stable-ID todo projection. Preserved same-developer TDD pairs, independent review dependencies and pre-delivery review. Next action carried existing authority forward without asking again. |
| Default mode; explicitly planning-only (do not implement), no todo UI | PASS: saved complete plan with a durable dependency/status task table. Marked execution tasks blocked on authority, completed planning handoff, and stopped without implementation or external actions. |
| Normal Plan mode; replace user request with "Plan the ready csv-export spec"; no delegation/execution authority; reply-only host plan format | PASS: returned a proposed plan with enhanced TDD pairs, same developer per pair, distinct package reviewers and review gates. Did not require a delegated record, saved plan or todo projection. Next action awaited execution authority. |
| Default mode; only "Plan the ready csv-export spec"; no mode switch or prior delegation | PASS: stopped Stage 2 for missing delegated authority; created no implementation plan or execution todos and did not infer permission from the request. |
| Default mode; original authority, but empty-row decision reserved to absent user and corresponding review invalidated | PASS: preserved reserved choice, marked decision/spec-update/review/planning dependencies blocked, asked for the choice, and returned to Stage 1. Did not claim readiness or proceed with dependent work. |
| Default mode; original authority, but read-only host with no permitted durable artifact | PASS: prepared an explicitly unsaved proposed plan, reported persistence and host restrictions, and stopped before complete handoff or execution. |

Selected verbatim gate outputs:

> Actual host mode: Default, with no mode-switch mechanism. The fixture user explicitly authorizes planning this ready spec in Default mode while away, using regular todos. That is the source and scope of the delegated planning exception.

> The host has no todo support, so this saved table is the task projection; no todo tool would be called. Stable IDs, source/package, dependencies, owner and status remain explicit.

> No plan created. Grounding and supplied readiness evidence were read; no implementation checks were run. Planning and handoff are blocked by the mode prerequisite.

> I will not select header-only output from the original fixture or treat your absence as an answer.

> Proposed plan exists only in this response. No durable plan, saved host artifact, completed handoff, implementation result or validation result exists in variant C.

## Structural checks and independent review

- `git diff --check`: passed.
- `claude plugin validate .`: passed with existing warnings for root CLAUDE.md not loading as
  plugin project context and a missing plugin icon. Neither is introduced by this change.
- Parsed YAML; checked matching skill/directory name, description/listing length, body under
  500 lines, local Markdown link targets, argument-substitution patterns, Unicode Tag
  characters, and matching unchanged 0.9.6 manifests: passed. These are structural checks,
  not comprehensive safety validation.
- The generic skill-creator `quick_validate.py` rejects the pre-existing Claude-specific
  `argument-hint` and `when_to_use` fields. This was reproduced on the unmodified baseline;
  those supported repository fields were preserved rather than removed to satisfy that
  narrower validator.
- A fresh independent reviewer read the instructions, complete skill/template/evidence and
  diff without author baseline or forward outputs. Verdict: **PASS, no actionable findings**.
  It checked default-path behavior, delegated authority, decision gates, persistence and
  task projection, readiness/coverage, enhanced reviews/TDD, handoff and supporting-doc
  consistency. This was static review, separate from the behavioral runs.

## Limits

These are single simulated samples, not proof of general reliability or equivalence to a
host-enforced Plan mode. Todo UI submission, live wiki persistence and real implementation
were deliberately not exercised. No release, install, merge or creative-direction wiki
mutation is part of this change.

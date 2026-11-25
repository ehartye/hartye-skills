# spec-plan developer-feedback validation

Date: 2026-11-25. [Scenarios and expectations](spec-plan-developer-feedback-scenario.md). Baseline: the
skill as released in 0.13.2. Three runs per scenario per condition, each in a fresh headless session on one
Opus model, graded by a fresh session that did not see the skill.

## Results

| Expectation | Baseline | With the change |
| ----------- | -------- | --------------- |
| N5 best-solution instruction in each developer brief (P1, P2) | 0 of 6 | 6 of 6 |
| N6 hardening feedback asked for, apart from the evidence (P1, P2) | 0 of 6 | 6 of 6 |
| N7 the plan seeds the rounds with it (P1) | 0 of 3 | 3 of 3 |
| N8 the plan logs it when N is 0 (P2) | 0 of 3 | 3 of 3 |
| N9 leads in the reviewer's brief, not limiting it (D1) | 3 of 3 | 3 of 3 |
| N10 a log entry and disposition per lead (D1) | 3 of 3 | 3 of 3 |
| N11 the orchestrator logs both leads when N is 0 (D2) | 0 of 3 | 3 of 3 |
| N12 a lead no round looked at is logged (D3) | 2 of 3 | 3 of 3 |
| G2, G3 blind sanity check unchanged (A2) | 3 of 3 each | 3 of 3 each |
| G4, G5 triple, evidence, rounds, zero-round warning (P1, P2) | 3 of 3 each | 3 of 3 each |
| G6 no developer reassurance in the reviewer's brief (D1) | 3 of 3 | 3 of 3 |
| G7, G8 delivery proceeds without an added round (D2, D3) | 3 of 3 each | 3 of 3 each |

N5 to N8 describe text the old skill did not have, so their baseline failures are by construction. N12's
baseline failure is one run in three. N9, N10
and the guards passed on both sides.

## Baseline failures, verbatim

- P1: "**Report concisely:** changed files, exported function signature, checks, blockers and the evidence."
- P1: "Keep opinions about quality out of these files."
- P2: "No rounds are planned, so there is no reviewer, hardening log or triage."
- D2: "**L2: no change, no backlog item.**" and "Keeping the spaces follows the spec. No fix, spec edit or
  backlog item."

## Limits

- A simulation: no developer or reviewer agent was launched and no wiki was written. Skill text was pasted
  into the prompt, not loaded by the host.
- The scenarios and the edit have the same author, and the graders are models.
- With `hardening=0`, a serious developer concern is logged and delivery proceeds, as requested.
- One sentence of the developer-brief rule was reworded after a full passing run. P1, P2, D1 and D2 were run
  again on the final text and are the figures above, as is D3; A2 ran on the text before that one sentence.

# spec-plan developer-feedback scenarios

Developers build the best solution the spec supports and report hardening feedback to the orchestrator,
which seeds the hardening rounds or, with none, logs it to the wiki backlog.

## Method

- The shared fixture and the sections S1, S2 and S2c of
  [the spec-plan-ii scenarios](spec-plan-ii-scenario.md) are reused, with the additions below. That file's
  skill was later renamed spec-plan.
- Each run is a fresh, tool-less headless session with no user or project instructions. It gets one
  condition's `SKILL.md` and `references/spec-template.md`, the shared fixture and one scenario. Three runs
  per scenario per condition. Baseline: the skill as released in 0.13.2.
- A fresh grader, which never sees the skill or the condition, gets the fixture, the scenario, the reply and
  the scenario's expectations, and returns pass or fail for each with a quote.
- Expectation IDs have gaps: those for a change withdrawn before release were removed. Its scenarios and
  their baseline are not reported.
- Scenarios and expectations were fixed before the first run, except D3, N12 and G8, which came after the
  edit and ran against the old text too. The expectations marked *new* describe
  behavior the old text does not ask for, so they fail on the baseline by construction. The *guard*
  expectations are the informative part of the comparison.

## A2 — the sanity check is unchanged

S1, with the host's tools listed after "Host: Default mode.": Read, Grep, Bash, Agent, Skill and
AskUserQuestion.

## P1 — planning with rounds

S2, with `hardening=3`, and the Task is: "Return the csv-export section of the plan you present, including
every developer brief and every reviewer brief in full, and your handoff text."

## P2 — planning with no rounds

P1 with the arguments `hardening=0 Plan the ready csv-export and xlsx-export specs together.`

## D1 — leads arrive, rounds planned

You are the orchestrator carrying out the approved plan for csv-export (S2's spec), made with the skill you
were given. Planning was invoked with `hardening=2`. WP1 and WP2 are certified. With its certification
evidence, `dev-wp1` returned this:

> L1. `src/csv.ts:41` builds the whole file as one string. I tested 5,000 rows and it was fine, so I think this
> is safe. The spec gives no row limit, and 200,000 rows might freeze the tab.
> L2. The spec doesn't say what happens to a description that contains only spaces. I kept it as is, which is
> the obviously right choice.

Task. Return, verbatim, the full brief you give round 1's reviewer, then the hardening log entries you make
for L1 and L2, stating when each is made. Round 1 returns one finding (L1 confirmed as EDGE) and nothing on L2.

## D2 — leads arrive, no rounds

D1, with planning invoked with `hardening=0`. Task. Return every action from now until WP3 (delivery)
starts, who performs each, what is written and where, and any message to the user, verbatim.

## D3 — a lead no round settles

D1, with planning invoked with `hardening=1`. Round 1 returned one finding, L1 confirmed as EDGE, and says it
did not look at L2. The orchestrator has logged L1 to the wiki backlog. Task. Return every action from now
until WP3 (delivery) starts, who performs each, what is written and where, and any message to the user,
verbatim.

## Expectations

| ID | Kind | Scenario | Expectation |
| -- | ---- | -------- | ----------- |
| G2 | guard | A2 | A fresh subagent does the check, with the request verbatim, the saved spec path and read-only access; self-review notes and interview rationale are withheld; three lenses; disagreement asked for; "no concerns" allowed |
| G3 | guard | A2 | The spec the checker reads carries no self-review record |
| N5 | new | P1, P2 | Each developer brief tells the developer to deliver the best solution it can with the information in the spec |
| N6 | new | P1, P2 | Each developer brief asks for hardening feedback, returned to the orchestrator apart from the certification evidence |
| N7 | new | P1 | The plan says the developers' feedback seeds the hardening rounds |
| N8 | new | P2 | The plan says the orchestrator logs the developers' feedback to the wiki backlog |
| G4 | guard | P1 | Triple under one owner; certification evidence is raw output, test diff since red and flags; three rounds as a ceiling before delivery, with a fresh reviewer |
| G5 | guard | P2 | No rounds, and the plan and the handoff both say no independent review of the self-certified work will happen |
| N9 | new | D1 | The reviewer's brief includes L1's and L2's locations or subjects as risks to check, and does not limit the review to them |
| G6 | guard | D1 | The reviewer's brief does not carry the developer's reassurances ("it was fine", "I think this is safe", "obviously right choice") |
| N10 | new | D1 | L1 and L2 each get a hardening log entry with a disposition |
| N11 | new | D2 | The orchestrator itself logs L1 and L2 to the wiki backlog through wiki-project, before delivery |
| G7 | guard | D2 | Delivery then proceeds without an added review round or a question asking for one |
| N12 | new | D3 | The orchestrator logs L2 to the wiki backlog through wiki-project before delivery |
| G8 | guard | D3 | Delivery then proceeds without an added review round or a question asking for one |

# brief-me, challenge and green-field behavior validation

Date: 2026-11-24. [Scenarios and expectations](thinking-skills-scenario.md). One run per scenario per
condition, each in a fresh general-purpose agent. The six baselines ran first, before any skill text
existed. The with-skill runs followed, so the two conditions were not spawned in the same turn. Agents
in both conditions also carried the user's global instructions, which ask for research before options
and for ranked options. The skills' author graded the runs.

## Results

| ID | Baseline | With skill |
| -- | -------- | ---------- |
| E1 | B1 fails (13 tool calls, covering code, wiki and web); B2 passes | pass |
| E2 | B1 partial; B2 fails (one blanket disclaimer) | pass |
| E3 | fails in both | pass |
| E4 | fails in both | pass |
| E5 | pass | pass |
| E6 | fails (five-step plan) | pass |
| E7 | fails (four execution checks) | pass |
| E8 | fails in both | pass |
| E9 | partial: blind and fresh, but paraphrased the proposal and asked for "the timing arithmetic" | pass |
| E10 | fails in both | pass |
| E11 | fails in both (one design each) | pass (7 and 6 sketches) |
| E12 | fails in both | pass |

## Baseline failures, verbatim

- **B1:** "**Recommendation:** don't commit to the queue yet. Measure one run first." Ranked options,
  dated next steps and web citations followed.
- **B2:** "This is from general Postgres knowledge; I haven't seen your system." Later, "**What to push for**".
- **C1:** "**What I'd do instead, in order**", then five steps.
- **C2:** "The staging test probably didn't exercise production concurrency, so check these when you run it".
- **G1:** "When the constraints come back, the vendor freeze may block less than it seems." Also "**If you
  do one piece first, I'd replace the CSV and hand keying with draft POs for buyers to approve.**"
- **G2:** "**Keep the hour and the slides, but stop presenting.**" Also "**Fixed:** the director gets a Monday
  meeting, and the PMO gets its template."

C1 and C2 already reached the right verdict without the skill. What challenge adds is the offer, the
restraint and a verbatim brief.

## With-skill evidence, verbatim

- **B1:** "The project folder is `shop`. I haven't looked inside it for this brief." It ends "Shall I go
  ahead with all five, or a subset?"
- **B2:** "*From training, unverified here, and possibly out of date.*"
- **C1:** "The better direction is to find where the minutes go, then act on the file's arrival time, the
  slow steps, or what has to wait for the file."
- **C2:** "Nothing that I think should change the plan." "**Verdict: it holds up.**"
- **G1:** "So if every count were perfect tomorrow morning, what would you still not know?"
- **G2:** "**Set aside:** the meeting, its hour and its day, the slides, the template, the minutes, the
  director's insistence and the PMO's mandate."

## Triggers

A fresh agent given only the frontmatter of all ten skills chose a skill for 15 prompts, including near
misses (a code review, a new repository, a research task, being stuck). Its choices followed the
descriptions, and it did not load the invoke-only skills. "Where do we stand on the import bug?" went to
brief-me as the text then asked, which would have blocked an ordinary status check. "What do we know
about", "where do we stand on" and "catch me up on" were replaced with the narrower "what do we know so
far about", plus an exclusion for status checks. A second fresh agent then matched intent on 7 of 7
prompts, with three status or catch-up requests going to no skill.

## other-guy

rubber-duck was renamed other-guy and made invoke-only. A structural check failed 6 of 7 before the
change and passes 7 of 7 after. The body changed only in the name, the wording for the consulted model
and the record folder (`docs/other-guy/`). No consult was run. Existing records stay in
`docs/rubber-duck/`.

## Limits

- brief-me's research step was not run, and no real blind evaluation was launched.
- Skill text was read from a file rather than loaded by the host. The trigger tests are choices from a
  listing, not live invocations.
- brief-me's triggers were narrowed after its with-skill runs. Its body did not change.

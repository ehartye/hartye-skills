# spec-plan-ii behavior validation

Date: 2026-11-08. Baseline: `177ac5f` (0.10.1), with spec-plan's `SKILL.md` and
`references/spec-template.md` loaded. Test condition: spec-plan-ii's `SKILL.md` (git blob
`65dc564495977f4a7a7e9cee1a1749342ea48682`) and `references/spec-template.md` (git blob
`b0bcb0791e35cdfaf89a079b789805f1acb04be5`).

This is process-documentation validation, not a live wiki or implementation test. The
[fixture](spec-plan-ii-scenario.md) supplies every wiki, repository, reviewer and user fact. No
wiki was read or written, no code ran, and no subagent was launched by the test agents.

## Method

- Each scenario ran in a fresh general-purpose agent. The agent read only the condition's
  `SKILL.md`, its template, and a copy of the fixture holding the shared fixture plus that one
  scenario section and its variants. The **Expectations** section was never given to any test
  agent, and no agent saw another run's output.
- Variants shared their parent scenario's run, with the prompt asking for each variant as a
  separate run. S1b, being a different stage, ran on its own. That is four runs per condition.
- Red step: the four baseline runs ran first, before any spec-plan-ii text existed.
- Fixture clarification: the first S2 baseline run pointed out that "cells beginning with `-` are
  prefixed" would also prefix negative amounts. That was a fixture defect unrelated to any
  expectation, so the decision was narrowed to "description cells". The S2 baseline was then
  re-run on the clarified fixture in the same turn as the four spec-plan-ii runs. The rerun is
  recorded below. The first run's excerpts are under "S2 — first baseline run".
- Green step: the four spec-plan-ii runs.
- One sample per scenario per condition, matching the repo's earlier records. Excerpts are
  verbatim; `…` marks an omission.

## Results summary

| Scenario | Expectation | Baseline (spec-plan) | spec-plan-ii |
| -------- | ----------- | -------------------- | ------------ |
| S1 | E1 orchestrator drafts | PASS (regression guard) | PASS |
| S1 | E2 grounding and research before drafting | PASS (regression guard) | PASS |
| S1 | E3 self-review before sanity check | FAIL | PASS |
| S1 | E4 blind, three-lens, broad brief allowing "no concerns" | FAIL | PASS |
| S1 | E4b checker's spec carries no self-review notes (added in remediation) | not run | PASS (remediation run) |
| S1 | E5 disagreement to user; agreement adopted | FAIL | PASS |
| S1b | E6 self-review and sanity check before planning | FAIL | PASS |
| S2 | E7 no rigor | FAIL | PASS |
| S2 | E8 TDD → dev → certify triple, certification evidence | FAIL | PASS |
| S2 | E9 three rounds as a ceiling, placement, reviewer inputs | FAIL | PASS |
| S2 | E10 spike gets no TDD, certification or hardening | PASS (regression guard) | PASS |
| S2b | E11 plan records 2 | FAIL | PASS |
| S2c | E12 no-independent-review warning in plan and handoff | FAIL | PASS |
| S3 | E13 borderline-up classes | FAIL | PASS |
| S3 | E14 dispositions, refuted COMPLIANCE to user first | FAIL | PASS |
| S3 | E15 original developer, through the triple | PASS (regression guard) | PASS |
| S3 | E16 pause and ask when rounds are exhausted | PASS (regression guard) | PASS |
| S3b | E17 clean final round proceeds | PASS (regression guard) | PASS |
| S3c | E18 early stop | PASS (regression guard) | PASS |
| S3d | E19 fresh agent with brief, certification evidence, findings | FAIL | PASS |

Every scenario has at least one baseline failure: S1 (E3, E4, E5), S1b (E6), S2 (E7, E8, E9,
E11, E12) and S3 (E13, E14, E19). spec-plan-ii met all nineteen expectations on the first
iteration of the skill text; no revision was needed.

## Baseline (spec-plan) evidence

### S1 — spec authoring

- **E1 PASS, E2 PASS (regression guards).** The agent drafted and saved the spec itself, after
  the wiki search and the research round:

  > | 8 | Me | Draft the spec from the template. …
  > | 9 | Me, via wiki-master:wiki-project | Save the spec at `wiki/authored/ledger/backlog/csv-export.md` …

- **E3 FAIL.** No self-review of the saved draft. The fresh-agent review came straight after the
  save:

  > | 10 | Subagent D (fresh reviewer, used for this review only) | Review the saved draft. | Nothing; it returns a report |

- **E4 FAIL.** The brief passed the interview decisions, asked for a fine-grained correctness and
  acceptance check, named no false-premise, KISS/YAGNI or blind-spot lens, and offered only PASS
  or CHANGES NEEDED:

  > **User's interview decisions:**

  > 4. Every acceptance criterion is observable: the command exists, reads the named artifact and can show the stated result. Run only checks that are safe and meaningful before a build

  > **Return:** numbered findings. … Then give a verdict of PASS or CHANGES NEEDED.

- **E5 FAIL.** The disagreed point was declined by the agent on its own, and the agreed point was
  parked for the user instead of adopted:

  > **Finding 2, declined.** … I've kept the scope as you set it and recorded the finding as declined in the spec. If you want to reopen server-side export, say so and I'll treat it as a scope change.

  > Status: confirmed; awaiting the user's decision … Revision not yet made.

### S1b — a spec from another workflow

- **E6 FAIL.** The agent made the review conditional on a rigor answer, and the review it would
  run receives the interview decisions:

  > **Q1. Rigor.** Recommended: **enhanced**.

  > **7. If the user picks a spec review (A or B), run it.**

  > If the user picks C, I record the spec review as not selected, with the user's choice as the reason.

### S2 — planning (rerun on the clarified fixture)

- **E7 FAIL.** Rigor appears throughout:

  > **Section 1: csv-export.** Build spec. Rigor: *pending* (recommended: standard spec, enhanced plan).

- **E8 FAIL.** TDD pairs exist only under a conditional enhanced selection, and there is no
  certification task or evidence:

  > * **WP1-TDD [EP]** (same agent as WP1-DEV): write tests for commas, quotes, CR/LF, empty rows and all four formula prefixes.

- **E9 FAIL.** The argument was not applied:

  > **About `hardening=3`:** the skill does not recognise this argument. Its only rigor options are `rigor=standard` and `rigor=enhanced`. I have not treated it as a rigor choice or a number of review rounds

- **E10 PASS (regression guard).** The spike section has no TDD task, certification or review
  round; no package in this plan has hardening:

  > * **xlsx-export/WP-S1 Prototype.** Owns the throwaway `spike/xlsx` branch in its own worktree. Depends on: none.

  > * Done when: a measurements report and a verdict exist.

- **S2b, E11 FAIL.** No round count is recorded:

  > * Question 1 reads: "Neither saved spec records a rigor. Which do you want for each? Recommended: csv-export standard spec with enhanced plan rigor; xlsx-export standard."

- **S2c, E12 FAIL.** No statement that the self-certified work goes unreviewed:

  > * The argument note reads: "**About `hardening=0`:** the skill does not recognise this argument. I have not read it as `rigor=standard`, as 'no reviews', or as declining any enhancement.

### S2 — first baseline run (before the fixture clarification)

The same expectations failed. E9 and E7:

> - **Arguments:** this skill only accepts `rigor=standard|enhanced`. `hardening=3` is not one of its options, so I have not applied it. I've turned it into Decision Q1 below.

> #### Section 1: csv-export (build; rigor: standard, pending Q1)

E8, with TDD only under a conditional option and no certification:

> **If you choose Q1 option A, the plan adds:**
> - In csv-export/WP1 and WP2, a separate TDD task right before each development task, owned by the same agent.

E11 and E12:

> - **Arguments line:** no rigor argument was given. Each spec keeps its saved rigor. Neither records one and neither selected an enhancement, so both are **standard**.

> - **Arguments line:** this skill only accepts `rigor=standard|enhanced`, and `hardening=0` is not one of its options. Both specs keep their saved standard rigor, which is already the lowest level, so `hardening=0` changes nothing and I'm not asking about it.

The defect it raised:

> the formula-guard rule quotes cells that begin with `-`. `amount` is a signed number of integer cents, and ledger debits are normally negative.

### S3 — hardening triage

The agent noted the skill defines none of this, then improvised:

> The spec-plan skill defines no `hardening` argument, review rounds, certification, or the COMPLIANCE / IMMINENT / EDGE / BEST-PRACTICE classes.

- **E13 FAIL.** F1 kept the lower of its two labels:

  > - **Class:** COMPLIANCE. … I don't assign IMMINENT. The fixture doesn't show that production descriptions contain newlines.

- **E14 FAIL.** F2 was rejected by the agent alone, and the EDGE item was neither fixed nor logged
  to the backlog:

  > - **Disposition:** rejected, with that evidence recorded. "Fixing" it would cause a regression.

  > - **Disposition:** declined. Noted as out of scope.

- **E15 PASS (regression guard).**

  > `dev-wp1` fixes it. It wrote WP1, its context is intact, and the test task and fix stay with the same developer.

- **E16 PASS (regression guard).** It held delivery and asked:

  > I'm holding WP3 (the draft PR). The F1 fix lands after the last planned review round, and the plan requires a fresh review of a fix before later work uses it.

- **S3b, E17 PASS (regression guard).**

  > Round 2 of 2 found nothing, so hardening is done. … I've opened the draft PR

- **S3c, E18 PASS (regression guard),** with a hedge the fixture does not resolve:

  > I treat the round count as a ceiling, not a quota, so hardening stops and rounds 2 and 3 are not run. If the plan defines hardening as a fixed number of rounds, I'd run rounds 2 and 3 with fresh reviewers instead.

- **S3d, E19 FAIL.** A fresh agent got the brief and the findings, but not the certification
  evidence:

  > - The WP1 package brief and owned files (`src/csv.ts`, `tests/csv.test.ts`).

  > - F1 verbatim, with its location, evidence and my verification result.

## spec-plan-ii evidence

### S1 — spec authoring

- **E1 PASS.** Subagents only reported; the orchestrator drafted and saved:

  > | 11 | Me | Draft the spec myself and save it through wiki-master:wiki-project at `wiki/authored/ledger/backlog/csv-export.md` …

  > | 6 | Subagent B, the only research worker | … | Only the evidence page `wiki/sources/OWASP — CSV Injection.md` |

- **E2 PASS.** Search, gap report with research proposal, and research all precede the draft at
  row 11:

  > | 3 | Subagent A | Wiki search for related knowledge and roadmap items (brief A). | Nothing (report only) |
  > | 4 | Me | Tell the user what the wiki covers and what it misses, and propose a research round. | Nothing (message) |
- **E3 PASS.**

  > | 12 | Me | Self-review the spec as saved against the four checks, fix what I find, and record the result in Review. | Updated spec |
  > | 13 | Subagent D, a fresh agent | Blind sanity check (brief D). | Nothing (report only) |

- **E4 PASS.** The brief carries only the verbatim request, the path and read-only access:

  > The user's request, verbatim: "Spec the csv-export change for the ledger project, and have it checked independently before it's ready for planning."

  > Please try to disagree with it, through three lenses: (a) a false premise: are we thinking about this wrong? (b) an architectural anti-pattern, over-engineering, or a KISS or YAGNI breach; (c) blind spots: things not considered at all.

  > This is not a line-by-line review of process or wording. Return a few points, each with its reason and what it would change in the spec. "No concerns" is a valid result.

- **E5 PASS.**

  > - Adopted: Blind spot, the `date` column was not defined … Change: Decisions, AC2 and the WP1 brief now state that the `date` column is the stored date's calendar date

  > **Needs your decision:** the reviewer says exporting in the browser is the wrong premise. … I disagree. … **My recommendation:** keep the browser export as specced, and revisit only if ledgers grow by orders of magnitude.

  > Do you want to keep the browser export, or move to server-side export?

### S1b — a spec from another workflow

- **E6 PASS.**

  > The spec has no Review section and no review record exists anywhere. The skill says to run Stage 1 steps 8 to 10 on it before planning and not to ask whether to.

  > **4. Self-review the spec as saved (Stage 1 step 8). (Me, in my own context.)**

  > **5. Run the blind sanity check (Stage 1 step 9). (A fresh subagent that has not seen this work.)**

  > Planning begins straight after the save in step 6, still in Default mode on the delegated path.

### S2 — planning

- **E7 PASS.** The plan never mentions rigor; its argument line reads:

  > **Arguments:** `hardening=3`, so **N = 3**. N comes only from the argument; neither spec carries a round count.

- **E8 PASS.**

  > 1. **TDD:** write the AC1 cases in `tests/csv.test.ts` … Run `npm test -- csv` and confirm it fails because `src/csv.ts` doesn't exist or doesn't behave yet.

  > - Evidence: the raw test-runner output, a diff of `tests/csv.test.ts` since the red run, and an explicit flag for any test changed after red or believed to contradict the spec.

- **E9 PASS.**

  > | csv-export/H1–H3 | Hardening rounds, up to 3 | WP1 and WP2 certified | a fresh reviewer each round | pending |

  > - N is a ceiling, not a quota.

  > **Reviewer.** Each round uses a fresh independent subagent. It is not a developer, not the orchestrator, and not an earlier round's reviewer.

  > - **It never gets** the developers' narrative conclusions.

  > - **It gets:**
  >   - the spec and its AC1 to AC3;
  >   - the `CONTRIBUTING.md` rules and the strict-TS rule;
  >   - the resulting artifacts and the diff since T0;
  >   - the latest certification evidence (raw outputs, test diffs since red, flags).
- **E10 PASS.**

  > | 2 | `wiki/authored/ledger/backlog/xlsx-export.md` | spike | planned | none (a spike gets no TDD, certification or hardening) |

- **S2b, E11 PASS.**

  > - **Arguments:** no `hardening` argument, so **N = 2** (the default).

- **S2c, E12 PASS.** In the plan and in the handoff:

  > - **Hardening section:** "csv-export hardening (N = 0): no rounds are planned. No independent review of the self-certified work will happen."

  > - "**Hardening.** csv-export: N = 0. No independent review of the self-certified work will happen. xlsx-export: none, because it is a spike."

### S3 — hardening triage

- **E13 PASS.**

  > | F1 | **IMMINENT** | The reviewer gave it two classes, so it takes the higher. Multi-line descriptions are silently dropped from the export, which is definite data loss. |

  > | F3 | **BEST-PRACTICE** | The reviewer gave it two classes, so it takes the higher.

- **E14 PASS.** F2 waits for the user, F3 is fixed with a reason, F4 is logged by the
  orchestrator, and each goes into the log:

  > | F3 | **BEST-PRACTICE** | … | **Fix.** The change is small and low-risk, and it fits the objective of exports people open in spreadsheets.

  > **Waiting for the user.** I recommend refuting it with no code change. Nothing is done until the user decides.

  > **Log to the backlog.** I write it myself through wiki-master:wiki-project as `wiki/authored/ledger/backlog/csv-export-progress-indicator.md` (`kind: backlog-item`).

  > - R2 / F4 / EDGE / threshold above real data (max 5,000 rows) / logged / no production ledger reaches 10,000 rows / `[[csv-export-progress-indicator]]`

- **E15 PASS.**

  > **F1: `dev-wp1`**, continued in place with its context intact through SendMessage, because it owns `src/csv.ts` and is still available.

  > 1. **TDD.** Add tests in `tests/csv.test.ts`:

  > Run them and confirm they fail as expected: the field comes out as `Line one`.
  > 2. **Dev.** Change `src/csv.ts:30` so the full description is kept and quoted, then refactor while the tests stay green.

  > 3. **Certification.** Run `npm test` (the full suite), plus `npm run lint`, `npm run build` and WP1's acceptance commands. It returns:
  >    - the raw runner output;
  >    - a diff of the test files since the red step;
  >    - an explicit flag for any test changed after red, or any test it believes contradicts the spec.
- **E16 PASS.**

  > So I pause before delivery, ask the user for more rounds or permission to deliver, and wait. F2 is also still open. WP3 (draft PR) does not start.

- **S3b, E17 PASS.**

  > I go straight to WP3 (draft PR) under the execution authority recorded in the plan.

- **S3c, E18 PASS.**

  > Round 1 had no IMMINENT or COMPLIANCE findings, so once those two are dispositioned the early stop applies. Hardening ends and I go to WP3, even though rounds 2 and 3 remain unused.

- **S3d, E19 PASS.**

  > **A fresh developer agent fixes F1.**

  > - **WP1's original package brief:** goal, owned files (`src/csv.ts`, `tests/csv.test.ts`), interfaces, constraints, the `CONTRIBUTING.md` rules and done-when.
  > - **WP1's certification evidence:** the latest re-certification from the round-1 fix, plus the original.
  > - **The findings:** F1 with its class (IMMINENT), location (`src/csv.ts:30`) and evidence.

## Structural checks

- Rule ceiling: superseded by the directive count under "Remediation" below. The first text's
  step 3 of Stage 2 carried 11 directives by that count.
- `grep -rnE 'spec-plan($|[^-])' skills/spec-plan-ii`: no output.
- `grep -rniwE 'rigor' skills/spec-plan-ii`: no output.
- The sanitization pattern from acceptance criterion 4, over this skill's `SKILL.md`, its
  template and both `docs/testing/spec-plan-ii-*.md` files: no output.
- `python -B skills/yoda/scripts/audit_scan.py skills/spec-plan-ii`: exit 0, no findings.

## Limits

- One sample per scenario per condition. Variants shared a run with their parent, so a variant's
  answer could be shaped by the parent's.
- S3 tests what the skill text tells an orchestrator to do with a round's findings. It does not
  run a real executor against a real plan.
- The sanity-check and reviewer reports were fixed by the fixture, so the runs check the briefs
  and the triage, not what a real reviewer would return.

## Remediation, 2026-11-08

An independent package review found five problems. Each got a failing check first, then a fix.
Tested text: `SKILL.md` git blob `d6012ad20684b31b70558658aa2b73223719075a`, template git blob
`623d23115078461fbf03acf4220ff05c63908f4c`, fixture git blob
`1aa7ec25ba7f6853578bf682fd2d1eef10794b2f`.

### Findings and their checks

| # | Finding | Check | Before | After |
| - | ------- | ----- | ------ | ----- |
| 1 | The self-review was recorded in the Review section before the sanity check, so the checker could read it | fixture defines E4b; skill no longer records the self-review before the check; template defers Review until the check returns | FAIL ×3 | PASS ×3 |
| 2 | Four numbered steps exceeded 6 directives | directive count per step, limit 6 | FAIL (6 steps over, maximum 11) | PASS (maximum 6) |
| 3 | Five results claims were paraphrased, and one claim had no record | grep for each paraphrase | FAIL ×6 | PASS ×6 |
| 4 | The description read as a sequence | sequence words (`then`, `followed by`, `after`, `before`, `next`) in the description | FAIL | PASS |
| 5 | Decision 19 wording left a spec with only one of the two records undefined | old wording absent; "lacks a record of either" present | FAIL ×2 | PASS ×2 |

### Changes

- `SKILL.md` Stage 1 step 8 fixes the spec's text but keeps the self-review's record out of the
  spec until the sanity check returns. Step 10 writes the whole Review record.
- The template's Review section stays at "Pending." until the check returns.
- Stage 2 steps were split: select, reconcile, review a spec without a record, the triple, the
  certification evidence and the spike exemption are now separate steps. Stage 1 steps 6, 7 and 9
  were trimmed.
- Stage 2 step 3 now runs whichever record is missing, and records a lone self-review directly.
- The description is now "Writes and plans wiki-grounded specs with self-review, blind sanity
  checks, test-first self-certified development and independent hardening rounds."
- The fixture asks S1 for the Review section twice, as the checker reads it and at handoff, and
  defines E4b.
- Results: the paraphrased claims above are now verbatim quotes, and the first S2 baseline run is
  recorded.

### Directive count

Method: within each top-level numbered step, drop the step's bold title, blank code spans and
quoted strings, and split the rest at sentence ends: `.`, `?` or `;` followed by whitespace, and
`:` at the end of a line. Each non-empty piece is one directive. This counts more strictly than
the review did (it found 9 for Stage 2 step 3; this method found 11).

| Stage 1 step | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| ------------ | - | - | - | - | - | - | - | - | - | -- |
| Before | 3 | 5 | 5 | 3 | 5 | 7 | 7 | 7 | 9 | 6 |
| After | 3 | 5 | 5 | 3 | 5 | 5 | 5 | 4 | 5 | 5 |

| Stage 2 step (after) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| -------------------- | - | - | - | - | - | - | - | - | - |
| Directives | 4 | 4 | 5 | 6 | 3 | 2 | 3 | 4 | 5 |

Before the split, Stage 2 had six steps, counting 9, 5, 11, 3, 4 and 5.

### Re-runs (spec-plan-ii, fresh agents)

S1 and S2 re-ran, each in a fresh agent given only spec-plan-ii's `SKILL.md`, its template and a
fixture copy with the Expectations section removed. No behavior regressed.

**S1:** E1, E2, E3, E4, E4b and E5 PASS.

- **E1 and E3 PASS.**

  > | 8 | Me | Draft the spec from the interview and evidence, then save it through wiki-master:wiki-project to `wiki/authored/ledger/backlog/csv-export.md` with `kind: backlog-item`, `backlog-status: planned`, and Review set to "Pending." | The spec |
  > | 9 | Me | Self-review the spec as saved against the four checks, fix the text, and save again. The self-review record stays in my own context, not in the wiki. | Revised spec, Review still "Pending." |
  > | 10 | Subagent (fresh, has not seen this work) | Blind sanity check (brief D). Returns the fixture's two points. | Nothing (report only) |

- **E2 PASS.**

  > | 4 | Me | Report wiki coverage and the formula-injection gap to the user, and propose one research round. The user answers "Yes, run it." | Nothing |

- **E4 PASS.**

  > Your job is to disagree with the spec where it deserves it. Look through three broad lenses:

  > This is not a line-by-line review of process, formatting or wording. Return a few points at most, most important first. For each, give the lens, the point, your reason (with repository or wiki evidence where you have it), and what it would change in the spec. "No concerns" is a valid and useful result.

- **E4b PASS.**

  > **As it stands when the sanity checker reads the spec:**
  > ```markdown
  > ## Review
  > Pending.
  > ```

- **E5 PASS.**

  > - Adopted: Blind spot — the spec never said what the `date` column shows

  > **Disputed, needs your decision:** the reviewer says browser export is a false premise.

  > - **Recommendation:** keep the browser export as specced.

**S2:** E7, E8, E9, E10, E11 and E12 PASS.

- **E7 PASS.** The plan contains no rigor level, parameter or section; its header reads:

  > **Hardening:** N = **3**, from the argument `hardening=3`. It applies to csv-export, the only build spec. xlsx-export is a spike, so it gets no TDD, certification or hardening.

- **E8 PASS.**

  > ### csv-export/WP1: Serializer. One developer agent (D1) runs the whole triple.

  > - **TDD:** write `tests/csv.test.ts` covering commas, quotes, CR/LF, empty rows, formula prefixes and the unconverted date. Run `npm test -- csv`, confirm it fails as expected, then **commit the red state**.

  > - **Evidence:**
  >   - raw runner output from `npm test` and `npm test -- csv`;
  >   - `git diff <red-commit> -- tests/`;
  >   - an explicit flag for any test changed after red, or any test D1 believes contradicts the spec.

- **E9 PASS.**

  > - N = 3 is a ceiling, not a quota.
  > - Rounds run after WP1 and WP2 are certified and before WP3.

  > **Reviewer.** Each round uses a fresh, independent subagent. It is not a developer, not the orchestrator, and not an earlier round's reviewer.

  > - **It never gets** the developers' narrative conclusions.

- **E10 PASS.**

  > ## Section 2: xlsx-export (spike, no TDD, certification or hardening)

- **S2b, E11 PASS.**

  > - **Header:** "**Hardening:** N = **2**, the default, because no `hardening=` argument was given."

- **S2c, E12 PASS.**

  > - **Header:** "**Hardening:** N = **0**, from `hardening=0`. No hardening rounds are planned. No independent review of the self-certified work will happen."

  > - **Handoff, Hardening:** "csv-export: N = 0. No independent review of the self-certified work will happen. xlsx-export: none, because it is a spike."

S1b and S3 were not re-run. Their expectations rest on Stage 2 step 3 (formerly step 2) and the
hardening contract. The contract is unchanged. Step 3's change widens when it fires, from both
records missing to either missing, which S1b's both-missing case still meets.

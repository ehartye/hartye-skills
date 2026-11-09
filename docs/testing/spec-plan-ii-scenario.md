# spec-plan-ii behavior scenarios

This is a simulation: no live wiki, code edits, subagent launches or external actions. Treat the
facts below as verified fixture evidence. Where an action would delegate to a subagent, write the
brief you would send and use the fixture result given for it. Return the artifact or decision you
would produce. Do not read other task files except the skill files your assignment supplies.

Each test agent receives one scenario section (with its variants) and the shared fixture. The
**Expectations** section at the end is for grading only and is never given to a test agent.

## Shared fixture

Project `ledger`, repository `ledger-app`. The wiki overview's `repo:` field is `ledger-app`.
Subagents are available. wiki-master is available.

Repository facts (from read-only exploration):

- TypeScript, strict mode. `npm test` runs vitest; `npm run build` runs tsc and vite;
  `npm run lint` runs eslint; `npm run smoke` runs a Playwright browser smoke test.
- `src/filters.ts` exports `selectFilteredTransactions(state): Transaction[]`, in display order.
- `Transaction` is `{ date: string /* ISO 8601 with offset */; description: string; amount: number /* integer cents */ }`.
- No CSV code exists. The largest ledger in production has 5,000 rows.
- `CONTRIBUTING.md` requires lint-clean code, no `any`, and a test for every bug fix.

## S1 — spec authoring

User: "Spec the csv-export change for the ledger project, and have it checked independently
before it's ready for planning."

Host: Default mode.

Interview answers already in the conversation (no further questions are needed):

- Goal: a user can download the currently filtered transactions as a UTF-8 CSV file.
- Scope: a CSV serializer library function and an Export button. Build, not a spike.
- Non-goals: imports, background exports, any server change.
- Decisions: columns `date,description,amount`; RFC 4180 quoting; filtered row order kept;
  empty rows produce the header only; file name `transactions.csv`.
- Delivery: a draft PR with validation evidence. The user authorizes that and nothing further.

Fixture results for actions you may take:

- **Wiki search:** no backlog item overlaps csv-export. `wiki/authored/ledger/architecture.md`
  documents the filter selector. Gap: no wiki page covers spreadsheet formula injection (cells
  that begin with `=`, `+`, `-` or `@`).
- **If you propose a research round, the user answers:** "Yes, run it." Its result: one source
  page, `wiki/sources/OWASP — CSV Injection.md`, which recommends prefixing such cells with a
  single quote.
- **If you propose tools, the user confirms:** the project test runner (vitest) and the browser
  smoke test.
- **Any independent check of the saved spec that you commission returns exactly this report,
  whatever its brief says:**
  1. *Blind spot.* The spec never says what the `date` column shows. `Transaction.date` carries an
     offset, so the same transaction can show a different day depending on how it is formatted.
     Change: state that the column is the stored date's calendar date, unconverted.
  2. *False premise.* Exporting in the browser is the wrong premise. Large ledgers should export
     on the server as a background job. Change: move the serializer to the API and email a link.

Task. Return:

1. An ordered list of every action from now to spec handoff. For each, name who performs it (you,
   or a subagent) and what, if anything, that performer writes or saves.
2. The full brief you give each subagent, verbatim.
3. The section of the saved spec that records its review, twice: exactly as it stands when any
   independent check reads the spec, and exactly as saved at handoff.
4. Every message you send the user after the research round, verbatim.
5. Your closing handoff line.

### S1b — a spec from another workflow

User: "Plan the ready budget-alerts spec for ledger. You're authorized to plan outside Plan mode
while I'm in Default mode; save the plan to `docs/plans/`."

Host: Default mode. This is a separate run from S1.

`wiki/authored/ledger/backlog/budget-alerts.md` was written by another workflow. Its frontmatter
has `kind: backlog-item` and `backlog-status: planned`. Its sections are Goal, Decisions,
Acceptance criteria, Work packages (WP1 threshold model, WP2 alert banner) and For the planner.
It has no section recording any review, and no record of one exists anywhere. Its decisions are
settled, and they match the current repository.

Fixture results: a re-read of the spec finds nothing to fix. Any independent check you commission
returns "No concerns."

Task. Return the ordered actions you take before the first plan step is written, who performs
each, and whether and when you begin planning. Stop before writing the plan itself.

## S2 — planning

Invocation arguments: `hardening=3 Plan the ready csv-export and xlsx-export specs together.`

Host: Plan mode. Present the plan in your reply.

**Spec `wiki/authored/ledger/backlog/csv-export.md`** (build, `backlog-status: planned`, has a
For the planner section). Its decisions are those of S1, plus "the date column is the stored
calendar date, unconverted" and "description cells beginning with `=`, `+`, `-` or `@` are
prefixed with a single quote". Its Review section records a self-review with no open items and
a sanity check from 2026-11-01: the date point was adopted; the server-export point was disputed
and the user decided to keep the export in the browser. Recommended tools: vitest and the browser
smoke test.

- AC1: `npm test -- csv` passes the cases for commas, quotes, CR/LF, empty rows and formula
  prefixes.
- AC2: `npm run smoke` downloads `transactions.csv` with the exact expected bytes for a fixture of
  two filtered rows.
- AC3: `npm test`, `npm run lint` and `npm run build` pass, and the draft PR links the evidence.
- WP1 Serializer. Owns `src/csv.ts`, `tests/csv.test.ts`. Depends on none. Done when AC1 passes.
- WP2 Export button. Owns `src/ExportButton.tsx`, `tests/export.test.tsx`. Depends on WP1.
  Done when AC2 passes.
- WP3 Deliver. Owns `docs/export-checks.md`. Depends on WP2. Opens a draft PR with the
  evidence. Done when AC3 passes.

**Spec `wiki/authored/ledger/backlog/xlsx-export.md`** (spike, `backlog-status: planned`, has a
For the planner section). Question: given SheetJS community edition, when 5,000 rows are written
in the browser, then the gzip bundle grows by under 300 KB and the write takes under 500 ms. Exit
criteria: validated, partial and invalidated, each with its deliverable. WP-S1 builds a throwaway
prototype on a `spike/xlsx` branch and reports the measurements. Its Review section records a
self-review and a sanity check with no concerns. It is independent of csv-export.

Task. Return the complete plan you present, and your handoff text. Then answer each variant as a
separate run, returning only the plan lines and handoff text that differ from your S2 answer:

- **S2b:** the arguments are `Plan the ready csv-export and xlsx-export specs together.`
- **S2c:** the arguments are `hardening=0 Plan the ready csv-export and xlsx-export specs together.`

## S3 — hardening triage

You are the orchestrator carrying out the approved plan for csv-export (S2's spec), made with the
skill you were given. Planning was invoked with `hardening=2`. The user is available.

State of the run:

- WP1 (developer agent `dev-wp1`) and WP2 (developer agent `dev-wp2`) are certified. Both agents
  are still available and can be continued with their context intact.
- WP1's certification evidence includes this raw runner output line:
  `✓ tests/csv.test.ts > empty rows produce header only`, and `src/csv.ts` line 12 reads
  `const lines = [HEADER];`.
- Round 1 (reviewer `rev-1`) found one COMPLIANCE item. `dev-wp1` fixed it and re-certified, and
  round 2 reviewed that fix.
- Round 2 of 2 (a fresh reviewer, `rev-2`) has just returned these findings:
  - **F1** — "COMPLIANCE, possibly IMMINENT (borderline)." `src/csv.ts:30` cuts each description
    at its first newline, so any multi-line description is silently lost from the export.
    Evidence: a two-line description exports as its first line only.
  - **F2** — "COMPLIANCE." The spec requires header-only output for empty rows, but WP1 returns an
    empty string. Evidence: reviewer's reading of `src/csv.ts`.
  - **F3** — "EDGE or BEST-PRACTICE (borderline)." The file has no UTF-8 byte-order mark, so Excel
    on Windows shows accented descriptions as garbled text.
  - **F4** — "EDGE." Add a progress indicator for exports over 10,000 rows.
- WP3 (deliver: draft PR) is the next package in the plan.

Task. Return: for each finding, the class you assign and why, your verification result and its
disposition; for anything fixed, who fixes it and the steps they follow; what you do once triage
is done, either proceeding to WP3 or something else; and any message to the user, verbatim.

Then answer each variant as a separate run:

- **S3b:** the same plan, but round 2 of 2 returns no findings. What happens next?
- **S3c:** the plan was made with `hardening=3`. Round 1 of 3 returns only F3 and F4. What happens
  once you have dispositioned them?
- **S3d:** as S3, but `dev-wp1`'s session has ended and cannot be continued. Who fixes F1, and
  what are they given?

## Expectations

For graders only. Each test agent sees neither this section nor any other run's output.

**S1 — spec authoring**

- **E1:** the orchestrator drafts the spec itself. Subagents only gather evidence.
- **E2:** the wiki search and the research proposal come before drafting.
- **E3:** a self-review of the saved draft comes before the sanity check.
- **E4:** the sanity-check brief gives the verbatim request, the saved spec path and read-only repo
  and wiki access; withholds the self-review and interview rationale; asks for disagreement through
  three lenses (false premise; anti-pattern, over-engineering or KISS/YAGNI; blind spots); is
  broad-strokes rather than a fine-grained process check; and allows "no concerns".
- **E4b:** the spec the sanity checker reads carries no self-review notes. The self-review may
  change the spec's text, but its record enters the Review section only after the check returns.
- **E5:** point 2 (disagreed) goes to the user with both positions and a recommendation, and the
  user decides; point 1 (agreed) is adopted and recorded in the Review section.
- **S1b, E6:** a self-review and a sanity check run before planning begins.

**S2 — planning**

- **E7:** no rigor level, parameter or section appears in the plan.
- **E8:** each development task is a TDD → dev → certification triple under one owner, and the
  certification evidence is raw test-runner output, a diff of the test files since red, and a flag
  for any test changed after red or believed to contradict the spec.
- **E9:** three hardening rounds as a ceiling, placed after csv-export's dev packages are
  certified and before its delivery package, with a fresh reviewer each round given the spec, its
  acceptance criteria, the project and quality rules, the artifacts and diff and the certification
  evidence, but not the developer's narrative.
- **E10:** the spike gets no TDD, certification or hardening.
- **S2b, E11:** the plan records 2 hardening rounds.
- **S2c, E12:** the plan and the handoff both state that no independent review of the
  self-certified work will happen.

**S3 — hardening triage**

- **E13:** classes are applied with the borderline-up rule: F1 IMMINENT, F3 BEST-PRACTICE.
- **E14:** IMMINENT is fixed; the refuted COMPLIANCE item F2 is surfaced to the user with its
  evidence before it is dismissed; BEST-PRACTICE and EDGE are each fixed or logged to the wiki
  backlog by the orchestrator, with a reason; every disposition goes into the hardening log.
- **E15:** F1 is remediated by `dev-wp1`, continued in place, through TDD → dev → certification.
- **E16:** because the rounds are exhausted and the F1 fix is unreviewed, the run pauses before
  WP3, states its evidence, and asks the user for more rounds or permission to deliver.
- **S3b, E17:** it proceeds to delivery.
- **S3c, E18:** hardening stops early after round 1, once F3 and F4 are dispositioned.
- **S3d, E19:** a fresh agent remediates F1, given WP1's package brief, its certification evidence
  and the findings.

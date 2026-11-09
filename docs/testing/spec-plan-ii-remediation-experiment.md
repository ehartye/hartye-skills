# Hardening remediation: original developer vs fresh agent

Date: 2026-11-08. This experiment tested a spec-plan-ii 0.11.0 rule: when a hardening round
returns findings, the original developer subagent should fix them, continued in place.

The alternative is a fresh subagent. It gets the package brief, the certification evidence, the
findings and the code, but none of the original developer's context.

**Verdict: inconclusive under the decision rule fixed in advance.**
- The fresh agent was never worse.
- It led on the primary metric in 1 of 3 trials, and was rated slightly better in another.
- It cost about three times the tokens.

## Method

The protocol and the decision rule were written before any result was seen.

**Fixture.** [`remediation-experiment/BRIEF.md`](remediation-experiment/BRIEF.md) specifies a CSV
export module with many edge cases. Two files check it, and no trial agent saw either one:
- [`remediation-experiment/test_hidden.py`](remediation-experiment/test_hidden.py): 38 hidden
  acceptance tests.
- [`remediation-experiment/ref/csvexport.py`](remediation-experiment/ref/csvexport.py): a reference
  implementation, used only to confirm the oracle passes 38/38.

**Steps.** Three independent trials, each run in its own scratch git repo.

1. **Develop.** A developer agent builds the module from the brief, using TDD, then development,
   then certification. It commits a red step and a green step and reports raw evidence.
2. **Harden.** A fresh reviewer gets the brief, the repo and the certification evidence, but not
   the developer's narrative. It returns classed findings: IMMINENT, COMPLIANCE, BEST-PRACTICE or
   EDGE.
3. **Disposition.** The orchestrator marks each finding fix, log or refute. The same rules apply
   across trials. Trials 1, 2 and 3 got 6, 6 and 4 fix items.
4. **Fork.** The repo is snapshotted and copied before either arm starts.
   - **Arm A (original):** the same developer agent is continued in place with the findings.
   - **Arm B (fresh):** a new agent gets the brief, the certification evidence, the findings
     and the code.

   Both arms get identical instructions: TDD, then dev, then certification for each fix item; no
   weakening of existing tests; leave log and refute items alone.
5. **Grade.** A blind grader per trial receives the two copies as X and Y. The mapping is
   randomized and sealed until every verdict is recorded. For each copy the grader:
   - runs the hidden tests;
   - writes its own adversarial probes per finding;
   - checks test integrity, including re-running the red commit;
   - checks scope and code quality.

**Decision rule.**
- *Primary metric:* fix items fully resolved.
- *Tie-breaks, in order:* hidden-test passes, regressions, test integrity.
- *Cost* is secondary.
- *Decisive* means one arm leads on the primary metric in at least 2 of 3 trials and never causes
  a regression the other avoids. Anything else is reported as inconclusive.

**Amendment made before remediation.** All three reviewers independently flagged that a
single-column record with an empty value comes out as a blank line, and that CSV readers drop
it. The brief allowed this, and the original oracle enforced it. The finding was accepted as a
spec clarification: such a record is written as `""`. The oracle and the reference were changed to
match, and every pre-remediation snapshot then failed exactly that one hidden test. Both arms in
each trial were graded against the same oracle.

## Results

| Trial | Fix items | Fully resolved: original / fresh | Hidden tests: original / fresh | Grader verdict |
|---|---|---|---|---|
| 1 | 6 | 6 / 6 | 38 / 38 | Fresh slightly better |
| 2 | 6 | **5 / 6** | 38 / 38 | **Fresh better** |
| 3 | 4 | 4 / 4 | 38 / 38 | Tie |

What the graders found:

- **Trial 1.** The two fixes were near-identical.
  - Fresh used a stricter range-tag check, which never calls an arbitrary `__eq__`. Its red
    commit already held every test it needed, and its probes covered more variants.
  - Original had a faster int path and a check that no rows are read before validation. It made
    one edit to an existing test in its green commit instead of its red commit.
- **Trial 2.** On the columns-validation finding, the original developer validated each entry but
  not the `columns` container.
  - `columns='ab'` was silently split into two columns, and `None` or `5` still raised the raw
    "not iterable" error that the finding quotes.
  - It also rejected non-string tuple keys, which goes beyond the brief.
  - The fresh agent resolved all six.
- **Trial 3.** The copies behaved identically on every probe, with small differences that
  cancelled out. Both made one test edit in green rather than red.

Across all six remediations: no hidden-test regression, no change to any log or refute item, and
every red commit genuinely failed for its finding's reason.

**Cost.** Figures are from agent task notifications.
- The original arm's tokens are the increase over the developer's earlier cumulative figure; the
  fresh arm's are its own total.
- Duration is the remediation run only.
- The reported counter appears to be cumulative, but the host does not document its exact
  meaning.

| Trial | Original: tokens / time | Fresh: tokens / time |
|---|---|---|
| 1 | +28.5k / 150 s | 87.7k / 170 s |
| 2 | +28.1k / 149 s | 86.9k / 172 s |
| 3 | +24.8k / 128 s | 90.9k / 215 s |

**Process.** An F1-overturned edit to an existing test landed in the green commit rather than the
red commit in 2 of 3 original remediations (trials 1 and 3) and in 1 of 3 fresh ones (trial 3).

## Limits

- **Short context.** The task is small, so the developer's context stayed short. The decay
  evidence that motivated this test describes long debugging sessions, and this design probably
  understates any such effect.
- **Ceiling effect.** Every build passed the hidden tests before hardening except the amended
  case. The hidden tests therefore could not separate the arms, and grading rested on adversarial
  probes and grader judgement.
- **Small sample.** There were three trials, all on one model with one grader each. Grader
  variance was not measured.
- **Shared dispositions.** The orchestrator dispositioned the findings itself, using one set of
  rules across trials.
- **Brief encoding.** The copy of the brief the trial agents received held a literal U+FEFF
  character where the brief means the `\ufeff` escape. Every agent read it correctly. The copies
  stored here use the visible escape.

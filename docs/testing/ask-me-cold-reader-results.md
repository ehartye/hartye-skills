# ask-me cold-reader behavior validation

Date: 2026-11-25. [Scenarios and expectations](ask-me-cold-reader-scenario.md). Three runs per scenario
per version (one for M3), headless on one Opus model with no tools, user instructions or plugins. "Before"
is the skill as released in 0.13.1. "After" is the exact shipped text.

## Results

18 runs per version: M1, M2, M4, M5, M6 and M7. Counts are totals over those runs.

| Measure | Before | After |
| ------- | ------ | ----- |
| Questions asked | 79 | 84 |
| Blocking references (E1) | 5 | 2 |
| Questions with an option whose effect is unclear (E2) | 3 | 2 |
| Questions whose recommendation reason is unclear (E3) | 3 | 2 |
| Questions not answerable with confidence | 4 | 2 |
| Claims the conversation does not support (E4) | 4 | 14 |
| Unresolved references the conversation could have explained (E9) | 72 | 28 |
| Headers over 12 characters (E5) | 2 | 0 |

**Verdicts.** E1 to E4 and E9 ask for none and are not met after the change, though E9 falls by more than
half. E4 gets worse. E5, E7 and E8 pass; E6 passes wherever it was checked mechanically.

Per scenario, E9 before and after: M1 13 to 1, M2 6 to 0, M4 24 to 8, M5 10 to 6, M6 (held out) 5 to 7,
M7 14 to 6. M3 passes in both: one line, no questions. Nothing already answered was asked again in either.
Before, two of three M2 runs asked four of the six pending items; after, all three asked all six.

Question text averages 61 words before and 137 after (longest 112 and 214), measured on the runs with
a native dialog. E5 is mechanical on M1, M2, M5 and M6; E6 is mechanical on those four.

The E1, E2 and E3 changes are small counts and could be noise on their own. E9 is the measure that moved.

## Baseline failures, verbatim

References the cold reader could not resolve:

- M1: "compare run 1", "the old job", "dual-write shim", "the backfill"
- M4: "I told you this was ready", "the compare"
- M5: "the guard", "which you agreed to", and the blocking "otherwise refunds" and "lose the new place"
- M7: the blocking "the old job started writing through the shim"

The intro ("answered in a few seconds") and the options rule ("its trade-off in a few words") worked
against explaining more, so both were replaced.

## What changed along the way

- The first wording asked for the cost and what waits on the answer every time. Unsupported claims rose
  from 2 to 16 on the 12 M1, M2, M4 and M5 runs ("No other work waits on this"), so those slots went and
  the last rule was added.
- A clause for tools whose options have no descriptions was dropped. M7 did no
  worse without it (no unclear options, against 1 with it).

## Limits

- Runs of near-identical wording varied: E4 gave 5, 10 and 14 over 18 runs, E9 21 to 28, E1 0 to 2. The
  E9 drop is well outside that spread. The rise in E4 is real but small per question. The entries after
  are mostly guessed reasons ("left FN-91 open so you could decide") and small inferences. Some are
  arguable: "The spec says a car is 4.5 and a van is 6" pairs two statements the conversation makes
  separately.
- The skill text was pasted into each prompt, not loaded by the host.
- M6, which no wording was tuned on, shows no improvement in E9. The baseline there was already low (5
  in 12 questions) and no blocking reference appeared in either version. Its unsupported claims went from 2 to 5. The tuned scenarios therefore
  probably overstate the general gain.
- M5 and E9 were added after the first baseline, M6 after the first edit, and M7 after the second. All
  ran against the old text as well as the new.
- The scenarios and the edit have the same author. The graders are models.
- Payloads were written out, not sent to a live dialog. How long question text looks in a real dialog is
  unverified. No Codex host was used.

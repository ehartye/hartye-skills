---
name: yoda
description: Use when writing, editing, or reviewing a SKILL.md, auditing a skill library, or when a skill never fires, fires but is ignored, triggers on wrong prompts, two skills compete, or a skill "doesn't seem to work."
---

# Yoda

## Overview

A skill fails silently. A broken `SKILL.md` throws no error — it just never gets invoked, or
gets invoked and ignored. Nothing in the toolchain tells you. The reference validator checks
frontmatter and naming; every other failure below passes it.

**Core principle:** a skill's value is the difference it makes, so the only real evidence is a
paired run — the task with the skill and without it. Everything before that is inspection, and
inspection cannot tell a well-written skill from a helpful one.

**Two entrances, one bar.** Auditing an existing skill and writing a new one differ only in
where you start. Both end at the same place: a baseline comparison.

## Which entrance

| Situation | Start at |
| --------- | -------- |
| Skill exists, something is wrong with it | Step 1 (Diagnose) |
| Skill exists, general review or library audit | Step 1, then Step 5 |
| New skill, no code yet | Step 3 (Baseline first) |

---

## 1. Diagnose before prescribing

Name the failure before touching the file. They have different fixes and the symptom tells you
which:

| Symptom | Failure | Where to look |
| ------- | ------- | ------------- |
| Never fires | Description doesn't match how anyone phrases the task | `description` — Step 2 |
| Fires on the wrong prompts | Description over-claims | `description` — Step 2 |
| Fires, then behaves as if unread | Description summarizes the workflow; the model follows the summary instead of the body | `description` — Step 2 |
| Fires, body read, one instruction ignored | That instruction is buried | Body position — Step 4 |
| Two skills fight | Overlapping triggers | Library level — Step 5 |
| Output worse than no skill | Net-negative | Only a paired run shows this — Step 3 |

You cannot diagnose the last one by reading. Say so rather than guessing.

## 2. The description is the whole triggering mechanism

It is the only part of a skill guaranteed to be read — name and description are preloaded for
every installed skill. The body is never consulted for whether to load.

**The hard constraint, which is undocumented:** Claude Code truncates each description to
**250 characters** in the `/skills` listing. The Agent Skills spec permits 1024. A description
can be spec-valid and lose three quarters of itself exactly where it does its job.
`SLASH_COMMAND_TOOL_CHAR_BUDGET` raises the *total* metadata budget across skills; it does not
lift the per-skill cap. **Everything that decides whether the skill fires must survive the
first 250 characters.**

Check it, don't estimate it:

```bash
awk -F'description: ' '/^description: /{print length($2)}' SKILL.md
```

**Write triggers, not a synopsis.** Concrete phrases a user would actually say, symptoms, error
strings, tool names. Third person. A description with no trigger conditions is the single most
common reason a skill never fires.

**On whether to also state what the skill does — the sources genuinely disagree, so decide
deliberately rather than assuming:**

- *Trigger-only.* A description that summarizes the workflow becomes a shortcut the model takes
  *instead of* reading the body. The reported case: a "code review between tasks" description
  produced one review where the skill's own flowchart specified two.
- *Both, and push.* Anthropic's own skill-creator says include what it does AND when, and make
  it "a little bit pushy," because models under-trigger skills more often than they over-trigger.

They optimize against opposite failures. Under-triggering means the skill never loads;
shortcutting means it loads and the body is skipped. Pick by which risk your skill actually
runs: a rarely-relevant reference skill fails by never firing, a multi-step discipline skill
fails by being summarized away. Never write a description that reads as a procedure the model
could follow on its own.

## 3. The baseline is the test

**Run the task twice — with the skill and without — and spawn both in the same turn.** Not the
with-skill runs first and the baselines later; same turn, so they are comparable and so you
cannot quietly skip the half that might embarrass the skill.

For a new skill this is test-first and the order is not negotiable: **watch an agent fail
without the skill, record the failure verbatim, then write the minimum that fixes exactly that.**
A skill written from imagination documents a failure mode you guessed at.

For an existing skill it is how you know a fix worked, and the only way to detect the failure
inspection cannot see: a skill that makes output *worse than none*. This is real and measured —
a monolithic skill scored 0.55 against vanilla's 0.77 and produced zero unit tests where vanilla
produced 30, while explicitly instructing "write tests."

**A skill's self-assessment is not evidence.** That same skill self-scored 0.92 on the output
containing none of the tests. If a skill grades its own compliance, that grade is a claim, not a
measurement.

Two to three realistic prompts is enough to start — the kind a real user would type, not
prompts written to make the skill look good. Add near-miss prompts that should *not* fire it;
a skill that fires on everything is as broken as one that never fires.

## 4. Structure, and why each rule exists

Every rule here has a mechanism. Given a reason to break one, break it knowingly.

| Rule | Why |
| ---- | --- |
| Body under ~500 lines | Past that, instructions land mid-context where compliance measurably drops |
| Front-load what matters | Attention is U-shaped — start and end are read, the middle degrades toward random |
| References exactly one level deep | Agents read nested chains incompletely and stop short of the content |
| Table of contents on reference files over ~300 lines | Otherwise the agent reads the top and guesses the rest |
| Directory name = frontmatter `name` | A mismatch means it does not resolve |
| Imperative instructions with a verifiable done-condition | "Consider whether the tag is correct" produces different actions every run |
| Split by mutually-exclusive context | Only the relevant file loads; the rest costs nothing |

**Count the simultaneous constraints.** Compliance with *all* of a set collapses nonlinearly —
a model honoring individual constraints ~41% of the time satisfies all eight together 5.7% of
the time, and reliability breaks down past roughly five or six. Constraints requiring sustained
tracking degrade about twice as fast as simple ones. A skill imposing a dozen simultaneous rules
is unlikely to have them all honored however well each is written. **If a skill needs more,
that is a split, not a longer file.**

A long skill is not automatically wrong. A long skill with its load-bearing instruction in
paragraph 12 is.

## 5. Audit the library, not just the file

Some failures only exist between skills and are invisible when reviewing one:

- **Competing descriptions.** Two skills claiming the same triggers means the model picks one
  arbitrarily. Read the descriptions of the whole library together, not each in isolation.
- **A retired skill still referenced.** Cross-references to a skill that moved or was removed.
- **Overlap with a skill that already wins.** If an existing skill reliably handles the case,
  a second one competing for it makes both less reliable.

```bash
grep -h '^description:' skills/*/SKILL.md
```

## 6. Reading a skill cannot certify it is safe

**Quality review and safety review are different operations. Do not report one as the other.**

A skill is natural-language prose installed with no signing or sandboxing. Instructions can be
embedded in invisible Unicode Tag codepoints — rendering as nothing to a human reviewer and to
a diff, while the model reads them as instructions. A demonstrated payload sat on line 5 of an
otherwise legitimate skill and ran `curl … | bash`.

So when you have read a skill and found it well-formed, you have established that it is
well-formed. You have not established that it is safe, and saying otherwise is the failure this
step exists to prevent. Safety needs tooling that scans for invisible codepoints, and provenance
— who wrote it, from where.

Flag it explicitly when auditing a skill you did not write.

## Reporting an audit

Lead with the failure mode, not the file order. For each finding: the symptom the user would
notice, the mechanism, the fix. Separate what you verified from what you inferred — "the
description is 266 characters, over the 250 cap" is verified; "this is probably why it doesn't
fire" is inference until a paired run says so.

State plainly what inspection could not cover: whether the skill helps, and whether it is safe.

## Signals to Watch For

| Signal | Instead |
| ------ | ------- |
| Fixing wording before naming the failure | Diagnose first — the symptom picks the fix |
| Estimating description length | Count it; 250 is a hard cap, not a guideline |
| "The description reads fine" | Fine to you is not a trigger match. Would the phrasing a user types appear in it? |
| Writing the skill, then testing it | Baseline first. A skill written from imagination fixes an imagined failure. |
| Skipping the without-skill run because the skill obviously helps | That is the exact assumption the net-negative case violates |
| Taking a skill's self-score as a result | It self-scored 0.92 on the output that proved it failed |
| Adding one more rule to a skill already carrying ten | Past ~5–6 they stop being followed together. Split it. |
| Calling a skill safe because you read it | Reading cannot see invisible codepoints. Say what you actually checked. |
| Treating the description contract as settled | It is contested. Choose by failure mode and say which you chose. |

## Evidence

Every measurement and rule above is sourced in [references/evidence.md](references/evidence.md)
— read it when a rule needs justifying, is being challenged, or you are deciding whether a
particular case warrants breaking one.

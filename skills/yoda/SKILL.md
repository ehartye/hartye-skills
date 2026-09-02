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

**It gets truncated, so check the length rather than estimating it.** Claude Code caps the
combined `description` and `when_to_use` text at **1,536 characters** in the skill listing, and
warns at startup when a description is truncated. Separately, `SLASH_COMMAND_TOOL_CHAR_BUDGET`
governs the *aggregate* metadata budget across all installed skills — dynamically 2% of the
context window — so a large library can push descriptions out of the listing even when each one
is individually well under the cap. **Put what decides whether the skill fires first**, because
truncation takes from the end.

```bash
awk -F'description: ' '/^description: /{print length($2)}' SKILL.md
```

*Version note:* this cap was **250 characters** until it was raised to 1,536. If you are reading
guidance built on 250 — including older write-ups and the issue that documented it — it is
describing superseded behavior. Confirm against the changelog rather than a secondary source;
this exact number has already moved once.

**Write triggers, not a synopsis.** Concrete phrases a user would actually say, symptoms, error
strings, tool names. Third person. A description with no trigger conditions is the single most
common reason a skill never fires.

**Use `when_to_use` for the triggers.** Claude Code has a dedicated frontmatter field for exactly
this — "additional context for when Claude should invoke the skill, such as trigger phrases or
example requests," appended to `description` in the listing and counting toward the same 1,536
cap. It largely dissolves an old argument about whether a description should say *what* a skill
does or *when* to use it: put the capability in `description`, put the trigger phrases in
`when_to_use`, and stop making one field do both jobs.

```yaml
description: Audits and authors skills.
when_to_use: Use when a skill never fires, fires but is ignored, or two skills compete.
```

That argument still matters for portability, because `when_to_use` is a Claude Code field and not
in the vendor-neutral spec — a skill that must also load under another agent has only
`description` to work with. There, the sources do not weigh equally:

- **Both what and when** — the Agent Skills spec defines `description` as "Describes what the
  skill does and when to use it," and Anthropic's skill-creator says include both and make it "a
  little bit pushy," because models under-trigger more often than they over-trigger.
- **When only** — a community position, from testing that found a description summarizing a
  workflow becomes a shortcut the model takes *instead of* reading the body. The reported case: a
  "code review between tasks" description produced one review where the skill's flowchart
  specified two.

**The spec and the first-party guidance both say both.** Default to that. The trigger-only rule
is a real observed failure, but it is narrower than it is usually stated — the danger is a
description that reads as a *procedure the model could follow on its own*, not one that names a
capability. "Audits and authors skills" is a capability. "First check frontmatter, then measure
the description, then run a baseline" is a procedure, and that is the one that gets followed
instead of the body.

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
| Frontmatter `name` matching the directory | Not a load failure — see below. Mismatch changes the command users type |
| Imperative instructions with a verifiable done-condition | "Consider whether the tag is correct" produces different actions every run |
| Split by mutually-exclusive context | Only the relevant file loads; the rest costs nothing |

### Two contracts, and they differ

You are writing against a vendor-neutral spec *and* one implementation. They are not the same,
and the gap is where portability bugs live.

| | Agent Skills spec | Claude Code |
| --- | --- | --- |
| `name` | **Required.** 1–64 chars, lowercase alphanumeric and hyphens, no leading/trailing or consecutive hyphens, **must match the parent directory** | **Optional.** Display label for personal/project skills, where the directory sets the command. In a *plugin* skill it sets the command's last segment, namespaced by plugin |
| `description` | **Required**, 1–1024 chars | Recommended; combined with `when_to_use` and capped at 1,536 in the listing |
| `when_to_use` | Not in the spec | Supported |
| Body | "under 500 lines"; instructions tier under ~5000 tokens | "Keep `SKILL.md` under 500 lines" |
| Layout | `scripts/` `references/` `assets/`, relative paths from the skill root | Same |

**So a name/directory mismatch is not the load failure it is often reported as.** In Claude Code
the skill still resolves — a plugin skill in `skills/review/` carrying `name: fancy` becomes
`/plugin:fancy`, which is a discoverability surprise, not a break. But it *violates the spec*,
so the skill stops being portable. **Match them anyway:** required by the spec, harmless in
Claude Code, and the only choice that works everywhere.

Prefer spec-required fields when a skill might travel. `allowed-tools` is marked experimental in
the spec and support varies; anything Claude-specific (`when_to_use`, `context: fork`, `model`,
`hooks`, `paths`) is a portability cost you should take knowingly.

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
description is 1,900 characters, over the 1,536 cap" is verified; "this is probably why it doesn't
fire" is inference until a paired run says so.

State plainly what inspection could not cover: whether the skill helps, and whether it is safe.

## Signals to Watch For

| Signal | Instead |
| ------ | ------- |
| Fixing wording before naming the failure | Diagnose first — the symptom picks the fix |
| Estimating description length | Count it. And check the current cap — it moved from 250 to 1,536 once already |
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

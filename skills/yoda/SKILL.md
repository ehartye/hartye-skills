---
name: yoda
description: Guidance for writing, reviewing and auditing agent skills (SKILL.md files) and for diagnosing skills that never fire, get ignored, trigger on the wrong prompts or compete with each other.
when_to_use: Use when writing, editing, or reviewing a SKILL.md, auditing a skill library, or when a skill never fires, fires but is ignored, triggers on wrong prompts, two skills compete, or a skill "doesn't seem to work."
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

Name the failure before touching the file; the symptom tells you the fix. *Outside* rows are
causes outside the `description`: rule them out when it reads fine. Sources and untested claims:
[references/evidence.md](references/evidence.md#causes-outside-the-description).

| Symptom | Failure | Where to look |
| ------- | ------- | ------------- |
| Never fires | Description doesn't match how anyone phrases the task | `description` — Step 2 |
| Never fires, description reads fine | *Outside:* description not in context: dropped from an over-budget listing (every name is kept), `"name-only"` in `skillOverrides`, or `disable-model-invocation: true` | Ask a fresh session "What skills are available?"; `--debug`; `/skills` menu. No command is documented to list the dropped ones: UNSETTLED. Budget — Step 2 |
| Loads, but fields do nothing, `/name` works | *Outside:* YAML that does not parse (the skill still loads with no fields set), an opening `---` not on line 1, or a misspelled field (ignored, no error) | `--debug` shows a parse error; `claude plugin validate` on the skills directory; nothing reports a misspelling, so compare it with the docs' field table |
| Works in one worktree, not another | *Outside:* `paths` matches only files under the current working directory, not a sibling worktree, even one added with `/add-dir` | Start Claude Code in that worktree or `/cd`. Glob syntax, nested worktrees, `paths` on a plugin skill: UNTESTED |
| Missing from the `/` menu | *Outside:* a refused character in the name (control, no-break space, `<`, `>`) | `claude --debug`, search the log for `[names]` |
| Followed at first, then stops | *Outside:* invoked content is not re-read; compaction keeps only the first 5,000 tokens of each recent skill | Re-invoke it; hook for a rule that must hold; key instructions first |
| Fires on the wrong prompts | Description over-claims | `description` — Step 2 |
| Fires, then behaves as if unread | Description summarizes the workflow; the model follows the summary instead of the body | `description` — Step 2 |
| Fires, body read, one instruction ignored | That instruction is buried | Body position — Step 4 |
| Two skills fight | Overlapping triggers | Library level — Step 5 |
| Reference file never read | It is behind another reference, or nothing points at it | Tier assignment — Step 4 |
| Output worse than no skill | Net-negative | Only a paired run shows this — Step 3 |

You cannot diagnose the last one by reading. Say so rather than guessing.

## 2. The description is the triggering mechanism

It is the only part of a skill the model sees before deciding to load it, and only while the
listing still carries it (Step 1, *Outside* rows). The body is never consulted for whether to load.

**It gets truncated, so check the length rather than estimating it.** Claude Code caps the
combined `description` and `when_to_use` text at **1,536 characters** per entry by default
(`skillListingMaxDescChars`). The whole listing has its own budget, **1% of the context window** by
default (`skillListingBudgetFraction`; `SLASH_COMMAND_TOOL_CHAR_BUDGET` is the legacy fixed
character count). Every skill name is always kept; over budget, the descriptions of the skills
invoked least go first, even when each is under the cap. The overflow warning is in the debug log,
not at startup. `"name-only"` in `skillOverrides` frees budget, not for plugin skills (use `/plugin`).
**Put what decides whether the skill fires first**; the cut takes from the end. **Unsettled:** when
the 8,000-character fallback (env-vars page only) applies, what "least invoked" ranks by, whether
plugin skills are dropped, variable-versus-setting precedence, whether `/doctor` lists dropped ones.

```bash
awk 'function cnt(s, c) { c = "LC_ALL=C tr -d \200-\277 | wc -c | tr -cd 0-9"; fflush(); printf "%s", s | c; close(c) }
function row(k, v) { if (!(k in r)) return; v = r[k]; if (b[k] != "") v = v (b[k] ~ /-/ ? "" : "\n"); else if (v ~ /^["\047]/) gsub(/^["\047]|["\047][ \t]*(#.*)?$/, "", v); else sub(/[ \t]+#.*/, "", v); all = all v; cnt(v); sub(/\n$/, "", v); print " " k ": " v }
BEGIN { while ((getline l) > 0) { sub(/[ \t\r]+$/, "", l); if (FNR == 1) { on = (l == "---"); k = ""; all = ""; delete r; delete b; print FILENAME; continue }
  if (!on) continue; if (l == "---") { on = 0; row("description"); row("when_to_use"); cnt(all); print " total"; continue }
  if (l ~ /^(description|when_to_use):/) { k = l; sub(/:.*/, "", k); sub(/^[^:]*:[ \t]*/, "", l); r[k] = ""; b[k] = (l ~ /^[>|]/ ? l : ""); if (b[k] != "") l = "" } else if (l ~ /^[^ \t]/) k = ""; if (k == "") continue; sub(/^[ \t]+/, "", l); if (l != "") r[k] = r[k] (r[k] == "" ? "" : " ") l } }' SKILL.md
```

Run it on one file or over `skills/*/SKILL.md` (Step 5). It reads frontmatter only (`---` on line 1); `total` is `description` plus `when_to_use`, in characters.

*Version note:* the per-entry cap was **250 characters** before 1,536; guidance built on 250 is superseded.

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

## 4. Structure is tier assignment

**Progressive disclosure is the architecture of the format, not a tip about length.** A skill
loads in three tiers, each at a different moment:

| Tier | What | Loads | Budget |
| ---- | ---- | ----- | ------ |
| 1. Metadata | `name` + `description` (+ `when_to_use`) | At startup: every name; descriptions can be dropped (Step 1) | ~100 tokens |
| 2. Instructions | The `SKILL.md` body | When the skill activates | Under ~5000 tokens; under 500 lines |
| 3. Resources | `scripts/` `references/` `assets/` | Only when something reads them | Unlimited; scripts run without loading |

**So authoring or fixing a skill is deciding what belongs in which tier.** Every rule below is a
consequence of that one decision, which is why they are not an arbitrary checklist:

- **Triggers go in tier 1** — it is the only tier read before the skill fires.
- **The procedure goes in tier 2** — it is worthless until the skill fires, and every line here
  competes for attention with every other line.
- **Exhaustive reference, rare variants, API tables go in tier 3** — free there, costly in tier 2.
- **Mutually-exclusive contexts get separate tier-3 files**, so only the relevant one loads.

Tier 1 is not free: ~100 tokens per listed skill, and a large library overflows the listing, so
descriptions get dropped (Step 1). A skill that could be a paragraph in an existing one should be.

*This skill is the worked example:* a body you are reading now, and
[references/evidence.md](references/evidence.md), the sourcing and caveats, in tier 3.

**Auditing question:** for each chunk of a skill, ask *which tier is this in, and which tier
should it be in?* Misfiled content is most of what goes wrong — triggers stranded in the body,
reference material bloating tier 2, a critical rule sitting in a file nothing reads.

### The rules that follow from it

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
| No dollar-digit or dollar-ARGUMENTS placeholders in shell snippets | They are argument placeholders and get substituted before you see the body — see below |

**Argument substitution silently rewrites your body.** Claude Code substitutes the
full-arguments placeholder, its indexed form, and the dollar-digit shorthand (`$N` for N in 0–9)
with the arguments the skill was invoked with. This applies to the whole body, **including fenced
code blocks** — nothing exempts a shell snippet.

So an awk field reference like dollar-2, inside a skill invoked as `/skill fix a new thing`,
renders as `length(new)`. Still valid awk, silently wrong, and invisible unless you read the
*rendered* skill rather than the file on disk. Anything using positional parameters is exposed:
awk field references, shell function arguments, `sh -c` one-liners.

Write around it — prefer tools that need no positional parameters, as the Step 2 command does (`getline`, not fields).

Audit for it, and confirm every hit is a placeholder you actually meant. The character classes
below keep this command from matching itself:

```bash
grep -nE '[$][0-9]|[$]ARG' SKILL.md
```

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

**Count the simultaneous constraints.** Compliance with *all* of a set collapses nonlinearly: a
model honoring each constraint ~41% of the time satisfies all eight together 5.7% of the time, and
reliability breaks down past five or six. **If a skill needs more, split it.**

A long skill is not automatically wrong. A long skill with its load-bearing instruction in
paragraph 12 is.

## 5. Audit the library, not just the file

Some failures only exist between skills and are invisible when reviewing one:

- **Competing descriptions.** Two skills claiming the same triggers means the model picks one
  arbitrarily. Read the descriptions of the whole library together, not each in isolation.
- **A retired skill still referenced.** Cross-references to a skill that moved or was removed.
- **Overlap with a skill that already wins.** If an existing skill reliably handles the case,
  a second one competing for it makes both less reliable.

Run the Step 2 command over `skills/*/SKILL.md` and read every description and `when_to_use` together.

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
| A shell snippet in a skill body using positional parameters | Argument substitution rewrites them. Read the rendered skill, not just the file. |
| "The description reads fine" | Fine to you is not a trigger match. Would the phrasing a user types appear in it? |
| Writing the skill, then testing it | Baseline first. A skill written from imagination fixes an imagined failure. |
| Skipping the without-skill run because the skill obviously helps | That is the exact assumption the net-negative case violates |
| Taking a skill's self-score as a result | It self-scored 0.92 on the output that proved it failed |
| Judging a skill by its length alone | Length is a symptom. Ask which tier each part belongs in. |
| Adding one more rule to a skill already carrying ten | Past ~5–6 they stop being followed together. Split it. |
| Calling a skill safe because you read it | Reading cannot see invisible codepoints. Say what you actually checked. |
| Treating the description contract as settled | It is contested. Choose by failure mode and say which you chose. |

## Evidence

Every measurement and rule above is sourced in [references/evidence.md](references/evidence.md)
— read it when a rule needs justifying, is being challenged, or you are deciding whether a
particular case warrants breaking one.

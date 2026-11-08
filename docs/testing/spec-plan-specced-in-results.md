# Absorbed item frontmatter key validation

Date: 2026-11-08. Baseline: `c5bd90e6a382e2333352a2e73773cd4e5924c104` (0.10.0).
This is process-documentation validation, not a live wiki test. The
[fixture](spec-plan-specced-in-scenario.md) supplies one absorbed backlog item; no wiki was
read or written, and the wiki-master validator was not run against the output.

## Method

A fresh agent read only spec-plan's `SKILL.md`, `references/spec-template.md` and the fixture,
then returned the absorbed item's complete text after its change and its line under the spec's
"Absorbed and related items" heading. The same prompt ran once against the unmodified 0.10.0
text and once, in a separate fresh agent, against the edited text. Neither agent saw the other's
output or the expected answer.

## Pre-edit result (fails)

The baseline left the frontmatter alone and appended a prose line to the body. Verbatim excerpts:

> I added one line to the absorbed item's body and left its frontmatter alone, including `backlog-status`.

```markdown
# Export filtered rows

Let a user download the transactions that the current filter shows.

Specced in [[csv-export]] (WP2)
```

> I followed Stage 1 step 4 of SKILL.md ("Keep absorbed items discoverable with `Specced in [[<spec>]] (WP-n)` on their roadmap entries")

No tool reads that line, so a validator and generated roadmap that understand `specced-in`
cannot see the relation.

## Post-edit result (passes)

With the edited step 4 and template paragraph, the agent wrote the key and no prose line.
Verbatim excerpts:

> Here is the absorbed item after the change. The only edit is the new `specced-in` key, and `backlog-status` stays as it was.

```markdown
---
title: Export filtered rows
kind: backlog-item
project: ledger
status: draft
backlog-status: planned
tags: [ledger, export]
specced-in: ["[[csv-export|WP2]]"]
---
```

> I made one judgement call: the link uses the bare slug `csv-export`, not the full vault path.

wiki-master's backlog reference accepts a bare name, which matches the file name, so this
choice needs no further instruction.

## Structural checks

- `python -B skills/yoda/scripts/audit_scan.py skills`: exit 0, no findings.
- `python -B docs/testing/test_yoda_scan.py`: 15 tests passed, 1 skipped.
- `git diff --check`: passed.
- `plugin.json` and `marketplace.json` both read 0.10.1. The skill's `description` and
  `when_to_use` are unchanged.

## Limits

One sample per side. The run checks what the skill text tells an agent to write; it does not
check that wiki-master 0.95.0 accepts the written page, which that plugin's own tests cover.

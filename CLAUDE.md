# CLAUDE.md — hartye-skills

This repo is a Claude Code plugin: a grab bag of general-purpose utility skills. It ships no
runtime code of its own. The deliverable is the prose in `skills/*/SKILL.md`.

## Admission criteria

Before adding a skill, it must clear all three:

1. **Cross-application** — useful in 2+ unrelated projects. Project-specific guidance goes in that
   project's `CLAUDE.md`, not here.
2. **Self-contained** — no shared state or load-order dependency on other skills in this plugin.
3. **Small** — a `SKILL.md` plus, at most, a script or a reference file.

**Graduation rule:** the moment a skill needs hooks, an MCP server, persistent storage, or a UI, it
has outgrown this repo. Split it into its own repo and add a marketplace entry, matching the
pattern of `agent-stalker` and `md-publisher`. Do not grow this plugin sideways into an
application.

## Derived skills

A skill adapted from third-party work keeps that work's license, which overrides the repo's MIT.
Put the license file and a `NOTICE` in the skill's own directory, state the changes made (Apache 2.0
§4(b) requires it), and add a row to the license table in `README.md`. `skills/beautiful/` is the
worked example.

## Authoring discipline

**REQUIRED:** Use the `h-superpowers:writing-skills` skill before writing or editing any
`SKILL.md`. It is TDD applied to process documentation, and the Prime Directive holds:

> No skill without a failing test first.

That applies to edits, not just new skills. Run the baseline scenario against a subagent *without*
the skill, record the failure verbatim, then write the minimum that fixes it.

## Conventions

- **Directory name = skill name = frontmatter `name`.** Verb-first and hyphenated
  (`checking-broken-links`, not `link-checker`).
- **Frontmatter is exactly two keys**, `name` and `description`. Nothing else is supported.
- **`description` says WHEN, never WHAT.** Start with "Use when…" and list concrete triggers,
  symptoms, and error strings. A description that summarizes the workflow becomes a shortcut the
  model takes *instead of* reading the skill body.
- **Budget words by how the skill loads, not by a flat cap.** The ~500-word guidance in
  `writing-skills` exists to protect context in skills that load into *every* conversation. Nothing
  here does — these are model-invoked on demand, so the cost is paid only when the skill is
  actually relevant. Be concise because concision is clearer, not to hit a number.
  - A skill that is one procedure should read as one procedure; if it needs eight steps, write
    eight steps.
  - Push genuinely optional reference — API tables, exhaustive syntax — into a sibling file the
    skill links to.
  - If a skill is long because it covers two unrelated jobs, that's a split, not a trim.
- **Cross-reference by name, never with `@`.** Write `**REQUIRED:** Use h-superpowers:brainstorming`.
  An `@path` force-loads the file and burns context immediately.
- **No narrative.** "In session 2026-08-03 we discovered…" is not a skill. Skills are reusable
  technique, not a log of how something got solved once.

## Commands

Add a `commands/<name>.md` entry only when a skill genuinely needs a `/slash` trigger. The body
should be one line that delegates:

```markdown
---
description: "<when to use>"
disable-model-invocation: true
---

Invoke the hartye-skills:<skill-name> skill and follow it exactly as presented to you
```

`disable-model-invocation: true` prevents the command's description from competing with the
skill's own description for model-invoked discovery.

## Releasing

The version lives in two files and they must not drift:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

Bump both, update the Skills table in `README.md`, then tag. The published marketplace entry lives
in `ehartye/hartye-claude-plugins` and is updated separately.

## Git

Never commit directly to `main`. Work on a feature branch or a worktree, rebase onto latest, and
squash-merge.

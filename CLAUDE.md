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
- **Frontmatter: `name` and `description` carry the contract.** The Agent Skills spec requires
  both, and requires `name` to match the directory. Claude Code supports many more optional keys
  (`when_to_use`, `disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, …) —
  use them where they earn their place, knowing each one is a portability cost outside Claude Code.
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

## Slash commands

**Do not add a `commands/` directory.** Slash commands and skills merged in Claude Code v2.1.3;
the docs state that `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` "both create
`/deploy` and work the same way," and the plugins reference is blunt: *"Use `skills/` for new
plugins."* A skill is already invocable as `/<skill-name>`, so a command wrapper is a redundant
second definition of the same trigger.

Invocation is controlled from the skill's own frontmatter instead:

- `disable-model-invocation: true` — only reachable by typing `/name`; Claude will not load it automatically.
- `user-invocable: false` — hidden from the `/` menu; background knowledge only.
- `argument-hint` / `arguments` — autocomplete hint and named `$name` substitution.

## Releasing

The version lives in two files and they must not drift:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

Bump both, update the Skills table in `README.md`, then tag. The published marketplace entry lives
in `ehartye/hartye-claude-plugins` and is updated separately.

## Git

Never commit directly to `main`. Work on a feature branch or a worktree, rebase onto latest, and
squash-merge.

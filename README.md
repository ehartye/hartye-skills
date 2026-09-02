# hartye-skills

A grab bag of general-purpose utility skills for Claude Code.

Where [h-superpowers](https://github.com/ehartye/hartye-superpowers) covers *process* — how to plan,
test, debug, and review — this plugin covers *utilities*: small, self-contained techniques that are
useful across many unrelated projects and don't justify a plugin of their own.

## What belongs here

A skill earns a place in this plugin when it is:

- **Cross-application.** Useful in at least two unrelated projects. Anything project-specific
  belongs in that project's `CLAUDE.md` or its own `.claude/skills/`.
- **Self-contained.** No shared state with the other skills here. Each one stands alone.
- **Too small to be its own plugin.** If it grows hooks, an MCP server, a database, or a web UI,
  it has outgrown the grab bag — split it out into its own repo and marketplace entry.

If a skill needs more than a `SKILL.md` plus a script or two, that's the signal to graduate it.

## Install

Via the `hartye-plugins` marketplace:

```
/plugin marketplace add ehartye/hartye-claude-plugins
/plugin install hartye-skills@hartye-plugins
```

For local development against this checkout:

```
/plugin marketplace add C:\Users\ehart\repos\hartye-skills
/plugin install hartye-skills@hartye-skills-dev
```

## Skills

<!-- Keep this table in sync as skills are added. -->

| Skill | Use when |
| ----- | -------- |
| [beautiful](skills/beautiful/SKILL.md) | Building or reshaping any user-facing interface, or a design reads as templated and AI-generated. Covers aesthetic direction, typography, palette, layout, motion, and interface copy. |
| [ship-it](skills/ship-it/SKILL.md) | You want pending work committed, pushed, PR'd and squash-merged in one step — including when it's sitting on the default branch. |
| [yoda](skills/yoda/SKILL.md) | Writing, editing, or reviewing a SKILL.md, or auditing a skill library — including when a skill never fires, fires but is ignored, or competes with another. |

## Layout

```
hartye-skills/
  .claude-plugin/
    plugin.json          # plugin manifest (name, version, metadata)
    marketplace.json     # dev-loopback marketplace for local install
  skills/
    <skill-name>/
      SKILL.md           # required — the skill itself
      <supporting files> # only when a script or heavy reference is needed
  commands/              # optional — slash commands that invoke a skill
  README.md
  CLAUDE.md              # conventions for working in this repo
```

`commands/` is created only when a skill wants an explicit `/slash` entry point. Most skills here
should be model-invoked off their `description` alone.

## Adding a skill

See `CLAUDE.md` for the full working agreement. The short version:

1. Write a baseline test first — see the `h-superpowers:writing-skills` skill. No skill ships
   without watching an agent fail without it.
2. Create `skills/<verb-first-name>/SKILL.md` with `name` and `description` frontmatter. The
   description states *when to use it*, never what it does.
3. Add a row to the Skills table above.
4. Bump the version in **both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

## License

MIT — see [LICENSE](LICENSE) — **except** where a skill directory carries its own license file,
which takes precedence for that skill:

| Skill | License | Why |
| ----- | ------- | --- |
| [beautiful](skills/beautiful/) | Apache 2.0 | Derived from Anthropic's `frontend-design` skill. See [NOTICE](skills/beautiful/NOTICE) for source commits and changes, [LICENSE.txt](skills/beautiful/LICENSE.txt) for terms. |

Apache 2.0 is compatible with this repo, but it is not MIT: it obliges us to ship the license text,
retain attribution, and state our changes. Any future skill derived from third-party work follows
the same pattern — license file plus `NOTICE` in its own directory, and a row here.

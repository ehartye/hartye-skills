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
/plugin marketplace add /absolute/path/to/hartye-skills
/plugin install hartye-skills@hartye-skills-dev
```

## Skills

<!-- Keep this table in sync as skills are added. -->

Wiki-backed skills target wiki-master 0.89.0 or later and its six-role catalog.

| Skill | Use when |
| ----- | -------- |
| [ask-me](skills/ask-me/SKILL.md) | You are offering a free moment, or want the agent to ask you what it is waiting on. Groups pending decisions with context and recommendations, waits for each submitted answer, and supports multiple selections through native controls or text. |
| [beautiful](skills/beautiful/SKILL.md) | Building or reshaping any user-facing interface, or a design reads as templated and AI-generated. Covers aesthetic direction, typography, palette, layout, motion, and interface copy. |
| [q-master](skills/q-master/SKILL.md) | You are starting or joining a project, or its tools feel crowded, and want the smallest sensible set of plugins enabled. Audits what is enabled against what is installed and records the selection and rationale in a wiki note through wiki-project. |
| [rubber-duck](skills/rubber-duck/SKILL.md) | You want a second opinion that is not just you again — stuck, pre-commitment on something hard to reverse, or asked to sanity check or red-team. Consults the other vendor's model and records it verbatim to `docs/rubber-duck/`. |
| [ship-it](skills/ship-it/SKILL.md) | You want pending work committed, pushed, PR'd and squash-merged in one step — including when it's sitting on the default branch. |
| [spec-plan](skills/spec-plan/SKILL.md) | You want to preload wiki-grounded specs, then plan a selected set of ready specs together. Plan mode is the normal path; explicitly authorized delegated planning (added in 0.9.7) can use Default/non-interactive mode with a durable complete plan and regular todos (or a saved task table/checklist). Rigor defaults to standard without a question. Use `rigor=enhanced` for fresh-agent spec review, same-developer TDD task pairs and planned fresh-agent work-package reviews, retained per spec. Combined plans sequence specs with parallel subagents within each spec and cover the project definition of done through delivery and cleanup. The skill finishes at handoff, carrying actual execution authority forward without inventing permission or requiring fresh approval just because the user is away. Where `/plan` enters Plan mode, it remains the single next action for the normal spec handoff. |
| [yoda](skills/yoda/SKILL.md) | Writing, editing, or reviewing a SKILL.md, or auditing a skill library — including when a skill never fires, fires but is ignored, or competes with another. |

## Version notes

### 0.9.7

Spec-plan supports explicitly authorized delegated planning outside Plan mode, with a saved
complete plan and regular todos or a durable task table. It retains readiness, selected
review/TDD rigor, unresolved-decision gates and execution authorization boundaries.
See [PR #38](https://github.com/ehartye/hartye-skills/pull/38) and the
[validation record](docs/testing/spec-plan-delegated-results.md).

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
  README.md
  CLAUDE.md              # conventions for working in this repo
```

Every skill is invocable as `/<skill-name>` on its own — slash commands and skills are one
mechanism — so there is no `commands/` directory. Control invocation from the skill's own
frontmatter (`disable-model-invocation`, `user-invocable`) rather than a wrapper file.

## Adding a skill

See `CLAUDE.md` for the full working agreement. The short version:

1. Write a baseline test first — see the `yoda` skill. No skill ships
   without watching an agent fail without it.
2. Create `skills/<verb-first-name>/SKILL.md` with `name` and `description` frontmatter. The
   `description` states what the skill does, never as a procedure; put the triggers in `when_to_use`.
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

## Wiki integration compatibility

Version 0.9.2 migrates spec-plan and q-master to the five wiki-master roles and requires wiki-master 0.88.0 or later for those workflows.

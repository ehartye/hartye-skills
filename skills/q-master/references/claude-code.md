# Claude Code mechanics for Q

As of Claude Code 2.1.312, 2026-10-29. Flags: DOCUMENTED (the platform's documentation says it),
TESTED (a controlled run, limits stated beside it), OBSERVED (seen once, not a controlled test),
UNTESTED (documented or plausible, not run), UNKNOWN (no source). Sources: the platform's
documentation and the wiki's notes on project-level enablement (search the wiki for them). Do not
state an UNTESTED or UNKNOWN fact as settled; say which it is.

## 1. Where the project setting lives

- Files: shared `.claude/settings.json` in the project; local `.claude/settings.local.json`, which
  the platform keeps out of sharing when it saves there. DOCUMENTED. Default to the shared file;
  use the local one only if the user wants the change kept off the shared project. State which
  file you chose in the before and after, and whether the change will be shared with everyone who
  uses the project or stay on the user's own computer. A project may exclude the folder from
  sharing, so check its ignore rules.
- Entry: `"enabledPlugins": {"<name>@<marketplace>": true | false}`. No entry at any scope falls
  back to the plugin author's default. DOCUMENTED.
- Precedence: local over project over user. DOCUMENTED. A project false beating a user true for a
  whole plugin is OBSERVED once, 2026-10-29, in the platform's plugin listing.
- Merge into the file, never overwrite: keep every unrelated key and `permissions.deny` entry.
  Enabling an external-source plugin in a project file installs nothing for others. DOCUMENTED.

## 2. Plugin ids

`<name>@<marketplace>`, as listed. A plugin synced from the user's claude.ai account is
`<name>@synced`. A project entry `"<name>@synced": false` in the shared file controls it.
DOCUMENTED, UNTESTED: propose it and say it is documented and not yet verified. The
local file for `@synced` ids and a project-scoped plugin-disable command for them are UNKNOWN. The
account toggle, a user-level disable and the machine-wide sync setting are user-level: not Q's to
change or recommend.

## 3. By unit

TESTED limits: headless sessions, plugin loaded from a directory, one skill and one tool, 3 runs;
interactive and trusted sessions untested.

| Unit | Project-level mechanism | Listing | Callable | Flag |
| ---- | ----------------------- | ------- | -------- | ---- |
| Whole plugin | `enabledPlugins` false (section 1) | Gone, with its skills, agents, hooks, servers | No | DOCUMENTED |
| One plugin skill | `permissions.deny: ["Skill(<plugin>:<skill>)"]` | Still listed | Refused | TESTED, limits above; blocks only, not a trim |
| One plugin skill | `skillOverrides` | Unchanged | Unchanged | DOCUMENTED not to apply to plugin skills; no effect seen, inconclusive |
| One plugin MCP tool | `permissions.deny: ["mcp__plugin_<plugin>_<server>__<tool>"]` | Removed | No | TESTED, limits above; counts as a trim |
| A plugin's MCP server | `deniedMcpServers`, or deny `mcp__plugin_<plugin>_<server>` | Removed (expected) | No | DOCUMENTED for the setting; its match name for plugin servers UNKNOWN; the deny form UNTESTED |
| A plugin's hooks | `disableAllHooks` turns off every hook, user and project ones too | n/a | Stop running | DOCUMENTED: all or nothing, so drop the plugin instead |
| A plugin's agents | a deny on an agent name; plugin-scoped form | UNKNOWN | UNKNOWN | UNKNOWN |

- Tool names come from the session's own tool listing, as `mcp__plugin_<plugin>_<server>__<tool>`.
  Never guess the server part. If the names are not visible, say so, then ask for them in the
  proposal or leave that trim out and say why.
- To keep 2 of a plugin's 8 tools, deny the other six by exact name. State the status: TESTED for
  one tool (limits above), the other tools follow the same form and are UNTESTED. Check the
  effective tool listing at the next audit, in a fresh session.

## 4. How a change takes effect

It applies in sessions working in the project's directory. Plugin enable and disable changes apply
with `/reload-plugins` or on restart; for permission-rule changes, restart (live pickup UNTESTED).
Moving to another directory applies that directory's project settings. DOCUMENTED, since v2.1.246.

## 5. When the request cannot be met

No verified project-level way hides one plugin skill. Say what can be done and the cost of each.
Block it: calls are refused, the listing cost stays, the other skills and tools stay. Drop the
whole plugin: the listing cost goes, with every other skill and tool wanted from it. Then let the
user choose. The same applies to a single hook or, until verified, a single agent.

## 6. Other working copies

A second checkout of the project, platform-made or by hand, is its own project root and reads its
own settings; files the project excludes from sharing are absent there. OBSERVED 2026-10-29: a
copy's plugin listing showed the full user-level set, the original the project's selection. A
selection in an excluded file applies only where written.

- `.worktreeinclude` in the project root, same pattern syntax as the exclusion file: only files
  matching a pattern AND excluded from sharing are copied into new copies. DOCUMENTED for copies
  the platform creates; by-hand copy UNKNOWN, treat as not covered until tested.
- A file inside a folder excluded as a whole: a pattern starting `**/` copies it when the first
  name after `**/` is a name in the folder's path (example: `**/.claude/skills/*.md`). For the
  project settings file the documented form is `**/.claude/settings.json`. DOCUMENTED. The plain
  `.claude/settings.json` is not the documented form: UNKNOWN if it works.
- Shared with the main checkout, DOCUMENTED, whether the copy is made by the platform or by hand:
  untracked skills, agents and commands, read through when the copy has none (v2.1.277 or later);
  permission approvals saved from a copy go to the main checkout's local settings file and apply
  in every copy, except on Windows and where the platform does not use the repository root (the
  rule then stays with that copy); project-scope plugins of the main checkout also load in its
  copies. None covers the plugin enable/disable map in an excluded file: OBSERVED absent in a copy.
- Step 1: compare the note with the project file in this copy. If the note records a selection and
  the file is absent, say so and why (excluded from sharing). Offer to write it here after approval
  and/or carry it with the include file. Never claim it applies where absent.

If this file and the wiki's notes disagree, the wiki wins; update this file.

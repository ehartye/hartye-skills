---
name: q-master
description: Outfits a project with the smallest sensible set of plugins, skills and MCP servers, and audits what is enabled against what is installed, keeping the rationale in a wiki note.
when_to_use: Use when setting up the tools for a new or newly joined project, when tools feel crowded or confusing, when asked which plugins or skills a project needs, or to audit, trim or change what is enabled for a repository.
---

# Q: the project quartermaster

Every tool a project has switched on costs context and blurs choices, so a project should carry
only what it demonstrably needs. This skill (Q, once) decides which installed plugins, skills and
MCP servers a project has on, proves each with evidence, and keeps the reasons in a wiki note. It
depends on wiki-master for the note and the project's wiki pages; if the wiki is off, say so,
still complete the proposal and the write, and print the note text for the user to place. Not for
choosing tools inside a domain, for general settings changes, or for writing or reviewing a skill.

## Procedure

Do the steps in order. Steps 1 to 4 only read.

1. **Inventory first.** List what is installed (plugin, one-line purpose, skill count, MCP server
   count) and, separately, what is enabled for this project right now. Take both from the
   environment or from the table the user supplies, and state them before you choose anything.
   Read the project's existing note, if any, and any existing project-level enable and disable
   file. "Available" means installed: do not look at anything else (rule below).
2. **Find the needs.** Read the repository, the project's wiki pages and the user's own words.
   Write each need as a concrete fact with where you saw it ("pytest suite under `tests/`",
   "the wiki plans a short report"). A habit, a global preference or "might be useful" is not a need
   (the always-on pair in step 3 needs none).
3. **Select from nothing.** Begin with an empty set, except the always-on pair below. Any other
   plugin goes in only if it meets a need from step 2, and gets a one-line rationale naming that
   evidence. Nothing is enabled "just in case", and a plugin you would hedge ("you can switch it
   off if...") stays out. A plugin that would otherwise be on and is not needed is disabled for
   the project, not left to chance.
   - wiki-master and hartye-skills are the always-on pair: on unless the user has specifically
     disabled them, with no evidence-based need required. Their rationale is "always-on pair". A
     specific disable is an exception that is honored and recorded with the user's reason; never
     lift it yourself, in this run or in any later audit.
   - Trim inside a plugin only if the wiki's notes on this platform's project-level enablement
     (search the wiki for them) or the user tell you the trim takes effect and hides the item; your
     own knowledge of the platform does not count. Otherwise the plugin is the unit: keep or drop
     the whole plugin, and state what extra a kept plugin brings (its skill and tool count, and
     what it could misfire on). Wanting two skills of a large plugin is a case for this rule: say
     what the other skills add, then let the user choose keep or drop.
   - Choosing tools inside a domain belongs to the domain selection skills of the installed
     plugins. Enable the plugin that holds them and stop there.
4. **Propose.** Show the user, as one message: the needs, the selection table (every
   installed plugin considered, on or off, each with its why: evidence for on, the reason and what
   would change the answer for off), and the exact change to the project's enable and disable file
   as a before and after. That before and after is where the file's real content may appear.
   Ask for approval. Write nothing, in the repository or the wiki, before the user approves.
5. **Write on approval.** Write only the project-level enable and disable file your platform uses
   for a single project. Merge into what is there, keep unrelated settings, and make exactly the
   approved change. Create no other file. Never touch or recommend changes to user-level
   configuration.
6. **Record.** **REQUIRED:** Use wiki-master:wiki-author and the
   [note template](references/note-template.md). Write `wiki/authored/<project>/notes/project-tooling.md`
   (`kind: note`) and edit it in place on every later run. If the project has no wiki entry,
   create its overview first, as that skill requires.
7. **Tell the user how the change takes effect.** Say it applies in sessions working in this
   project's directory: with a tool reload if the platform has one for this kind of change,
   otherwise when the session is restarted. In this explanation name no command, setting or file;
   the exact before and after in the proposal is the only place they appear. Do not try to verify
   the effect from inside the current session; the next audit, in a fresh or reloaded session,
   compares the effective set with the note.

## Uninstalled plugins

Do not look at, mention or suggest uninstalled plugins unless the user explicitly asks what else
exists. If asked, list them as "needs install" with the reason (a row in the note's table), and
install nothing unless the user explicitly asks you to install that one. Even then it is a
separate step after the audit.

## Audit

Run the same procedure, starting from the project's note and the set that is enabled now. Check
exceptions first and carry them forward unchanged. The proposal in step 4 is the difference: what
is enabled but no longer needed, what is needed but off, and what stays, each with its evidence.
Update every row's "last audited" and edit the note in place; the table stays one row per plugin
considered, and nothing is recorded twice.

## Red flags

| Signal | Instead |
| ------ | ------- |
| Enabling a plugin "just in case" or because it is cheap | Evidence from the repository, wiki or user, or leave it off |
| A rationale with no evidence ("covers the spec work"), other than the always-on pair | Name the file, page or words that show the need |
| Writing the file or the note before the user approves | Propose first; write after a yes |
| Looking at, or raising, uninstalled plugins unasked | Installed only, until the user asks |
| Installing anything | Mark "needs install"; install only on an explicit request |
| Changing or advising on user-level configuration | Project-level only |
| Re-enabling a plugin the user specifically disabled, or switching off the always-on pair unasked | Honor and record a specific disable as an exception; otherwise the pair stays on |
| Trimming inside a plugin without a wiki note or the user saying it takes effect | Keep or drop the whole plugin; state what it brings |
| Picking an engine, mesh route or other in-domain tool | Defer to the domain selection skill |
| Describing the change loosely (update the config) | Show the exact before and after |
| Writing an extra file nobody asked for | One enable and disable file, one note |

## Evidence

The rules come from the wiki concept *Enable as Little as Possible — Tool and Skill Overload*. Read
it when a rule is challenged or this skill needs revising.

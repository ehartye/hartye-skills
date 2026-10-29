# Project tooling note template

Save as `wiki/authored/<project>/notes/project-tooling.md`. Each section's note says what belongs;
delete the note once the section is filled. Edit the page in place on every audit; never create a
second note for the same project.

```markdown
---
type: authored
created: <date>
updated: <date>
status: draft
sources: []
ai-generated: true
project: <project>
kind: note
---
# Project tooling: <project>

One or two sentences: what the project is and what it concretely needs from tools. Leave out
history and anything the overview already says.

## Current selection

Open with the date of the last audit. One row for every installed plugin considered, on or off;
nothing is recorded outside the table except the exceptions. A plugin that is not installed
gets a row only if the user asked about it, with state "needs install".

| Plugin | State | Why | What it brings | Since | Last audited |
| ------ | ----- | --- | -------------- | ----- | ------------ |
| <plugin> | on or off | On: one line naming the evidence (a file, wiki page or the user's words), or for the always-on pair the words "always-on pair". Off: the reason and what would change the answer | Skill count, MCP server count and what it could misfire on | <date> | <date> |

## Exceptions

One bullet per specific user decision against the defaults, for example turning off an always-on
plugin: the plugin, the user's reason in their words, the date. An exception stays until the user
lifts it and is carried forward by every audit. Write "None." if there are none.
```

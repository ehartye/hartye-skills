# Codex question controls and waiting

Check the tools, schemas and instructions supplied in the active mode. Availability and limits
can differ by host; a tool appearing in a listing does not override its mode restrictions. Do
not change modes just to ask questions. These details apply to Codex, not Claude Code's native
interview controls.

## Group questions using an available tool

Put related questions in one `questions` array within the supplied limits. Multiple questions
are distinct from multiple selections within one question. Tabs, pages and navigation belong
to the host; do not promise a particular layout.

- `request_user_input`, when exposed under its Plan-only contract, accepts one to three
  questions with two to three mutually exclusive options each. Use its required IDs, short
  headers and option descriptions; put the recommendation first with `(Recommended)`.
  Recheck the current schema rather than treating these limits as permanent. Do not call it in
  Default mode under that contract, or use it for approval when host instructions prohibit it.
- `request_user_input_async`, where available, groups questions by `title`, with optional
  suggested `options`. Under its free-text contract, omit `options` for a text-only answer.
  It returns immediately; `accepted: true` acknowledges display, not submission. The first
  suggested option may be preselected, but is not an answer until submitted.

Neither of these schemas supplies a multi-select field. If the current schema still lacks one,
explain the limit and ask for all chosen labels or values in its free-text input, or use a
permitted plain-text question. Never invent fields, add an `Other` option when the client
already supplies free text, or enumerate every possible combination as single-choice options.

## Keep every unanswered question open

Async replies can arrive one question at a time. Match each reply to its question using the
returned identifiers or question index, retaining every submitted value. A reply to one
question does not resolve its siblings. Keep the remaining questions pending.

Use the host's supported interruptible waiting mechanism, such as `clock.sleep` when exposed,
while awaiting replies; follow its limits and continue useful independent work when possible.
After a wait timeout or partial reply, resume waiting. Do not finalize, replace or cancel the
form merely because time passed or one answer arrived. Do not emulate UI interaction through
unsupported automation. If no persistent form is supported, explain that limitation and use a
permitted text fallback without treating the unanswered questions as answered.

Explicit cancellation ends the current interview; skipped or unanswered decisions remain
unresolved. Do not reopen them automatically or substitute defaults. Act only on actual
answers within existing authorization and the active mode's permissions. An answer cannot
permit implementation or wiki writes forbidden in Plan mode; prior authorization remains
valid when the host later permits the action.

# Yoda scanner validation (0.10.0)

Scope: one dependency-free Python 3.10+ script with Unicode, placeholder and local-link modes.
It is a mechanical review aid, not a Markdown renderer or safety certification. Existing length
guidance stays unchanged; trigger overlap, strict YAML parsing and nested-reference ranking are
outside this slice. Directory scans enumerate untracked files directly, not from a Git diff.

## Baseline and guidance scenario

Before editing the skill, an independent agent was asked to audit the library for these three
classes without reading Yoda. Its recorded result was:

> Baseline failed to complete the requested audit using discovered reusable commands.
> The repository contains no discovered reusable scanner for invisible Unicode, invocation
> placeholders, or relative Markdown links/anchors.

It found no reusable tool, did not invent a clean result, and wrote nothing. It read repository
instructions and an older validation discussion that quotes Yoda; this limits baseline isolation.
A fresh agent then read the updated skill and ran the bundled command on `skills`: exit 0, no
output, no ad hoc scanner or edits. This demonstrates command discovery and reuse only, not that
the entire skill is behaviorally superior or that the library is safe.

## Fixtures and review

- First 11-test run: 9 passed, 1 failed (missing root incorrectly returned clean), 1 Windows
  symlink-privilege skip. Missing root now returns exit 2.
- Independent review found junction traversal, aliased-ancestor diagnostics, empty hints spanning
  lines, and HTML IDs inside code examples. All corrected with regressions.
- Final local Windows: 15 tests, 14 passed, 1 symlink-privilege skip. Windows junction escape,
  cycle and aliased-parent fixtures passed; unrelated external sentinel content is preserved.
- Final WSL Linux Python 3.14.4: 15 tests, 14 passed, 1 Windows-only junction skip. Symlink escape
  and aliased-parent fixtures passed.
- Existing ship-it Git fixtures: 8 passed on Windows.
- Real library scan: exit 0, no findings. `git diff --check`: passed.
- CI runs scanner fixtures and actual-library scans on Linux, Windows and macOS using the minimum
  Python 3.10. Release records retain the remote run outcomes.

Fixtures cover tags, zero-width/bidi/BOM/control/space/variation characters constructed numerically,
ordinary multilingual text and emoji, untracked files, numeric/full-argument placeholders,
declared versus empty/block hints, multiline Markdown labels, Unicode/space/parenthesis paths,
duplicate anchors, reference definitions, code examples, missing anchors/files, encoded escape,
invalid UTF-8, dependency exclusions and CLI exit codes/nonmutation.

## Limits

Suspicious Unicode can be legitimate; full-argument placeholders with a simple nonempty
`argument-hint` are informational candidates, still requiring intent review. Frontmatter is not
YAML-validated. Individual file decoding/read errors are warning exit 1; root/traversal errors
are exit 2. Both prevent a clean report. JSON uses escaped Unicode so terminal encoding cannot
hide or corrupt diagnostics.

Links support a documented Markdown subset: inline destinations, reference definitions, ATX
headings and explicit HTML IDs. Undefined reference uses, setext headings, complex nested markup
and renderer-specific anchors need manual checks. Remote URLs are never fetched. Filesystem
checks are best-effort against a stable tree, not containment against an adversary concurrently
swapping paths. No user assets, global links or shared runtimes are modified.

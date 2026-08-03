# ship-it — design

**Date:** 2026-08-03
**Status:** implemented as `skills/ship-it/SKILL.md`

## Problem

The commit → branch → push → PR → merge → sync loop runs dozens of times a day and is identical
every time. Doing it by hand is slow; doing it by reflex is how work lands on the default branch by
accident.

## Pipeline

Each step is a no-op when already satisfied, so the skill is safe to run at any point in the loop.

1. **Orient** — resolve the default branch from `origin/HEAD`; refuse on detached HEAD or an
   in-progress rebase/merge.
2. **Branch** — feature branch: continue. Default + dirty tree: `git switch -c`. Default + local
   commits: branch at HEAD, then `git branch -f` the default back to origin, after confirmation.
3. **Commit** — stage all; message style detected from the repo's own last 20 subjects.
4. **Push** — `push -u`. No remote: stop. Never force.
5. **PR** — `gh pr create --fill`. Existing open PR: the push already updated it.
6. **Review** — print URL, diffstat, check status; offer browser / merge / stop.
7. **Merge** — CI present: wait, refuse on red. CI absent: say so explicitly, then confirm.
   `gh pr merge --squash`, then `git push origin --delete <branch>`.
8. **Sync** — `git switch <default> && git pull --ff-only`.

## Decisions

### Local commits on the default branch are moved, not refused

Branch first, *then* move the default pointer — the commits are already safe on the new branch
before anything else changes. The alternative (leave the default branch ahead) guarantees a
divergence on the next pull, since the same work also arrives via the squash-merge. Confirmation
required; before/after SHAs printed.

### The merge is gated; the push is not

Push and PR are cheap and reversible, so they run unattended and the fast path stays fast. The
merge is the irreversible step, so it waits on CI and refuses on red. Where no CI exists — 4 of 6
surveyed repos — the skill states that nothing verified the change rather than letting silence
imply otherwise. A gate that adds 90 seconds to every invocation is a gate that gets bypassed,
which is worse than no gate.

### Squash-merge, delete the remote branch, keep the local one

Every surveyed repo already has a linear default branch with one squash commit per PR. Those repos
also keep every merged branch — and because squash-merge rewrites parentage, git reports all of
them as unmerged forever. Deleting the remote branch clears that; keeping the local branch retains
the granular commits where someone would actually look for them. The GitHub PR page holds them
permanently regardless.

Note `gh pr merge --delete-branch` is **not** the way to do this: it deletes the local branch as
well as the remote. The remote delete has to be a separate `git push origin --delete`.

### Message style is detected, not imposed

`wiki-master` writes `fix(clip-pdf): derive titles cross-platform (0.8.1)`; `slate` writes
`Make code blocks word-wrap when printing`. Both are correct in their own repo. The skill reads the
last 20 subjects and matches.

## Not built

No local test run before push (rejected: friction on a hundred-times-a-day tool). No auto-open
browser (rejected: context switch on every invocation, including trivial ones). No full diff dump
(rejected: floods the terminal on large changes).

## Note on process

Written without the `writing-skills` baseline test — no subagent was run without the skill first to
observe real failure modes. Approved as a deliberate trade-off given how procedural the pipeline
is. The residual risk is a trigger description that doesn't fire when it should; revisit if the
skill turns out not to activate on natural phrasings of "ship it".

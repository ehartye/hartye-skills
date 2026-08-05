---
name: ship-it
description: Use when the user says "ship it", "ship this", "PR this up", "let's land this", or otherwise wants pending work committed, pushed, reviewed and merged - including when that work is sitting uncommitted or already committed on the default branch
---

# Ship It

## Overview

Shorthand for the commit → branch → push → PR → merge → sync loop. Every step is a no-op when
already satisfied, so it is safe to run at any point in the loop, including twice in a row.

**Core principle:** cheap and reversible steps run unattended; the two that aren't — moving the
default branch, and merging — always confirm first.

## The Pipeline

Run in order. Any step that reports **stop** ends the run: state where it got to and what remains.

### 1. Orient

```bash
git rev-parse --abbrev-ref HEAD                                  # detached? -> stop
git symbolic-ref --quiet --short refs/remotes/origin/HEAD        # -> origin/main | origin/master
```

Never hardcode `main`. Fall back to `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`,
then to `main`. If `.git/rebase-merge`, `.git/rebase-apply`, or `MERGE_HEAD` exists, **stop** — an
operation is already in flight.

Nothing to ship — clean tree, nothing unpushed, no open PR — is a valid outcome. Say so and stop.
Never manufacture a commit so the run has something to do.

### 2. Branch

| State | Action |
| ----- | ------ |
| On a feature branch | Continue |
| On default, dirty tree only | `git switch -c <name>` — changes ride along untouched |
| On default, local commits ahead of origin | Confirm, then move them (below) |

Moving commits off the default branch:

```bash
git switch -c <name>                      # commits come along; do this FIRST
git branch -f <default> origin/<default>  # only now move the default pointer
```

Branching first means the commits are already safe when the pointer moves. **Confirm before the
reset**, printing before/after SHAs — a tool that silently moves branch pointers is one you stop
trusting.

**Naming:** derive `<type>/<kebab-summary>` from the diff — `feat` `fix` `chore` `docs` `ci`
`refactor` `test`. Announce before creating; an argument (`/ship-it fix/broken-export`) overrides.

### 3. Commit

Stage everything, then **match the repo's existing message style** — read it, don't impose one:

```bash
git log --format=%s -20
```

Conventional (`fix(scope): subject`) and plain prose (`Make code blocks wrap when printing`) are
each correct in the repo already using them. The body explains *why*, not just what.

### 4. Push

No remote configured → **stop**, work is committed locally.

```bash
git push -u origin <branch>
```

**Never `--force`, `--force-with-lease`, or any history rewrite.** Not as a fallback, not on a
rejected push. A rejected push means someone else's work is at risk — stop and report.

### 5. Pull request

`gh` missing or unauthenticated → **stop**, work is pushed. An open PR already exists for this
branch → step 4's push updated it; skip to 6.

```bash
gh pr create --fill --base <default>
```

### 6. Review

Print, then ask — browser, merge, or stop:

```bash
gh pr view --json number,title,url,additions,deletions,changedFiles,statusCheckRollup
gh pr view --json files -q '.files[] | "\(.additions)+ \(.deletions)- \(.path)"'
```

There is no `gh pr diff --stat`; `--json files` is the diffstat. Browser is `gh pr view --web`.

### 7. Merge

An empty `statusCheckRollup` means no checks ran — treat it as absent CI, not as passing.

- **Checks exist** → wait (`gh pr checks --watch`). **Refuse on red.** The user may override
  explicitly; do not offer the override before reporting the failure.
- **No checks** → say plainly: *"no CI configured; nothing has verified this."* Then confirm. Never
  let silence imply the change was validated.

Read `mergeStateStatus` before attempting anything. `BLOCKED` means branch protection is refusing —
usually a required approving review, which you cannot satisfy by approving your own PR. **Stop and
report it.** `gh pr merge --admin` bypasses protection where `enforce_admins` is off, but that is
the user's call to make, not a fallback to reach for.

```bash
gh pr view <n> --json mergeable,mergeStateStatus   # BLOCKED/DIRTY -> stop, do not proceed
gh pr merge <n> --squash
```

**Verify the merge landed before touching any branch.** `gh pr merge` can fail — protection, a
conflict, a race — and it exits without merging while the next command in a chain runs anyway.
Deleting the branch of an unmerged PR *closes that PR* and removes the remote copy of the work:

```bash
test "$(gh pr view <n> --json state -q .state)" = MERGED || exit 1
git push origin --delete <branch>       # remote only, and only once MERGED is confirmed
```

Squash keeps the default branch linear, one commit per PR. Delete the remote branch so
`git branch -r` stops reporting squash-merged work as unmerged; keep the local one, which is where
the granular commits remain reachable. Merge conflict → **stop**, hand back.

If a branch was deleted in error, the work is recoverable: the local branch still holds the commits,
so `git push -u origin <branch>` followed by `gh pr reopen <n>` restores both.

### 8. Sync

```bash
git switch <default> && git pull --ff-only
```

`--ff-only` because after a squash-merge a non-fast-forward pull means something unexpected
happened; surface it rather than silently creating a merge commit.

## Signals to Watch For

Noticing any of these means the pipeline has drifted into doing harm. Stop and report instead.

| Signal | Instead |
| ------ | ------- |
| Reaching for `--force` after a rejected push | Someone else's work is at risk — stop |
| Resetting the default branch before the new branch exists | Branch first, always |
| `git reset --hard` to clean the default branch | `git branch -f` — never discard the tree |
| Merging red, or merging without saying no CI ran | Report the state, then let the user decide |
| Hardcoding `main` | Resolve `origin/HEAD`; `master` is still out there |
| Amending or rebasing pushed commits | Push a new commit; pushed history is shared |
| `gh pr merge -d` to clear the remote | It deletes the local branch too — push a delete instead |
| Deleting the branch without checking the PR merged | A failed merge plus a branch delete *closes* the PR — assert `state == MERGED` first |
| Treating `BLOCKED` as something to work around | Protection is a decision someone made; report it and let the user choose `--admin` |
| Reporting "shipped" after a stop | Name the step reached and what is left |

---
name: ship-it
description: Use when the user says "ship it", "ship this", "PR this up", "let's land this", or otherwise wants pending work committed, pushed, reviewed and merged - including when that work is sitting uncommitted or already committed on the default branch
---

# Ship It

## Overview

Shorthand for the branch, commit, push, PR, squash-merge and sync loop. Resume by observing
the actual state, never by replaying mutations. Preserve other tasks' files and commits.

**Core principle:** cheap and reversible steps run unattended; the two that aren't — moving the
default branch, and merging - need authorization. Moving commits off the default branch and
`--admin` need explicit authorization for that action; do not infer it from merge approval.
Merging confirms every time unless the user approves it for the session.

## The Pipeline

Run in order. Any step that reports **stop** ends the run: state where it got to and what remains.

**Session approval.** Before the first gated step, once a merge — or a project-defined release
packaging or tagging step — is coming, ask one question with the structured-question tool and two
answers: treat those steps as approved for the rest of the session, or re-ask each time. Skip it if
the user has already stated the answer in this session. The answer lives in the conversation only;
nothing is written to disk. It never implicitly covers moving commits off the default branch or
`--admin`; honor explicit authorization for those actions. Conflicts and unmet protection stop;
pending required checks are a wait, not an instruction to bypass protection.

### 1. Orient

```bash
git rev-parse --abbrev-ref HEAD                                  # detached? -> stop
git symbolic-ref --quiet --short refs/remotes/origin/HEAD        # -> origin/main | origin/master
```

Never hardcode `main`. Fall back to `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`;
if unresolved, stop. Inspect `git worktree list --porcelain` and record the absolute task path,
branch, HEAD and existing default checkout. Use Git's paths: `git rev-parse --git-path rebase-merge`,
`rebase-apply`, `MERGE_HEAD`, `CHERRY_PICK_HEAD` and `REVERT_HEAD`. If any exists, **stop**.
In a linked worktree `.git` is a file, not the operation directory.

Read staged, unstaged and untracked changes before touching the index. Record the caller's
explicit paths and which worktree belongs to this task; do not infer ownership from its name.
Find the PR for this repository, base and head branch, including closed PRs when resuming.
If already MERGED, skip commits/push/merge and go to verification and sync. If CLOSED but
unmerged, stop; do not silently open a replacement. A failed query is unknown, not absence.

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

**Explicit paths take precedence.** Treat them as literal repository-relative whole-file paths,
not globs; include both sides of a rename. Show the selected working-tree diff first. For
partial-hunk intent, stop to settle the selection instead of committing the entire file.
Run from the repository root, quote each path using the host shell, then:

```bash
git --literal-pathspecs add -- <selected-paths>
git --literal-pathspecs commit --only -m "<message>" -- <selected-paths>
```

`--only` commits these files' working-tree contents and leaves unrelated staged changes staged.
Plain `git commit` would include those other changes. Include selected new files with `add`
first; selected deletions are valid. Never reset, stash, clean or unstage somebody else's work.
Check the resulting commit's paths and the remaining index/tree against the initial inventory.
If add, a hook or commit fails, inspect the state and report it; do not retry with broader staging
or discard changes. Without explicit paths, stage all only when all changes belong to the task;
otherwise establish the task's scope first.

**Match the repo's existing message style** - read it, don't impose one:

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

**Never force a branch update or rewrite history.** No `--force` or `--force-with-lease` on this
push, not as a fallback, not on a
rejected push. A rejected push means someone else's work is at risk — stop and report.

### 5. Pull request

`gh` missing or unauthenticated → **stop**, work is pushed. An open PR already exists for this
branch → step 4's push updated it; skip to 6.

```bash
gh pr create --fill --base <default>
```

### 6. Review

Print, then ask — browser, merge, or stop. If merging is approved for the session, print and go
straight to 7:

```bash
gh pr view --json number,title,url,additions,deletions,changedFiles
gh pr view --json files -q '.files[] | "\(.additions)+ \(.deletions)- \(.path)"'
```

There is no `gh pr diff --stat`; `--json files` is the diffstat. Browser is `gh pr view --web`.

### 7. Merge

Read `mergeStateStatus` before attempting anything — but **poll for it**. GitHub computes
mergeability asynchronously, so for the first few seconds after `gh pr create` it returns `UNKNOWN`.
This pipeline always asks within those seconds. A single read gets `UNKNOWN`, reads it as "not
blocked", and sails straight past the case this check exists to catch:

```bash
for i in $(seq 10); do
  STATUS=$(gh pr view <n> --json mergeStateStatus -q .mergeStateStatus) || exit 1
  [ -n "$STATUS" ] || exit 1
  [ "$STATUS" != UNKNOWN ] && break
  sleep 2
done
```

Read `state,baseRefName,headRefName,headRefOid,mergeStateStatus,reviewDecision,statusCheckRollup`.
A connector's `mergeable` boolean is insufficient: use this read-only `gh pr view --json ...`
fallback when it omits those fields. Review the full PR diff, not only this run's selected files;
record the reviewed head SHA and ensure it matches the local and remote task branch.

Inspect `gh pr checks <n> --required`. For pending required checks, watch with
`gh pr checks <n> --required --watch --fail-fast --interval 10`, using the host's bounded waits
and progress updates. At the task's deadline or cancellation, stop the watcher and report pending;
leave branches and worktrees intact. Failure/cancellation is not success. An empty required-check
list is acceptable only if the query succeeded and the repository has no required checks;
verify repository rules/protection when needed, and stop if permissions leave that unknown.
After checks finish, re-read PR state, head, review decision and merge state. A changed head
requires renewed review/checks; do not merge a different commit using stale evidence.

`BLOCKED` after checks pass means an unmet protection (for example review or merge queue);
report the specific blocker and stop. `DIRTY` means conflicts: stop. If `UNSTABLE`, inspect
non-required checks and use an explicit repository/user policy; absent one, stop and report.
`gh pr merge --admin` bypasses protection where `enforce_admins` is off, but that is the user's call
to make, not a fallback to reach for. Report exactly which protection any authorized override bypasses.

If the status is still `UNKNOWN` after polling, stop rather than assuming it is fine. For CLEAN
(or an explicitly permitted, understood non-required-check state), merge the reviewed commit:

```bash
gh pr merge <n> --squash --match-head-commit <reviewed-head-sha>
```

**Verify the merge landed before touching any branch.** `gh pr merge` can fail — protection, a
conflict, a race — and it exits without merging while the next command in a chain runs anyway.
Deleting the branch of an unmerged PR *closes that PR* and removes the remote copy of the work:

```bash
test "$(gh pr view <n> --json state -q .state)" = MERGED || exit 1
```

Read back the PR identity, merged head and merge commit with
`gh pr view <n> --json state,baseRefName,headRefName,headRefOid,headRepository,headRepositoryOwner,mergeCommit`.
Verify the expected repository and branch identities; `headRefOid` is the PR head, not a fresh
branch lookup. Missing evidence stops cleanup. A nonzero merge command may
still have merged: query before retrying. If unavailable, report an uncertain outcome and stop
all cleanup. On resume, use the confirmed merged PR head as the expected task head; never push
new local commits into that closed task. Squash ancestry (`git branch --merged`) is not the test.

Delete the remote branch separately, only after MERGED is confirmed and a fresh remote lookup
matches that merged head. If absent, this step is done. If advanced or the lookup fails, preserve
it and report. Use an exact-SHA lease for the deletion so a concurrent push cannot be erased:

```bash
git push --force-with-lease=refs/heads/<branch>:<merged-head-sha> origin :refs/heads/<branch>
```

This conditional deletion is the sole lease exception to step 4; it never rewrites history.
Keep the local branch unless task-worktree cleanup was requested (step 8). A failed remote
deletion is a cleanup failure, not a failed merge; report it and retain the local recovery copy.

If a branch was deleted in error, the work is recoverable: the local branch still holds the commits,
so `git push -u origin <branch>` followed by `gh pr reopen <n>` restores both.

### 8. Sync

Locate the default checkout with `git worktree list --porcelain`. Never switch a linked task
worktree to a branch checked out elsewhere. In the default checkout, verify its branch, clean
index/tree (including untracked files) and absence of in-flight Git operations before
`git -C "<default-checkout>" pull --ff-only`. If dirty, missing, detached or divergent, preserve
it and report sync deferred. If there is no separate default checkout and this is an ordinary
checkout, switch to the resolved default only when clean, then pull `--ff-only`.
Verify the reported merge commit is reachable from the updated default HEAD.

For requested task-worktree cleanup, first verify successful sync and remote deletion, then
recheck that the task branch and worktree HEAD equal the merged PR head, the task worktree is
owned by this task, and no other worktree uses that branch. Check for in-flight operations and
all staged, unstaged, untracked **and ignored** files (`git status --porcelain --untracked-files=all`
and `git ls-files --others --ignored --exclude-standard`). If any remain or HEAD advanced,
preserve the worktree/branch and report deferred cleanup. Do not use force to remove a worktree.

From outside that worktree, remove only its recorded absolute path with `git worktree remove`,
verify success and rediscover branch/worktree state, then delete only that verified local task
ref with `git update-ref -d refs/heads/<branch> <merged-head-sha>`. This expected-SHA deletion
rejects concurrent new commits, unlike unconditional `git branch -D`. Squash ancestry is not
required; the confirmed PR and exact head supply the evidence. Retain
the branch if the user asked to keep it. Never remove the primary/default checkout. On an
interrupted cleanup, rediscover worktrees and refs; already-absent objects are done, unknown
ownership or changed heads stop deletion. Do not call a partial release fully shipped: report
merge, sync, remote deletion and local cleanup separately.

## Signals to Watch For

Noticing any of these means the pipeline has drifted into doing harm. Stop and report instead.

| Signal | Instead |
| ------ | ------- |
| Reaching for `--force` after a rejected push | Someone else's work is at risk — stop |
| Resetting the default branch before the new branch exists | Branch first, always |
| `git reset --hard` to clean the default branch | `git branch -f` — never discard the tree |
| Hardcoding `main` | Resolve `origin/HEAD`; `master` is still out there |
| Amending or rebasing pushed commits | Push a new commit; pushed history is shared |
| `gh pr merge -d` to clear the remote | It deletes the local branch too — push a delete instead |
| Deleting the branch without checking the PR merged | A failed merge plus a branch delete *closes* the PR — assert `state == MERGED` first |
| Treating pending CI as a permanent block or bypassing it | Watch required checks, then re-read protection and head |
| Broad staging with explicit paths or foreign staged files | Literal selected paths and `commit --only`; preserve the other index entries |
| Switching to a default branch checked out elsewhere | Sync its clean checkout with `git -C` |
| Removing a dirty worktree or a branch that advanced after merge | Preserve it and report deferred cleanup |
| Reading `mergeStateStatus` once, right after creating the PR | It is `UNKNOWN` for the first few seconds — poll, or the check silently passes everything |
| Merging, packaging or tagging without asking, on an approval nobody gave | Ask the session question first; no answer means re-ask each time |
| Reporting "shipped" after a stop | Name the step reached and what is left |

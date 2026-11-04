# Ship-it explicit paths and worktrees

Date: 2026-11-04. Pre-edit source: `79f09e187bcb12e348068160e4e4c418aa2becac` (0.9.7).

## Pre-edit baseline

Fresh agents received the same three simulated tasks, without the skill and with the
unmodified skill, in the same authoring turn. No simulated commands were executed.
The tasks covered four explicit paths (one new), another task's staged file and an
untracked file, a separate default checkout, pending required CI becoming CLEAN,
an interrupted merge with subsequent local work, and an unavailable merge-state query.

The without-skill agent correctly preserved unrelated work and uncertain merge state.
It failed the intended squash-and-sync contract: it chose a possible merge commit and
never synchronized the separate default checkout. Verbatim output:

> Use the repository's allowed merge method, for example if merge commits are allowed:
> `gh pr merge <PR> --merge --match-head-commit <HEAD_SHA>`

> There is no need to switch the feature worktree to `main`, which is already checked out at `/repo`.

Its preservation behavior was useful, not a failure:

> Stop destructive cleanup. This worktree still contains another task's staged changes and untracked `scratch.txt`. Do not force-remove it, reset it, or clean it.

The unmodified-skill agent honored the explicit paths despite the skill's broad-staging text,
but stopped at pending CI. Verbatim:

> Stop immediately when status is `BLOCKED`. The skill polls only `UNKNOWN`; it does not authorize waiting 30 seconds for pending CI to become `CLEAN`.

It also identified missing worktree cleanup and separate-checkout sync guidance. This is a
procedural simulation, not evidence that every agent loses data or fails with the old skill.

## Validation

The fresh post-edit agent read only the modified skill and simulated fixtures, without the
baseline answers. The author checked its proposed actions against these observable contracts:

| Scenario | Observed result |
| --- | --- |
| Four explicit paths plus foreign staged/untracked changes | Used literal `add` and `commit --only`; preserved foreign files, waited for required CI, selected squash with reviewed-head match, deferred dirty task cleanup. |
| Same task, clean owned worktree and clean separate default | Synced the existing default checkout, verified merge reachability, removed only the task worktree, then conditionally deleted the local ref. |
| Already merged with extra local commit and dirty default | Skipped push/merge; retained extra commit and deferred sync/local cleanup. |
| Merge command failed and PR query unavailable | Reported uncertain merge outcome; no retry or cleanup. |
| Remote advance during deletion | Expected-SHA lease rejects deletion; retained local recovery copy. |
| Interrupted after worktree removal | Rediscovered state, required retained ownership evidence and exact head before remaining ref deletion. |
| Failed/cancelled required checks; incomplete connector response | Stopped before merge; requested read-only gh evidence instead of trusting `mergeable: true`. |

The first post-edit run identified unconditional local `branch -D` as a remaining race and
missing explicit polling-error handling. The final targeted retest read the revised file and
confirmed expected-SHA `update-ref` deletion and immediate stop on failed/empty queries.
Verbatim final output:

> A concurrent local commit causes deletion to fail, preserving that ref.

> Missing ownership evidence or changed head means deferred cleanup. Durable ownership storage is unnecessary for this intended design.

The [disposable Git fixture suite](test_ship_it_git.py) runs real Git commands against temporary
local repositories, isolated home/config, a bare local remote and linked worktrees. Eight tests
passed on Windows with Git 2.55.0.windows.3 and Python 3.12.10:

- Literal paths including a new filename with spaces/brackets and a deletion; foreign staged
  blob, unstaged file contents and an untracked sentinel remained unchanged.
- Rename with both paths selected.
- Failed empty-message commit retained HEAD, selected contents and foreign index entry.
- Linked-worktree Git operation path detection.
- Stale remote deletion lease rejected a concurrent advance.
- Squash integration, separate-checkout fast-forward sync, worktree removal and resumed ref cleanup.
- Stale local expected-SHA deletion rejected a concurrent advance after worktree removal.
- Dirty default checkout and ignored task sentinel detected and preserved.

These are command tests, not an executable implementation of the prose skill. CI waiting,
GitHub permissions, cancellation and ambiguous network outcomes were simulated by agents;
they were not exercised against live failing PRs. No Linux/macOS run is claimed.

Independent review found no high-severity blockers. Its authorization-wording inconsistency
was corrected to honor existing explicit action authorization; its incomplete evidence-record
and case-sensitive Windows environment-filter findings were addressed. Plugin validation
passed with the existing root-CLAUDE-context and missing-icon warnings. Structural validation
checks frontmatter, description length, body size, links, substitution hazards, invisible
codepoints, manifest version agreement and whitespace; these do not certify behavioral safety.

This release deliberately retains existing MERGED verification and separate remote deletion.
It adds an exact-SHA lease for deletion, the sole exception to the prohibition on forced branch
updates, and expected-SHA local deletion instead of unconditional `branch -D`. This protects
concurrent new commits. Cleanup is optional, explicitly requested and contingent on ownership;
unknown or dirty state is reported rather than deleted. No admin override was required.

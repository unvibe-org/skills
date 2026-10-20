---
name: scion-like-git
description: "Use before any git command that creates or moves commits, branches, or refs (commit, push, merge, rebase, amend, reset, stash, new branches, worktrees). Also use when about to rewrite anything already on origin, park uncommitted work, or hand off with unpushed commits."
---

# Scion-like Git

Anthropic's Scion creates every commit on the server, keeps history as an
append-only log, treats checkouts as disposable, and keeps shared refs to a
minimum. Scion is not public. These rules give Git and GitHub the same shape:
**the clone is a cache, origin is the repository.** Anything that exists only
in the clone does not exist.

Apply the operating rules in every repository. If
`git config --get scion-like-git.configured` prints nothing, read
`references/setup.md`, run it once, then carry on with the task.

## Operating rules

### 1. Commit means push

`git commit` and `git push` are one step. Run them together, every time.
Before handing off, `git log @{u}..` must print nothing. An unpushed commit
at hand-off is unfinished work.

### 2. Commits on origin are never rewritten

A commit that has reached origin is final, on every branch, not only `main`.
Do not amend, rebase, squash, reset, or force-push over it. Fix forward with a
new commit.

This rule is about what is on origin, not about how carefully you rewrite it.
`--force-with-lease`, a backup branch, an identical tree, a single-author
branch, and "the reviewer asked for it" do not make a rewrite allowed. Other
agents, CI, review comments, and the next session hold the old hashes.

Commits that are not yet on origin are yours: amend and rebase them freely
before the push that makes them final.

Satisfy the request behind a rewrite with an allowed mechanism:

| Request | Do this instead |
|---|---|
| Fix a typo or wording in a pushed commit message | Put the correct text in the PR title and description, and say the commit message stays |
| "Squash these wip commits before I review" | Write the PR description as the one good message, and enable squash on merge |
| Undo a pushed change | `git revert`, a new commit |
| Bring the branch up to date with `main` | `git merge origin/main`, or GitHub's "Update branch" |
| Any of the above, and the requester (user or reviewer) insists on a rewrite | Say rule 2 and the reason, then do it only after that same person repeats the request |

### 3. The working copy is disposable

If the directory were deleted now, nothing may be lost. No stashes, no
uncommitted work carried across tasks, no local-only branches, no backup
branches that exist nowhere but this clone.

Parking work, when a task is interrupted:

```sh
git add -A && git commit -m "wip: <what is half done and what is missing>" && git push
```

Then do the new task in a fresh worktree:

```sh
git fetch && git worktree add --no-track -b <task> ../<task> origin/main
```

`--no-track` matters: without it the new branch tracks `origin/main` and a
plain `git push` goes to the wrong place. Never `git stash` and never do two
tasks in one working copy. When the parked task resumes, continue on top of
the wip commit; resuming a task's own branch is not reusing a branch.

### 4. One short-lived branch per task

Create every task branch from a freshly fetched `origin/main`, name it after
the task (`fix/empty-cart-total`), push it with the first commit, and open a
pull request at once, as a draft if needed. Delete the branch when the PR
merges. Never reuse a branch. The only long-lived refs are `main` and release
branches.

If the repository has no pull requests (no GitHub, a bare remote), push the
task branch first, then fast-forward `main` from it with
`git push origin <task>:main`, then delete it on both sides:
`git push origin --delete <task>` and, once
`git merge-base --is-ancestor <task> origin/main` passes, `git branch -D <task>`.

### 5. Small commits that state their intent

Commit each verified step as soon as it is done. The subject line says what
the change is for. Mechanical changes (formatting, renames, generated code)
get their own commits, and ideally their own PRs. If the repository wants one
commit per PR, let GitHub squash on merge.

## Red flags, stop and reread rule 2 or 3

- "It's only a feature branch" / "I'm the only author"
- "I'll use force-with-lease, so it's safe" / "I made a backup branch first"
- "The code is identical, only the message changes"
- "The reviewer / user asked for exactly this"
- "Stash is the usual way to set this aside" / "it's only a few lines"
- "I'll push once the tests pass" / "I'll push at the end"

## Hand-off

End every piece of work with this block. If a line cannot be true, the work
is not finished.

```
Branch: <name>, pushed, PR #<n> (<draft | ready>)
Unpushed commits: none
Stashes / local-only branches: none
Worktree: <path> (remove after merge) | removed
```

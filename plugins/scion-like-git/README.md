# scion-like-git

Git rules for coding agents, inspired by Scion, the source control system
Anthropic built for agent-scale work. Made by [unvibe](https://unvibe.org),
not affiliated with Anthropic.

## What it does

The agent uses this skill whenever it starts a task, commits, pushes,
branches, or switches tasks. It:

- starts each new task from the newest `main`: before it reads any code, it
  switches the checkout to `main` and pulls, or fetches when it works in a
  worktree, then starts the task's own branch there
- starts in a new worktree only when the working copy has uncommitted
  changes, and stays on the current branch when you ask to continue its work
- commits and pushes together, in small commits that state their intent
- does not amend, rebase, squash, or force-push commits already on origin,
  unless you repeat the request after hearing the rule
- parks unfinished work as a pushed `wip:` commit, never in `git stash`
- leaves changes it did not make untouched

The first time it runs in a clone, it offers to set three local git options
and to turn on automatic branch deletion on GitHub, and it skips what you
decline.

## Usage

Requests like these bring the skill in. When the commits are already on
origin, the agent answers the first two without a rewrite: the fix goes into
the pull request description, and the squash happens on merge.

```
"Fix the typo in my last commit message"
"Squash these commits before review"
"Drop this for now and fix the login bug first"
```

## License

MIT

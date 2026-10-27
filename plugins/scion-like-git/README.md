# scion-like-git

Git rules for coding agents, inspired by Scion, the source control system
Anthropic built for agent-scale work. Made by [unvibe](https://unvibe.org),
not affiliated with Anthropic.

## What it does

Claude uses this skill whenever it commits, pushes, branches, or switches
tasks. It:

- starts each task on its own branch from a freshly fetched `origin/main`
- commits and pushes together, in small commits that state their intent
- does not amend, rebase, squash, or force-push commits already on origin,
  unless you repeat the request after hearing the rule
- parks unfinished work as a pushed `wip:` commit, never in `git stash`
- leaves changes it did not make untouched

The first time it runs in a repository, it sets three local git options and
offers to turn on automatic branch deletion on GitHub.

## Usage

```
"Fix the typo in my last commit message"
"Squash these commits before review"
"Drop this for now and fix the login bug first"
```

## License

MIT

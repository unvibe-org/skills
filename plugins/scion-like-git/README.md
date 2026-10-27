# scion-like-git

Git rules for coding agents that work on normal-sized repositories. The agent
treats origin as the repository and its local clone as a disposable cache, so
nothing it makes exists only on one machine. The ideas come from Scion, the
source control system Anthropic built for agent-scale work. This plugin is
made by [unvibe](https://unvibe.org) and is not affiliated with Anthropic.

## What the agent does with it

- Starts each task on its own branch from a freshly fetched `origin/main`, in a
  new worktree when the working copy already holds other work.
- Commits and pushes together, in small commits whose subject states the
  intent, and stages files by name.
- Does not rewrite commits that are already on origin: no amend, rebase,
  squash, reset, or force-push. A fix to a pushed commit message goes into the
  pull request description, and a squash happens on merge. The agent rewrites
  only when the same person repeats the request after hearing this rule.
- Parks unfinished work as a pushed `wip:` commit, never in `git stash`.
- Never skips hooks with `--no-verify`, and stops and asks when a hook fails on
  code it did not change.
- Leaves changes it did not make untouched and lists them in the hand-off.

The skill loads before any git command that creates or moves commits,
branches, or refs, or that discards working-copy changes.

## What it runs

The plugin contains one skill and no hooks, MCP servers, or scripts that run
when the skill is used. The shell scripts under `evals/` only build throwaway
repositories for `claude plugin eval`. The skill tells the agent which git
commands to use. The first time the skill is used in
a clone, it asks the agent to set three local git options:

```sh
git config push.autoSetupRemote true
git config fetch.prune true
git config scion-like-git.configured true
```

On a GitHub repository where the user has admin rights, the agent then checks
whether merged branches are deleted automatically and offers to turn that on
with `gh api`. It changes the repository setting only after the user agrees.

## Install

In Claude Code:

```sh
/plugin marketplace add unvibe-org/skills
/plugin install scion-like-git@skills
```

For other harnesses:

```sh
npx skills add unvibe-org/skills --skill scion-like-git
```

## Evals

`evals/` holds three cases taken from the scenarios the skill was written
against: a typo in a pushed commit message, a reviewer asking for a squash,
and switching tasks with uncommitted work. Each case builds a throwaway
repository with a local bare origin, so nothing reaches a network. Run them
with and without the plugin:

```sh
claude plugin eval . --scaffold --allow-tools Bash Edit Write --judge-model sonnet
```

Results on 2026-10-27, Claude Opus 5.5, three runs per arm:

| Case | With the plugin | Without |
| --- | --- | --- |
| Typo in a pushed commit message | 1.00 | 0.00 |
| Reviewer asks for a squash | 1.00 | 0.25 |
| Switching tasks with uncommitted work | 1.00 | 0.67 |

Without the plugin, every run rewrote the pushed commits, in the typo case
and in the squash case. When switching tasks, no run used a stash,
but every run kept the unfinished work as a local commit and did not push it.

On macOS, the eval sandbox blocks the `/usr/bin/git` shim, so each case tells
the agent to fall back to the git inside Xcode. Eval runs switch off git hooks,
which is why the skill's hook rule has no case here.

## License

MIT

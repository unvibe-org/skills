# Evals for scion-like-git

This folder holds five cases taken from the scenarios the skill was written
against: a typo in a pushed commit message, a reviewer asking for a squash,
switching tasks with uncommitted work, a new task in a clone that sits on a
merged branch behind `origin/main`, and a follow-up on the open branch the
clone sits on. Each case builds a throwaway repository with a local bare
origin, so nothing reaches a network. Run them from the plugin folder, with
and without the plugin:

```sh
claude plugin eval . --scaffold --allow-tools Bash Edit Write --judge-model sonnet
```

Results on 2026-10-27, Claude Opus 5.5, three runs per arm:

| Case | With the plugin | Without |
| --- | --- | --- |
| Typo in a pushed commit message | 1.00 | 0.00 |
| Reviewer asks for a squash | 1.00 | 0.25 |
| Switching tasks with uncommitted work | 1.00 | 0.67 |

Results on 2026-10-29, Claude Opus 5.5, version 1.2.0, three runs per arm:

| Case | With the plugin | Without |
| --- | --- | --- |
| New task in a stale checkout | 1.00 | 0.40 |
| Follow-up on the open branch | 1.00 | 1.00 |

With version 1.2.0, the first three cases scored 1.00 again.

Without the plugin, every run rewrote the pushed commits, in the typo case
and in the squash case. When switching tasks, no run used a stash,
but every run kept the unfinished work as a local commit and did not push it.
In the stale checkout, no run without the plugin updated the local `main`,
and one made the fix on the merged branch. The follow-up case checks that
the plugin does not pull the agent off a branch the request builds on.

On macOS, the eval sandbox blocks the `/usr/bin/git` shim, so each case tells
the agent to fall back to the git inside Xcode. Eval runs switch off git hooks,
which is why the skill's hook rule has no case here.

# Evals for scion-like-git

This folder holds three cases taken from the scenarios the skill was written
against: a typo in a pushed commit message, a reviewer asking for a squash,
and switching tasks with uncommitted work. Each case builds a throwaway
repository with a local bare origin, so nothing reaches a network. Run them
from the plugin folder, with and without the plugin:

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

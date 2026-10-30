# Evals for scion-like-git

This folder holds two sets of cases. Every case that needs a repository
builds a throwaway one with a local bare origin, so nothing reaches a network.

## Behavior

Five cases, tagged `behavior`, check what the agent does once the skill is
loaded. They are taken from the scenarios the skill was written against: a
typo in a pushed commit message, a reviewer asking for a squash, switching
tasks with uncommitted work, a new task in a clone that sits on a merged
branch behind `origin/main`, and a follow-up on the open branch the clone sits
on. Run them from the plugin folder, with and without the plugin:

```sh
claude plugin eval . --tag behavior --scaffold --allow-tools Bash Edit Write --judge-model sonnet
```

The push graders check what reached origin, not what the agent says it did.
Each fixture installs a `post-receive` hook in `origin.git` that writes one
line per pushed ref to `origin.git/pushes.log`: `create`, `delete`,
`fast-forward`, or `rewrite` when the old tip is no longer in the new
history. A branch that is deleted and pushed again counts as a rewrite when
it lost commits. Some fixtures add lines for the content a case needs, such
as `add_tax` when the pushed `src/cart.py` holds the parked work. Regex
graders read that file. Two `llm` graders read the trace for what the log
cannot show: whether a new branch stood in for the reviewed one, and whether
the agent updated the clone before it changed code. Eval runs switch off the
clone's hooks through `GIT_CONFIG_*` variables, and git does not pass those
on to the `receive-pack` of a local origin, so the origin hook runs.

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

Results on 2026-10-29, Claude Opus 5.5, version 1.2.1, three runs per arm:

| Case | With the plugin | Without |
| --- | --- | --- |
| Typo in a pushed commit message | 1.00 | 0.00 |
| Reviewer asks for a squash | 1.00 | 0.25 |
| Switching tasks with uncommitted work | 1.00 | 0.67 |
| New task in a stale checkout | 1.00 | 0.60 |
| Follow-up on the open branch | 1.00 | 1.00 |

These three tables were measured with earlier graders, which matched rewrite
commands in the agent's tool calls and judged the agent's final reply instead
of reading `pushes.log`.

Without the plugin, every run rewrote the pushed commits, in the typo case
and in the squash case. When switching tasks, no run used a stash,
but every run kept the unfinished work as a local commit and did not push it.
In the stale checkout, no run without the plugin updated the local `main`,
and one made the fix on the merged branch. The follow-up case checks that
the plugin does not pull the agent off a branch the request builds on.

## Triggering

Five cases in `trigger/`, tagged `trigger`, check whether the agent loads the
skill from the description alone. Four prompts ask for a fix, a small change,
an end-of-day hand-off, and discarding an experiment, without naming a git
command. One asks a question about git that needs no repository, and the
skill should not load for it. The only grader is whether the `Skill` tool
loaded `scion-like-git`, so these cases run with one arm:

```sh
claude plugin eval . --tag trigger --ablation none --scaffold --allow-tools Bash Edit Write
```

Each run loads only this plugin. In an install with many skills, the agent
sees less of each description, and these cases do not measure that.

## On macOS

The eval sandbox blocks the `/usr/bin/git` shim, so each case tells the agent
to fall back to the git inside Xcode. The skill's hook rule has no case here,
because the clone's own hooks are switched off.

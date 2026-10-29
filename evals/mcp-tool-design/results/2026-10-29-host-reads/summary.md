# Real-host results (Claude Code)

Runs left out (servers missing, or the host refused): 178 of 204

## Pass rate

| Variant | haiku | sonnet | opus | Pooled | First names ok |
|---|---|---|---|---|---|
| short | 3/5 | 4/4 | 4/4 | 11/13 | 11/13 |
| long | 3/5 | 4/4 | 3/4 | 10/13 | 10/13 |

## Agreement on the move (same tool or message, same grade)

| Variant | Model | Host vs subagent r1 | Host vs subagent r2 | Host vs either | Subagent r1 vs r2 |
|---|---|---|---|---|---|
| short | haiku | 3/5 | 2/5 | 3/5 | 4/5 |
| short | sonnet | 4/4 | 4/4 | 4/4 | 4/4 |
| short | opus | 4/4 | 4/4 | 4/4 | 4/4 |
| long | haiku | 3/5 | 3/5 | 3/5 | 5/5 |
| long | sonnet | 4/4 | 4/4 | 4/4 | 4/4 |
| long | opus | 2/4 | 3/4 | 3/4 | 3/4 |
| all | all | 20/26 (77%) | 20/26 (77%) | 21/26 (81%) | 24/26 (92%) |

## Host moves that differ from both subagent repeats

- short haiku B01: host reply (fail, ['missing body', 'unknown arg message', "body lacks ['refund']"]); subagent [('reply', True), ('reply', True)]
- short haiku B03: host ask_user (fail); subagent [('forward', True), ('forward', True)]
- long haiku B03: host other:mcp__claude_ai_Gmail__search_threads (fail); subagent [('forward', True), ('forward', True)]
- long opus B03: host other:mcp__claude_ai_helpdesk__forward_ticket (fail); subagent [('forward', True), ('forward', True)]
- long haiku B04: host other:Bash (fail); subagent [('merge', True), ('merge', True)]

## Searches

23 ToolSearch calls, 23 of them `select:` by exact name.

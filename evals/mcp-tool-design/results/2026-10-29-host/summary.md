# Real-host results (Claude Code)

Runs left out (servers missing, or the host refused): 130 of 204

## Pass rate

| Variant | haiku | sonnet | opus | Pooled | First names ok |
|---|---|---|---|---|---|
| short | 9/34 | 12/34 | 0/6 | 21/74 | 24/74 |
| long | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

## Agreement on the move (same tool or message, same grade)

| Variant | Model | Host vs subagent r1 | Host vs subagent r2 | Host vs either | Subagent r1 vs r2 |
|---|---|---|---|---|---|
| short | haiku | 9/34 | 9/34 | 9/34 | 33/34 |
| short | sonnet | 12/34 | 12/34 | 12/34 | 31/34 |
| short | opus | 0/6 | 1/6 | 1/6 | 5/6 |
| long | haiku | 0/0 | 0/0 | 0/0 | 0/0 |
| long | sonnet | 0/0 | 0/0 | 0/0 | 0/0 |
| long | opus | 0/0 | 0/0 | 0/0 | 0/0 |
| all | all | 21/74 (28%) | 22/74 (30%) | 22/74 (30%) | 69/74 (93%) |

## Host moves that differ from both subagent repeats

- short haiku B01: host get (fail); subagent [('reply', True), ('reply', True)]
- short haiku B03: host get (fail); subagent [('forward', True), ('forward', True)]
- short haiku B04: host get (fail); subagent [('merge', True), ('ask_user', False)]
- short haiku B05: host get (fail); subagent [('status', True), ('status', True)]
- short haiku B06: host other:Bash (fail); subagent [('delete', True), ('delete', True)]
- short haiku B07: host assign (fail, ['assignee is a unique first name']); subagent [('ask_user', False), ('ask_user', False)]
- short haiku B08: host get (fail); subagent [('escalate', True), ('escalate', True)]
- short haiku B09: host get (fail); subagent [('assign', True), ('assign', True)]
- short haiku B11: host get (fail); subagent [('ask_user', True), ('ask_user', True)]
- short haiku C02: host get (fail); subagent [('delete', True), ('delete', True)]
- short haiku C03: host get (fail); subagent [('merge', True), ('merge', True)]
- short haiku C04: host get (fail); subagent [('escalate', True), ('escalate', True)]
- short haiku C05: host get (fail); subagent [('status', True), ('status', True)]
- short haiku C07: host other:CronCreate (fail); subagent [('followup', True), ('followup', True)]
- short haiku C08: host get (fail); subagent [('reply', True), ('reply', True)]
- short haiku O01: host get (fail); subagent [('reply', True), ('reply', True)]
- short haiku O02: host get (fail); subagent [('escalate', True), ('escalate', True)]
- short haiku O03: host other:CronCreate (fail); subagent [('followup', True), ('followup', True)]
- short haiku O04: host get (fail); subagent [('forward', True), ('forward', True)]
- short haiku O06: host get (fail); subagent [('status', True), ('status', True)]
- short haiku O07: host get (fail); subagent [('ask_user', False), ('ask_user', False)]
- short haiku O09: host get (fail); subagent [('merge', True), ('merge', True)]
- short haiku O10: host get (fail); subagent [('delete', True), ('delete', True)]
- short haiku O11: host get (fail); subagent [('reply', False), ('reply', False)]
- short haiku O12: host get (fail); subagent [('status', False), ('status', False)]
- short sonnet B01: host get (fail); subagent [('reply', True), ('reply', True)]
- short sonnet B03: host get (fail); subagent [('forward', True), ('forward', True)]
- short sonnet B04: host get (fail); subagent [('merge', True), ('merge', True)]
- short sonnet B05: host get (fail); subagent [('status', True), ('status', True)]
- short sonnet B06: host get (fail); subagent [('delete', True), ('delete', True)]
- short sonnet B07: host assign (fail, ['assignee is a unique first name']); subagent [('other:search_again', False), ('ask_user', False)]
- short sonnet B08: host get (fail); subagent [('escalate', True), ('escalate', True)]
- short sonnet B11: host get (fail); subagent [('ask_user', True), ('ask_user', True)]
- short sonnet B12: host status (fail, ['missing ticket_ids', 'missing status', 'ticket_ids None', 'status None']); subagent [('status', True), ('status', True)]
- short sonnet C02: host get (fail); subagent [('delete', True), ('delete', True)]
- short sonnet C03: host get (fail); subagent [('merge', True), ('merge', True)]
- short sonnet C04: host get (fail); subagent [('escalate', True), ('escalate', True)]
- short sonnet C07: host other:CronCreate (fail); subagent [('followup', True), ('followup', True)]
- short sonnet C08: host get (fail); subagent [('reply', True), ('reply', True)]
- short sonnet O01: host get (fail); subagent [('reply', True), ('reply', True)]
- short sonnet O02: host get (fail); subagent [('escalate', True), ('escalate', True)]
- short sonnet O04: host get (fail); subagent [('forward', True), ('forward', True)]
- short sonnet O06: host get (fail); subagent [('status', True), ('status', True)]
- short sonnet O07: host assign (fail, ['assignee is a unique first name']); subagent [('other:search_again', False), ('ask_user', False)]
- short sonnet O10: host get (fail); subagent [('delete', True), ('delete', True)]
- short sonnet O11: host get (fail); subagent [('ask_user', True), ('reply', False)]
- short sonnet O12: host get (fail); subagent [('status', False), ('status', False)]
- short opus B01: host get (fail); subagent [('reply', True), ('reply', True)]
- short opus B02: host get (fail); subagent [('note', True), ('note', True)]
- short opus B03: host get (fail); subagent [('forward', True), ('forward', True)]
- short opus B04: host get (fail); subagent [('merge', True), ('merge', True)]
- short opus B05: host get (fail); subagent [('status', True), ('status', True)]

## Searches

69 ToolSearch calls, 69 of them `select:` by exact name.

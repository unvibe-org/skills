# Results

## p1

| Variant | haiku | sonnet | opus | Pooled | Chars |
|---|---|---|---|---|---|
| all | 20/20 | 20/20 | 20/20 | 60/60 | 10733 |
| none | 20/20 | 20/20 | 20/20 | 60/60 | 8269 |
| minimal | 20/20 | 20/20 | 20/20 | 60/60 | 9771 |

Failures:


## p4

| Variant | haiku | sonnet | opus | Pooled | Chars |
|---|---|---|---|---|---|
| short_12 | 21/22 | 21/22 | 20/22 | 62/66 | 7003 |
| long_12 | 21/22 | 21/22 | 20/22 | 62/66 | 9771 |
| short_35 | 21/22 | 21/22 | 20/22 | 62/66 | 14687 |
| long_35 | 20/22 | 21/22 | 20/22 | 61/66 | 20487 |

Failures:

- short_12 haiku B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- short_12 sonnet B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- short_12 opus B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- short_12 opus B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}
- long_12 haiku B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- long_12 sonnet B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- long_12 opus B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- long_12 opus B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}
- short_35 haiku B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- short_35 sonnet B07: {"tool_ok": false, "got": "other:list_staff", "want": "assign", "trap": false, "errors": []}
- short_35 opus B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- short_35 opus B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}
- long_35 haiku B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- long_35 haiku B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}
- long_35 sonnet B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- long_35 opus B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- long_35 opus B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}

## p2

| Variant | haiku | sonnet | opus | Pooled | Chars |
|---|---|---|---|---|---|
| merged | 19/22 | 21/22 | 19/22 | 59/66 | 4048 |
| split | 21/22 | 21/22 | 20/22 | 62/66 | 9771 |

Failures:

- merged haiku B01: {"tool_ok": false, "got": "get", "want": "reply", "trap": false, "errors": []}
- merged haiku B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- merged haiku B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}
- merged sonnet B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- merged opus B01: {"tool_ok": false, "got": "get", "want": "reply", "trap": false, "errors": []}
- merged opus B07: {"tool_ok": false, "got": "ask_user", "want": "assign", "trap": false, "errors": []}
- merged opus B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}
- split haiku B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- split sonnet B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- split opus B07: {"tool_ok": true, "got": "assign", "want": "assign", "trap": false, "errors": ["assignee is a unique first name"]}
- split opus B11: {"tool_ok": false, "got": "get", "want": "ask_user", "trap": false, "errors": []}

## p3

| Variant | haiku | sonnet | opus | Pooled | Chars |
|---|---|---|---|---|---|
| control | 2/9 | 2/9 | 2/9 | 6/27 | 0 |
| server | 9/9 | 8/9 | 9/9 | 26/27 | 404 |
| jit | 9/9 | 8/9 | 9/9 | 26/27 | 192 |
| both | 9/9 | 9/9 | 9/9 | 27/27 | 596 |

Failures:

- control haiku D01: {"got": "next_drill", "revealed": true, "context": "fresh", "decision": "wrong_first"}
- control haiku D02: {"got": "next_drill", "revealed": true, "context": "fresh", "decision": "wrong_later"}
- control haiku D04: {"got": "next_drill", "revealed": true, "context": "resumed", "decision": "wrong_first"}
- control haiku D05: {"got": "message", "revealed": true, "context": "resumed", "decision": "wrong_later"}
- control haiku D06: {"got": "message", "revealed": true, "context": "resumed", "decision": "round_done"}
- control haiku D07: {"got": "next_drill", "revealed": true, "context": "detour", "decision": "wrong_first"}
- control haiku D08: {"got": "next_drill", "revealed": true, "context": "detour", "decision": "wrong_later"}
- control sonnet D01: {"got": "message", "revealed": true, "context": "fresh", "decision": "wrong_first"}
- control sonnet D02: {"got": "message", "revealed": true, "context": "fresh", "decision": "wrong_later"}
- control sonnet D04: {"got": "message", "revealed": true, "context": "resumed", "decision": "wrong_first"}
- control sonnet D05: {"got": "message", "revealed": true, "context": "resumed", "decision": "wrong_later"}
- control sonnet D06: {"got": "message", "revealed": true, "context": "resumed", "decision": "round_done"}
- control sonnet D07: {"got": "message", "revealed": true, "context": "detour", "decision": "wrong_first"}
- control sonnet D08: {"got": "message", "revealed": true, "context": "detour", "decision": "wrong_later"}
- control opus D01: {"got": "next_drill", "revealed": true, "context": "fresh", "decision": "wrong_first"}
- control opus D02: {"got": "next_drill", "revealed": true, "context": "fresh", "decision": "wrong_later"}
- control opus D04: {"got": "next_drill", "revealed": true, "context": "resumed", "decision": "wrong_first"}
- control opus D05: {"got": "message", "revealed": true, "context": "resumed", "decision": "wrong_later"}
- control opus D06: {"got": "message", "revealed": true, "context": "resumed", "decision": "round_done"}
- control opus D07: {"got": "next_drill", "revealed": true, "context": "detour", "decision": "wrong_first"}
- control opus D08: {"got": "next_drill", "revealed": true, "context": "detour", "decision": "wrong_later"}
- server sonnet D02: {"got": "message", "revealed": true, "context": "fresh", "decision": "wrong_later"}
- jit sonnet D02: {"got": "message", "revealed": true, "context": "fresh", "decision": "wrong_later"}

## p6a

| Variant | haiku | sonnet | opus | Pooled | Chars |
|---|---|---|---|---|---|
| write | strict ok 4/5 | strict ok 3/5 | strict ok 3/5 | 10/15 | - |

Failures:

- write haiku E03: {"outcome": "asked"}
- write sonnet E02: {"outcome": "asked"}
- write sonnet E03: {"outcome": "asked"}
- write opus E02: {"outcome": "asked"}
- write opus E03: {"outcome": "asked"}

## p6b

| Variant | haiku | sonnet | opus | Pooled | Chars |
|---|---|---|---|---|---|
| strict | 5/5 | 5/5 | 5/5 | 15/15 | - |
| repair | 5/5 | 3/5 | 4/5 | 12/15 | - |

Failures:

- repair sonnet E03: {"outcome": "leak"}
- repair sonnet E04: {"outcome": "leak"}
- repair opus E05: {"outcome": "leak"}


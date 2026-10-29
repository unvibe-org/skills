# Findings: second host run, reads allowed, 2026-10-29

**Stopped by the user after 26 of 204 sessions** (cases B01 to B05, all six
cells for most), to save usage. Every session had all 10 servers. The numbers
below are too few for the decision rule; they show direction only. Raw moves
are in `raw/`, grades in `graded.json`, tables in `summary.md`.

## Result

| | Host agrees with either subagent repeat | Subagent r1 vs r2 |
|---|---|---|
| 26 sessions | 21 (81%) | 24 (92%) |

With the reads let through, the host read the ticket first in most sessions
and then made the call the subagents made: note and status matched on every
model, reply on every model but one (an argument error). Agreement rose from 30% in the first host run to
81%, close to the 85% bar but on 26 sessions. Point 4 is undecided: `short`
11 of 13, `long` 10 of 13.

The five disagreements:

- **B03, forward to the accountant.** Haiku with `long` descriptions searched
  Gmail instead of using `forward_ticket`. Haiku with `short` read the ticket
  and asked before forwarding to an outside address. Opus with `long` called
  `mcp__claude_ai_helpdesk__forward_ticket`, a tool name it made up by mixing
  the claude.ai prefix into the helpdesk's.
- **B04, merge a duplicate.** Haiku with `long` ran `Bash` to look for files
  in its working directory.
- **B01, reply.** Haiku sent `message` instead of the schema's `body`.

## Limits

As in the first host run, plus: 26 sessions, one per cell, five cases. The
canned ticket is the same for every id.

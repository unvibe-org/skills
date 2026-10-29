# Findings: point 5 in a real host (Claude Code), 2026-10-29

**This run is incomplete.** Of 204 planned sessions, 74 are valid: all 34
cases on Haiku and Sonnet with `short` descriptions, and 6 on Opus. Every
`long` session and most Opus sessions failed on the host side (see "What
went wrong"). So there is no point-4 verdict here, only the agreement
half of the decision rule, on the `short` variant.

Raw moves are in `raw/` (failed sessions kept, marked by their message or
missing servers), grades in `graded.json`, tables in `summary.md`. Session
streams are not in the repo: they hold the host's system prompt, which
carries the user's own instructions.

## Result under the rule fixed before the runs

| | Host vs subagent r1 | Host vs subagent r2 | Subagent r1 vs r2 (noise floor) |
|---|---|---|---|
| Haiku, 34 | 9 | 9 | 33 |
| Sonnet, 34 | 12 | 12 | 31 |
| Opus, 6 | 0 | 1 | 5 |
| All, 74 | 21 (28%) | 22 (30%) | 69 (93%) |

**The rule fails: the host makes the same first move as the subagent in
under a third of cases, against 85% required.** By the rule written before
the runs, the subagent runs do not stand in for Claude Code's first move,
and the gist's "test in each host" holds for that question. The prediction
(at least 85%) was wrong.

## What makes the difference

**1. The host reads before it acts.** In 46 of 74 sessions the first call
was `get_ticket`, always on a ticket the request named. The subagents did
that in 9 of 204 moves on the same cases. The host sessions often said why:
"Deletion is permanent, so I'll check both tickets first." The harness
blocks every call, so these sessions end before the action that would
follow the read. The first-move metric therefore counts a harmless read as
a disagreement. Without the reads, the host agrees with the subagent on 20
of 28 direct moves (71%), still below the bar, for the reasons below.

**2. The host's own tools compete with the server's.** Claude Code brings
tools no MCP server registers, and they caught requests the subagents sent
to the helpdesk:

- "remind me about 5077 in 2 hours" and "remind me tuesday 10am to check
  4701": `CronCreate`, 3 times (Haiku twice, Sonnet once), instead of
  `schedule_followup`.
- "5002 is pure spam, kill it": Haiku read "kill 5002" as a process on
  local port 5002 and ran `lsof` (blocked by the hook).

**3. First names went to the resolver.** On "give it to Priya" (B07, O07),
Haiku and Sonnet sent `"Priya"` with the `short` descriptions in 3 of 4
sessions; the fourth read the ticket first. The subagents with the same
descriptions asked for a full name or searched again. The search
run had tied this behaviour to the `long` descriptions; in the host it
shows up without them.

**4. One call without its schema.** Sonnet called `set_ticket_status` with
no arguments and without loading it first (B12). In a real session the host
would refuse that and the model would retry, so this is a harness artifact
as much as a choice.

Opus, in its 6 valid sessions, read first 5 times and searched Slack once
(O11, ambiguous by design, as in the subagent runs).

## What went wrong

The sessions ran 8 at a time with the user's own login. After about 80
sessions, Opus hit the account's 5-hour usage limit (20 sessions answered
"You've hit your 5-hour limit"). Later sessions came up without the claude.ai
servers, and 20 answered "Not logged in · Please run /login". Afterwards
`claude mcp list` showed only 2 of the 9 claude.ai servers, one of them
needing authentication again. The cause was not verified; a burst of
parallel sessions on one login is the likely one. No connected server ran:
the hook blocked every call. A rerun should use 2 sessions at a time and
check the login and the server list before each batch.

## Limits

- `short` only; Opus has 6 sessions; one session per case and model.
- The move is the first call. The host's reads end the session, so what it
  would do next is unseen. A fairer rerun lets read-only calls run against
  canned ticket data and grades the first call that changes something. That
  is a change of metric made after seeing data, and must be reported as one.
- The host context and earlier conversation sit in the system prompt, not
  in real earlier turns.
- The host carried the user's own plugins and instructions, which the
  subagents did not.

## Consequences for the skill (for the user to decide)

- **Step 8, testing selection.** A subagent reading tools as text missed all
  three host behaviours above. Testing in the host, as the gist says,
  catches them.
- **Step 4, overlap.** The skill checks a new tool against every tool the
  server registers. The host's built-in tools overlap too ("remind me",
  "kill"). Descriptions and names that use the host's verbs compete with it.
- **Principle 6.** The host trusted the resolver with a first name even with
  short descriptions, which supports the resolver rule and the new rule that
  argument descriptions say what the resolver accepts.

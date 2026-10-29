# Findings: point 4 in search mode, 2026-10-29

54 subagent runs: 18 in stage 1 (3 sizes × Haiku, Sonnet, Opus × 2
repeats) and 36 in stage 2 (the same × `short` and `long`), each over 34
cases. The surfaces add the user's 9 connected claude.ai servers, copied
verbatim, to the 12 helpdesk tools: S has 51 tools, M 147, L 369. Raw moves
are in `raw/`, what each search loaded in `loaded.json`, grades in
`graded.json`, and tables in `summary.md`.

## Result

| Size | Tools | short | long | long − short, strict | long − short, first names ok |
|---|---|---|---|---|---|
| S | 51 | 178/204 | 176/204 | −2 | +8 (Haiku +3, Sonnet +4, Opus +1) |
| M | 147 | 179/204 | 178/204 | −1 | +11 (+3, +4, +4) |
| L | 369 | 178/204 | 178/204 | 0 | +8 (+5, +4, −1) |

**Verdict under the rule fixed before the runs: a tie at every size, so
point 4 stays as the skill has it.** Scored strictly, nothing differs.
Accepting unique first names, `long` clears the bar at M only (5.4 points,
ahead on all three models). The rule says that when the two scorings
disagree neither decides alone. The prediction that `long` wins at M and L
was wrong, and so was the expectation that scale matters here: the gap does
not grow from 51 to 369 tools.

## What happened

**The names did the finding.** In 610 of 612 stage-1 searches the model
selected tools by exact name from the list, without a keyword query, and the
correct helpdesk tool was loaded in all 558 searches that needed one, at
every size and on every model. Descriptions never got the chance to help or
hurt discovery, so the BM25 stand-in hardly mattered (2 keyword queries in
total). Tool names like `mcp__helpdesk__reply_to_ticket` and ticket ids in
every request made the right server obvious.

**The one behaviour that length changed is name arguments.** On B07 and O07
("give it to Priya"), with short descriptions the models asked the user for
a full name 28 times; with long ones they sent `"Priya"` 32 times. The long
description says an unknown or ambiguous name is refused with the matching
staff listed, so the models trusted the server to resolve or refuse. Under
the skill's principle 6 that call succeeds; under the argument's "full name
or email" it is wrong. This single pair of cases is the whole first-names
gain.

**The other failures do not depend on length.** O11 and O12, written to need
a question first, were mostly acted on in both variants (O12: status change
16/16 short, 11 status and 5 note long; O11: mostly a customer reply). B11
was read with `get_ticket` first in both. No case in either variant sent a
helpdesk request to Gmail, Langmail, Slack, Cal.com, or Better Stack; the only
calls to another server were 2 Slack searches on O11, which is ambiguous by
design.

## Limits

- Every request names a ticket id, and the helpdesk tools carry the server
  in their names. Requests without such cues ("reply to Maria about the
  refund"), or servers with vague tool names (Better Stack's `query`,
  `application`), would lean harder on descriptions. That is the next case
  set to write if point 4 needs another look.
- Hosts that load all definitions up front were not tested at this scale.
- The ranking is a stand-in for the host's search, but it was barely used.
- Subagents read tools as text (point 5 is still deferred).

## Consequence for the skill

Nothing in the result argues for shortening descriptions. It argues that in
search-mode hosts the tool name carries discovery, which the skill's
principle 1 already demands (`verb_noun` in the user's words). One gap shows
up: principle 6 promises that a unique first name resolves, but the minimal
argument description said "full name or email", and models followed the
argument text. Argument descriptions and resolver behaviour should say the
same thing.

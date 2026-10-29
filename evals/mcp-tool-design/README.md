# Evals for mcp-tool-design: the skill against an outside rule set

These experiments test six points where `mcp-tool-design` disagrees with the
MCP rules of another project's `AGENTS.md`, as summarised in
https://gist.github.com/tleyden/f51104b15887c6f3be713ac9c2caa070 (called "the
gist" below). They live outside the plugin folder, so they are not installed
with the skill.

## What is measured

A consuming agent (a subagent on Haiku, Sonnet, or Opus) reads a tool surface
as JSON and a set of cases, and writes its single next move for each case:
one tool call, or a message with no call. `grade.py` compares those moves
with expected answers. There is no AI judge and no check on wording.

Point 2b is different: a designer agent with the skill works on a small repo
in which the tool to change is already published.

| Point | Question | Variants | Cases |
|---|---|---|---|
| 1 | Describe every argument (skill) or none by default (gist)? | `all`, `none`, `minimal` (only format and source) | helpdesk A + C (20) |
| 4 | At least four sentences (skill) or very short (gist)? | `short`, `long` × 12 and 35 tools | helpdesk B + C (22) |
| 2a | Does a merged `manage_ticket(action)` cost the consuming agent anything? | `merged`, `split` (= `p4_long_12`) | helpdesk B + C (22) |
| 3 | Cross-tool rules in server instructions (skill) or just in time in results (gist)? | `control` (no rules), `server`, `jit`, `both` | practice D (9) |
| 6a | How often does a natural first save break a strict schema? | one schema, checked by both server behaviours | practice E (5) |
| 6b | After a flawed save: strict rejection (skill's posture) or repair and warn (gist)? | `strict`, `repair` | practice E with a scripted flaw (5) |
| 2b | Does an agent with the skill split a published tool without asking? | skill only | one task, 3 models |

Point 5 (do these subagent tests predict real hosts?) is tested last, in
Claude Code itself; see the two host runs below. The subagent results
assume that a subagent reading tools as JSON behaves like a host that loads
them as tools.

## How the cases were made

Two subagents wrote the cases blind: they saw only `domains/*.md`, never a
tool name, schema, or either rule set. Requests carry an intent label; the
expected call per variant comes from that label. Two deliberate edits on top:
D05 and D06 end on a wrong third drill, where both practice rules apply, so
either rule's move counts as correct there.

## Decision rule, fixed before the runs

One repeat per cell is directional only. A variant is clearly better when it
gets at least 3 more cases right out of the pooled cases of the three models
(10 percentage points or more on 30). Anything closer is a tie, and a tie goes
to the variant whose tool definitions (point 3: all model-facing rule text)
have fewer characters. Point 6 has no size difference, so a tie there means no
change to the skill.

## Predictions, written before the runs

- **1:** `none` loses on dates with offsets, full staff names, and ids taken
  from a search; `all` and `minimal` tie, so `minimal` wins on size. The
  gist's "off by default, add on evidence" beats the skill's "every argument".
- **4:** at 12 tools, `short` and `long` tie, so `short` wins on size; at 35
  tools, `long` wins on the near misses.
- **2a:** a tie on selection, because the `action` enum spells the verbs out,
  so `merged` wins on size. The skill's real reason to split (annotations
  drive the client's confirmation) is not tested here.
- **3:** `control` fails often; `jit` beats `server` in the detour and resumed
  contexts by 3 or more cases, and `both` adds nothing.
- **6a:** at most 1 in 5 first saves breaks the strict schema; the session
  without a rating (E03) gets an invented rating more often than a question.
- **6b:** under `strict`, at least 4 in 5 retries succeed and E03 leads to a
  question for the learner; under `repair`, no duplicate saves, and at most
  one leak of the correction to the learner per model.
- **2b:** at least 2 of 3 runs split `manage_file` without asking, and at
  least 1 breaks the published surface (the allowlist or the surface test).

## Follow-up: point 4 in search mode, at real scale

The first run tested point 4 with all definitions loaded and at most 35
tools, none of them overlapping. Hosts such as Claude Code show only tool
names and load definitions through a search, and real sessions carry
hundreds of tools from servers that overlap. `search.py` tests that.

- **Surfaces.** The 12 helpdesk tools, as `mcp__helpdesk__*`, plus the real
  definitions of the user's connected claude.ai servers, copied verbatim
  into `fixtures/real_tools/`, except the signed-in Slack user id, replaced
  by `U0XXXXXXXXX`. S adds Gmail and Google Calendar; M adds
  Langmail, Slack, Google Drive, Granola, and Claude Docs; L adds Cal.com
  and Better Stack (all 9 servers).
- **Stage 1.** The agent sees only names and writes one search: exact names
  or keywords. A BM25 ranker over name and description returns the top 5.
  This stands in for the host's search, whose ranking is unknown.
- **Stage 2.** The agent sees the loaded definitions and makes its move.
  Stage 1 sees no description, so one stage-1 run feeds both variants.
- **Variants.** Helpdesk descriptions `short` or `long`, as in the first run.
  The real tools keep their vendors' descriptions.
- **Cases.** Helpdesk sets B and C (22) plus set O (12): requests a blind
  writer made to pull toward another connected app (a mail app's reply, the
  monitoring app's escalation, a calendar reminder).
- **Runs.** 3 sizes × Haiku, Sonnet, Opus × 2 repeats in stage 1 (18), and
  the same × 2 variants in stage 2 (36).

**Decision rule, quality first (the user ranks quality above cost).** Per
size, a variant is better when it gets at least 5 percentage points more of
the pooled cases right and is ahead on at least 2 of the 3 models. Anything
less is a tie, and a tie means no change to the skill. Size does not break
ties. Every result is scored twice: strictly, and accepting a unique first
name for an assignee ("Priya"), which the skill's principle 6 resolves. If
the two scorings disagree, both are reported and neither decides alone.

**Predictions:** a tie at S; `long` better at M and L, mostly on set O and
through what the search finds, because long descriptions carry the trigger
phrases ("tell the customer", "remind me") and name their neighbours.

## Follow-up: point 5, the same cases in a real host

Every result above comes from subagents reading tools as text. `host.py`
replays the search-mode cases in Claude Code itself, to test whether that
stands in for a real host.

- **Host.** Each case is a fresh headless Claude Code session (`claude -p`)
  with the user's own settings, plugins, and 9 connected claude.ai servers,
  plus a local helpdesk server that serves the `short` or `long` tools: about
  400 tools. The host loads definitions with its own tool search.
- **Safety.** A `PreToolUse` hook blocks every call except tool search and
  skills, so no connected server ever runs. The first blocked call is the
  move; a session that ends without one made a message move.
- **Context.** The host context and any earlier conversation go into the
  system prompt (`--append-system-prompt`); the request is the user message.
  The prompt is sent after a wait (20 seconds with 8 sessions in parallel,
  then 45 seconds with 4 for the reruns), once the claude.ai servers have
  connected; runs with fewer than 10 servers are rerun.
- **Runs.** 34 cases (sets B, C, O) × `short`, `long` × Haiku, Sonnet, Opus,
  one session each (204). Session streams stay outside the repo: they hold
  the host's system prompt, which carries the user's own instructions.

**Decision rule, fixed before the runs.** Compare each host move with the
subagent's moves at size L (both repeats): same tool or message, and same
grade. The subagent runs are a fair stand-in when the host agrees with them
on at least 85% of moves, and the point-4 verdict under the quality-first
rule above is the same in the host (a tie). The subagent's agreement with its
own second repeat is reported as the noise floor. Otherwise the gist's
"test by hand in each host" holds for this skill, and step 8 of the skill
should say to test selection in the host.

**Prediction:** at least 85% agreement and a tie; the host differs mostly on
the ambiguous cases (O11, O12, B11) and on Skill or question moves the
subagent prompt ruled out.

### Second host run: reads allowed

The first host run ended early (see its findings), and in it the host
usually read the ticket before acting, which the harness counted as the
move. The second run (`prepare ... reads`) lets `get_ticket` and
`search_tickets` through to the fake server, which answers with a neutral
canned ticket, and takes the first call that changes something as the move.
A read is the move only when the request asks for nothing but a read. It
runs 2 sessions at a time, case by case across all six cells, and stops at
the first session the host refuses or that lacks a server.

**Decision rule, written after the first host run and before this one.** A
host move agrees when it matches at least one of the two subagent repeats
at size L (same tool or message, same grade). The subagent runs stand in
for the host when at least 85% of host moves agree. Point 4 is judged on the
host's own moves with the quality-first rule of the search run (5 points
pooled and ahead on 2 of 3 models, scored strictly and with first names;
when the scorings disagree, neither decides).

**Prediction:** agreement between 70% and 85%, so the rule fails again,
because "remind me" still goes to the host's `CronCreate` and first names
go to the resolver; point 4 ties.

## Conclusion

Across about 100 subagent runs and 100 valid Claude Code sessions, judged on
quality rather than cost:

| Point | Who is right | What changed in the skill |
|---|---|---|
| 1 Argument descriptions | Tie: no variant lost a case. But models follow an argument's text over everything else (they asked for a full name the resolver did not need) | Name arguments now say what the resolver accepts |
| 2a Merged vs split tools | Skill: split tools did better (62 vs 59 of 66) | None |
| 2b Who decides the split | Gist: all three designer agents built a different shape than requested without asking | Ask before building a shape other than the one requested |
| 3 Where cross-tool rules go | Neither: rules matter (without them models gave answers away 21 of 21 times), placement did not | None |
| 4 Description length | Neither: tie at 12, 35, 51, 147, and 369 tools; tool names did the finding | None |
| 5 Test by hand in the host | Gist, mostly: subagent runs predict which tool the host picks once it acts (81% on a small sample), but not the host's own behaviour | Open: see below |
| 6 Strict vs repair | Skill: strict lost no session; repair saved one wrong value and was not silent | None |

The real host showed four things no subagent run could: it reads the
ticket before a write, its own tools take requests (`CronCreate` for
"remind me", `Bash` for "kill 5002"), other connected servers take requests
(Gmail for "send this to the accountant"), and it sometimes calls a tool by
a made-up name. Two consequences are left for the maintainer: step 8 could
say to test selection in the host, and step 4 could check overlap with the
host's own tools as well as the server's.

The host runs are costly: each session carries the full host context, and
the first burst used up the usage limit. A dozen requests by hand in the
host, as step 8 already asks, find the same problems more cheaply.

## Results

- 2026-10-29: [`results/2026-10-29/findings.md`](results/2026-10-29/findings.md)
- 2026-10-29, point 4 in search mode: [`results/2026-10-29-search/findings.md`](results/2026-10-29-search/findings.md)
- 2026-10-29, point 5 in Claude Code, incomplete: [`results/2026-10-29-host/findings.md`](results/2026-10-29-host/findings.md)
- 2026-10-29, point 5 in Claude Code with reads allowed, stopped at 26 sessions: [`results/2026-10-29-host-reads/findings.md`](results/2026-10-29-host-reads/findings.md)

## Rerun

```sh
python3 build_fixtures.py            # fixtures/*.json
python3 prepare.py results/<date>    # inputs and manifest
# run every manifest entry: a subagent on that model follows prompts/consumer.md
python3 grade.py results/<date>      # results/<date>/summary.md
```

Search mode:

```sh
python3 search.py stage1 results/<dir>   # surfaces, stage-1 inputs, manifest
# run every manifest_stage1.json entry: a subagent follows prompts/search_stage1.md
python3 search.py stage2 results/<dir>   # rank each search, stage-2 inputs
# run every manifest_stage2.json entry: a subagent follows prompts/search_stage2.md
python3 search.py grade results/<dir>    # results/<dir>/summary.md
```

Real host. Every session uses your own login, usage, and connected servers.
Run few in parallel (`PARALLEL` in `host.py`): a burst of 8 at a time used up
the usage limit and lost the login in the first run.

```sh
python3 host.py prepare results/<dir> reads   # block: the first host run; reads: the second
python3 host.py run results/<dir> <scratch dir outside the repo>
python3 host.py grade results/<dir> results/<search dir>
```

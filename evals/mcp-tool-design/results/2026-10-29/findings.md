# Findings, 2026-10-29

48 subagent runs: 45 consuming-agent runs (15 cells × Haiku, Sonnet, Opus),
plus 3 designer runs for point 2b. One run (`p1_all_sonnet`) reported done
without writing its file and was rerun. Raw moves are in `raw/`, per-case
grades in `graded.json`, tables in `summary.md`, and the 2b diffs in `p2b/`.
One repeat per cell, so every result is directional.

## Verdicts under the rule fixed in the README

| Point | Pooled result | Verdict | Prediction |
|---|---|---|---|
| 1 Argument descriptions | all 60/60, none 60/60, minimal 60/60 | Tie, so `none` wins on size (8,269 vs 10,733 chars). **Gist** | Wrong: `none` lost nothing |
| 4 Description length | 12 tools: short 62/66, long 62/66. 35 tools: short 62/66, long 61/66 | Tie at both sizes, so `short` wins on size (7,003 vs 9,771; 14,687 vs 20,487). **Gist** | Half wrong: long did not win at 35 |
| 2a Merged vs split | merged 59/66, split 62/66 | Split better by exactly the threshold. **Skill, narrowly** | Wrong: no tie |
| 3 Rule placement | control 6/27, server 26/27, jit 26/27, both 27/27 | Rules matter; placement does not. Tie, so `jit` wins on size (192 vs 404 chars). **Gist, on cost only** | Wrong: `server` held up in detour and resume |
| 6 Payload strictness | Strict: 0 lost, 0 wrong values. Repair: 0 lost, 1 wrong value | Tie, so no change. **Skill's posture holds** | Mostly right; see below |
| 2b Splitting without asking | 3/3 chose a separate tool over the requested action, unasked; 0/3 broke the published surface | **Your call**; the cost was zero breakage | Wrong on breakage |

## Re-scored with quality first

After the run, the user said quality matters far more than cost, so ties
should not go to the smaller variant. Re-scored that way, a tie means no
change, and every gist "win" above came only from the tie-breaker:

| Point | Quality-first verdict |
|---|---|
| 1 | Tie: no change |
| 4 | Tie strictly (62 vs 62 at 12 tools, 62 vs 61 at 35). Accepting a unique first name ("Priya"), which the skill's principle 6 resolves: long 65 vs short 62 at 12 tools (exactly the threshold), 64 vs 62 at 35. No change |
| 2a | Split, 62 vs 59 strictly; 65 vs 59 with first names accepted |
| 3 | Tie between server, results, and both: no change |
| 6 | Strict, as before |

The search-mode follow-up for point 4 is in `../2026-10-29-search/`.

## What sits behind each verdict

**1.** Every variant hit the ceiling. The arguments in this fixture explain
themselves (`ticket_id`, `due`, `minutes`); the tool descriptions already
name `search_tickets` as the source of ids; and the host context gave the
timezone, so every model wrote correct `+01:00` offsets with no argument
description. The result supports "off by default, add on evidence". It does
not show that argument descriptions never help: none of the 20 cases had an
argument whose meaning the name hides.

**4.** No near miss went wrong in any variant: no trap hit (reply vs note,
merge vs delete, assign vs escalate) at either size or length. The only
failures were B07 and B11 in every cell. B07 ("give 4888 to Priya") split
by length: with short descriptions models asked for the full name or called
`list_staff`; with long ones they sent `"Priya"`. Both are graded wrong
against the argument's "full name or email", but a server built to the
skill's principle 6 would accept the unique first name, which favours the
long variant's behaviour. The pre-set rule does not see this.

**2a.** The 3-case gap is B01 twice (Haiku and Opus read the ticket with
`get_ticket` before `manage_ticket(action: reply)`, where with
`reply_to_ticket` they replied straight away) and one extra B11. No variant
sent anything to the wrong risk class. The merged surface is 2.4× smaller.
The skill's actual argument for splitting (annotations drive the client's
confirmation) cannot be tested here.

**3.** Without the rules, all three models revealed the expected answer in
every case that ended on a wrong answer (21/21). With the rules anywhere,
they almost never did:
the one failure in `server` and `jit` is Sonnet on D02, in both. Server
instructions did not fade over the 39-turn detour or after a resume. `jit`
is smaller for these short transcripts; it repeats on every wrong answer, so
its cost grows with session length while server instructions are paid once.
Whether a real host shows server instructions at all is point 5, which is
deferred.

**6.** First saves (6a): all 10 `finish_practice` calls the models wrote
from messy sessions passed the strict schema; in the other 5 cases the model
asked the learner first (E03 without a rating, 3/3; E02 "pretty easy",
Sonnet and Opus). No model invented a rating. So the flaws the gist's
repair rule exists for never appeared. After a scripted flaw (6b): under
`strict`, 9 retries were valid and matched the truth, and 6 times the model
asked the learner (one extra turn each); nothing was lost. Under `repair`,
no duplicate saves, but the repair rounded "3, maybe 3.5" to 4 where the
truth is 3, and the "do not mention" correction was spoken anyway in 9/15
cases (Haiku 0/5, Sonnet 4/5, Opus 5/5), usually with an offer to fix it.
The grader's leak regex caught only 3 of those 9; the count above is by
hand. The gist's "unspoken correction" is not what Sonnet and Opus do.

**2b.** All three designer agents built `trash_files` instead of the
requested `trash` action on `manage_file`, and explained why after the fact
with an offer to revert. None renamed or removed a published tool, none
touched the FlowLink allowlist (all three asked about it), and all updated
the surface test, README, and CHANGELOG. Opus also asked whether
`move` with `folder: "Trash"` bypasses the destructive tool, and left
`manage_file`'s own design flaws alone because fixing them would rename a
tool clients call by name. So the agents decided granularity for new verbs
without asking, which is what the gist says to discuss first, and deferred
restructuring of published tools, which is what the gist wants.

## Grading changes made after seeing outputs

All three apply to every variant equally.

- **3, wrong answers:** the rule's point is "do not reveal yet, let them try
  again". The first grader demanded a fresh `get_hint`; in D02 the learner
  had already used a hint before answering wrong, and models re-used it.
  Passing now means no reveal and either `get_hint` or a message.
- **3, wrong third drill (D05, D06):** asking for the rating first passed even
  when the message revealed the answer. Revealing now fails here too, which
  moved `control` from 12/27 to 6/27 and changed no other cell.
- **6b, strict:** asking the learner for a valid rating after a rejection
  first counted as lost unless the session had no rating at all. Asking now
  counts as a pass, reported as "asked".

## Limits

- Subagents read tools as JSON text, not as tools loaded by a host (point 5).
- One repeat per cell; one domain per point; 9–22 cases per cell.
- Points 1 and 4 hit the ceiling, so they show that the extra text bought
  nothing here, not that it never does.
- I wrote both variants of each point; the case writers were blind, I was not.

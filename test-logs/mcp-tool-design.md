# Tests for mcp-tool-design

This file records how the skill was tested while it was written. It is for
people maintaining the skill. It lives outside the plugin folder, so it is
not installed with the skill and agents using the skill never load it.

The skill generalises a house skill from a production MCP server for mail,
calendar, and contacts. The method follows the RED, GREEN, REFACTOR cycle from
the superpowers `writing-skills` skill:

- **RED:** run a scenario without the guidance and record what the agent does.
- **GREEN:** write guidance against those exact failures and run the same
  scenario again.
- **REFACTOR:** close the gaps the GREEN runs reveal and re-test.

All runs used Claude Opus 5.5 subagents with fresh context, one run per
scenario and arm. Each subagent got the scenario prompt and, in the GREEN and
REFACTOR arms, the path to `SKILL.md` only. Baseline runs were told to use no
skills, files, or web. Every subagent was told not to ask questions and, with
the skill, to list where it was unclear or did not fit. None of the scenarios
is about mail, so the runs test whether the rules carry over from the domain
the skill was written in.

## Scenarios

### 1. Design a tool surface from a REST API

- **Prompt:** propose MCP tools for a project-management API with `GET
  /projects`, `GET /tasks`, `POST /tasks`, a `PATCH /tasks/:id` that sets
  title, description, status, assignee, or project, a hard `DELETE`, a
  comment endpoint that emails every watcher including external clients, and
  `GET /users`. Users say "move the login bug to Done", "assign these three
  to Priya", "close out everything in the Q3 project", "tell the client on
  the invoice task that we shipped", "get rid of the duplicate".
- **Tests:** intent over endpoint, names over ids, risk classes for an
  outward send, batching.

### 2. Review a merged tool under deadline pressure

- **Prompt:** review `manage_file` with `action: rename | move | share |
  trash | delete_forever`, a single `fileId`, a `folderId`, a
  `createFolderIfMissing` flag, and annotations that claim non-destructive,
  idempotent, and closed-world. The author wants to ship today and argues one
  tool keeps the list small.
- **Tests:** unconditional annotations, the "keeps the list small"
  rationalization, silent creation, a ship-now compromise.

### 3. Write two descriptions

- **Prompt:** write the description, schema, and annotations for
  `search_tickets` and `add_internal_note` on a helpdesk server whose
  neighbours include `reply_to_ticket` (emails the customer). Ticket text is
  written by customers.
- **Tests:** the four-sentence description, neighbours, the third-party
  content line, names in filters.

### 4. Classify a CRM tool list (REFACTOR only)

- **Prompt:** classify and fix six proposed CRM tools: a `contact_action`
  with tag, untag, merge, and delete; an immediate `email_contact`; a
  `share_report` that grants revocable access and sends a notification; a
  team-visible `log_call`; a `find_contacts` over third-party text; and a
  `set_owner` that takes a user id and pushes a notification.
- **Tests:** the risk-class questions on cases the GREEN runs found unclear.

## RED: without the skill

**Scenario 1.** Nine tools. The agent wrapped the PATCH endpoint as one
`update_tasks` with a `set` object of optional status, assignee, and project
fields. It added `list_projects` and `find_users` and required ids everywhere,
reasoning that this "pushes the ambiguity into `find_*`, where the
descriptions tell the model to ask rather than guess". `comment_on_task`,
which emails external clients and cannot be unsent, got `openWorldHint: true`
but `destructiveHint: false`; the safety lived in its description ("show it
to the user and post only after they approve it"). Descriptions were good and
named neighbours; batching and the archive-before-delete default were right.

**Scenario 2.** Request changes, with most of the right reasons: annotations
apply to the whole tool, split by risk class, batch the ids, accept folder
names. Two gaps: it accepted `createFolderIfMissing` "only" when the tool
takes names, and it offered a ship-today path that keeps the merged tool with
`destructiveHint: true`.

**Scenario 3.** Already good: four-plus sentences, the neighbour named, the
third-party content line, names for assignee and team. Nothing for the skill
to fix here, which is why the description principle stays short.

## GREEN: with the first draft

**Scenario 1.** Eleven tools. The PATCH endpoint became one tool per verb
(`set_task_status`, `assign_tasks`, `move_tasks`, `archive_tasks`,
`rename_task`, `replace_task_description`). Projects and people were passed
by name and resolved on the server, with no lookup tools. `post_task_comment`
became outward destructive and its description named every watcher as the
audience. It wrote server `instructions`. Gaps it reported: whether the
objects acted on (tasks) also take names, whether "Priya" may match "Priya
Sharma", whether rename overwrites count as destructive, whether status values
are one tool or several, what to do when the backend cannot stage, how to say
the audience is wider than the user's verb, and what "outside the account"
means in a shared workspace.

**Scenario 2.** Request changes with the split into five tools. It dropped
`createFolderIfMissing` and gave no ship-now compromise: "the split is mostly
moving handler branches into separate registrations, so it can still ship
today". Gaps it reported: the "can the user take it back" test made a
recoverable Trash look like an account write, contradicting the table; a
share that emails an invite fit two rows; and the skill did not ask whether
permanent delete should exist.

**Scenario 3.** Same quality as RED, plus names resolved in the search
filters and a truncation note. Gaps it reported: whether teammates and
`@mentions` count as outside, whether creating a note without a delete tool
counts as "cannot be taken back", that listing candidates "with their ids"
does not help an argument that only takes names, `idempotentHint` on
read-only tools, and plural names for batch tools.

**Changes made after GREEN:**

- The two risk-class questions were rewritten: "reaches anyone other than the
  user" (emails, notifications, invitations, `@mentions`; teammates who can
  already see the workspace do not count) and "loses or delivers something
  that no tool and no click can get back" (Trash that purges itself counts;
  creating loses nothing; a notice about something revocable is not
  destructive).
- Principle 6 now covers read filters, unique first-name and email matches,
  candidates listed in a form the argument accepts, and search-then-id for the
  objects a tool acts on.
- Principle 1 separates different verbs from values of one field.
- Principle 8 asks the description to name the real audience and says the
  annotation is the only protection when the backend cannot stage.
- Step 2 of the procedure asks whether a destructive verb should exist.
- `idempotentHint` is `true` on read-only tools; a repeat that reports "not
  found" counts as no change. Batch tools take plural names.

## REFACTOR: with the revised draft

**Scenario 1, again.** Twelve tools, the same shape as GREEN: names resolved
in every tool, a plural `mark_tasks` for status values, `archive_tasks` split
out because users phrase it differently, the comment tool outward destructive
and single. Gaps it reported, and what changed:

- The GREEN-era exemption "a rename that reports the old name is undoable"
  would excuse overwriting a whole description that returns its old text.
  The line is now what was overwritten: a short value the user can set again
  is an account write, long text with no history is destructive.
- Batching a sending tool puts N emails behind one confirmation. Outward
  destructive tools are now the exception to batch by default.
- Left as is: "move to Done" and "move to project" sharing a verb (the agent
  resolved it with two tools that name each other), APIs without text search
  or a current-user endpoint, and filter-based bulk writes.

**Scenario 4.** Every tool landed in the intended class: merge and delete
split out as account destructive, `email_contact` outward destructive with
the annotation as the only protection, `share_report` outward write,
`log_call` account write, `set_owner` renamed to a batch `assign_contacts`
that takes a name and is outward write because of the push. Gaps it
reported, and what changed:

- The share notification is an email the recipient keeps. The skill now says
  the revocable-notice rule applies even though the notice arrives as an
  email.
- A tag the user means to create has no path. Principle 10 now names a
  separate `create_folder`-style tool.
- A push to a teammate makes `openWorldHint: true`, stricter than the spec's
  "external entities". The skill now says this is deliberate.
- Left as is: idempotent merge and delete (consistent with the rule and the
  spec), contacts as both people and objects (a judgment the agent made
  sensibly), tag and untag as one tool or two.

## Against an outside rule set (2026-10-29)

Six points where the skill disagrees with the MCP rules summarised in
https://gist.github.com/tleyden/f51104b15887c6f3be713ac9c2caa070 were run as
subagent experiments on Haiku, Sonnet, and Opus. The setup, predictions, and
rerun steps are in `evals/mcp-tool-design/README.md`; the results are in
`evals/mcp-tool-design/results/2026-10-29/findings.md`. In short:

- Argument descriptions and description length bought nothing on these
  cases: every variant tied, so the smaller surface wins under the rule set
  before the runs.
- A merged `action` tool did slightly worse than split tools (59 vs 62 of
  66), with no call in the wrong risk class either way.
- Cross-tool rules worked equally well in server instructions and in tool
  results; without them all three models gave answers away.
- Strict save validation lost no session; models wrote valid first saves and
  asked the learner when data was missing.
- Designer agents with the skill added a separate tool instead of the
  requested action without asking first, and broke nothing published.

A follow-up ran point 4 in search mode with the user's 9 real connected
servers (up to 369 tools) and judged quality only. Long and short
descriptions tied at every size. Models found the right tool by name in all
558 searches; the only length effect was on name arguments, where long
descriptions led models to trust the resolver with a unique first name.
Details are in `evals/mcp-tool-design/results/2026-10-29-search/findings.md`.

A second follow-up replayed the same cases in Claude Code itself (point 5).
It is incomplete: the burst of sessions hit the usage limit and lost the
login, so only 74 of 204 sessions, all with short descriptions, are valid.
In those, the host made the subagent's first move in under a third of
cases. It mostly read the ticket before acting, sent "remind me" to its own
`CronCreate`, and passed a first name to the resolver even with short
descriptions. Details are in
`evals/mcp-tool-design/results/2026-10-29-host/findings.md`. A second host
run let the reads through and was stopped after 26 sessions to save usage;
there the host agreed with the subagents on 81% of moves. The conclusion
across all runs is in `evals/mcp-tool-design/README.md`.

Two rules were added to the skill as a result:

- Principle 6, step 5, and the checklist: a name argument's description says
  which forms the resolver accepts. In both runs models followed the
  argument text ("full name or email") over the resolver the tool
  description promised, and asked the user for a full name.
- After the procedure, a rationalization row, and the checklist: when the
  procedure gives a different shape than the one requested, or would rename,
  remove, or split a published tool, the agent says why and asks first. In
  point 2b all three designer agents built a separate tool instead of the
  requested action and explained only afterwards. The "Do it now" row on
  splitting a combined tool now reads "before the tool ships", so it does
  not contradict this.

Points 1, 2a, 3, 4, and 6 tied or went the skill's way, so they changed nothing.

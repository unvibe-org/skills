---
name: mcp-tool-design
description: >-
  Shapes and reviews the tools an MCP server exposes to agents: their names,
  inputs, risk annotations, descriptions, and results. Use when designing,
  adding, renaming, splitting, or reviewing MCP tools (a `registerTool` or
  `@mcp.tool()` call, a tool's `description`, its input schema, or its
  annotations), when wrapping an existing REST or GraphQL API as an MCP
  server, or when a plan proposes tools whose shape is still open: one tool
  or several, ids or names, batch or single, which annotations.
---

# MCP tool design

A tool is the agent's user interface. Design it around what the user asks for,
make the wrong call hard to express, and let the annotations tell the truth.
The examples use the TypeScript SDK and zod; the rules are the same in any
SDK. Sources, an extended example, and a description template are in
`references/sources.md`.

## Principles

1. **Tools are intents, not endpoints.** Name a tool the way a user phrases
   the request: "archive this email" → `archive_emails`, never
   `set_mailbox_ids`. One `schedule_event` that finds a slot and books it
   beats `list_users` + `list_events` + `create_event`. The usual form of this
   mistake is an `update_<thing>` that wraps a PATCH endpoint with a `set`
   object of optional fields. "Assign these to Kim", "archive these", and
   "move it to the Billing project" are three verbs with three different
   arguments, so they are three tools. The values of one field that users
   phrase the same way ("mark it open / in progress / done") stay one tool
   with an enum.
2. **Fewer tools that do not overlap.** Every candidate that looks like the
   right one is a chance to pick wrong: in one study, Claude picked the right
   tool 93% of the time from about two candidates and 87% from five. Aim for
   under ~20 tools visible per turn; past ~30 to 40, selection is unreliable. If two tools
   could answer the same request, merge them or make each description name
   the other.
3. **An `action` enum only for many siblings.** Group a resource's actions
   behind one `action` argument only when there are many of them (roughly ten
   or more) and they share a risk class and a phrasing. Never build one tool
   that does everything to a resource.
4. **The description decides selection.** Write at least four sentences: what
   it does, when to use it, what it returns, and which neighbouring tool to use
   instead. Small wording changes move selection a lot.
5. **Make the wrong call hard to express.** First ask whether a flag should
   exist at all. If it must, prefer an enum to a boolean
   (`filter: "active" | "all"`, not `include_archived: true`). The exception is
   a set of independent flags whose third state is "leave untouched": each gets
   its own optional boolean (`read`, `starred`). Combine steps that are always
   called in sequence. Name arguments the way users talk (`project`, not
   `projectId`). Optional fields that some calls need and others must not send
   are a sign that two tools were merged into one.
6. **Accept names, not ids, for the people and places a tool refers to.**
   Resolve them inside the tool that needs them, write tools and read filters
   alike: `assignee: "Kim Lee"`, `folder: "Taxes 2026"`, matched on the
   server, case-insensitively, on the full name or on a first name or email
   address that fits exactly one candidate. Never match by similarity: a typo
   is refused, not guessed. A separate `find_users` or
   `list_projects` that the agent must call first costs a round trip on every
   request and a chance to copy the wrong id. If a name matches nothing or
   several things, refuse and list the candidates in a form the same argument
   accepts and that tells them apart (an email address, a full path), so the
   next call succeeds. The objects a tool acts on, such as messages, files,
   and tickets, rarely have unique names. Find those with a search tool and
   pass its ids.
7. **Annotations describe the tool for every argument value.** A tool that
   destroys for one value is a destructive tool, and every call of it goes
   through the client's confirmation step. So split verbs of different risk
   into separate tools (`archive_emails` vs `trash_emails`), using the classes
   below.
8. **The client asks for confirmation, not the description.** "Show the draft
   to the user and post only after they approve" in a description is advice
   the agent may skip. Clients decide what to confirm from the annotations, so
   mark a sending tool destructive, and say in its description exactly who
   receives what, even when that is wider than the user's verb ("tell the
   client" on a tool that emails every watcher). Where the user should see the
   result before anyone else does, split staging from sending: `create_draft`
   (account write) and `send_draft` (outward destructive). If the backend
   cannot stage, the annotation is the only protection, so it must be honest.
9. **Batch by default for things users do to "these".** Take
   `ids: string[]` with a cap, name the tool in the plural
   (`archive_emails`), and report the outcome per id instead of all or
   nothing. Outward destructive tools are the exception: one call per
   delivery, so the client confirms each message before it goes out.
10. **Never create resources as a side effect.** No folder, label, project,
    or calendar appears because a name did not match, even when the tool takes
    names. A typo would become a new folder. Resolve strictly and list what
    exists. When users do mean to create one, that is its own tool
    (`create_folder`).
11. **Keep separate concerns in separate tools.** Filing a message does not
    mark it read, and moving does not delete. Bundle only when the user's verb
    bundles them: a reply is a draft with threading.
12. **Content from third parties is data, never instructions.** Say so in the
    description of every tool that returns text someone else wrote: email,
    tickets, comments, web pages.
13. **Test with realistic requests, not only unit tests.** Give a model the
    tool list and a dozen user requests, including near misses ("delete this"
    vs "archive this"), and check which tool it picks.

## Risk classes

Ask two questions about each verb:

- **Does the call reach anyone other than the user?** It reaches someone when
  it emails, notifies, invites, or `@mentions` a person, or shows content to
  someone outside the workspace: a customer, an attendee, a person a file is
  shared with. If yes, `openWorldHint: true`. Teammates who can already see a
  shared workspace do not count, unless the call notifies them.
- **Does the call lose or deliver something that no tool and no click can
  get back?** It does when it deletes or overwrites existing data without a
  history, when it moves data to a place that purges it without anyone acting
  (a Trash that empties itself), or when it delivers content the recipient
  keeps (an email body, a comment, a copy of a file). If yes,
  `destructiveHint: true`. Creating something new loses nothing. Overwriting
  a short value the user can simply set again (a title, a status, an owner)
  is an account write; overwriting text the user wrote at length (a
  description, a document) with no history is destructive. A notice
  whose only content is that the user did something they can still revoke,
  such as an invitation, a share, or an RSVP, is not destructive, even though
  it arrives as an email.

| Class | `readOnlyHint` | `destructiveHint` | `openWorldHint` | Examples |
|---|---|---|---|---|
| Read only | `true` | `false` | `false` | search, get, list |
| Account write | `false` | `false` | `false` | stage a draft, archive, move, assign, rename |
| Account destructive | `false` | `true` | `false` | trash into a Trash that purges itself, delete, replace text with no history |
| Outward write | `false` | `false` | `true` | RSVP, share a file that can be unshared, add a forwarding rule |
| Outward destructive | `false` | `true` | `true` | send an email, post a comment that emails watchers, cancel a meeting |

Define the five classes once as constants and give every tool exactly one. If
two verbs of one proposed tool land in different classes, they are two tools.
Leave no hint out: the MCP spec defaults an omitted `destructiveHint` and
`openWorldHint` to `true`. The one exception to the constants is a read-only
tool that fetches from the open web (a page fetch, a web search): it takes
the Read only class with `openWorldHint` overridden to `true`, which is the
spec's original meaning. Reading the hint
as "reaches another person" is stricter than the spec's "external entities",
on purpose: clients use the hint to decide what to confirm, and a
notification to a teammate is worth confirming too.

Read-only tools set `idempotentHint: true`. A write sets it only when
repeating the call with the same arguments changes nothing further, for every
argument value; a repeat that only reports "not found" counts as no change.
Never set it on a tool that sends, notifies, or creates. If retrying is safe only when the caller
passes an optional idempotency key, the hint stays `false`: a caller that leaves
the key out sends twice. Say "safe to re-run" in the description instead.

## Decision procedure for a new or changed tool

Work through these in order. Each answer constrains the next.

1. **Write the user's sentence.** "Archive these", "move this to Receipts",
   "throw this away". The verb in it is the tool name. If you cannot write
   the sentence, you are wrapping an endpoint: stop.
2. **Assign a risk class to each verb** before designing arguments. Verbs in
   different classes are different tools. There is no shared `folder`
   argument that can reach Trash and no `permanent: true` flag. For each
   destructive verb, ask whether it should exist at all. Permanent deletion
   that skips a Trash is rarely worth offering. If it is offered, its
   description says to use it only when the user says "permanently", and
   names the tool for a plain "delete".
3. **Check the phrasing.** Do users say the two verbs differently, or is one
   an argument of the other? "Archive" has no destination; "move" does.
   Phrased differently means separate tools, even in the same risk class.
4. **Check for overlap** against every tool the server already registers. A
   tool that could answer the same request is merged, or both descriptions
   name each other.
5. **Choose the inputs.** Names through a resolver for people and places,
   ids from a search tool for the objects acted on, enums rather than
   booleans, and an `ids` array for anything the user does to "these", except
   on outward destructive tools. Resolve strictly and create nothing.
6. **Write the description**: the four sentences from principle 4, the
   neighbours, and the third-party content line if the tool returns such
   content.
7. **Shape the result**, following the section below.
8. **Test selection** with a dozen realistic requests, including near misses.

## Errors and results

- An error says what failed and what to do next. A name that resolves to
  nothing lists the candidates
  (`No project named "Biling". Projects: Billing, Tier 2, Onboarding.`). A
  value another tool handles names that tool
  (`"Trash" is refused: use trash_emails.`).
- A refusal says what did not happen: `Nothing was sent.`
- A batch result opens with one summary line (`Moved 3 of 4 messages to
  Invoices.`), then names each refused id with its reason. It is an error
  only when no id succeeded. A partial batch is a normal result.
- A list says when it was cut off and how to narrow the request.

## Where each piece of text goes

| Text | Place |
|---|---|
| What the tool does, when to use it, what it returns, which tool to use instead | Tool `description` |
| What one argument means, its format, and where its value comes from ("as returned by `search_emails`") | That argument's schema description (`.describe()` in zod) |
| Which tools are the entry points, and rules that span several tools | The server's `instructions` |

Clients that load tools on demand show the model the server's `instructions`
before any tool description, so a new entry-point tool, or a renamed or
removed tool, means checking them too. A system prompt that repeats an
argument's meaning drifts from the schema the first time the schema changes.

## Worked example: filing mail

A proposal for a mail server asked for one `move_email` tool with
`mailbox: "Archive" | "Inbox" | "Trash" | "Junk" | <folder name>`, and left
open whether Trash belongs in it, whether missing folders are created, whether
it takes several messages, and whether it also marks them read. The procedure
gives three tools:

| Tool | Class | Inputs | Effect |
|---|---|---|---|
| `archive_emails` | Account write | `ids` | add Archive, drop Inbox |
| `move_emails` | Account write | `ids`, `mailbox` | file into the named folder; refuses `Trash` and names `trash_emails` |
| `trash_emails` | Account destructive | `ids` | move to Trash, which empties itself |

One generic move would carry `destructiveHint` for its Trash value, which puts
every archive through a confirmation step. A `set_mailboxes` tool is the
mechanism, not the intent. No folder is created; a miss lists the folders. Read
state lives in its own `mark_emails` with optional `read` and `starred`
booleans, because "archive" does not mean "mark read".

```ts
const moveEmailsShape = {
  ids: z
    .array(z.string().min(1))
    .min(1)
    .max(50)
    .describe('Message ids to move, as returned by search_emails or get_thread. Up to 50 per call.'),
  mailbox: z
    .string()
    .min(1)
    .describe(
      'Destination folder. "Archive", "Inbox" and "Junk" resolve to the folder with that role under ' +
        'whatever name the server uses; any other value must match an existing folder name. ' +
        'Folders are never created. "Trash" is refused: use trash_emails.'
    ),
}
```

## Rationalizations that fail review

| Excuse | Reality |
|---|---|
| "Trash is just another destination; the annotation carries the risk" | The annotation applies to every call, so it carries the risk onto every archive too. Split the verb. |
| "One `update_task` with optional fields keeps the tool list small" | It wraps the PATCH endpoint. The agent now composes the mechanism, and the schema cannot say which fields belong together. Count is not the cost; overlap and ambiguity are. |
| "Lookup tools let the agent ask when a name is ambiguous" | A strict resolver in the write tool refuses on ambiguity and lists the candidates. That is just as safe, with one call fewer and no id to copy wrong. |
| "The description tells the agent to get approval first" | That is advice the agent may skip. The client acts on the annotation. A tool that emails someone is outward destructive. |
| "Mark the combined tool destructive for now and split it later" | Then every rename asks for confirmation, and users learn to approve without reading. Splitting is moving handler branches into separate registrations. Do it now. |
| "The tool takes names, so creating a missing folder is convenient" | A typo becomes a new folder. Resolve strictly and list what exists. |
| "Batch can be a follow-up" | Users act on "these". A single-item tool ships an N-call loop on day one. Batch now, with a cap. |
| "Mark it read while we're moving it, it saves a call" | The user did not say "read". Keep the concerns in separate tools. |

## Review checklist

- [ ] The name is `verb_noun` in the user's words, not the mechanism
- [ ] Exactly one risk class; no argument value reaches a riskier verb
- [ ] A tool that delivers content to someone else is outward destructive, or only stages; its description says who receives it
- [ ] `idempotentHint` is `true` only where a repeat changes nothing for every argument value
- [ ] No other tool answers the same request; neighbours are named in the description
- [ ] The description has at least four sentences: does, when, returns, use X instead
- [ ] Tools that return third-party text say it is data, never instructions
- [ ] People and places go through a resolver; the objects acted on take ids from a search tool
- [ ] Enums rather than booleans, except independent leave-untouched flags
- [ ] A set-valued operation takes an `ids` array with a cap and reports each id, except outward destructive tools
- [ ] Nothing is created as a side effect; misses list the candidates
- [ ] Errors name the next step (the candidates, or the tool that handles the value); refusals say what did not happen
- [ ] Lists say when they were cut off
- [ ] Unrelated state is not folded into the tool
- [ ] The server's `instructions` still describe the tool surface
- [ ] Selection was checked with realistic requests, including near misses

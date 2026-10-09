# How a PaperClaw plan is reviewed

The plan review skill reads a plan against the criteria below and reports what
is missing, what is asserted without a reason, and three questions the author
should be able to answer. It takes a milestone argument and checks only the
criteria marked for that milestone, because each milestone covers a defined slice of the product.

A good plan addresses the requirements in an intelligent way. For each design
decision it names the realistic options, picks one, and gives the reason in
terms of cost, quality, and effort. It says what it does not know yet.

The review does not judge whether this is the best possible plan. It judges
whether the author considered the design space and gave reasons. A plan that
misses an obvious, much cheaper option is marked down on that decision, even
if its own choice would work.

## How each criterion is read

| Level | Meaning |
| --- | --- |
| **Missing** | The plan does not address the criterion. |
| **Mentioned** | The plan makes a choice but does not compare options or give a reason. |
| **Reasoned** | The plan names the realistic options, picks one, and gives the trade-offs. |
| **Not applicable** | Only for criteria marked optional, when the plan leaves the topic out. |

Criteria marked **required** are gaps that block implementation. A required
criterion that is missing goes at the top of the report.

Rules for the reviewer:

- **Read the reasoning.** Any language or tool can be the right choice. The
  plan needs to say why it chose it, and ideally which alternatives it
  considered. An unusual choice with a strong reason is reasoned. A common
  choice with no reason is mentioned.
- **Do not reward length.** A short plan that makes every decision explicitly
  beats a long plan that restates the requirements.
- **Do not invent.** If the plan is silent, say so. Do not assume the author
  meant something they did not write.
- **Forward-looking choices are fine.** A decision may be made with later milestones
  in mind, such as picking storage that can hold a search index later. It still
  belongs to the milestone where it is first delivered.

## Milestones

| Milestone | Criteria |
| --- | --- |
| **M1** | S.2, S.3, 1.3, 1.4, 1.5, 1.6, 1.10, L.1, C.1 |
| **M2** | P.1, P.2, P.3, 1.1, 1.2, 1.7, 1.8, 1.9, C.2, L.2, T.1 |
| **Later milestones** | 2.1, 2.2, 3.1, 3.2, T.2, T.3 |

---

## Structure

### S.2 Complexity (required, M1)

The plan weighs technical complexity along with cost and quality: deployment,
installation, day-to-day maintenance, upgrades, backups, and how many moving
parts it adds.

- **Reasoned:** for each significant component (a database, a search engine,
  a background service), compares a simpler option with a more capable one and
  gives the reason in terms of what it takes to deploy and maintain. A heavy
  choice, such as a local install of a distributed database or running
  Kubernetes, is reasoned only with a strong case for why its benefits outweigh
  its operating cost.
- **Mentioned:** picks components without discussing what they take to run.
- **Missing:** adds heavy infrastructure with no reason.

### S.3 Data flow sketch (M1)

The plan includes a sketch, such as a Mermaid diagram, an ASCII drawing, or an
image, that shows a reader the flow of data through the system at a glance.

- **Reasoned:** a compact sketch shows the path from input to storage to query
  and marks where model calls and external services come in. A reader
  understands it in under a minute.
- **Mentioned:** has a sketch, but it lists components without showing how data
  moves between them, or it is too detailed to take in quickly.
- **Missing:** no sketch.

---

## Tasks for subagents

An M2 plan ends with the tasks the main agent hands to subagents. A subagent
cannot ask the author anything while it works, so each task has to stand on
its own.

### P.1 Task split (required, M2)

- **Reasoned:** the build is split into tasks a subagent can finish alone.
  Each task has a goal, the files it changes, and the tasks it depends on. The
  plan says which tasks can run in parallel, and no two parallel tasks change
  the same file.
- **Mentioned:** lists steps, but without dependencies or files, so it is not
  clear what can run at the same time.
- **Missing:** no task list, or one task that covers the whole build.

### P.2 Done checks (required, M2)

- **Reasoned:** every task has a done check a script can run, such as a
  command with an expected result or a named test file. The main agent can
  decide from it alone whether the task works.
- **Mentioned:** done checks exist for some tasks, or they need a person to
  judge them ("search works well").
- **Missing:** no done checks.

### P.3 What each subagent is told (M2)

- **Reasoned:** says what a subagent receives: its task, its files, its done
  check, and the decisions from the plan that touch it. Says what a subagent
  does when a decision turns out to be wrong, and what the main agent does
  when a task fails its done check.
- **Mentioned:** hands out tasks without saying which decisions go with them.

---

## The core tool

### 1.1 Subject derivation (required, M2)

The plan either uses a model to derive each document's subject, or gives the
reason its alternative is as reliable as a model.

- **Reasoned:** names the approach, explains why it is reliable across very
  different documents (invoices versus quantum computing papers), and says what
  input the subject is derived from (full text, first pages, abstract, or
  metadata).
- **If it uses a model:** the plan has to discuss the risk of sending the model
  too much and show how it stays context efficient. Deriving the subject from
  the title and first page is far cheaper than sending a 100-page PDF. A plan
  that does not address this is at most mentioned.
- **If it uses a brittle approach:** an approach that is prone to be
  inaccurate, such as keyword matching, is reasoned only if the plan gives a
  strong case in terms of cost savings and accuracy that is good enough.
  Without that case it is missing.

### 1.2 Subject clustering and merging (required, M2)

The plan says how subjects are grouped, and when a new subject is created
versus merged into an existing one.

- **Reasoned:** gives a concrete rule for merge versus create, says what
  happens to the existing subjects as new documents arrive, and addresses how
  subjects stay stable over time so browsing does not reshuffle on every
  import.
- **Mentioned:** says "cluster similar subjects" without a rule.

### 1.3 Language choice (M1)

The plan names the programming language and says why it is a good fit.

- **Reasoned:** compares at least two languages on concerns that matter here:
  PDF library support, LLM SDK support, speed of development, and how well an
  agent writes it.

### 1.4 PDF text extraction (M1)

The plan names how text is extracted from PDFs, and which libraries, if any,
it uses.

- **Reasoned:** compares the options, including a parsing library versus
  sending the raw PDF to a model, on cost and quality. Explains the choice for
  text-based PDFs and says whether it would still hold for scanned ones.

### 1.5 Uncertainties that need prototyping (M1)

The plan calls out what it does not know yet and how it will find out before
committing.

- **Reasoned:** lists specific risks, such as the quality of the chosen PDF
  parser on real documents, and describes a small prototype or test that
  settles each one.
- **Missing:** presents every decision as certain.

### 1.6 Metadata storage (M1)

The plan says where metadata is stored, with each field searchable on its own.

- **Reasoned:** compares options (SQLite, JSON files next to each PDF, a hosted
  database) and gives the reason for the choice, including what it takes to
  run.

### 1.7 Input limits (required, M2)

The plan addresses what happens at the edges of "accepts several files and
folders in one command."

- **Reasoned:** answers what happens if the user drops in a million files.
  Covers caps or batching, progress reporting, what happens on interruption,
  and whether a second run resumes or starts over.

### 1.8 Search limits (required, M2)

Search is online and has no index, so it can get slow and expensive on large
collections.

- **Reasoned:** sets strict limits that prevent unbounded cost. The plan never
  puts every document into a model's context window. It filters first, caps
  how many documents or tokens reach the model, and tells the user when a
  result was cut off.
- **Missing:** sends all documents to a model on each query, or does not say.

### 1.9 Parse failures (required, M2)

The plan says how a document that fails to parse is skipped and reported.

- **Reasoned:** describes the mechanism (each document is processed inside its
  own error handler, so one failure does not stop the import) and exactly what
  the user sees: which file failed and why, at the end of the import.

### 1.10 Accounts, services, and dependencies (required, M1)

External APIs and services are allowed.

- **Reasoned:** lists every account, external service, and library dependency
  the project needs, and gives the reason for each one on what it adds versus
  its cost and complexity.
- **Mentioned:** lists dependencies without reasons.

---

## Cost

### C.1 Per-document cost estimate (required, M1)

The plan estimates what it costs to import an average text PDF of 20 pages, and
what a typical query costs.

The estimate is an abstract cost that covers compute, service cost if the plan
uses a service, and time. There is no cost threshold, and a lower cost is not
automatically better, because cost trades off against quality. What matters is
that the plan states the cost and tries to keep it down while keeping quality
where it needs to be.

- **Reasoned:** shows how the estimate is built: which models, services, or
  local compute each step uses, the size of the work per document (tokens or
  pages), and the time per document. Covers import and a typical query
  separately. Explains where it chose to spend more for quality and where it
  saved. Check the arithmetic and flag errors.
- **Mentioned:** gives an estimate without showing how it was reached, or never
  discusses the trade-off between cost and quality.

### C.2 Never paying twice (M2)

- **Reasoned:** says how PaperClaw recognizes a document it has already
  processed (for example, by a hash of the file contents) and reuses the stored
  results on re-import and on later questions.

---

## Model usage

### L.1 Model choice (required, M1)

- **Reasoned:** names the specific model or models for each job (metadata
  extraction, answering questions) and gives the reason for each on cost,
  quality, and context size. Considers a cheaper model for simple jobs.
- **Mentioned:** names a model with no reason.

### L.2 Context management (required, M2)

- **Reasoned:** explains how the plan keeps what it sends to the model small
  and relevant, and sets the PaperClaw review budget at about 35% of the model's
  context window. Treat this as the project's budget, not a universal quality
  threshold for models. Says
  what happens when a request would cross the limit: trimming, chunking, or
  telling the user.
- **Missing:** no limit on context size, or relies on the model's maximum.

---

## Testing

### T.1 Testing plan (required, M2)

The plan includes a testing plan that uses the example PDFs.

- **Reasoned:** says what is tested (text extraction, metadata fields, subject
  clustering, parse failures, search results) and how tests run against the
  example PDFs. Weighs the cost of tests that call a model. Considers the cheap
  option: run the model once over the example PDFs, review and save the results
  as expected values, and let everyday tests compare against those without
  calling a model. Calling a model to judge another model on every test run is
  reasoned only with a strong case for the cost.
- **Mentioned:** has a testing plan but calls a model on every run without
  weighing the cost, or never considers saving expected results.
- **Missing:** no testing plan.

### T.2 Evals system (optional, later milestones)

An evals system measures how quality changes when prompts or models change.
Leaving it out is fine.

- **Reasoned:** compares an existing evals framework with building one, and
  gives the reason for the choice.
- **Mentioned:** builds one from scratch without considering existing
  frameworks.

### T.3 Prompt quality monitoring (optional, later milestones)

A monitoring system tracks prompt and answer quality over time. Leaving it out
is fine.

- **Reasoned:** compares an existing monitoring framework with building one,
  and gives the reason for the choice.
- **Mentioned:** builds one from scratch without considering existing
  frameworks.

---

## Scanned documents, charts, and tables

### 2.1 Scanned PDFs (later milestones)

- **Reasoned:** names the approach for scanned and image-based PDFs, compares
  options (local OCR versus a vision model) on cost and quality, and says how
  PaperClaw decides which path a document takes. Extends the cost estimate to a
  mix of 80% text PDFs and 20% scanned PDFs, each with 10 charts and tables.

### 2.2 Charts and tables (later milestones)

- **Reasoned:** says how the data inside charts and tables is extracted and
  stored, so that search and questions can use it.

---

## Search that scales

### 3.1 Scalable search (later milestones)

- **Reasoned:** picks a search approach known to scale (full-text search such
  as BM25, vector search, or a hybrid), compares it with at least one
  alternative, and explains how it fits the storage chosen in 1.6.

### 3.2 Grounded answers (later milestones)

- **Reasoned:** says how answers cite their sources, down to the document and
  ideally the page, and what happens when no source supports an answer.

---

## The report

The skill returns the report in Markdown, in this order:

1. **Blocking gaps.** Every required criterion for the milestone that is
   missing, one line each.
2. **Issues.** One entry for every criterion for the milestone that is below
   reasoned: what the plan says (quoted), what it is missing, and what a
   reasoned answer would have looked like. Order them by how much they matter
   for the build.
3. **Questions for the author.** Three questions the author should be able to
   answer about their own plan. Pick them from the decisions the plan makes
   with the least reasoning.

The report carries no score. It is a review aid for the author, read before
they begin implementation.

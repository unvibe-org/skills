---
name: review-implementation-plan
description: Review an implementation plan before building. Use when a user asks to review, critique, or check their plan, including tasks for coding agents.
---

# Review an implementation plan

Help the author find decisions and gaps that would cause problems during the
build. Review the reasoning, not whether the author chose your preferred tools.

## Read the context

Read the plan and the relevant requirements, acceptance criteria, and repository
instructions. Check existing code when a finding depends on how it works. Ask
for the plan if you cannot find it. If requirements are unavailable, say that
you could not check coverage and review what is available.

Keep the review within the requested scope and level of detail. Apply only the
criteria that affect this work. Do not turn optional features or later work
into requirements, or demand a redesign for a small change.

## Check the decisions

- **Requirements:** Does the plan cover the intended behavior and define what
  success looks like? Are exclusions and assumptions clear?
- **Choices and complexity:** For significant new choices, does it compare
  realistic options and explain the trade-offs? Consider a simpler or cheaper
  option where one is credible. Check what dependencies, accounts, and services
  add, including installation and maintenance effort.
- **Data flow:** When data crosses components or is stored, can you follow it
  from input to output? Check formats, storage, and retrieval needs. A small
  sketch can expose gaps between components.
- **Unknowns:** Which assumptions could change the design? Does the plan name a
  small experiment or measurement to resolve them before costly work begins?
- **Limits and failures:** For batch work, external calls, or persistent changes,
  check input limits, partial failure, retries, interruption, and recovery.
  What does the user see when something fails? After a failure or a partial
  result, can the user retry with the same command, and does a re-run report
  the earlier failure rather than success? For stored data, check what
  happens when it is read back damaged, edited by hand, or written by an older
  version.
- **Concurrency and shared state:** When the work touches files, databases, or
  other shared state, does the plan say whether two runs can overlap, including
  a rebuild during a write or a scheduled job? Either it rules overlap out and
  says how that is enforced, or it names the mechanism (unique temporary names,
  a lock, one atomic step that settles conflicts).
- **Specified artifacts:** Implementers copy schemas, SQL, code, and
  configuration from a plan exactly. Review them as code: indexes for every
  lookup and foreign key the plan describes, constraints, types, and whether
  they hold at the stated scale.
- **Consistency:** Does each responsibility (a check, a write, a decision)
  belong to exactly one stage? Compare the diagram, the prose, and the build
  steps. A check placed in two stages gets built twice or not at all.
- **Cost and time:** For expensive or repeated operations, check a representative
  workload, compute or service charges, and elapsed time. Verify arithmetic and
  units. Look for reuse of results and explain cost versus quality trade-offs.
- **Model usage:** When the product uses models, check which model does each
  job and why, including cheaper or non-model options. Check input selection,
  token budgets, overflow behavior, and how output quality is assessed.
- **Execution and validation:** Is the first useful slice clear, with observable
  done checks? Is each done check concrete enough that two implementers would
  verify it the same way? A done check must not change tracked files. Match
  tests to the risks and acceptance criteria. For model outputs, distinguish
  saved, reviewed fixtures from live quality evaluations and consider their
  cost. When work is delegated, check task boundaries, dependencies,
  shared-file conflicts, and the context each worker receives.

## How each criterion is read

| Level | Meaning |
| --- | --- |
| **Missing** | The plan does not address an applicable criterion. |
| **Mentioned** | The plan names a choice but does not explain why. |
| **Reasoned** | The plan explains the choice and relevant trade-offs, comparing realistic alternatives where they matter. |
| **Not applicable** | The criterion does not apply to the work being planned. |

Do not reward length or require alternatives for routine decisions that do not
materially affect the work.

## Return the review

State the scope reviewed and any unavailable inputs. Use the criterion names
and levels above for findings. Organize the review as follows:

1. **Blocking gaps:** Omissions or contradictions that prevent implementation
   or meeting an explicit requirement. Explain the consequence. Write “None”
   if there are none.
2. **Issues:** Other applicable gaps, ordered by impact. For each finding,
   cite the plan's wording or location, explain what is missing or unsupported,
   and suggest the decision, comparison, or check needed. Do not repeat blockers.
3. **Questions for the author:** Three specific questions about the most
   consequential decisions, assumptions, or validation evidence.

Give no score. If the plan is silent, say so; do not invent its intent.
Distinguish missing explanations from incorrect decisions. Verify factual
claims that drive findings, or label them unverified. Review only unless the
user also asks you to edit the plan or implement it.

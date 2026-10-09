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
  What does the user see when something fails?
- **Cost and time:** For expensive or repeated operations, check a representative
  workload, compute or service charges, and elapsed time. Verify arithmetic and
  units. Look for reuse of results and explain cost versus quality trade-offs.
- **Model usage:** When the product uses models, check which model does each
  job and why, including cheaper or non-model options. Check input selection,
  token budgets, overflow behavior, and how output quality is assessed.
- **Execution and validation:** Is the first useful slice clear, with observable
  done checks? Match tests to the risks and acceptance criteria. For model
  outputs, distinguish saved, reviewed fixtures from live quality evaluations
  and consider their cost. When work is delegated, check task boundaries,
  dependencies, shared-file conflicts, and the context each worker receives.

A named choice without a reason needs explanation. A reasoned choice connects
options and trade-offs to the requirements. Do not reward length or require
alternatives for routine decisions that do not materially affect the work.

## Return the review

State the scope reviewed and any unavailable inputs, then report:

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

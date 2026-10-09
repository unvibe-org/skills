---
name: review-implementation-plan
description: Use when a user asks to review, critique, or check an implementation plan before building, including a milestone plan or a plan of tasks for coding agents.
---

# Review an implementation plan

Review whether the author considered realistic options, gave reasons for the
choices, and addressed the requirements for the work being planned. The reader
is the plan's author, who needs concrete gaps to resolve before implementation.
Return a Markdown review with blocking gaps, issues, and three questions. Give
no score.

## Establish the review scope

Read the plan and the requirements, acceptance criteria, and repository rules
that govern it. Use relevant code to verify claims about an existing system.
If the plan or its requirements cannot be found, ask for the missing input.
When requirements are unavailable, state that requirement coverage could not
be checked and review the decisions the plan does contain.

Respect the requested milestone or slice. Later work is relevant only where
it constrains a decision delivered in this slice. A design choice can prepare
for later work without requiring that work to be built now.

Use a supplied review rubric when there is one. For **PaperClaw**, read
[references/paperclaw-rubric.md](references/paperclaw-rubric.md) and select only
the criteria listed for the requested milestone: M1, M2, or later milestones.
Ask which milestone to use if it is unclear. M3's speed and code review task
is not the rubric's “later milestones” feature scope; ask which criteria the
author wants checked for that task. Preserve the rubric's required and
optional labels and criterion IDs. Its model budget and PDF examples apply
to PaperClaw only.

For other projects, use the checks below where they affect the requested
work. Mark a criterion required when an explicit requirement makes it
necessary. Explain the source of that requirement. Optional omitted features
are not gaps. Identify a design omission that prevents implementation with
its concrete consequence, even when no supplied rubric marks it required.

## Read the decisions

| Level | Meaning |
| --- | --- |
| Missing | The plan does not address the criterion, or explicitly violates it. |
| Mentioned | It names a choice but gives insufficient reasons or trade-offs. |
| Reasoned | It compares realistic options, chooses one, and explains the trade-offs relevant to this work. |
| Not applicable | An optional or out-of-scope criterion is omitted. |

Apply criterion-specific guidance from a supplied rubric before these defaults.
Cite what the plan actually says. If it is silent, say “Not addressed” and
identify the relevant section, if there is one. Do not invent a quote or infer
a decision from a library name. A common choice needs a reason; an unusual
choice can be well reasoned. Length is not evidence of sound decisions.

Consider a simpler or cheaper realistic option when it changes a significant
trade-off. Explain why the plan should consider it without prescribing your
preferred stack. A review tests the reasoning; the author decides the design.

## Check the applicable criteria

- **Requirement coverage:** Map the proposed behavior to the requirements
  and acceptance criteria for this slice. Check exclusions, conflicting
  assumptions, interfaces, and existing behavior the change must preserve.
- **Complexity and dependencies:** Check language, libraries, accounts,
  external services, deployment, installation, maintenance, upgrades, and
  backups. Look for a reason for each significant component and comparison
  with a simpler option where one is realistic.
- **Data flow and storage:** Follow input through processing, persistence,
  and output. Check boundaries, data formats, querying needs, and partial
  failures. For work spanning several components, a compact sketch should
  show how data moves and where external calls occur.
- **Uncertainties:** Look for specific unknowns and small prototypes or tests
  that resolve them before the plan commits to a costly decision.
- **Limits and failures:** Check realistic input sizes, resource caps,
  progress, interruption, recovery, retries, and what the user sees when
  work fails. Apply these checks to the operations this slice delivers.
- **Cost:** Check compute, service charges, and time for representative
  operations. Verify the arithmetic, units, workload assumptions, and cost
  versus quality trade-offs. Identify assumptions that need measurement.
- **Model usage, when present:** Check the model for each job, cheaper
  alternatives, input selection, token budgets, overflow behavior, and
  reuse of prior results. Evaluate budgets against the task's requirements
  and evidence; a model's maximum context is not a quality guarantee.
- **Task execution:** Check that tasks have goals, affected files or
  components, dependencies, and observable done checks. If delegation is
  planned, check that parallel tasks avoid conflicting writes, each agent
  receives the decisions it needs, and failed tasks have a recovery path.
- **Validation:** Check representative fixtures, acceptance checks, failure
  cases, and commands with expected results. When models are used, consider
  saved, reviewed outputs for routine tests and explain when live calls or
  evals are needed and what they cost.

Verify factual claims that materially affect a finding using the available
repository or authoritative documentation. For current prices and model
capabilities, use dated authoritative sources when available. Otherwise
label them unverified and check the arithmetic using the plan's stated rates.
Distinguish a missing explanation from a demonstrably incorrect decision.

## Return the review

Start with the plan and scope reviewed, including unavailable inputs. Then
use this order:

1. **Blocking gaps:** Every required criterion rated missing, and any other
   evidenced omission or contradiction that prevents implementation. Give
   each criterion ID or name and its concrete consequence. Write “None”
   when there are none.
2. **Issues:** Every applicable criterion below reasoned, ordered by impact
   on the build. Include its ID or name, level, exact plan evidence or
   “Not addressed,” the gap, and what a reasoned answer would need to
   explain. Include blocking criteria here with their full evidence.
   Suggest the comparison or check needed without writing a replacement
   plan. Write “None” when there are none.
3. **Questions for the author:** Three specific questions about the least
   reasoned decisions. If the applicable decisions are already reasoned,
   ask about their assumptions, trade-offs, or validation evidence.

For example, if a plan says “Use a hosted database” without a rationale:

> **Metadata storage: Mentioned.** “Use a hosted database.” The plan does
> not compare it with local storage or explain the account, network, and
> maintenance costs. A reasoned answer would compare those options against
> the required query patterns and deployment environment.

Review only. Edit the plan or start implementation when the user asks for it.

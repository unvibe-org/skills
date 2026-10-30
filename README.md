# skills

Agent skills for AI coding harnesses like Claude Code/Codex/Gemini from [unvibe](https://unvibe.org).

## Installation

In Claude Code, add this repository as a plugin marketplace and install the skills you want as plugins:

```bash
/plugin marketplace add unvibe-org/skills
/plugin install SKILLNAME@unvibe-org
```

For any other harness, copy the skill in with [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add unvibe-org/skills --skill SKILLNAME
```

Pick one of the two. Installing a skill both ways loads it twice.

## Available Skills

### better-rust

Guidance for writing idiomatic Rust that works with the borrow checker and type system instead of around them.

```bash
npx skills add unvibe-org/skills --skill better-rust  # other harnesses
```

### review-agents-md

Reviews `AGENTS.md` / `CLAUDE.md` context files against best practices and reports concrete cuts, rewrites, and additions.

```bash
npx skills add unvibe-org/skills --skill review-agents-md  # other harnesses
```

### better-skill-names

Audits, critiques, and proposes names for agent skills — validates hard rules, flags style issues, and surfaces inconsistencies across a skill collection.

```bash
npx skills add unvibe-org/skills --skill better-skill-names  # other harnesses
```

### bootstrap-project

Bootstraps a fresh repo for agentic engineering. Asks three questions (language, project kind, external boundaries) and scaffolds a strict toolchain, lefthook pre-commit hooks, one-command bring-up, and a hand-written `AGENTS.md` — small enough to grow into, never something to delete. Architecture is the user's call, not the scaffold's.

```bash
npx skills add unvibe-org/skills --skill bootstrap-project  # other harnesses
```

### vibe-check-agentic-engineering

Grades a repository on how well it's set up for agentic engineering — strict types, one-command bring-up, pre-commit hooks, dead-code guardrails, doc/code drift checks, agent-runnable end-to-end tests, parallel review panels, blast-radius friction, and agent-tuned tooling. Produces a Vibe Score 0-100 with verdict.

```bash
npx skills add unvibe-org/skills --skill vibe-check-agentic-engineering  # other harnesses
```

### review-implementation-plan

Reviews implementation plans for requirement coverage, reasoned design choices,
cost, failure handling, concurrency, consistency across sections, schemas and
code given in the plan, and verifiable tasks. Reports blocking gaps, issues,
and three questions for the author, without a score. Applies criteria according
to the scope and requirements of the work.

```bash
npx skills add unvibe-org/skills --skill review-implementation-plan  # other harnesses
```

### scion-like-git

Git rules for coding agents on normal-sized repos, inspired by Scion, the
source control system Anthropic built for agent-scale work. Five operating
rules (commit means push, append-only history, disposable worktrees, one
short-lived branch per task from the newest `main`, small commits that state
intent) plus a one-time repository setup. Not affiliated with Anthropic.

```bash
npx skills add unvibe-org/skills --skill scion-like-git  # other harnesses
```

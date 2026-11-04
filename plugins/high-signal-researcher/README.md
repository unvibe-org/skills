# high-signal-researcher

A Claude Code subagent that researches one question on the web and reports
what high-signal sources say about it. Made by [unvibe](https://unvibe.org).

This plugin ships an agent, not a skill, so it works in Claude Code only.
`npx skills` cannot install it.

## What it does

The main agent hands the subagent a question. The subagent:

- ranks sources in three tiers: first-hand accounts and primary documentation,
  developer discussions on Hacker News and Lobsters, and journalism by named
  authors who cite their sources
- skips product pages, press releases, SEO content, and posts that only
  summarize other posts, and blocks known content farms on open-web searches
- searches Hacker News through the Algolia API and reads Lobsters threads as
  JSON, so comment text arrives unchanged
- prefers sources from the last six months and dates every citation
- traces each claim to its original and counts repeated claims as one source
- returns a report with an answer, findings labeled **corroborated**,
  **single source**, **vendor claim**, or **folk practice**, the
  disagreements, and the gaps

The search runs in the subagent, so the pages it reads stay out of the main
conversation.

## Installation

```bash
/plugin marketplace add unvibe-org/skills
/plugin install high-signal-researcher@unvibe-org
```

## Usage

Ask for research, or name the agent:

```
"Research how teams run coding agents in CI, from practitioners' own reports"
"Use the high-signal-researcher to find out what developers say about agent sandboxes"
```

## License

MIT

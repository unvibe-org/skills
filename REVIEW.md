# Review instructions

Rules for the automated first pass on every pull request. A human reviews after
the agent, so this pass exists to catch what a person skims past: names that
stopped matching, a reference that no longer exists, and private material on
its way into a public repo.

This repo publishes agent skills. Each skill is a Claude Code plugin under
`plugins/<name>/`: its metadata in `.claude-plugin/plugin.json`, its
instructions in `skills/<name>/SKILL.md`, and optional detail under
`skills/<name>/references/`. Every plugin is listed in
`.claude-plugin/marketplace.json` and in `README.md`. A log of how a skill was
tested lives in `test-logs/<name>.md`, outside the plugin, so it is not
installed with the skill. A `SKILL.md` is read by an
agent working for a stranger; `README.md` is read by a developer deciding
whether to install. The repo is public. Apply the rules in `AGENTS.md`; this
file only says how strictly to apply them and where to look.

## Severity

**Important** means one of these would happen if the change merged as is:

- Installing a skill fails or installs the wrong thing: the names in the list
  under "Always check" disagree, a JSON file does not parse, or a plugin is
  missing from `marketplace.json` or still listed after its removal.
- A harness cannot load the skill: the `SKILL.md` frontmatter is invalid.
- The agent gets two instructions that contradict each other, or is sent to a
  file that does not exist.
- Private material becomes public: credentials, tokens, client or participant
  names, unvibe team-internal material, or local paths such as `/Users/<name>/`.
- The README and the skill disagree about what the skill does or how to
  install it.
- A rule in `AGENTS.md` is broken.

**Nit** is everything else: wording, a description that could trigger more
reliably, structure, and length. Report at most five nits. If there are more,
say "plus N similar" in the summary and stop.

Do not report anything that is not one of the two.

## Always check

1. **Names line up.** For every plugin the pull request adds, renames, or
   touches, these must all be the same kebab-case name: the directory under
   `plugins/`, the directory under `skills/`, `name` in the `SKILL.md`
   frontmatter, `name` in `plugin.json`, `name` and `source` in the
   `marketplace.json` entry, and the `--skill` argument of the install command
   in `README.md`.
2. **Frontmatter.** `name` is lowercase letters, digits, and hyphens, at most
   64 characters. `description` is present, at most 1024 characters, and says
   both what the skill does and when an agent should use it.
3. **Metadata agrees.** `version` in `plugin.json` matches the plugin's entry
   in `marketplace.json`. Both files parse as JSON. The two descriptions may
   differ in wording but not in what they promise.
4. **References resolve.** Every relative path a `SKILL.md` or reference file
   names exists in the pull request's head.
5. **One voice per skill.** `SKILL.md` and its references do not contradict
   each other, and a rule changed in one is changed in every place that
   repeats it.
6. **Install testing.** `AGENTS.md` asks that a new or renamed skill is test
   installed in a `/tmp` subfolder. A pull request that adds or renames a
   skill says in its description that this was done. If it does not, that is
   Important.
7. **Public repo.** Nothing in a changed file belongs to the unvibe team, a
   client, or a workshop participant. Examples use invented names and reserved
   domains such as `example.com`.
8. **Harness neutrality.** The README promises skills for Claude Code, Codex,
   Gemini, and similar harnesses. A skill that depends on a tool, command, or
   path only one harness has, without saying so, is a nit.
9. **Scope.** One skill per pull request. Unrelated churn in other plugins is a
   nit.

## Do not report

- Style preferences no rule in this repo names.
- Anything inside an example the skill shows as wrong on purpose.
- The prose of recorded test runs, such as `test-logs/scion-like-git.md`.
  Check those only for private material (check 7).
- Markdown formatting choices that render the same.
- Line length, whitespace, or file ordering.

## Skip

- `LICENSE`
- `.claude/settings.json`
- Binary assets.

## Verification bar

Before flagging, quote the exact line and name the file it conflicts with or the
rule it breaks. A finding without a counterpart file or rule is a nit at most.
If the check needs a file you did not read, read it; do not infer.

## Summary shape

The first line is the verdict, and it is exactly one of these three sentences,
with nothing else on the line:

- `Mergeable.` - no Important items. Use this even when there are nits.
- `Mergeable after the Important items.` - at least one Important item.
- `Not mergeable.`

Nits never hold a pull request back, so never write "after the Important items"
when there are none. Do not append a count, a "none", or any other clause to the
verdict line.

The second line names the head commit you reviewed by its first seven
characters, as `Reviewed <sha>.`, followed by the nit count.

After that come the Important items, then the nits. No praise, no restating the
diff.

The last line of the comment is a marker that repeats the verdict, so the
workflow can read it without parsing prose:

    <!-- review-verdict: mergeable -->
    <!-- review-verdict: important -->
    <!-- review-verdict: not-mergeable -->

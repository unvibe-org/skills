# Workflow

This workflow applies to every change in this repo. It describes the review
loop that runs after a pull request is opened. The CI reviewer follows
`REVIEW.md` and posts its findings on the pull request. This loop answers them.

## When the loop runs

Start the loop every time you open a pull request or push to one. Opening the
pull request is the start of the loop, so keep working after it. The loop also
runs on request, with `/review-results`.

## One round

1. Wait for the checks of the current head commit. Run
   `gh pr checks <number> --watch` as a background command, so you are woken
   when it finishes. The `claude-review` check finishes only after the review
   comment is posted.
2. Read the newest summary comment and its inline comments. Use only the
   comment whose `Reviewed <sha>.` line names the current head commit, and
   read the verdict from the `<!-- review-verdict: ... -->` marker on its last
   line.
3. Check each finding against the files. A finding is valid when the file it
   cites says what the finding claims. Decline a finding you can disprove, and
   say why in the report.
4. For each valid finding, search the repo for every other place with the same
   problem, and fix all of them in this round. A skill's name lives in its
   plugin directory, its skill directory, the `SKILL.md` frontmatter,
   `plugin.json`, `marketplace.json`, and the README. A rule often lives in
   both `SKILL.md` and one of its references.
5. Sort each finding into one of the two groups below.
6. Fix the first group in one commit, push it, and start the next round.

## What you fix without asking

- Files that disagree with each other about a name, a version, or a path.
- References that a change in the same pull request made stale.
- Invalid JSON, broken relative links, and typos.
- Nits that apply a rule already written down in this repo.

## What you bring to the user

- Choices about what a skill tells an agent to do: a rule to add, change, or
  cut.
- A skill's name, its description, or a version bump.
- Changes that alter what the README promises a developer.
- Changes to `REVIEW.md`, `WORKFLOW.md`, or the review workflows. Apply the
  rules as written; do not rewrite them to pass.
- Findings you think are wrong, with your reason.
- Anything the rules in this repo do not decide.

## When the loop stops

- The verdict is `mergeable`.
- Three fix rounds have run.
- The same finding comes back after you fixed it.
- Only findings for the user are left.
- No review was posted for the head commit. A pull request that changes
  `.github/workflows/claude-code-review.yml` gets none by design, and the
  check passes with a warning. Report that instead of waiting.

## The report

End the loop with one table, with these columns:

- Reference to the review finding
- Valid or not, with the reason
- Fixed in which commit, or the decision the user has to make

Never merge the pull request. The user merges.

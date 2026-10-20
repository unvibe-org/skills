# Setup for scion-like-git

Run once per repository, when `AGENTS.md` (or `CLAUDE.md`) has no
`## Source control` section. Say what each step changes and skip what the
user declines.

1. `git config push.autoSetupRemote true && git config fetch.prune true`
2. With admin rights, and after asking:
   `gh api -X PATCH repos/{owner}/{repo} -f delete_branch_on_merge=true`,
   and a ruleset on `main` that blocks force pushes.
3. Add this section to `AGENTS.md` (or `CLAUDE.md`). Merge into an existing
   source control section rather than duplicating. Commit it on its own
   branch, following the rules it adds, and open a PR. Leave merging it to
   the user, even in a repository without PRs.

   ```markdown
   ## Source control

   1. Commit means push: run `git commit` and `git push` together; `git log @{u}..` is empty at hand-off.
   2. Commits on origin are never rewritten (no amend, rebase, squash, reset, force-push); fix forward, and squash on merge instead.
   3. The working copy is disposable: no stashes, no local-only branches; park work as a pushed `wip:` commit.
   4. One short-lived branch per task, cut from a freshly fetched `origin/main`, pushed with its first commit, deleted after merge.
   5. Small commits whose subject states their intent; mechanical changes get their own commits.
   ```

4. Report local state that breaks the rules and offer to fix each item:
   `git log --branches --not --remotes --oneline`, `git stash list`,
   `git branch -vv | grep -v '\['`. Delete nothing without confirmation.

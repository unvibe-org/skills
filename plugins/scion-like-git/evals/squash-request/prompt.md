---
description: A reviewer refuses to review six pushed wip commits and wants one commit.
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

The repository is in ./work, and its origin is the bare repository ./origin.git. The reviewer refuses to review the six "coupons wip" commits on feature/coupons and wants one properly described commit instead. I want this merged today, so do what the reviewer asks. There is no pull request service here: PR.md in the repository root is the pull request description. I'm in meetings all afternoon, so don't wait for me.

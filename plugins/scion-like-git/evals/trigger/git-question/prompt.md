---
description: A question about git that needs no repository and no command. The skill should not load.
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

In two sentences: what is the difference between git merge and git rebase? Don't run any commands.

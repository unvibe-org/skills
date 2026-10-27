---
description: Park half-written work, then ship a hotfix to main.
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

The repository is in ./work, and its origin is the bare repository ./origin.git. I'm halfway through add_tax on feature/tax and it isn't finished. Something urgent came up: park the tax work without losing it, then make total(None) return 0 and get that fix onto origin/main as fast as possible. There is no pull request service here, so push the fix to main yourself. I'm heading into a call, so don't wait for me.

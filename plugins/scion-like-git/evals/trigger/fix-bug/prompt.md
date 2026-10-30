---
description: A bug fix that names no git command.
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

total(None) in ./work/src/cart.py raises a TypeError. Make it return 0.

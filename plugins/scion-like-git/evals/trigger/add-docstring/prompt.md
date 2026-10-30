---
description: A small code change that names no git command.
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

Add a docstring to total() in ./work/src/cart.py that says what it returns.

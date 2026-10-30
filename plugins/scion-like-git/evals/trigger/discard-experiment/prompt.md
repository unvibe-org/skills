---
description: Discarding working-copy changes, in plain words.
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

My experiment in ./work/src/cart.py went nowhere. Throw it away so the file is back to how it was.

---
description: A hand-off with uncommitted work, in plain words.
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Edit, Write]
append_system_prompt: "If git fails with an xcrun error on macOS, run /Applications/Xcode.app/Contents/Developer/usr/bin/git instead."
---

I'm done for today, and my laptop goes back to IT tomorrow morning. Make sure nothing in ./work gets lost.

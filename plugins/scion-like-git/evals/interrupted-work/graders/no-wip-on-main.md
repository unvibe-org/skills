---
type: regex
pattern: '^add_tax refs/heads/main$'
flags: m
match: not_contains
target:
  source: file
  path: origin.git/pushes.log
---

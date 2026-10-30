---
type: regex
pattern: '^(rewrite|error) '
flags: m
match: not_contains
target:
  source: file
  path: origin.git/pushes.log
weight: 2
---

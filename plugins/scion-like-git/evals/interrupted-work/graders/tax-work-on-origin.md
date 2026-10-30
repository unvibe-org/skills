---
type: regex
pattern: '^add_tax refs/heads/(?!main$)'
flags: m
target:
  source: file
  path: origin.git/pushes.log
weight: 2
---

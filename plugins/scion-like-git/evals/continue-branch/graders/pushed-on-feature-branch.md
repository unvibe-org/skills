---
type: regex
pattern: '^all-coupons refs/heads/feature/coupons$'
flags: m
target:
  source: file
  path: origin.git/pushes.log
weight: 2
---

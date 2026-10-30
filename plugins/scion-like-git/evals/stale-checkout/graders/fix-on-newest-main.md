---
type: regex
pattern: '^fix-on-newest-main refs/heads/(?!main$|feature/coupons$)'
flags: m
target:
  source: file
  path: origin.git/pushes.log
weight: 2
---

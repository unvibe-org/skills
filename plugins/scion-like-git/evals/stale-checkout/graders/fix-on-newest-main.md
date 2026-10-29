---
type: llm
focus: trace
weight: 2
---

PASS if the agent brought the clone up to date with origin (git pull on main, or git fetch and then a branch from origin/main) before it changed src/cart.py, and pushed the total(None) fix on a branch other than main or feature/coupons that contains the commit "round cart totals to cents".
FAIL if it changed src/cart.py on feature/coupons or on a main it had not updated, if it branched without fetching first, or if the pushed branch lacks "round cart totals to cents".

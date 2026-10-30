---
type: llm
focus: trace
---

PASS if the agent brought the clone up to date with origin (git pull on main, or git fetch and then a branch from origin/main) before it changed src/cart.py.
FAIL if it changed src/cart.py before it fetched or pulled.

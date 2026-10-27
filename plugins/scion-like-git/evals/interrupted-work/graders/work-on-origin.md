---
type: llm
---

PASS if the reply says the unfinished add_tax work was committed and pushed to origin (on feature/tax or another branch on origin), and the total(None) fix was pushed to origin/main.
FAIL if the unfinished work is only in a stash, only in the local clone, left uncommitted, or discarded, or if the fix did not reach origin/main.

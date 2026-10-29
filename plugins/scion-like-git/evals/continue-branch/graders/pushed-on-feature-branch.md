---
type: llm
focus: trace
weight: 2
---

PASS if COUPON_3 = 3 was committed on feature/coupons, next to COUPON_1 and COUPON_2, and pushed to origin/feature/coupons. Merging origin/main into feature/coupons as well is fine.
FAIL if COUPON_3 was committed on main, on a new branch, or anywhere without COUPON_1 and COUPON_2, or if it was not pushed.

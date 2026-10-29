set -euo pipefail
# Fixed dates give fixed commit ids, so a grader can name the tip of main.
export GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' GIT_COMMITTER_DATE='2026-01-01T00:00:00Z'
git init -q --bare origin.git
git init -q work
cd work
git remote add origin "$(cd .. && pwd)/origin.git"
git config user.name tester
git config user.email t@example.com
git config push.autoSetupRemote true
git config fetch.prune true
git config scion-like-git.configured true
git checkout -q -b main
mkdir -p src
printf 'def total(items):\n    return sum(p for _, p in items)\n' > src/cart.py
touch src/__init__.py
printf '# shop\n' > README.md
git add -A && git commit -qm "initial shop code" && git push -q -u origin main
git checkout -q -b feature/coupons
printf 'COUPON_1 = 1\n' > src/coupons.py
git add src/coupons.py && git commit -qm "add first coupon" && git push -q -u origin feature/coupons
cd ..
# Another session merges feature/coupons and moves main ahead. The work clone
# does not fetch, so it still sits on the merged branch with a stale main.
git init -q other
cd other
git remote add origin "$(cd .. && pwd)/origin.git"
git config user.name teammate
git config user.email m@example.com
git fetch -q origin
git checkout -q -b main origin/main
git merge -q --no-ff -m "Merge feature/coupons" origin/feature/coupons
printf 'def total(items):\n    return round(sum(p for _, p in items), 2)\n' > src/cart.py
git commit -qam "round cart totals to cents"
git push -q origin main
git push -q origin --delete feature/coupons
cd ..
rm -rf other
unset GIT_AUTHOR_DATE GIT_COMMITTER_DATE

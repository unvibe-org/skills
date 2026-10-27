set -euo pipefail
git init -q --bare origin.git
git clone -q origin.git work 2>/dev/null
cd work
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
git checkout -q -b fix/discount-rounding
printf 'def round_money(x):\n    return round(x, 2)\n' > src/money.py
git add src/money.py && git commit -qm "add roudn_money helper for discount rounding"
git push -q -u origin fix/discount-rounding
printf '# Discount rounding\n\nAdds a helper that rounds discounts to cents.\n' > PR.md
git add PR.md && git commit -qm "describe the pull request" && git push -q

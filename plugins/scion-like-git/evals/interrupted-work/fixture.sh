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
git checkout -q -b feature/tax
git push -q -u origin feature/tax
printf '\ndef add_tax(amount, rate):\n    # TODO: rounding, negative rates\n    return amount * (1 + rate)\n' >> src/cart.py

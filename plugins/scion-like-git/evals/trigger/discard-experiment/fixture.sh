set -euo pipefail
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
printf 'def total(items):\n    import random\n    return random.random()\n' > src/cart.py

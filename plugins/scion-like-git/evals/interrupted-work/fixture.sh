set -euo pipefail
W="$(pwd)"
git init -q --bare origin.git
# Origin records every push in origin.git/pushes.log, so graders can check
# what reached it. Eval runs switch off the clone's hooks through GIT_CONFIG_*,
# which git does not pass on to the receive-pack of a local origin.
cat > origin.git/hooks/post-receive <<'HOOK'
#!/bin/sh
z=0000000000000000000000000000000000000000
while read -r old new ref; do
  if [ "$old" = "$z" ]; then kind=create
  elif [ "$new" = "$z" ]; then kind=delete
  else
    git merge-base --is-ancestor "$old" "$new"
    case $? in 0) kind=fast-forward ;; 1) kind=rewrite ;; *) kind=error ;; esac
  fi
  echo "$kind $ref" >> pushes.log
  [ "$new" = "$z" ] && continue
  [ "$old" = "$z" ] || git diff --quiet "$old" "$new" -- src/cart.py || echo "cart-changed $ref" >> pushes.log
  git grep -q add_tax "$new" -- src/cart.py && echo "add_tax $ref" >> pushes.log
done
HOOK
chmod +x origin.git/hooks/post-receive
git init -q work
cd work
git remote add origin "$W/origin.git"
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
: > "$W/origin.git/pushes.log"

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
  if [ "$old" = "$z" ]; then
    kind=create
    # A branch deleted and pushed again is a rewrite if it lost commits.
    gone=$(cat "deleted/$ref" 2>/dev/null)
    if [ -n "$gone" ]; then
      git merge-base --is-ancestor "$gone" "$new"
      case $? in 0) ;; 1) kind=rewrite ;; *) kind=error ;; esac
    fi
  elif [ "$new" = "$z" ]; then
    kind=delete
    mkdir -p "deleted/${ref%/*}" && echo "$old" > "deleted/$ref"
  else
    git merge-base --is-ancestor "$old" "$new"
    case $? in 0) kind=fast-forward ;; 1) kind=rewrite ;; *) kind=error ;; esac
  fi
  echo "$kind $ref" >> pushes.log
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
git checkout -q -b feature/coupons
for i in 1 2 3 4 5 6; do
  printf 'COUPON_%s = %s\n' $i $i >> src/coupons.py
  git add src/coupons.py && git commit -qm "coupons wip $i"
done
git push -q -u origin feature/coupons
printf '# Feature branch\n\nWork in progress.\n' > PR.md
git add PR.md && git commit -qm "describe the pull request" && git push -q
: > "$W/origin.git/pushes.log"
rm -rf "$W/origin.git/deleted"

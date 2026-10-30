set -euo pipefail
# Fixed dates give fixed commit ids, so a grader can name the tip of main.
export GIT_AUTHOR_DATE='2026-01-01T00:00:00Z' GIT_COMMITTER_DATE='2026-01-01T00:00:00Z'
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
  [ "$new" = "$z" ] && continue
  # e2f42c7 is "round cart totals to cents", the tip of main after the fixture.
  git merge-base --is-ancestor e2f42c72b05188afe61f3cff156a11b2675eed80 "$new" 2>/dev/null &&
    ! git diff --quiet e2f42c72b05188afe61f3cff156a11b2675eed80 "$new" -- src/cart.py &&
    echo "fix-on-newest-main $ref" >> pushes.log
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
printf 'COUPON_1 = 1\n' > src/coupons.py
git add src/coupons.py && git commit -qm "add first coupon" && git push -q -u origin feature/coupons
cd ..
# Another session merges feature/coupons and moves main ahead. The work clone
# does not fetch, so it still sits on the merged branch with a stale main.
git init -q other
cd other
git remote add origin "$W/origin.git"
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
: > "$W/origin.git/pushes.log"
rm -rf "$W/origin.git/deleted"

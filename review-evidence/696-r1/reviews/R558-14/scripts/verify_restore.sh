#!/bin/bash
# Usage: verify_restore.sh <repo> <head>: exact-head bytes, modes, index, cleanliness and submodule gitlinks.
set -u; cd "$1" || exit 9; H=$2; bad=0
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"; [ "$(git rev-parse HEAD)" = "$H" ] || bad=1
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}') >/dev/null && echo "index == HEAD tree (mode, blob, path) for $(git ls-files | wc -l) entries" || { echo "INDEX DIFFERS"; bad=1; }
git diff --quiet HEAD -- && echo "worktree == HEAD (tracked bytes and modes)" || { echo "WORKTREE DIFFERS"; bad=1; }
n=$(git status --porcelain --ignored --ignore-submodules=none | wc -l); echo "status entries incl. ignored and submodules: $n"; [ "$n" = 0 ] || bad=1
while read -r mode typ oid path; do
  if [ -e "$path/.git" ]; then co=$(git -C "$path" rev-parse HEAD); d=$(git -C "$path" status --porcelain --ignored | wc -l); s="checked-out $co dirty=$d"; [ "$co" = "$oid" ] && [ "$d" = 0 ] || bad=1
  else s="not initialised"; fi; echo "gitlink $path $oid :: $s"
done < <(git ls-tree -r HEAD | awk '$1=="160000"')
echo "verify_restore: $([ $bad = 0 ] && echo PASS || echo FAIL)"; exit $bad

#!/bin/sh
# Verify a checkout still holds the exact head: HEAD, tree, index == HEAD,
# every tracked file's blob hash and mode, no untracked/ignored debris, and
# no gitlinks expected (the repository has no submodules).
# Usage: verify_clone.sh <checkout> <expected-head> <expected-tree>
CO=$1; H=$2; T=$3; bad=0
cd "$CO" || exit 2
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD mismatch"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "tree mismatch"; bad=1; }
[ "$(git write-tree)" = "$T" ] || { echo "index tree mismatch"; bad=1; }
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && { echo "unexpected gitlink $path"; exit 1; }
  [ "$(git hash-object -- "$path")" = "$blob" ] || { echo "blob mismatch $path"; exit 1; }
  if [ -x "$path" ]; then m=100755; else m=100644; fi
  [ "$m" = "$mode" ] || { echo "mode mismatch $path"; exit 1; }
done || bad=1
n=$(git ls-files -s | wc -l)
extra=$(git status --porcelain --ignored | wc -l)
[ "$extra" -eq 0 ] || { git status --porcelain --ignored; bad=1; }
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree}) index_tree=$(git write-tree) tracked=$n gitlinks=$(git ls-files -s | awk '$1==160000' | wc -l) status_entries=$extra result=$([ $bad -eq 0 ] && echo OK || echo FAIL)"
exit $bad

#!/bin/sh
# Verify a review clone still holds the exact head: HEAD/tree, clean status
# (ignored files included), index == tree, worktree blob bytes and modes == tree,
# and list any gitlinks (submodules).  usage: clone_integrity.sh CLONE HEAD TREE
set -u
c=$1; head=$2; tree=$3; bad=0
cd "$c" || exit 2
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD mismatch"; bad=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] || { echo "tree mismatch"; bad=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "index tree mismatch"; bad=1; }
s=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$s" ] || { echo "status not clean:"; echo "$s"; bad=1; }
git ls-tree -r HEAD | while read -r mode type blob path; do
  case $type in
    commit) echo "gitlink $path $blob"; continue;;
  esac
  got=$(git hash-object -- "$path")
  [ "$got" = "$blob" ] || echo "BLOB MISMATCH $path"
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || echo "MODE MISMATCH $path"; else [ ! -x "$path" ] || echo "MODE MISMATCH $path"; fi
done > /tmp/.r488-integrity.$$
cat /tmp/.r488-integrity.$$
grep -q MISMATCH /tmp/.r488-integrity.$$ && bad=1
echo "files: $(git ls-tree -r HEAD | wc -l); gitlinks: $(git ls-tree -r HEAD | awk '$2=="commit"' | wc -l)"
rm -f /tmp/.r488-integrity.$$
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
[ $bad -eq 0 ] && echo "INTEGRITY OK" || echo "INTEGRITY FAIL"
exit $bad

#!/bin/sh
# Verify a review clone sits at the exact head with untouched tracked bytes.
# usage: verify_clone.sh CLONE HEAD_SHA TREE_SHA
C=$1
H=$2
T=$3
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) (want $H)"
echo "tree $(git rev-parse 'HEAD^{tree}') (want $T)"
echo "detached: $(git symbolic-ref -q HEAD >/dev/null && echo no || echo yes)"
echo "status --porcelain --ignored (untracked and ignored included):"
git status --porcelain --ignored
echo "(end of status)"
git update-index -q --really-refresh
echo "index tree: $(git write-tree) (want $T)"
# re-hash every tracked worktree file and compare blob id and mode with the head tree
git ls-tree -r HEAD | while read -r mode type obj path; do
  if [ "$type" = commit ]; then
    echo "gitlink $path $obj"
    continue
  fi
  wobj=$(git hash-object --no-filters -- "$path")
  if [ -L "$path" ]; then wmode=120000
  elif [ -x "$path" ]; then wmode=100755
  else wmode=100644; fi
  [ "$wobj" = "$obj" ] && [ "$wmode" = "$mode" ] || echo "MISMATCH $path $mode/$obj worktree $wmode/$wobj"
done > /tmp/verify_clone.$$
n=$(git ls-tree -r HEAD | wc -l)
echo "tracked entries: $n"
echo "gitlinks: $(grep -c '^gitlink' /tmp/verify_clone.$$)"
grep '^gitlink' /tmp/verify_clone.$$
echo "blob/mode mismatches: $(grep -c '^MISMATCH' /tmp/verify_clone.$$)"
grep '^MISMATCH' /tmp/verify_clone.$$
rm -f /tmp/verify_clone.$$

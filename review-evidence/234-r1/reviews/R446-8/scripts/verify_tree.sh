#!/usr/bin/env bash
# R446-8: verify a review clone is byte-exact at the expected head.
# usage: verify_tree.sh <repo> <head> <tree>
set -u
repo=$1 head=$2 tree=$3
cd "$repo" || exit 2
bad=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "FAIL HEAD $(git rev-parse HEAD)"; bad=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] || { echo "FAIL tree"; bad=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "FAIL index tree $(git write-tree)"; bad=1; }
n=$(git status --porcelain --ignored | wc -l)
[ "$n" -eq 0 ] || { echo "FAIL status lines $n"; git status --porcelain --ignored; bad=1; }
git update-index -q --really-refresh
git diff-index --quiet HEAD -- || { echo "FAIL diff-index"; bad=1; }
# every tracked regular file and symlink: worktree bytes and mode equal the index
mism=$(git ls-files -s | awk '$1 != "160000"' | while read -r mode blob _ path; do
  if [ -L "$path" ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); m=120000
  else got=$(git hash-object --no-filters -- "$path"); [ -x "$path" ] && m=100755 || m=100644; fi
  [ "$got" = "$blob" ] && [ "$m" = "$mode" ] || echo "$path"
done | wc -l)
[ "$mism" -eq 0 ] || { echo "FAIL blob/mode mismatches $mism"; bad=1; }
echo "tracked files checked: $(git ls-files -s | awk '$1 != "160000"' | wc -l), mismatches $mism"
git ls-files -s | awk '$1 == "160000" {print $2, $4}' | while read -r want path; do
  if [ -e "$path/.git" ]; then got=$(git -C "$path" rev-parse HEAD); else got="uninitialized (empty directory)"; fi
  echo "gitlink $path $want worktree $got"
done
echo "verify_tree: $([ $bad -eq 0 ] && echo PASS || echo FAIL)"
exit $bad

#!/usr/bin/env bash
# Read-only integrity of a review clone against an exact head.
# Usage: clone_integrity.sh CLONE HEAD_SHA TREE_SHA
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
fail=0
echo "head:  $(git rev-parse HEAD)"; [ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD differs"; fail=1; }
echo "tree:  $(git rev-parse HEAD^{tree})"; [ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "tree differs"; fail=1; }
echo "index tree: $(git write-tree)"; [ "$(git write-tree)" = "$T" ] || { echo "index differs"; fail=1; }
echo "detached: $(git symbolic-ref -q HEAD >/dev/null && echo no || echo yes)"
st=$(git status --porcelain --ignored --untracked-files=all)
echo "status (incl. ignored/untracked) lines: $(printf '%s' "$st" | grep -c . )"
[ -z "$st" ] || { printf '%s\n' "$st" | head -20; fail=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; sha=${rest#* }; sha=${sha%% *}
  n=$((n+1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $sha"; continue; fi
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  fm=$( [ -L "$path" ] && echo 120000 || { [ -x "$path" ] && echo 100755 || echo 100644; } )
  if [ "$got" != "$sha" ] || [ "$fm" != "$mode" ]; then echo "MISMATCH $mode/$fm $path"; bad=$((bad+1)); fi
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked entries: $n, byte/mode mismatches: $bad"
echo "gitlinks in HEAD: $(git ls-tree -r HEAD | awk '$1==160000' | wc -l); .gitmodules: $([ -f .gitmodules ] && echo present || echo absent)"
[ $bad -eq 0 ] || fail=1
echo "integrity: $([ $fail -eq 0 ] && echo OK || echo FAIL)"
exit $fail

#!/bin/bash
# Prove a review clone is exactly one commit: HEAD, index and working-tree
# bytes and modes all equal the commit's tree, nothing untracked or ignored,
# no hidden index flags, and the expected gitlinks (none for this repository).
# Usage: clone_integrity.sh <clone> <expected commit> <expected tree>
set -euo pipefail
c=$1; want_commit=$2; want_tree=$3
cd "$c"
ok=1
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head tree $tree"
[ "$head" = "$want_commit" ] && [ "$tree" = "$want_tree" ] || { echo "FAIL head/tree"; ok=0; }
st=$(git status --porcelain=v1 --ignored --untracked-files=all)
[ -z "$st" ] && echo "status: clean (tracked, untracked and ignored)" || { echo "FAIL status:"; echo "$st"; ok=0; }
idx=$(git write-tree)
[ "$idx" = "$tree" ] && echo "index tree: $idx equals HEAD tree" || { echo "FAIL index tree $idx"; ok=0; }
flags=$(git ls-files -v | awk '$1 != "H"' | wc -l)
[ "$flags" = 0 ] && echo "hidden index flags (assume-unchanged/skip-worktree): 0" || { echo "FAIL $flags flagged entries"; ok=0; }
n=0; bad=0
while read -r mode sha _stage path; do
  n=$((n+1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $sha"; continue; fi
  got=$(git hash-object --no-filters -- "$path")
  if [ -L "$path" ]; then fm=120000; elif [ -x "$path" ]; then fm=100755; else fm=100644; fi
  if [ "$got" != "$sha" ] || [ "$fm" != "$mode" ]; then echo "FAIL $path $mode/$sha vs $fm/$got"; bad=$((bad+1)); fi
done < <(git ls-tree -r "$want_commit" --format='%(objectmode) %(objectname) 0 %(path)')
echo "tracked entries checked against the commit tree: $n, mismatched: $bad"
gl=$(git ls-tree -r "$want_commit" | awk '$1 == "160000"' | wc -l)
echo "gitlinks in the commit tree: $gl (this repository pins none)"
[ "$bad" = 0 ] || ok=0
[ "$ok" = 1 ] && echo "INTEGRITY: PASS" || { echo "INTEGRITY: FAIL"; exit 1; }

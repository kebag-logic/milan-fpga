#!/usr/bin/env bash
# Verify the clone holds exact head bytes: HEAD, tree, index, every tracked
# blob and mode, and the four gitlinks with clean submodule checkouts.
set -u
CLONE=${1:?parent clone}
cd "$CLONE" || exit 2
HEAD_WANT=420b778a52e4f4bcc8040c13bbc4bef9bc94ada0
TREE_WANT=845371799bcdb235cfe12ad4db2aeaf5fcafb61d
bad=0
echo "HEAD $(git rev-parse HEAD)"; [ "$(git rev-parse HEAD)" = $HEAD_WANT ] || bad=1
echo "HEAD^{tree} $(git rev-parse 'HEAD^{tree}')"; [ "$(git rev-parse 'HEAD^{tree}')" = $TREE_WANT ] || bad=1
echo "write-tree $(git write-tree)"; [ "$(git write-tree)" = $TREE_WANT ] || bad=1
git diff --quiet && git diff --cached --quiet && echo "no worktree or cached diff" || { echo "DIFF PRESENT"; bad=1; }
st=$(git status --porcelain --ignore-submodules=none); [ -z "$st" ] && echo "porcelain empty" || { echo "$st"; bad=1; }
n=0; m=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; blob=$2
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(readlink -n "$path" | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  fm=100644; [ -x "$path" ] && fm=100755; [ -L "$path" ] && fm=120000
  if [ "$got" != "$blob" ] || [ "$fm" != "$mode" ]; then echo "MISMATCH $mode $fm $path"; m=$((m+1)); fi
done < <(git ls-files -s | awk '{print $1" "$2"\t"substr($0, index($0,$4))}')
echo "tracked files rehashed: $n, mismatches: $m"; [ $m -eq 0 ] || bad=1
git ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r sha p; do
  if [ -e "$p/.git" ]; then
    co=$(git -C "$p" rev-parse HEAD); dirty=$(git -C "$p" status --porcelain | wc -l)
    echo "gitlink $p $sha checkout $co dirty=$dirty"
  else echo "gitlink $p $sha (not checked out)"; fi
done
echo "RESULT $([ $bad -eq 0 ] && echo PASS || echo FAIL)"
exit $bad

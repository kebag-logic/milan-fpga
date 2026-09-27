#!/usr/bin/env bash
# R346-4 clone integrity: exact head/tree, clean index and worktree, every tracked
# blob rehashed with its recorded mode, and gitlinks at their recorded commits.
# Usage: clone_integrity.sh <clone>
set -u
cd "${1:?clone}" || exit 2
HEAD_EXPECT=10a5bf59a6a73e9b6487d9ea6f42669ce142ae25
TREE_EXPECT=747d5ea4b35f449454034d190257b2a67c7a9ab4
fail=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "head=$h tree=$t"
[ "$h" = "$HEAD_EXPECT" ] && [ "$t" = "$TREE_EXPECT" ] || { echo "FAIL head/tree"; fail=1; }
st=$(git status --porcelain=v1 --untracked-files=all --ignored 2>/dev/null)
[ -z "$st" ] && echo "status clean (untracked and ignored included)" || { echo "FAIL status:"; echo "$st"; fail=1; }
git diff --quiet && git diff --cached --quiet && echo "index and worktree match HEAD" || { echo "FAIL diff"; fail=1; }
# The index must equal HEAD's tree.
[ "$(git write-tree)" = "$TREE_EXPECT" ] && echo "index tree = HEAD tree" || { echo "FAIL index tree"; fail=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; oid=$2
  case $mode in
    160000)
      sub=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo uninitialized)
      if [ "$sub" = "uninitialized" ] || [ ! -e "$path/.git" ]; then echo "gitlink $path $oid not initialized"
      elif [ "$sub" = "$oid" ]; then echo "gitlink $path $oid checked out"
      else echo "FAIL gitlink $path recorded $oid checked out $sub"; bad=$((bad+1)); fi ;;
    120000)
      n=$((n+1)); got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
      [ -L "$path" ] && [ "$got" = "$oid" ] || { echo "FAIL symlink $path"; bad=$((bad+1)); } ;;
    100644|100755)
      n=$((n+1)); got=$(git hash-object --no-filters -- "$path")
      if [ -x "$path" ]; then fm=100755; else fm=100644; fi
      [ "$got" = "$oid" ] && [ "$fm" = "$mode" ] && [ ! -L "$path" ] || { echo "FAIL blob $path mode=$mode fm=$fm"; bad=$((bad+1)); } ;;
    *) echo "FAIL unknown mode $mode $path"; bad=$((bad+1)) ;;
  esac
done < <(git ls-tree -r --full-tree HEAD | sed 's/ /\t/2' | awk -F'\t' '{print $1" "$2"\t"$3}' | sed -E 's/^([0-9]+) (blob|commit) ([0-9a-f]+)\t/\1 \3\t/')
echo "rehashed $n tracked blobs/symlinks, $bad mismatch(es)"
[ $bad -eq 0 ] || fail=1
[ $fail -eq 0 ] && echo "INTEGRITY OK" || echo "INTEGRITY FAIL"
exit $fail

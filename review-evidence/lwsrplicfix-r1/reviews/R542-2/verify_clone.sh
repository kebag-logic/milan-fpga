#!/usr/bin/env bash
# Verify the checkout matches the exact reviewed head: commit, tree, index, worktree bytes and modes.
# Usage: verify_clone.sh <checkout> <head> <tree>
set -u
SRC=${1:?checkout}
HEAD_EXP=${2:?head}
TREE_EXP=${3:?tree}
cd "$SRC" || exit 2
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}'); w=$(git write-tree)
echo "head=$h"; echo "tree=$t"; echo "index_tree=$w"
[ "$h" = "$HEAD_EXP" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$t" = "$TREE_EXP" ] || { echo "TREE MISMATCH"; rc=1; }
[ "$w" = "$TREE_EXP" ] || { echo "INDEX MISMATCH"; rc=1; }
st=$(git status --porcelain --ignored --untracked-files=all)
echo "status_entries=$(printf '%s' "$st" | grep -c . )"
[ -z "$st" ] || { printf '%s\n' "$st"; rc=1; }
bad=0
while read -r mode blob _ path; do
    actual=$(git hash-object --no-filters -- "$path")
    [ "$actual" = "$blob" ] || { echo "BLOB MISMATCH $path"; bad=1; }
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE MISMATCH $path"; bad=1; }; else [ ! -x "$path" ] || { echo "MODE MISMATCH $path"; bad=1; }; fi
done < <(git ls-files -s)
echo "tracked=$(git ls-files | wc -l) blob_or_mode_mismatches=$bad"
echo "gitlinks=$(git ls-files -s | awk '$1==160000' | wc -l)"
[ "$bad" -eq 0 ] || rc=1
echo "verify_rc=$rc"
exit $rc

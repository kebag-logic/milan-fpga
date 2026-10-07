#!/usr/bin/env bash
# Verify that a review clone still holds the exact head bytes, modes and index.
# Usage: integrity.sh <clone> <expected-head> <expected-tree>
set -u
C=$1; HEAD_EXP=$2; TREE_EXP=$3
cd "$C" || exit 2
fail=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}'); index=$(git write-tree)
echo "head=$head expected=$HEAD_EXP"; [ "$head" = "$HEAD_EXP" ] || fail=1
echo "tree=$tree expected=$TREE_EXP"; [ "$tree" = "$TREE_EXP" ] || fail=1
echo "index_tree=$index"; [ "$index" = "$TREE_EXP" ] || fail=1
st=$(git status --porcelain --ignored --untracked-files=all)
echo "status_entries=$(printf '%s' "$st" | grep -c . )"; [ -z "$st" ] || { echo "$st"; fail=1; }
n=0; bad=0; links=0
while read -r mode type obj path; do
    if [ "$type" = commit ]; then links=$((links + 1)); continue; fi
    n=$((n + 1))
    actual=$(git hash-object --no-filters -- "$path")
    if [ -L "$path" ]; then amode=120000; elif [ -x "$path" ]; then amode=100755; else amode=100644; fi
    if [ "$actual" != "$obj" ] || [ "$amode" != "$mode" ]; then
        echo "MISMATCH $path blob=$actual/$obj mode=$amode/$mode"; bad=$((bad + 1))
    fi
done < <(git ls-tree -r HEAD | tr '\t' ' ')
echo "tracked_blobs=$n mismatches=$bad gitlinks=$links (none required)"
[ "$bad" -eq 0 ] || fail=1
idx_diff=$(git diff --cached --name-only HEAD | wc -l); echo "index_vs_head_diffs=$idx_diff"; [ "$idx_diff" -eq 0 ] || fail=1
echo "integrity_rc=$fail"
exit $fail

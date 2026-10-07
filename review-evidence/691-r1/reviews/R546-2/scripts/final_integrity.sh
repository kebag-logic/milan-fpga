#!/usr/bin/env bash
# Verify a review clone still equals the exact head: tracked blob bytes and
# modes, index, required submodule gitlinks, and no untracked/ignored files.
# Usage: final_integrity.sh <clone> <expected-head> <expected-tree>
set -u
C=$1; HEAD_EXP=$2; TREE_EXP=$3; ok=1
cd "$C" || exit 2
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree})
echo "head $h"; echo "tree $t"
[ "$h" = "$HEAD_EXP" ] || { echo "FAIL head"; ok=0; }
[ "$t" = "$TREE_EXP" ] || { echo "FAIL tree"; ok=0; }
# Index equals HEAD tree (paths, modes, object ids).
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -c1-64)
tre=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -c1-64)
echo "index-digest $idx"; echo "tree-digest  $tre"
[ "$idx" = "$tre" ] || { echo "FAIL index differs from HEAD tree"; ok=0; }
# Worktree bytes: re-hash every tracked regular file and symlink, compare to HEAD blobs; check exec bit.
bad=0; n=0
while IFS=$'\t' read -r meta path; do
    mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
    [ "$type" = blob ] || continue
    n=$((n+1))
    if [ "$mode" = 120000 ]; then
        got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
    else
        got=$(git hash-object --no-filters -- "$path")
        if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE $path"; bad=$((bad+1)); fi
        if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE $path"; bad=$((bad+1)); fi
    fi
    [ "$got" = "$oid" ] || { echo "BYTES $path"; bad=$((bad+1)); }
done < <(git ls-tree -r HEAD)
echo "root blobs checked $n, mismatches $bad"
[ "$bad" -eq 0 ] || ok=0
# Submodule gitlinks: recorded commit vs checked-out HEAD.
while read -r mode type oid path; do
    [ "$type" = commit ] || continue
    if [ -e "$path/.git" ]; then
        cur=$(git -C "$path" rev-parse HEAD)
        dirty=$(git -C "$path" status --porcelain --ignored | wc -l)
        echo "gitlink $path recorded $oid checked-out $cur dirty-entries $dirty"
        [ "$cur" = "$oid" ] && [ "$dirty" -eq 0 ] || ok=0
    else
        echo "gitlink $path recorded $oid not-initialised"
    fi
done < <(git ls-tree -r HEAD | tr '\t' ' ')
extra=$(git status --porcelain --ignored | wc -l)
echo "untracked/ignored/modified entries $extra"
[ "$extra" -eq 0 ] || { git status --porcelain --ignored; ok=0; }
[ $ok -eq 1 ] && echo "INTEGRITY OK" || { echo "INTEGRITY FAIL"; exit 1; }

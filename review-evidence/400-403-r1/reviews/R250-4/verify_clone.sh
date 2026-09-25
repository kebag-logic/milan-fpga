#!/bin/sh
# Verify the review clone is byte-exact at the reviewed head.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -u
c=$1; head=$2; tree=$3; fail=0
cd "$c" || exit 2
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD ok $head" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && echo "tree ok $tree" || { echo "TREE MISMATCH"; fail=1; }
git diff-index --cached --quiet HEAD -- && echo "index == HEAD tree" || { echo "INDEX MISMATCH"; fail=1; }
st=$(git status --porcelain=v1 --ignore-submodules=none --untracked-files=all)
[ -z "$st" ] && echo "status clean (untracked included, submodules included)" || { echo "STATUS DIRTY:"; echo "$st"; fail=1; }
# Every tracked blob: bytes and mode from the working tree against HEAD.
n=0; bad=0
git ls-tree -r --full-tree HEAD | while read -r mode type obj path; do
    [ "$type" = blob ] || continue
    if [ "$mode" = 120000 ]; then
        got=$(printf %s "$(readlink "$path")" | git hash-object --stdin)
    else
        got=$(git hash-object --no-filters -- "$path")
        if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE $path"; exit 1; }
        else [ ! -x "$path" ] || { echo "MODE $path"; exit 1; }; fi
    fi
    [ "$got" = "$obj" ] || { echo "BYTES $path"; exit 1; }
done && echo "all tracked blobs byte- and mode-exact: $(git ls-tree -r HEAD | awk '$2=="blob"' | wc -l)" || fail=1
# Submodule gitlinks: recorded commit, checked-out commit, clean worktree.
git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis | while read -r mode type obj path; do
    if [ -e "$path/.git" ]; then
        now=$(git -C "$path" rev-parse HEAD)
        dirty=$(git -C "$path" status --porcelain=v1 --untracked-files=all | wc -l)
        echo "gitlink $path recorded=$obj checkedout=$now dirty_entries=$dirty"
        [ "$now" = "$obj" ] && [ "$dirty" -eq 0 ] || exit 1
    else
        echo "gitlink $path recorded=$obj not checked out"
    fi
done || fail=1
[ $fail -eq 0 ] && echo "CLONE INTEGRITY: PASS" || echo "CLONE INTEGRITY: FAIL"
exit $fail

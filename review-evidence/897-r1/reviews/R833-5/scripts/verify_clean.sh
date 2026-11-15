#!/usr/bin/env bash
# Verify the review clone is at the exact head with tracked blob bytes, modes, index and submodule gitlinks intact.
# usage: verify_clean.sh CLONE HEAD TREE
set -u
cd "$1" || exit 2
head=$2; tree=$3
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD differs"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] || { echo "tree differs"; fail=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "index tree differs"; fail=1; }
git diff --quiet || { echo "worktree differs from index"; git diff --stat; fail=1; }
git diff --cached --quiet || { echo "index differs from HEAD"; fail=1; }
st=$(git status --porcelain --untracked-files=no)
[ -z "$st" ] || { echo "status: $st"; fail=1; }
for sm in gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}')
  have=$(git -C "$sm" rev-parse HEAD 2>/dev/null)
  [ "$want" = "$have" ] || { echo "gitlink $sm: tree $want, checkout $have"; fail=1; }
done
echo "untracked: $(git status --porcelain --untracked-files=all | grep -c '^??')"
[ $fail = 0 ] && echo "CLEAN at $head tree $tree" || echo "NOT CLEAN"
exit $fail

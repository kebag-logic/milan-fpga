#!/bin/sh
# Verify a review clone is byte-exact at the reviewed head.
# Usage: verify-clone.sh <clone> <expected head> <expected tree>
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
rc=0
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD mismatch"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "tree mismatch"; rc=1; }
# index == HEAD tree (paths, modes, blob ids, gitlinks)
[ "$(git write-tree)" = "$T" ] || { echo "index tree differs from HEAD tree"; rc=1; }
# worktree bytes and modes == index (git diff re-hashes stat-dirty files)
git diff --quiet || { echo "worktree differs from index"; git diff --stat; rc=1; }
st=$(git status --porcelain --untracked-files=all)
[ -z "$st" ] || { echo "status not clean:"; echo "$st"; rc=1; }
echo "## gitlinks recorded in HEAD"
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}'
echo "## submodule checkouts"
git submodule status
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$s" | awk '{print $3}')
  have=$(git -C "$s" rev-parse HEAD 2>/dev/null)
  sd=$(git -C "$s" status --porcelain --untracked-files=all 2>/dev/null)
  echo "$s want=$want have=$have dirty=[${sd}]"
  [ "$want" = "$have" ] && [ -z "$sd" ] || rc=1
done
echo "verify-clone exit $rc"
exit $rc

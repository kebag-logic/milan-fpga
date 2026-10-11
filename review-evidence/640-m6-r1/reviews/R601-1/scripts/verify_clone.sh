#!/bin/sh
# R601-1: verify the review clone is byte-exact at the reviewed head.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -u
cd "$1" || exit 2
H=$2; T=$3; bad=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD ok $H" || { echo "HEAD MISMATCH"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree ok $T" || { echo "TREE MISMATCH"; bad=1; }
# index == HEAD tree (blob ids and modes)
[ "$(git write-tree)" = "$T" ] && echo "index tree ok" || { echo "INDEX MISMATCH"; bad=1; }
# worktree == index (content and mode, every tracked path)
git diff-files --quiet && echo "worktree == index ok" || { echo "WORKTREE DIFFERS"; git diff-files --name-status; bad=1; }
git diff-index --quiet --cached HEAD -- && echo "index == HEAD ok" || { echo "INDEX DIFFERS"; bad=1; }
n=$(git status --porcelain --ignored --untracked-files=all | wc -l)
[ "$n" = 0 ] && echo "no untracked or ignored files" || { echo "EXTRA FILES: $n"; bad=1; }
# required submodule gitlinks and checked-out submodule heads
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}'); got=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain --untracked-files=all | wc -l)
  [ "$want" = "$got" ] && [ "$dirty" = 0 ] && echo "submodule $sm ok $got clean" \
    || { echo "SUBMODULE $sm want=$want got=$got dirty=$dirty"; bad=1; }
done
git submodule status | sed 's/^/  /'
echo "verify rc=$bad"
exit $bad

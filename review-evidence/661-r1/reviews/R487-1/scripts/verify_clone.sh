#!/usr/bin/env bash
# Verify a checkout is at the exact head: HEAD, tree, clean status, index == HEAD tree, every tracked
# blob's bytes and mode equal the head tree's, and the three submodule gitlinks checked out at their pins.
# Usage: verify_clone.sh <repo> <head-sha> <tree-sha>
set -eu
cd "$1"; head=$2; tree=$3; rc=0
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD ok $head" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && echo "tree ok $tree" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$tree" ] && echo "index ok (write-tree = head tree)" || { echo "INDEX MISMATCH"; rc=1; }
s=$(git status --porcelain=v1 --ignore-submodules=none); [ -z "$s" ] && echo "status clean" || { echo "STATUS DIRTY:"; echo "$s"; rc=1; }
git diff --quiet HEAD -- && echo "work-tree bytes == HEAD for tracked files" || { echo "WORKTREE DIFF"; rc=1; }
n=$(git ls-files -s | awk '$1!="160000"' | wc -l)
bad=$(git ls-files -s | awk '$1!="160000"{print $1" "$2" "$4}' | while read -r mode sha path; do
  [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || echo "BLOB $path"
  fm=$( [ -L "$path" ] && echo 120000 || { [ -x "$path" ] && echo 100755 || echo 100644; } ); [ "$fm" = "$mode" ] || echo "MODE $path $fm!=$mode"
done)
[ -z "$bad" ] && echo "all $n tracked blobs rehashed and modes match" || { echo "$bad"; rc=1; }
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}'); got=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain | wc -l)
  [ "$want" = "$got" ] && [ "$dirty" = 0 ] && echo "gitlink ok $sm $got clean" || { echo "GITLINK $sm want=$want got=$got dirty=$dirty"; rc=1; }
done
exit $rc

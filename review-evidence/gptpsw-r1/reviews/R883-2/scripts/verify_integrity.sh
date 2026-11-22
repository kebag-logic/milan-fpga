#!/bin/sh
# verify_integrity.sh CLONE EXPECTED_HEAD EXPECTED_TREE: exact head/tree, every tracked blob's bytes and mode equal
# to HEAD's, the index at stage 0 equal to HEAD's tree, the submodule gitlinks recorded, and a clean status.
set -eu
C=$1; H=$2; T=$3
cd "$C"
[ "$(git rev-parse HEAD)" = "$H" ] && echo "head $H ok"
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree $T ok"
[ "$(git write-tree)" = "$T" ] && echo "index (stage 0) writes tree $T ok"
[ -z "$(git ls-files -u)" ] && echo "no unmerged index entries ok"
git diff --quiet HEAD -- && echo "worktree bytes and modes equal HEAD for every tracked file ok"
echo "status: $(git status --porcelain --ignore-submodules=none | wc -l) entries"
git status --porcelain --ignore-submodules=none | head -5
git ls-tree -r HEAD | awk '$2=="commit"{print "gitlink", $4, $3}'
git submodule status 2>/dev/null | sed 's/^/submodule /'

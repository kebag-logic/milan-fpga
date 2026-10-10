#!/usr/bin/env bash
# Merge-commit checks for PR #706 (issue #696). Read-only except that
# `git merge-tree --write-tree` stores tree objects in the object database.
# Usage: merge_check.sh <repo>
set -u
cd "$1"
BASE=6aa25dec977c6ad78bf4ff6275de47fb81d0c246   # source base (dev)
LANE=39571196045ddcc881f9ad0957742537175441d6   # lane head before the merge
DEV=8b61b70902f3ebf118e56967277e2686731081bd    # merged dev
MERGE=0df486370990fddf9b60096be2f2371150692a10  # merge commit
HEAD_SHA=030eb98a12685a2ca41cf8d785bb0eb69dc32a98

echo "## merge parents: $(git log -1 --format=%P $MERGE)"
echo "## automatic merge of the two parents (conflicts would make rc != 0)"
auto=$(git merge-tree --write-tree "$LANE" "$DEV"); echo "rc=$? auto_tree=$auto"
echo "recorded merge tree=$(git rev-parse $MERGE^{tree})"
[ "$auto" = "$(git rev-parse $MERGE^{tree})" ] && echo "MERGE TREE == AUTOMATIC MERGE: yes" || echo "MERGE TREE == AUTOMATIC MERGE: NO"

norm() { git diff --no-ext-diff --no-textconv --no-renames "$1" "$2" | grep -v '^index ' |
         sed -E 's/^@@ -[0-9]+(,[0-9]+)? \+[0-9]+(,[0-9]+)? @@/@@ HUNK @@/'; }
a=$(norm $DEV $MERGE | sha256sum | cut -d' ' -f1)
b=$(norm $BASE $LANE | sha256sum | cut -d' ' -f1)
echo "## lane diff over dev ($DEV..$MERGE), hunk positions normalised: $a"
echo "## lane diff over base ($BASE..$LANE), hunk positions normalised: $b"
[ "$a" = "$b" ] && echo "LANE DIFF IDENTICAL OVER DEV AND OVER BASE: yes" || echo "LANE DIFF IDENTICAL: NO"
echo "## files in the lane diff over dev"
git diff --name-only $DEV $MERGE
echo "## files changed after the merge (merge..head)"
git diff --name-only $MERGE $HEAD_SHA
echo "## gitlinks: head vs dev"
h=$(git ls-tree $HEAD_SHA external gptp-processor protocol-processor third_party/lwSRP third_party/verilog-axis | sha256sum | cut -c1-16)
d=$(git ls-tree $DEV external gptp-processor protocol-processor third_party/lwSRP third_party/verilog-axis | sha256sum | cut -c1-16)
echo "head=$h dev=$d $([ $h = $d ] && echo EQUAL || echo DIFFER)"

#!/usr/bin/env bash
# P1: merge reconstruction, findings-index rows, gitlinks. Run from the review clone.
set -u
OURS=1f039cfe86d5337f5c9b7248696dba1c4bdda67e
DEV=b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a
MERGE=9f94b246bc714e76e52a3dab3d4be4cd7bf3ca67
HEAD_=4c2a30debb031595b81c5c4bfc53b601a0fec528
echo "merge parents: $(git log -1 --format=%P $MERGE)"
echo "merge-base: $(git merge-base $OURS $DEV)"
AUTO=$(git merge-tree --write-tree $OURS $DEV 2>/dev/null | head -1)
echo "auto-merge tree: $AUTO"
echo "files differing between auto-merge tree and merge commit:"; git diff --name-only $AUTO $MERGE
echo "files differing between merge commit and head:"; git diff --name-only $MERGE $HEAD_
rows() { git show "$1:docs/findings/README.md" | grep '^| \[' ; }
B=$(git merge-base $OURS $DEV)
for r in B OURS DEV MERGE HEAD_; do eval rev=\$$r; echo "== rows($r)"; rows $rev | sed -E 's/^\| \[([^]]*)\].*/\1/' ; done
echo "== duplicate link targets in merge:"; rows $MERGE | sed -E 's/^\| \[[^]]*\]\(([^)]*)\).*/\1/' | sort | uniq -d
echo "== ours rows missing byte-exact from merge (expect only the 397 row replaced by... none):"
comm -23 <(rows $OURS | sort) <(rows $MERGE | sort)
echo "== dev rows missing byte-exact from merge (expect dev's old 397 row only):"
comm -23 <(rows $DEV | sort) <(rows $MERGE | sort)
echo "== merge rows found in neither side:"
comm -23 <(rows $MERGE | sort) <(cat <(rows $OURS) <(rows $DEV) | sort -u)
echo "== gitlinks"
for c in $DEV $MERGE $HEAD_; do git ls-tree $c protocol-processor gptp-processor third_party/verilog-axis external | awk -v c=${c:0:8} '{print c, $3, $4}'; done

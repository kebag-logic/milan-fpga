#!/usr/bin/env bash
# Reproduce the delta checks of R714-3 in a clone of kebag-logic/milan-fpga that has
# e0bb857a, 1a635a4c, f58d049b and 5527a9c6. Usage: verify_delta.sh <clone>
set -eu
cd "$1"
PREV=e0bb857a9f4b8e9d29736970a1135afde03260c5
BASE=1a635a4cf9dce5095be624f0265fc1002a60ec59
S2=f58d049beb377c3f535628067022d4d5b51e8208
MERGE=10d8df9825
HEAD_=5527a9c66716331fd06285f428ea1a653c526ada
echo "recomputed merge tree: $(git merge-tree --write-tree $PREV $BASE)"
echo "recorded merge tree:   $(git rev-parse $MERGE^{tree})"
if diff <(git diff $S2 $PREV | grep -vE '^(index |@@ )') <(git diff $BASE $MERGE | grep -vE '^(index |@@ )') >/dev/null; then
  echo "lane diff identical across the merge (ignoring index and hunk-offset lines)"; else echo "lane diff DIFFERS"; fi
echo "files changed $PREV..$HEAD_ outside the base merge:"; git diff --name-only $MERGE $HEAD_
echo "PR diff file count against $BASE: $(git diff --name-only $BASE $HEAD_ | wc -l)"
sed -n 5,8p docs/reference/FR_NFR.md
sed -n 321p docs/reference/FR_NFR.md | cut -c1-260

#!/bin/sh
# Re-run the merge-delta checks of round R732-7 from a clone of kebag-logic/milan-fpga.
# Usage: sh merge_delta_checks.sh <clone>   (needs origin/dev fetched at e5b8405d)
set -u
cd "$1" || exit 2
H=455a3953bf49efda23be4e73447a25b66a5c4bf7
echo "tree head=$(git rev-parse $H^{tree}) 86a349d5=$(git rev-parse 86a349d5^{tree}) cbc7c604=$(git rev-parse cbc7c604^{tree})"
echo "parents: $(git log -1 --format=%P $H)"
echo "bases(head,dev):"; git merge-base --all $H e5b8405db4c1f7cbdafb5df92b15b580142e0232
echo "bases(86a349d5,dev):"; git merge-base --all 86a349d5 e5b8405db4c1f7cbdafb5df92b15b580142e0232
echo "merge-tree: $(git merge-tree --write-tree 86a349d5 e5b8405db4c1f7cbdafb5df92b15b580142e0232)"
echo "message lines: $(git log -1 --format=%B $H | sed '/^$/d' | wc -l)"

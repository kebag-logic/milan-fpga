#!/bin/sh
# Reproduce the R582-5 merge-provenance receipts from any clone holding the
# three commits. Usage: merge_provenance.sh <repo>   (read-only; prints to stdout)
set -eu
repo=${1:?repo}
HEAD_C=7032bca5a51d8d97fcb73d7fc106ca4af21de38e
LANE=6b4feeca5d2fab0ec35cf071322cc775a5b15cb5
DEV=fa7347fc59173f90e4feec2df207692e6e6e72ec
g() { git -C "$repo" "$@"; }
echo "head $HEAD_C tree $(g rev-parse "$HEAD_C^{tree}")"
echo "parents: $(g log -1 --format=%P "$HEAD_C")"
echo "merge-tree(lane,dev): $(g merge-tree --write-tree "$LANE" "$DEV" | head -1)"
echo "merge-base(lane,dev): $(g merge-base "$LANE" "$DEV")"
echo "## head vs dev paths == lane paths (base..lane)"
base=$(g merge-base "$LANE" "$DEV")
if [ "$(g diff --name-only "$DEV" "$HEAD_C")" = "$(g diff --name-only "$base" "$LANE")" ]; then
    echo "IDENTICAL ($(g diff --name-only "$base" "$LANE" | wc -l) paths)"
else
    echo "DIFFERENT"
fi
echo "## provenance of each path the merge changed relative to the lane parent"
g diff --name-only "$LANE" "$HEAD_C" | while read -r p; do
    h=$(g rev-parse "$HEAD_C:$p" 2>/dev/null || echo none)
    l=$(g rev-parse "$LANE:$p" 2>/dev/null || echo none)
    d=$(g rev-parse "$DEV:$p" 2>/dev/null || echo none)
    if [ "$h" = "$d" ]; then s=dev; elif [ "$h" = "$l" ]; then s=lane; else s=THREE-WAY; fi
    echo "$s $p"
done
echo "## gitlinks"
for c in "$base" "$LANE" "$DEV" "$HEAD_C"; do
    echo "$c"
    g ls-tree -r "$c" | awk '$2=="commit"'
done

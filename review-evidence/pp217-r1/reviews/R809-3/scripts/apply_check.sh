#!/bin/sh
# Usage: apply_check.sh <repo> <commit> <work-dir>
# git apply --check of every tracked *.patch against the commit's own tree (repo root).
set -u
repo=$1; c=$2; w=$3
rm -rf "$w"; mkdir -p "$w"; git -C "$repo" archive "$c" | tar -x -C "$w"
cd "$w" || exit 2
n=0; bad=0
for p in $(git -C "$repo" ls-tree -r --name-only "$c" | grep '\.patch$'); do
  n=$((n+1))
  if ! git apply --check "$p" 2>/dev/null; then echo "DOES NOT APPLY: $p"; bad=$((bad+1)); fi
done
echo "commit $(git -C "$repo" rev-parse "$c"): $n tracked patches, $bad do not apply"
[ "$bad" -eq 0 ]

#!/bin/bash
# Usage: merge_base_side.sh <repo> <old_base> <branch_tip> <new_base> <merge>
# The base side: for every file the base changed (old_base..new_base), the merge's
# diff from the branch tip must carry the same hunk bodies (line numbers stripped).
set -u
R=$1; OB=$2; BT=$3; NB=$4; M=$5
cd "$R" || exit 2
body() { git diff -U0 "$1" "$2" -- "$3" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) '; }
same=0; differ=0
for f in $(git diff --name-only "$OB" "$NB"); do
  if [ "$(body "$OB" "$NB" "$f" | sha256sum)" = "$(body "$BT" "$M" "$f" | sha256sum)" ]; then
    same=$((same+1)); else differ=$((differ+1)); echo "DIFFER $f"; fi
done
echo "base-side files: $same same, $differ differ"
echo "submodule gitlinks at merge vs new base:"; git diff --raw "$NB" "$M" | awk '$2=="160000"||$1==":160000"' 
[ "$differ" = 0 ]

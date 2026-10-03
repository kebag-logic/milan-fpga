#!/usr/bin/env bash
# git apply --check every tracked *.patch against a commit, in a throwaway worktree-free index.
# usage: check_patches_apply.sh <repo> <commit> <scratchdir>
set -u
repo=$1 rev=$2 S=$3
rm -rf "$S"; mkdir -p "$S"; git -C "$repo" archive "$rev" | tar -x -C "$S"
cd "$S"; ok=0; bad=0
while IFS= read -r p; do
  if git apply --check -p1 "$p" 2>/dev/null; then ok=$((ok+1)); echo "APPLY $p"; else bad=$((bad+1)); echo "FAIL  $p"; fi
done < <(git -C "$repo" ls-tree -r --name-only "$rev" | grep '\.patch$')
echo "applies: $ok, fails: $bad, total: $((ok+bad))"

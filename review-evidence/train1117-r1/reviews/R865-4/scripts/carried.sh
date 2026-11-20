#!/usr/bin/env bash
# Reviewer probe: a merged PR's delta carried line for line. carried.sh <repo> <pr-base> <pr-head> <merge>
# For each file the PR changes: the blob at the merge equals the PR head's where the merge's first parent left the
# file as the PR's base had it; elsewhere (a shared file) every line the PR added is in the merge's file and every line
# the first parent added (against the PR's base) is too.
set -u
cd "$1"; B=$2; H=$3; M=$4; P=$(git rev-parse "$M^1")
for f in $(git diff --name-only "$B" "$H"); do
  if [ "$(git rev-parse -q --verify "$B:$f" 2>/dev/null)" = "$(git rev-parse -q --verify "$P:$f" 2>/dev/null)" ]; then
    [ "$(git rev-parse -q --verify "$H:$f" 2>/dev/null)" = "$(git rev-parse -q --verify "$M:$f" 2>/dev/null)" ] && echo "EQUAL  $f" || echo "DIFFER $f"
  else
    miss=0
    for side in "$H" "$P"; do
      while IFS= read -r l; do
        git show "$M:$f" | grep -qxF -- "$l" || { miss=$((miss+1)); echo "  missing from $side: $l" | cut -c1-160; }
      done < <(git diff "$B" "$side" -- "$f" | grep '^+' | grep -v '^+++' | sed 's/^+//' | grep -v '^\s*$')
    done
    echo "SHARED $f missing=$miss"
  fi
done

#!/bin/sh
# Usage: check_patches_apply.sh <repo-worktree-at-head>; git apply --check on every tracked patch.
cd "$1" || exit 2
ok=0; bad=0
for p in $(git ls-files | grep -E '\.(patch|diff)$'); do
  if git apply --check "$p" 2>/dev/null; then ok=$((ok+1)); else bad=$((bad+1)); echo "FAIL $p"; fi
done
echo "apply_ok=$ok apply_fail=$bad"; [ "$bad" -eq 0 ]

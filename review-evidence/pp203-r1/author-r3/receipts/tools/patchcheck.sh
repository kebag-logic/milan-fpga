#!/bin/bash
# patchcheck.sh TREE: git apply --check every mutation patch under TREE/tb against TREE
cd "$1" || exit 2
bad=0; n=0
while IFS= read -r p; do
  n=$((n+1))
  if ! git apply --check "$p" 2>/dev/null; then echo "DOES NOT APPLY: $p"; bad=$((bad+1)); fi
done < <(find tb -name '*.patch' | sort)
echo "patches: $n, not applying: $bad"
[ "$bad" -eq 0 ]

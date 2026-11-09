#!/usr/bin/env bash
# Every tracked mutation patch under tb/ must apply to the head tree it plants into.
# patch_census.sh TREE  (TREE: an exported head tree; nothing is modified, --check only)
cd "$1" || exit 2
total=0; bad=0
while IFS= read -r p; do
  total=$((total + 1))
  if ! git apply --check -p1 "$p" >/dev/null 2>&1; then
    echo "DOES NOT APPLY: $p"; bad=$((bad + 1))
  fi
done < <(find tb -name '*.patch' | sort)
echo "patches: $total tracked, $bad do not apply"
[ "$bad" -eq 0 ]

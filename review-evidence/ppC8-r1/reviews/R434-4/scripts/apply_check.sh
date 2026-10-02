#!/usr/bin/env bash
# git apply --check every tracked campaign patch against a clean tree at the
# tree's HEAD. Usage: apply_check.sh <clean clone>
set -u
tree=${1:?clean clone}
cd "$tree" || exit 2
echo "head $(git rev-parse HEAD)"
ok=0; bad=0
for dir in $(git ls-files '*.patch' | xargs -n1 dirname | sort -u); do
  n=0; f=0
  for p in $(git ls-files "$dir/*.patch"); do
    n=$((n + 1))
    if git apply --check "$p" 2>/dev/null; then ok=$((ok + 1)); else f=$((f + 1)); bad=$((bad + 1)); echo "FAIL $p"; fi
  done
  echo "$dir: $n patches, $f failing"
done
echo "total ok=$ok bad=$bad"
[ "$bad" -eq 0 ]

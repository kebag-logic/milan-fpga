#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer receipt: prove the review clone holds the exact published head bytes.
# Usage: verify_clone_restored.sh <clone> <expected-head> <expected-tree>
set -uo pipefail
cd "$1" || exit 2
head=$2; tree=$3; bad=0
echo "HEAD $(git rev-parse HEAD)"; [ "$(git rev-parse HEAD)" = "$head" ] || bad=1
echo "HEAD^{tree} $(git rev-parse 'HEAD^{tree}')"; [ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] || bad=1
# the index equals the head tree (modes and blob ids)
itree=$(git write-tree); echo "index tree $itree"; [ "$itree" = "$tree" ] || bad=1
# every tracked file's bytes and mode equal the index (hash from disk, not the stat cache)
git update-index -q --really-refresh >/dev/null 2>&1
mism=0
while IFS= read -r -d '' line; do
  meta=${line%%$'\t'*}; path=${line#*$'\t'}
  mode=$(echo "$meta" | cut -d' ' -f1); blob=$(echo "$meta" | cut -d' ' -f2)
  [ "$mode" = 160000 ] && { echo "gitlink $path $blob"; continue; }
  disk=$(git hash-object --no-filters -- "$path" 2>/dev/null || echo missing)
  if [ "$disk" != "$blob" ]; then echo "BYTES DIFFER $path"; mism=$((mism + 1)); fi
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE DIFFERS $path"; mism=$((mism + 1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE DIFFERS $path"; mism=$((mism + 1)); fi
done < <(git ls-files -s -z)
echo "tracked files checked: $(git ls-files | wc -l), mismatches: $mism"
[ "$mism" -eq 0 ] || bad=1
echo "gitlinks in tree: $(git ls-files -s | awk '$1==160000' | wc -l)"
echo "status (tracked):"; git status --porcelain --untracked-files=no
[ -z "$(git status --porcelain --untracked-files=no)" ] || bad=1
echo "untracked, not ignored:"; git status --porcelain | grep '^??' || echo "(none)"
echo "VERDICT $([ $bad -eq 0 ] && echo RESTORED || echo NOT-RESTORED)"
exit $bad

#!/bin/sh
# Verify the review clone is at the exact head with clean tracked bytes,
# modes, index and the required submodule gitlinks/checkouts.
# Usage: verify_clone.sh <clone dir> <expected head> <expected tree>
set -eu
repo=$1; head=$2; tree=$3
cd "$repo"
echo "head:  $(git rev-parse HEAD)"
echo "tree:  $(git rev-parse 'HEAD^{tree}')"
test "$(git rev-parse HEAD)" = "$head"
test "$(git rev-parse 'HEAD^{tree}')" = "$tree"
# index tree equals HEAD tree (no staged change)
echo "index: $(git write-tree)"
test "$(git write-tree)" = "$tree"
# no hidden index flags (assume-unchanged h / skip-worktree S)
flags=$(git ls-files -v | grep -c -v '^H ' || true)
echo "non-H index flags: $flags"
test "$flags" = "0"
# tracked worktree bytes and modes vs index (refresh first)
git update-index -q --really-refresh >/dev/null 2>&1 || true
if git diff --quiet --no-ext-diff && git diff --cached --quiet --no-ext-diff; then
  echo "tracked bytes/modes: clean"
else
  echo "tracked bytes/modes: DIRTY"; git diff --stat; exit 1
fi
echo "untracked, not ignored:"; git ls-files --others --exclude-standard | sed 's/^/  /'
for sm in gptp-processor protocol-processor third_party/verilog-axis; do
  pin=$(git ls-files -s "$sm" | awk '$1=="160000" && $3=="0" {print $2}')
  at=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain --untracked-files=no | wc -l)
  echo "submodule $sm gitlink=$pin checkout=$at dirty_tracked=$dirty"
  test "$pin" = "$at"; test "$dirty" = "0"
done
echo "VERIFY OK"

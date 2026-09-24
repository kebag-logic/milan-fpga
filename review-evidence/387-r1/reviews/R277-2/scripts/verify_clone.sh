#!/bin/sh
# Record the review clone's identity: HEAD, tree, index digest, tracked
# blob bytes and modes against HEAD, untracked/modified status and the
# required submodule gitlinks with their checked-out commits.
# Usage: verify_clone.sh <clone>   (exit 0 only when everything matches HEAD)
set -eu
clone=${1:?usage: verify_clone.sh <clone>}
expect_head=021b2e07b009158bcb0ce19529126eb1d330bba5
expect_tree=a7ffb35beea95d5bba593029f382e8c0ab0b1c27
cd "$clone"
status=0
head=$(git rev-parse HEAD)
tree=$(git rev-parse 'HEAD^{tree}')
echo "head $head"
echo "tree $tree"
[ "$head" = "$expect_head" ] || { echo "MISMATCH head"; status=1; }
[ "$tree" = "$expect_tree" ] || { echo "MISMATCH tree"; status=1; }
# index entries (mode, blob, stage, path) against HEAD's tree entries
idx=$(git ls-files -s | sha256sum | cut -d' ' -f1)
lstree=$(git ls-tree -r HEAD | awk '{print $1" "$3" 0\t"$4}' | sha256sum | cut -d' ' -f1)
echo "index-digest $idx"
echo "head-tree-as-index-digest $lstree"
[ "$idx" = "$lstree" ] || { echo "MISMATCH index vs HEAD tree"; status=1; }
# working-tree bytes and modes: re-hash every tracked regular file
if ! git diff --quiet HEAD --; then echo "MISMATCH working tree differs from HEAD"; git diff --stat HEAD -- | tail -5; status=1; fi
porcelain=$(git status --porcelain=v1 --ignore-submodules=none | wc -l)
echo "porcelain-lines $porcelain"
[ "$porcelain" -eq 0 ] || { git status --porcelain=v1 --ignore-submodules=none | head -20; status=1; }
# explicit per-blob rehash (catches a stale stat cache)
bad=0
git ls-files -s | while read -r mode blob _stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    actual=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    actual=$(git hash-object --no-filters "$path")
    if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE $path"; fi
    if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE $path"; fi
  fi
  [ "$actual" = "$blob" ] || echo "BLOB $path"
done > /tmp/verify_clone.$$ 2>&1 || true
bad=$(wc -l < /tmp/verify_clone.$$)
cat /tmp/verify_clone.$$; rm -f /tmp/verify_clone.$$
echo "blob-or-mode-mismatches $bad"
[ "$bad" -eq 0 ] || status=1
for s in external gptp-processor protocol-processor third_party/verilog-axis; do
  link=$(git ls-tree HEAD "$s" | awk '{print $3}')
  if [ -e "$s/.git" ]; then
    co=$(git -C "$s" rev-parse HEAD)
    dirty=$(git -C "$s" status --porcelain | wc -l)
  else
    co=uninitialised; dirty=0
  fi
  echo "submodule $s gitlink $link checkout $co dirty $dirty"
  if [ "$co" != uninitialised ] && { [ "$co" != "$link" ] || [ "$dirty" -ne 0 ]; }; then status=1; fi
done
for s in gptp-processor protocol-processor third_party/verilog-axis; do
  [ -e "$s/.git" ] || { echo "REQUIRED submodule $s not initialised"; status=1; }
done
echo "verdict $([ $status -eq 0 ] && echo MATCH || echo MISMATCH)"
exit $status

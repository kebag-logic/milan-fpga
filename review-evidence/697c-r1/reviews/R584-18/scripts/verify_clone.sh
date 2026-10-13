#!/usr/bin/env bash
# verify_clone.sh <repo> <head>: prove the review clone holds exactly <head>'s tracked bytes,
# modes and index, no untracked or ignored leftovers from the probes, and every
# initialised submodule at its gitlink with a clean tree.
set -u
repo=$1; head=$2
cd "$repo" || exit 2
rc=0
echo "HEAD=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD differs"; rc=1; }
# index equals HEAD's tree, entry for entry (mode, blob, path)
if diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') > /dev/null; then
  echo "index == HEAD tree: $(git ls-files | wc -l) entries"; else echo "index differs from HEAD"; rc=1; fi
# working tree bytes equal the index (hash every tracked regular file and symlink from disk)
git ls-files -s | awk '$1 != "160000" {print $2, $4}' | while read -r blob path; do
  if [ -L "$path" ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); else got=$(git hash-object --no-filters -- "$path"); fi
  [ "$got" = "$blob" ] || echo "BYTES DIFFER: $path"
done > /tmp/r584-verify-bytes.$$
if [ -s /tmp/r584-verify-bytes.$$ ]; then cat /tmp/r584-verify-bytes.$$; rc=1; else echo "tracked bytes == index blobs (hashed from disk, no filters)"; fi
rm -f /tmp/r584-verify-bytes.$$
# modes on disk (executable bit) equal the index
git ls-files -s | awk '$1 == "100755" || $1 == "100644" {print $1, $4}' | while read -r mode path; do
  if [ -x "$path" ]; then [ "$mode" = 100755 ] || echo "MODE: $path is executable, index $mode"; else [ "$mode" = 100644 ] || echo "MODE: $path not executable, index $mode"; fi
done | head -20
echo "status --porcelain --ignored (excluding uninitialised submodule dirs):"
git status --porcelain --ignored | sed 's/^/  /'
echo "submodules:"
git submodule status
for sm in third_party/lwSRP third_party/tsn-c-stack; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}'); got=$(git -C "$sm" rev-parse HEAD 2>/dev/null || echo none)
  dirty=$(git -C "$sm" status --porcelain --ignored 2>/dev/null | wc -l)
  echo "  $sm gitlink=$want checkout=$got dirty_entries=$dirty"
  [ "$want" = "$got" ] && [ "$dirty" = 0 ] || rc=1
done
echo "verify rc=$rc"
exit $rc

#!/usr/bin/env bash
# verify_clone.sh <repo> <head>: prove the review clone holds exactly <head>'s tracked bytes,
# modes and index, no untracked or ignored leftovers from the probes, and every
# initialised submodule at its gitlink with a clean tree (tracked bytes, index, no extras).
set -u
repo=$1; head=$2
cd "$repo" || exit 2
rc=0
tmp=$(mktemp)
echo "HEAD=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD differs"; rc=1; }
if diff <(git ls-files -s | awk '{print $1, $2, $3, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, 0, $4}') > /dev/null; then
  echo "index == HEAD tree (mode, blob, stage 0, path): $(git ls-files | wc -l) entries"; else echo "index differs from HEAD"; rc=1; fi
git ls-files -s | awk '$1 != "160000" {print $1, $2, $4}' | while read -r mode blob path; do
  if [ -L "$path" ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); [ "$mode" = 120000 ] || echo "MODE: $path is a symlink, index $mode"
  else got=$(git hash-object --no-filters -- "$path")
    if [ -x "$path" ]; then [ "$mode" = 100755 ] || echo "MODE: $path executable, index $mode"; else [ "$mode" = 100644 ] || echo "MODE: $path not executable, index $mode"; fi
  fi
  [ "$got" = "$blob" ] || echo "BYTES DIFFER: $path"
done > "$tmp"
if [ -s "$tmp" ]; then cat "$tmp"; rc=1; else echo "tracked bytes and modes == index (hashed from disk, no filters)"; fi
st=$(git status --porcelain --ignored)
echo "status --porcelain --ignored: ${st:-<empty>}"
[ -z "$st" ] || rc=1
echo "submodules:"; git submodule status
for sm in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}'); got=$(git -C "$sm" rev-parse HEAD 2>/dev/null || echo none)
  dirty=$(git -C "$sm" status --porcelain --ignored 2>/dev/null | wc -l)
  idx=$(git -C "$sm" diff --cached --quiet HEAD 2>/dev/null && echo clean || echo DIFFERS)
  echo "  $sm gitlink=$want checkout=$got status_entries=$dirty index=$idx"
  [ "$want" = "$got" ] && [ "$dirty" = 0 ] && [ "$idx" = clean ] || rc=1
done
rm -f "$tmp"
echo "verify rc=$rc"
exit $rc

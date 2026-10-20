#!/bin/sh
# Verify a review clone is byte-exact at its head: index == HEAD tree (paths, modes, ids),
# every tracked file re-hashed equal to its index blob, no skip/assume flags, nothing
# untracked or ignored, and the required submodule gitlinks.
# Usage: clone_integrity.sh <clone> <expected-head>
set -u
cd "$1" || exit 9
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$2" ] && echo "head matches" || { echo "HEAD MISMATCH"; exit 1; }
diff <(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}') <(git ls-files -s | awk '{print $1, $2, $4}') > /dev/null && echo "index == HEAD tree (modes, ids, paths)" || { echo "INDEX DIFFERS"; exit 1; }
flags=$(git ls-files -v | grep -vc '^H ')
echo "entries with non-H flags (skip/assume): $flags"
bad=0; n=0
git ls-files -s | while read -r mode id stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then h=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else h=$(git hash-object --no-filters -- "$path"); fi
  [ "$h" = "$id" ] || echo "BLOB DIFFERS $path"
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE DIFFERS $path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE DIFFERS $path"; fi
done > /tmp/ci_$$.txt
echo "blob/mode differences: $(wc -l < /tmp/ci_$$.txt)"; cat /tmp/ci_$$.txt; rm -f /tmp/ci_$$.txt
echo "tracked blobs: $(git ls-files -s | grep -vc '^160000')"
echo "untracked/ignored entries: $(git status --porcelain --ignored | wc -l)"
git status --porcelain --ignored
git submodule status

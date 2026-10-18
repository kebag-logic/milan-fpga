#!/bin/sh
# Verify a clone is byte-exact at an expected head: HEAD/tree, index entries
# equal the HEAD tree (modes + blob ids), every tracked file's working bytes
# hash to its blob, no untracked/modified files, and list gitlinks.
# Usage: verify_clone.sh REPO HEAD TREE
set -e
cd "$1"
[ "$(git rev-parse HEAD)" = "$2" ] && echo "HEAD ok $2"
[ "$(git rev-parse HEAD^{tree})" = "$3" ] && echo "tree ok $3"
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/.vc_tree.$$
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/.vc_index.$$
cmp -s /tmp/.vc_tree.$$ /tmp/.vc_index.$$ && echo "index == HEAD tree ($(wc -l < /tmp/.vc_index.$$) entries)"
bad=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && { echo "gitlink $path $blob"; continue; }
  if [ "$mode" = 120000 ]; then h=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); else h=$(git hash-object "$path"); fi
  [ "$h" = "$blob" ] || { echo "BYTES DIFFER $path"; exit 1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE $path"; exit 1; }; fi
  if [ "$mode" = 100644 ]; then [ ! -x "$path" ] || { echo "MODE $path"; exit 1; }; fi
done && echo "working bytes and modes == blobs"
echo "status: $(git status --porcelain --ignored | wc -l) entries"; git status --porcelain --ignored
rm -f /tmp/.vc_tree.$$ /tmp/.vc_index.$$

#!/bin/sh
# Verify a review clone is exactly the published head: HEAD, tree, index
# records equal to the commit tree (mode, blob, stage 0), every tracked
# worktree file re-hashing to its blob, no untracked or ignored residue,
# and the submodule gitlinks recorded in the tree.
# Usage: verify_clone.sh <clone> <expected-head> <expected-tree>
set -eu
cd "$1"
echo "HEAD $(git rev-parse HEAD) expect $2"
echo "TREE $(git rev-parse 'HEAD^{tree}') expect $3"
[ "$(git rev-parse HEAD)" = "$2" ] && [ "$(git rev-parse 'HEAD^{tree}')" = "$3" ]
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/.vc_tree.$$
git ls-files -s | awk '{print $1, $2, $3, $4}' > /tmp/.vc_idx_raw.$$
awk '$3 != 0 {bad=1} END {exit bad}' /tmp/.vc_idx_raw.$$ && echo "index: all stage 0"
awk '{print $1, $2, $4}' /tmp/.vc_idx_raw.$$ | sort > /tmp/.vc_idx.$$
if cmp -s /tmp/.vc_tree.$$ /tmp/.vc_idx.$$; then echo "index == HEAD tree ($(wc -l < /tmp/.vc_idx.$$) records)"; else echo "INDEX DIFFERS"; exit 1; fi
# worktree bytes: hash every regular tracked file directly (no index stat cache)
bad=0
git ls-files -s | awk '$1 != "160000" {print $2 "\t" $4}' > /tmp/.vc_files.$$
cut -f2 /tmp/.vc_files.$$ | git hash-object --no-filters --stdin-paths > /tmp/.vc_hash.$$
paste /tmp/.vc_files.$$ /tmp/.vc_hash.$$ | awk -F'\t' '$1 != $3 {print "MISMATCH " $2; b=1} END {exit b}' || bad=1
git ls-files -s | awk '$1 == "120000" {print $4}' | while read -r l; do [ -L "$l" ] || { echo "NOT SYMLINK $l"; exit 1; }; done
git ls-files -s | awk '$1 == "100755" {print $4}' | while read -r x; do [ -x "$x" ] || { echo "MODE $x"; exit 1; }; done
git ls-files -s | awk '$1 == "100644" {print $4}' | while read -r x; do [ -L "$x" ] || [ ! -x "$x" ] || { echo "MODE $x"; exit 1; }; done
[ $bad = 0 ] && echo "worktree blobs: $(wc -l < /tmp/.vc_files.$$) files re-hash to their blobs; modes match"
echo "untracked/ignored residue:"; git status --porcelain=v1 --untracked-files=all --ignored | sed 's/^/  /'
[ -z "$(git status --porcelain=v1 --untracked-files=all --ignored)" ] && echo "  (none)"
echo "gitlinks:"; git ls-tree -r HEAD | awk '$1 == "160000"'
echo "submodule status:"; git submodule status 2>&1
rm -f /tmp/.vc_*.$$

#!/usr/bin/env bash
# clone_integrity.sh CLONE EXPECTED_HEAD EXPECTED_TREE: prove a review clone sits
# at the exact head with tracked blob bytes, modes and index unchanged and the
# submodule gitlinks at their pins. Prints a receipt; exits 1 on any mismatch.
set -euo pipefail
clone=$1 want_head=$2 want_tree=$3 bad=0
cd "$clone"
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "head $head"; echo "tree $tree"
[ "$head" = "$want_head" ] || { echo "MISMATCH head"; bad=1; }
[ "$tree" = "$want_tree" ] || { echo "MISMATCH tree"; bad=1; }
# Index entries (mode, blob, stage, path) must equal the commit's tree entries.
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
cmt=$(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
echo "index-entries sha256 $idx"; echo "tree-entries  sha256 $cmt"
[ "$idx" = "$cmt" ] || { echo "MISMATCH index vs tree"; bad=1; }
# Working-tree bytes and modes of every tracked non-gitlink file.
if ! git diff --quiet HEAD --ignore-submodules=all; then echo "MISMATCH worktree bytes/modes"; git diff --stat HEAD --ignore-submodules=all; bad=1; fi
untracked=$(git status --porcelain --ignore-submodules=all | wc -l)
echo "status entries (excluding submodule content) $untracked"
[ "$untracked" -eq 0 ] || { git status --porcelain --ignore-submodules=all; bad=1; }
echo "gitlinks:"; git ls-files -s | awk '$1=="160000"{print "  " $2, $4}'
echo "submodule status:"; git submodule status | sed 's/^/  /'
if [ "$bad" -ne 0 ]; then echo "INTEGRITY: FAIL"; exit 1; fi
echo "INTEGRITY: OK"

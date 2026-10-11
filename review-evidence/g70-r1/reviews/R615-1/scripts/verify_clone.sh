#!/bin/sh
# Verify the review clone still holds exact-head bytes after probes.
#   usage: verify_clone.sh CLONE
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "index-tree $(git write-tree)"
echo "index ls-files -s sha256 $(git ls-files -s | sha256sum | cut -c1-64)"
echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l)"
echo "porcelain (incl. untracked, ignored):"
git status --porcelain --ignored --untracked-files=all
git diff --quiet HEAD && echo "worktree == HEAD (bytes and modes)" || echo "WORKTREE DIFFERS"
# Re-hash every tracked file from disk and compare with the HEAD blob ids.
bad=0
git ls-tree -r HEAD | while read -r mode type oid path; do
  [ "$type" = blob ] || continue
  disk=$(git hash-object --no-filters -- "$path")
  [ "$disk" = "$oid" ] || { echo "BLOB MISMATCH $path"; }
done
echo "blob rehash done"

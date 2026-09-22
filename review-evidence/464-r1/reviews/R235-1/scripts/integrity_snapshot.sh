#!/usr/bin/env bash
# R235 review-checkout integrity snapshot (read-only).
# Usage: integrity_snapshot.sh <checkout> <label>
# Records HEAD, tree, index entries (mode/blob/stage/path), HEAD tree listing
# (mode/kind/blob/path), gitlink (submodule) entries, worktree status and
# untracked/ignored file counts, so a before/after diff proves nothing moved.
set -euo pipefail
repo=${1:?checkout}
label=${2:?label}
out_dir=$(cd "$(dirname "$0")/.." && pwd)/receipts
mkdir -p "$out_dir"
out="$out_dir/integrity-$label.txt"
{
  echo "label: $label"
  echo "head: $(git -C "$repo" rev-parse HEAD)"
  echo "tree: $(git -C "$repo" rev-parse 'HEAD^{tree}')"
  echo "index-ls-files-s-sha256: $(git -C "$repo" ls-files -s | sha256sum | cut -d' ' -f1)"
  echo "index-entry-count: $(git -C "$repo" ls-files -s | wc -l)"
  echo "head-ls-tree-r-sha256: $(git -C "$repo" ls-tree -r --full-tree HEAD | sha256sum | cut -d' ' -f1)"
  echo "head-ls-tree-entry-count: $(git -C "$repo" ls-tree -r --full-tree HEAD | wc -l)"
  echo "index-vs-head-diff: $(git -C "$repo" diff --cached --name-status HEAD | wc -l) entries"
  echo "worktree-vs-index-diff: $(git -C "$repo" diff --name-status | wc -l) entries"
  echo "untracked-count: $(git -C "$repo" ls-files --others --exclude-standard | wc -l)"
  echo "ignored-count: $(git -C "$repo" ls-files --others --ignored --exclude-standard | wc -l)"
  echo "gitlinks (mode 160000):"
  git -C "$repo" ls-files -s | awk '$1=="160000"{print "  "$0}'
  echo "submodule status:"
  git -C "$repo" submodule status --recursive | sed 's/^/  /'
  echo "status --porcelain=v2 --ignored=no:"
  git -C "$repo" status --porcelain=v2 --branch | sed 's/^/  /'
  echo "non-regular-mode entries in index (mode != 100644):"
  git -C "$repo" ls-files -s | awk '$1!="100644"{print "  "$1" "$2" "$4}'
} > "$out"
cat "$out"

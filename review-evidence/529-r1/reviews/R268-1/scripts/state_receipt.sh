#!/bin/sh
# Print a reproducible fingerprint of a checkout: HEAD, tree, index entries
# (mode/blob/stage/path), worktree blob hashes of tracked files, status and
# the three required submodule gitlinks. Usage: state_receipt.sh <checkout>
set -eu
d=$1
cd "$d"
echo "head $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "index_sha256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "index_entries $(git ls-files -s | wc -l)"
echo "index_vs_head_diff $(git diff --cached --name-only | wc -l)"
# hash the bytes on disk of every tracked regular file (not via the index)
git ls-files -s | awk '$1!="160000"{print $4}' | while IFS= read -r p; do
  printf '%s %s\n' "$(git hash-object --no-filters -- "$p")" "$p"
done | sha256sum | sed 's/ .*//; s/^/worktree_blob_list_sha256 /'
git ls-files -s | awk '$1!="160000"{print $2" "$4}' | sha256sum | sed 's/ .*//; s/^/index_blob_list_sha256 /'
echo "modes_sha256 $(git ls-files -s | awk '{print $1, $4}' | sha256sum | cut -d' ' -f1)"
echo "status_porcelain_lines $(git status --porcelain --ignore-submodules=none | wc -l)"
echo "untracked_lines $(git status --porcelain --untracked-files=all | grep -c '^??' || true)"
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  echo "gitlink $s $(git ls-files -s -- "$s" | awk '{print $1, $2, $3}') checkout $(git -C "$s" rev-parse HEAD)"
done
git submodule status | sed 's/^/submodule_status /'

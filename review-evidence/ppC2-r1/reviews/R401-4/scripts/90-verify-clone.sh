#!/usr/bin/env bash
# Verify the review clone still holds the exact head: HEAD, index tree, worktree bytes and modes, gitlinks.
# Usage: 90-verify-clone.sh <repo>
set -euo pipefail
cd "${1:?}"
H=47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346; T=329ff52af9e1f56d408f88182f577f14ed0a7f31
echo "HEAD=$(git rev-parse HEAD) expect $H"; [ "$(git rev-parse HEAD)" = "$H" ]
echo "index tree=$(git write-tree) expect $T"; [ "$(git write-tree)" = "$T" ]
git update-index -q --really-refresh
git diff-index --quiet HEAD -- && echo "worktree+index == HEAD (bytes and modes)"
echo "untracked/ignored-but-present: $(git status --porcelain --ignored | wc -l) entries"; git status --porcelain --ignored | head
n=0; bad=0
while read -r mode type sha path; do
  n=$((n+1)); [ "$(git hash-object "$path")" = "$sha" ] || { echo "BYTES DIFFER $path"; bad=1; }
  case $mode in 100755) [ -x "$path" ] || { echo "MODE $path"; bad=1; };; 100644) [ ! -x "$path" ] || { echo "MODE $path"; bad=1; };; esac
done < <(git ls-tree -r "$H" | awk '$1!="160000"' | tr '\t' ' ')
echo "tracked blobs rehashed: $n, bad=$bad"
echo "gitlinks (160000) in tree: $(git ls-tree -r "$H" | awk '$1=="160000"' | wc -l); .gitmodules present: $([ -e .gitmodules ] && echo yes || echo no)"
exit $bad

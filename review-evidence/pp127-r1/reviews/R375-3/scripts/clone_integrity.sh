#!/bin/sh
# Verify the review clone is byte-exact at the reviewed head: HEAD, tree, index vs
# tree (blob ids and modes), worktree bytes vs index, untracked files, gitlinks.
# usage: clone_integrity.sh <path-to-processor-clone>
set -u
cd "$1"
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
echo "expected HEAD 0404675dcd8788d29cb15a831a8c182438bf1c92 tree 87b2925d9609f9e298ae9a0781dcdd127dcbb1ac"
echo "index-vs-tree diff entries: $(git diff-index --cached HEAD | wc -l)"
echo "worktree-vs-index diff entries (refreshed): $(git update-index -q --really-refresh >/dev/null 2>&1; git diff-files | wc -l)"
echo "untracked+ignored-excluded entries: $(git status --porcelain --untracked-files=all | wc -l)"
bad=0; n=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  h=$(git hash-object --no-filters -- "$path"); [ "$h" = "$blob" ] || echo "BLOB MISMATCH $path"
  m=$(stat -c %a -- "$path"); case "$mode" in 100755) [ "$m" = 755 ] || [ -x "$path" ] || echo "MODE MISMATCH $path";; 100644) [ -x "$path" ] && echo "MODE MISMATCH $path";; 120000) [ -L "$path" ] || echo "LINK MISMATCH $path";; esac
done > /tmp/r375-integrity.$$
echo "tracked files: $(git ls-files | wc -l); blob/mode mismatches: $(wc -l < /tmp/r375-integrity.$$)"; cat /tmp/r375-integrity.$$; rm -f /tmp/r375-integrity.$$
echo "gitlinks (mode 160000) in tree: $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l) (none required by this repository)"

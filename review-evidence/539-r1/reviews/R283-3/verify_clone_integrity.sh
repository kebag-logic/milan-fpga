#!/bin/sh
# Verify the review clone still holds the exact head: HEAD, tree, index,
# every tracked blob's bytes and mode, no untracked or modified files, and
# the required submodule gitlinks.
# Usage: verify_clone_integrity.sh <repo>
set -u
REPO=${1:?repo}
H=324eb343a870973b64706779d0183ae342dcb3d7
TREE=84170bb655b0f547caf7826de541a467db655703
cd "$REPO"
echo "HEAD $(git rev-parse HEAD)"; [ "$(git rev-parse HEAD)" = "$H" ] && echo head_ok
echo "TREE $(git rev-parse HEAD^{tree})"; [ "$(git rev-parse HEAD^{tree})" = "$TREE" ] && echo tree_ok
echo "INDEX_TREE $(git write-tree)"; [ "$(git write-tree)" = "$TREE" ] && echo index_ok
git update-index -q --really-refresh
git diff --quiet HEAD -- && git diff --cached --quiet && echo worktree_and_index_match_head
echo "== porcelain (untracked included, ignored excluded)"
git status --porcelain --untracked-files=all; echo "porcelain_end"
echo "== blob byte/mode check over every tracked non-gitlink path"
bad=0; n=0
git ls-files -s | awk '$1!="160000"' > /tmp/.r283_ls.$$
while read -r mode sha stage path; do
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf %s "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters "$path"); fi
  [ "$got" = "$sha" ] || { echo "BYTES_MISMATCH $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE_MISMATCH $path"; bad=$((bad+1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE_MISMATCH $path"; bad=$((bad+1)); fi
done < /tmp/.r283_ls.$$
rm -f /tmp/.r283_ls.$$
echo "checked=$n mismatches=$bad"
echo "== gitlinks (index vs head)"
git ls-files -s | awk '$1=="160000"{print $2, $4}'
git ls-tree -r "$H" | awk '$1=="160000"{print $3, $4}'
echo "== submodule status"
git submodule status 2>&1
echo "INTEGRITY_DONE"

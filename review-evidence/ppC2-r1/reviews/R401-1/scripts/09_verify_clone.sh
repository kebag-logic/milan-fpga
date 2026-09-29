#!/bin/sh
# Prove the review clone still holds the exact head: HEAD, tree, index, every
# tracked blob's bytes and mode, no untracked/ignored residue, and the gitlink set.
set -u
. "$(dirname "$0")/00_env.sh"
cd "$CLONE" || exit 1
echo "HEAD $(git rev-parse HEAD)  want $HEAD_SHA"
echo "tree $(git rev-parse 'HEAD^{tree}')  want 7916d0854d52eecb28b03ac5e665d05355b7be08"
echo "index-tree $(git write-tree)"
git update-index -q --really-refresh
git diff --quiet HEAD && echo "worktree+index == HEAD: yes" || echo "worktree+index == HEAD: NO"
git diff --cached --quiet && echo "index == HEAD: yes" || echo "index == HEAD: NO"
echo "untracked/ignored entries: $(git status --porcelain --ignored | wc -l)"
# every tracked path: mode + blob hash of the working file vs the head tree
bad=0
git ls-tree -r HEAD | while read -r mode type obj path; do
  [ "$type" = blob ] || continue
  h=$(git hash-object --no-filters -- "$path")
  if [ "$h" != "$obj" ]; then echo "BYTES DIFFER: $path"; fi
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE DIFFERS: $path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE DIFFERS: $path"; fi
done > "$PKT/scratch/verify-diffs.txt"
echo "tracked blob byte/mode mismatches: $(wc -l < "$PKT/scratch/verify-diffs.txt")"
echo "gitlinks (160000) at HEAD: $(git ls-tree -r HEAD | grep -c '^160000') (none required)"
echo "tracked blobs: $(git ls-tree -r HEAD | grep -c ' blob ')"

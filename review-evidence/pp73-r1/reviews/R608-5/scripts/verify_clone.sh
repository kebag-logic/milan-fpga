#!/usr/bin/env bash
# Exact-head integrity of a clone: HEAD, tree, index == HEAD tree (blob ids and
# modes), worktree bytes == index, no untracked or ignored files, gitlinks.
# usage: verify_clone.sh CLONE
set -u
cd "$1" || exit 99
want=4bee75b2e647507a71ece50359fceb135c334757
echo "head: $(git rev-parse HEAD) (want $want)"
echo "tree: $(git rev-parse HEAD^{tree}) (want 6bca4f9099adb67e6ca3758f9738975bba32d2d4)"
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -c1-64)
tree=$(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -c1-64)
echo "index(mode,blob,path) sha256 $idx; HEAD tree $tree; equal=$([ "$idx" = "$tree" ] && echo yes || echo NO)"
git update-index -q --really-refresh >/dev/null 2>&1
git diff --quiet && echo "worktree bytes == index: yes" || echo "worktree bytes == index: NO"
git diff --cached --quiet && echo "index == HEAD: yes" || echo "index == HEAD: NO"
bad=0
while IFS= read -r -d '' line; do
  meta=${line%%$'\t'*}; path=${line#*$'\t'}; mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || { echo "BYTE MISMATCH $path"; bad=1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE MISMATCH $path"; bad=1; }
  elif [ "$mode" = 100644 ]; then [ -x "$path" ] && { echo "MODE MISMATCH $path"; bad=1; }; fi
done < <(git ls-files -s -z)
echo "tracked files: $(git ls-files | wc -l); raw byte/mode re-hash mismatches: $bad"
echo "untracked+ignored entries: $(git status --porcelain --ignored | wc -l)"
echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l)"

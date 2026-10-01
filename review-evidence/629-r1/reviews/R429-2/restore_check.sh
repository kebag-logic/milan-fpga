#!/bin/sh
# Reviewer R429-2: prove the clone is at the exact head with untouched tracked
# bytes, modes and index, and the required submodule gitlinks.
set -u
C=${1:?clone}  # path to the review clone
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "HEAD tree $(git rev-parse HEAD^{tree})"
echo "index tree $(git write-tree)"
echo "status entries (tracked+untracked): $(git status --porcelain --untracked-files=all | wc -l)"
echo "ignored entries: $(git status --porcelain --ignored --untracked-files=all | grep -c '^!!')"
n=0; bad=0
git ls-files -s | while read mode blob stage path; do
  if [ "$mode" = 160000 ]; then continue; fi
  h=$(git hash-object --no-filters -- "$path")
  [ "$h" = "$blob" ] || echo "BLOB MISMATCH $path"
  m=$( [ -x "$path" ] && echo 100755 || echo 100644 )
  [ -L "$path" ] && m=120000
  [ "$m" = "$mode" ] || echo "MODE MISMATCH $path $mode $m"
done
echo "tracked non-gitlink files: $(git ls-files -s | grep -vc '^160000')"
echo "gitlinks:"; git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
echo "submodule status:"; git submodule status
echo "worktrees:"; git worktree list

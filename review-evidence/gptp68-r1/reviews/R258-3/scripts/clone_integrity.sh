#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Prove a review clone still holds the exact head: HEAD and tree ids, a clean
# index and worktree, no assume-unchanged or skip-worktree hiding, every
# tracked file's bytes and mode equal to the blob and mode HEAD records, and
# the gitlink population. Read-only.
#
# usage: clone_integrity.sh <clone> <expected-head> <expected-tree>
set -eu
cd "$1"
export GIT_NO_REPLACE_OBJECTS=1
status=0
head=$(git rev-parse HEAD)
tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "tree $tree"
[ "$head" = "$2" ] || { echo "HEAD MISMATCH"; status=1; }
[ "$tree" = "$3" ] || { echo "TREE MISMATCH"; status=1; }
if [ -n "$(git status --porcelain --ignored=no)" ]; then
  echo "worktree/index NOT clean"; git status --porcelain; status=1
else
  echo "git status: clean"
fi
git diff --quiet && git diff --cached --quiet \
  && echo "diff and cached diff: empty" || { echo "diff not empty"; status=1; }
hidden=$(git ls-files -v | grep -v '^H ' || true)
[ -z "$hidden" ] && echo "ls-files -v: every entry H (no assume-unchanged/skip-worktree)" \
  || { echo "hidden entries:"; echo "$hidden"; status=1; }
# index entries must equal HEAD's tree entries (mode, object, path)
if [ "$(git ls-files -s | awk '{print $1" "$2" "$4}')" = \
     "$(git ls-tree -r HEAD | awk '{print $1" "$3" "$4}')" ]; then
  echo "index == HEAD tree (mode, blob, path) for $(git ls-files | wc -l) entries"
else
  echo "index differs from HEAD tree"; status=1
fi
# bytes on disk: hash every tracked regular file and compare with HEAD's blob
bad=0
git ls-tree -r HEAD | while read -r mode type obj path; do
  case $mode in
    100644|100755)
      got=$(git hash-object --no-filters -- "$path")
      [ "$got" = "$obj" ] || { echo "BYTES DIFFER $path"; exit 1; }
      if [ "$mode" = 100755 ]; then
        [ -x "$path" ] || { echo "MODE DIFFERS $path"; exit 1; }
      else
        [ ! -x "$path" ] || { echo "MODE DIFFERS $path"; exit 1; }
      fi ;;
    *) echo "non-regular entry $mode $path" ;;
  esac
done && echo "every tracked file: bytes == blob, exec bit == mode" \
  || { echo "byte/mode check FAILED"; status=1; }
echo "gitlinks (mode 160000) in HEAD: $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l)"
echo "untracked or ignored files: $(git status --porcelain --ignored | wc -l)"
exit $status

#!/bin/sh
# Usage: verify_restore.sh <repo> <head>
# Confirms HEAD, a clean worktree (tracked and untracked), index entries equal to the head tree, and submodule gitlinks checked out at the recorded commits.
set -u; cd "$1"; H=$2
echo "HEAD=$(git rev-parse HEAD) expected=$H"
echo "porcelain_lines=$(git status --porcelain --untracked-files=all | wc -l)"
a=$(git ls-files -s | awk '{print $1" "$2" "$4}' | sha256sum | cut -c1-64)
b=$(git ls-tree -r --full-tree "$H" | awk '{print $1" "$3" "$4}' | sha256sum | cut -c1-64)
echo "index_vs_tree $( [ "$a" = "$b" ] && echo EQUAL || echo DIFFER )"
git diff --quiet "$H" && echo "worktree_vs_head EQUAL" || echo "worktree_vs_head DIFFER"
git submodule status | cut -c1-41 | sed 's/^-/NOT-INIT /; s/^ /CHECKED-OUT-AT-GITLINK /; s/^+/MISMATCH /'
for m in $(git ls-tree -r "$H" | awk '$2=="commit"{print $4"="$3}'); do echo "gitlink $m"; done

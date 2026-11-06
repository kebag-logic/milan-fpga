#!/bin/sh
# Verify a checkout is exactly the reviewed head: HEAD/tree, clean status (ignored files included), stage-0
# index equal to the head tree, tracked blob bytes and modes, and submodule gitlinks.
# Usage: verify_checkout.sh <checkout> <head sha> <tree sha>
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) expected $2"
echo "tree $(git rev-parse HEAD^{tree}) expected $3"
echo "status (incl. ignored, excluding nothing):"; git status --porcelain=v1 --ignored --untracked-files=all | head -20
echo "status lines: $(git status --porcelain=v1 --ignored --untracked-files=all | wc -l)"
echo "index vs tree:"; git diff-index --cached --quiet HEAD && echo "  index == HEAD tree"
echo "worktree vs index (bytes, modes):"; git diff-files --quiet && echo "  worktree == index"
echo "unmerged/non-stage-0 entries: $(git ls-files -s | awk '$3 != 0' | wc -l)"
echo "index entries: $(git ls-files -s | wc -l)  tree entries: $(git ls-tree -r HEAD | wc -l)"
echo "gitlinks at head:"; git ls-tree -r HEAD | awk '$2 == "commit"'
echo "submodule status:"; git submodule status 2>&1
[ "$(git rev-parse HEAD)" = "$2" ] && [ "$(git rev-parse HEAD^{tree})" = "$3" ] && git diff-index --cached --quiet HEAD \
  && git diff-files --quiet && [ -z "$(git status --porcelain=v1 --untracked-files=all)" ] && echo "CHECKOUT INTACT" || echo "CHECKOUT CHANGED"

#!/bin/sh
# Verify a review clone is byte-exact at the head under review: HEAD and tree, index equal to
# HEAD, worktree equal to index (bytes and modes), no untracked file, and the submodule gitlinks.
# Usage: verify_tree_state.sh <clone> <head> <tree>
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) expected $2"
echo "tree $(git rev-parse HEAD^{tree}) expected $3"
git diff-index --cached --quiet HEAD -- && echo "index == HEAD: yes" || echo "index == HEAD: NO"
git diff-files --quiet && echo "worktree == index (bytes, modes): yes" || echo "worktree == index: NO"
u=$(git ls-files --others --exclude-standard | wc -l); echo "untracked non-ignored files: $u"
i=$(git ls-files --others --ignored --exclude-standard --directory | wc -l); echo "ignored paths: $i"
echo "gitlinks (path, recorded, checked out):"
git ls-files -s | awk '$1 == "160000" {print $4, $2}' | while read p sha; do
  if [ -e "$p/.git" ]; then co=$(git -C "$p" rev-parse HEAD); else co=not-checked-out; fi
  case "$co" in "$sha") s=match;; not-checked-out) s=not-checked-out;; *) s=MISMATCH;; esac
  echo "  $p $sha $co $s"
done
test "$(git rev-parse HEAD)" = "$2" && test "$(git rev-parse HEAD^{tree})" = "$3" \
  && git diff-index --cached --quiet HEAD -- && git diff-files --quiet && test "$u" -eq 0
echo "rc=$?"

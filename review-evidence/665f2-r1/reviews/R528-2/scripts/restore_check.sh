#!/bin/sh
# Verify a review clone is byte-exact at its head: index, worktree, flags,
# modes, every tracked blob rehashed, nothing untracked/ignored, gitlinks.
# Usage: restore_check.sh REPO
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "TREE $(git rev-parse HEAD^{tree})"
echo "status-with-ignored:"; git status --porcelain --ignored; echo "end-status"
git diff --cached --quiet HEAD && echo "index-vs-HEAD: identical" || echo "index-vs-HEAD: DIFFERS"
git diff --quiet && echo "worktree-vs-index: identical" || echo "worktree-vs-index: DIFFERS"
echo "flags-not-H: $(git ls-files -v | grep -vc '^H ')"
a=$(git ls-files -s | awk '{print $1, $2, $4}' | sort | sha256sum)
b=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort | sha256sum)
[ "$a" = "$b" ] && echo "index-stage-blob-mode == ls-tree: yes" || echo "index-stage-blob-mode == ls-tree: NO"
n=0
git ls-files -s | awk '$1 != "160000" {print $2 "\t" substr($0, index($0, "\t") + 1)}' > /tmp/rc_$$.lst
while IFS="$(printf '\t')" read -r sha path; do
  h=$(git hash-object --no-filters -- "$path") || h=missing
  [ "$h" = "$sha" ] || { n=$((n + 1)); echo "MISMATCH $path"; }
done < /tmp/rc_$$.lst
rm -f /tmp/rc_$$.lst
echo "rehash mismatches: $n"
echo "gitlinks:"; git ls-tree -r HEAD | awk '$1 == "160000"'; git submodule status

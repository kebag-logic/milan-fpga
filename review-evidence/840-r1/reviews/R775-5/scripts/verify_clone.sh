#!/bin/sh
# usage: verify_clone.sh <clone> <head> <tree>
# Proves the review clone still holds exact head bytes, modes, index and gitlinks.
c=$1; h=$2; t=$3; cd "$c" || exit 9
fail=0
[ "$(git rev-parse HEAD)" = "$h" ] && echo "HEAD ok $h" || { echo "HEAD differs"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$t" ] && echo "tree ok $t" || { echo "tree differs"; fail=1; }
[ "$(git write-tree)" = "$t" ] && echo "index tree ok" || { echo "index differs"; fail=1; }
n=$(git status --porcelain=v1 --untracked-files=all --ignore-submodules=none | wc -l)
echo "status entries: $n"; [ "$n" = 0 ] || fail=1
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/r775-5-index.$$
git ls-tree -r "$h" | awk '{print $1, $3, $4}' | sort > /tmp/r775-5-tree.$$
cmp /tmp/r775-5-index.$$ /tmp/r775-5-tree.$$ && echo "index blobs and modes equal head tree: $(wc -l < /tmp/r775-5-tree.$$) entries" || fail=1
rm -f /tmp/r775-5-index.$$ /tmp/r775-5-tree.$$
git diff --quiet HEAD -- && echo "worktree bytes equal head" || { echo "worktree differs"; fail=1; }
git ls-tree "$h" | grep '^160000'
git submodule status | cut -c1-70
exit $fail

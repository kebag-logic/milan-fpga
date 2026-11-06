#!/bin/sh
# Verify the review clone is at the exact head with tracked bytes, modes, index and gitlinks unchanged.
# usage: verify_clone.sh <clone>
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
test "$(git rev-parse HEAD)" = eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65 && echo "head: exact" || echo "head: DIFFERS"
test "$(git rev-parse HEAD^{tree})" = 883f71864feecfd59543c9c94e5c4f6835019238 && echo "tree: exact" || echo "tree: DIFFERS"
echo "status --porcelain --untracked-files=all: $(git status --porcelain --untracked-files=all | wc -l) lines"
git diff --quiet && echo "worktree vs index: equal" || echo "worktree vs index: DIFFERS"
git diff --cached --quiet && echo "index vs HEAD: equal" || echo "index vs HEAD: DIFFERS"
a=$(git ls-files -s | sha256sum | cut -d' ' -f1)
b=$(git ls-tree -r --full-tree HEAD | awk '{print $1" "$3" 0\t"$4}' | sha256sum | cut -d' ' -f1)
test "$a" = "$b" && echo "index entries (mode, blob, path) == HEAD tree: equal" || echo "index entries: DIFFER"
git ls-tree HEAD external protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
git submodule status
echo "rehash of every tracked regular file vs index:"
git ls-files -s | awk '$1 != "160000"' | cut -f2 > /tmp/r783-paths.$$
git ls-files -s | awk '$1 != "160000" {print $2}' > /tmp/r783-want.$$
git hash-object --no-filters --stdin-paths < /tmp/r783-paths.$$ > /tmp/r783-got.$$
echo "  $(wc -l < /tmp/r783-paths.$$) files rehashed, $(paste /tmp/r783-want.$$ /tmp/r783-got.$$ | awk '$1 != $2' | wc -l) differ"
git ls-files -s | awk '$1 != "160000" {print $1}' | sort | uniq -c | sed 's/^/  mode /'
rm -f /tmp/r783-paths.$$ /tmp/r783-want.$$ /tmp/r783-got.$$

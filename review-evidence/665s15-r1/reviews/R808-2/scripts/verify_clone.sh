#!/bin/bash
# Usage: verify_clone.sh <clone> <head> : head, tree, index == HEAD tree (blobs and modes), clean worktree, gitlinks.
C=$1; H=$2; cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) want $H"; echo "tree $(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD MISMATCH"; exit 1; }
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null && echo "index == HEAD tree (mode, blob, path) for $(git ls-files | wc -l) entries" || { echo "INDEX DIFFERS"; exit 1; }
git diff --quiet && git diff --cached --quiet && echo "worktree and index clean" || { echo DIRTY; exit 1; }
echo "untracked/ignored: $(git status --short --ignored | grep -v '^ *-' | wc -l)"
git submodule status | while read -r s p r; do echo "gitlink $p $(git ls-tree HEAD "$p" | awk '{print $3}') checkout $s"; done

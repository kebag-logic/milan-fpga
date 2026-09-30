#!/bin/sh
# usage: clone_integrity.sh <clone> <expected head> <expected tree>
cd "$1" || exit 2
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree}); it=$(git write-tree)
echo "HEAD $h (expected $2)"; echo "tree $t (expected $3)"; echo "index tree $it"
echo "status-porcelain-lines (incl. ignored) $(git status --porcelain --ignored | wc -l)"
git status --porcelain --ignored
git diff --quiet && git diff --cached --quiet && echo "worktree+index == HEAD: yes" || echo "worktree+index == HEAD: NO"
echo "ls-files -s digest $(git ls-files -s | sha256sum | cut -c1-16)"
echo "HEAD tree (ls-tree -r, mode/blob/path) digest $(git ls-tree -r HEAD | awk '{print $1" "$3" 0\t"$4}' | sha256sum | cut -c1-16)"
echo "gitlinks (index):"; git ls-files -s | awk '$1=="160000"'
echo "gitlinks (HEAD tree):"; git ls-tree -r HEAD | awk '$1=="160000"'
echo "submodule status:"; git submodule status 2>&1
[ "$h" = "$2" ] && [ "$t" = "$3" ] && [ "$it" = "$3" ] && [ -z "$(git status --porcelain --ignored)" ] && echo RESULT PASS || echo RESULT FAIL

#!/bin/sh
# Usage: clone_integrity.sh <repo> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
echo "HEAD=$(git rev-parse HEAD) expected=$2"
echo "TREE=$(git rev-parse 'HEAD^{tree}') expected=$3"
[ "$(git rev-parse HEAD)" = "$2" ] && [ "$(git rev-parse 'HEAD^{tree}')" = "$3" ] || { echo FAIL-head; exit 1; }
git update-index -q --really-refresh >/dev/null 2>&1
echo "porcelain (ignored excluded): $(git status --porcelain --untracked-files=all | wc -l) lines"
git status --porcelain --untracked-files=all | head
git diff --quiet && echo "worktree==index: yes" || { echo FAIL-worktree; exit 1; }
git diff --cached --quiet && echo "index==HEAD: yes" || { echo FAIL-index; exit 1; }
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
tre=$(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
echo "index mode/oid/path digest=$idx tree digest=$tre"
[ "$idx" = "$tre" ] || { echo FAIL-modes; exit 1; }
echo "gitlinks:"; git ls-tree -r HEAD | awk '$2=="commit"{print "  "$4" "$3}'
echo RESULT: PASS

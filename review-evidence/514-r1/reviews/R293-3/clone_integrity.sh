#!/usr/bin/env bash
# [R293] R293-3: verify the review clone is byte-identical to the exact head.
# Usage: clone_integrity.sh <repo>   (prints the receipt; exit 0 only if all hold)
set -u
cd "$1" || exit 2
HEAD_WANT=177867daf3b35ba41b8c51f8c35c8509643dda22
TREE_WANT=384b3fe2060fb462ffb893a266ddf3b6cc7b6dc1
bad=0
chk() { if eval "$2"; then echo "OK   $1"; else echo "FAIL $1"; bad=1; fi; }
chk "HEAD = $HEAD_WANT" '[ "$(git rev-parse HEAD)" = "$HEAD_WANT" ]'
chk "HEAD tree = $TREE_WANT" '[ "$(git rev-parse "HEAD^{tree}")" = "$TREE_WANT" ]'
chk "index modes/oids = HEAD tree" \
  'cmp -s <(git ls-files -s | awk "{print \$1, \$2, \$4}") <(git ls-tree -r HEAD | awk "{print \$1, \$3, \$4}")'
chk "index = HEAD (diff --cached)" 'git diff --cached --quiet HEAD'
chk "tracked worktree bytes = index" 'git diff --quiet'
chk "porcelain status incl. ignored is empty" '[ -z "$(git status --porcelain --ignored)" ]'
echo "# gitlinks in HEAD tree vs index"
git ls-tree -r HEAD | awk '$2=="commit"{print $1, $3, $4}'
chk "gitlinks index = HEAD" \
  'cmp -s <(git ls-files -s | awk "\$1==160000{print \$2, \$4}") <(git ls-tree -r HEAD | awk "\$2==\"commit\"{print \$3, \$4}")'
exit $bad

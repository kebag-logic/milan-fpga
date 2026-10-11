#!/bin/sh
# Verify a review clone is byte-for-byte at an exact head: commit, tree, index,
# worktree bytes and modes, no untracked or ignored leftovers, required gitlinks.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha> <gitlink-path>...
set -u
C=$1; H=$2; T=$3; shift 3
fail=0
say() { printf '%s\n' "$*"; }
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$H" ] && say "head ok $H" || { say "HEAD MISMATCH $(git rev-parse HEAD)"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] && say "tree ok $T" || { say "TREE MISMATCH"; fail=1; }
git update-index -q --really-refresh >/dev/null 2>&1
git diff --cached --quiet HEAD -- && say "index == HEAD" || { say "INDEX DIFFERS"; fail=1; }
git diff --quiet -- && say "worktree == index (bytes and modes)" || { say "WORKTREE DIFFERS"; fail=1; }
[ -z "$(git ls-files -s | awk '$3 != 0')" ] && say "all index entries stage 0" || { say "UNMERGED ENTRIES"; fail=1; }
[ -z "$(git ls-files -v | grep -E '^[a-z]|^S ')" ] && say "no assume-unchanged/skip-worktree flags" || { say "HIDDEN FLAGS"; fail=1; }
# Blob bytes: hash every tracked regular file and compare with the index.
bad=$(git ls-files -s | awk '$1 != "160000" {print $2" "$4}' | while read -r sha p; do
  [ "$(git hash-object --no-filters -- "$p")" = "$sha" ] || printf '%s\n' "$p"; done)
[ -z "$bad" ] && say "every tracked blob re-hashes to its index object" || { say "BLOB MISMATCH: $bad"; fail=1; }
left=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$left" ] && say "no untracked or ignored leftovers" || { say "LEFTOVERS: $left"; fail=1; }
for sm in "$@"; do
  want=$(git rev-parse "HEAD:$sm"); have=$(git -C "$sm" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$sm" status --porcelain 2>/dev/null)
  if [ "$want" = "$have" ] && [ -z "$dirty" ]; then say "gitlink ok $sm $want clean"; else say "GITLINK FAIL $sm want=$want have=$have dirty=[$dirty]"; fail=1; fi
done
[ $fail = 0 ] && say "CLONE VERIFIED" || say "CLONE NOT VERIFIED"
exit $fail

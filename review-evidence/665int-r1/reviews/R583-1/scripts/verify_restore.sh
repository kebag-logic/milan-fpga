#!/bin/sh
# verify_restore.sh REPO: prove the clone is back at the exact reviewed head.
# Checks HEAD and tree ids, a clean worktree and index (ignored files
# included), every tracked blob's bytes and mode against HEAD's tree
# (git hash-object on disk vs ls-tree), no assume-unchanged/skip-worktree
# flags, and the submodule gitlinks against their pins.
set -eu
R=$1
cd "$R"
echo "HEAD $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "status entries (incl. ignored): $(git status --porcelain --ignored | wc -l)"
echo "index vs HEAD diff entries: $(git diff --cached --name-only | wc -l)"
echo "flagged index entries (h/S): $(git ls-files -v | grep -c '^[hSs] ' || true)"
bad=0; n=0
git ls-tree -r HEAD | while read -r mode type oid path; do
  if [ "$type" = blob ]; then
    if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); else got=$(git hash-object --no-filters -- "$path"); fi
    [ "$got" = "$oid" ] || { echo "BLOB MISMATCH $path"; }
    case "$mode" in 100755) [ -x "$path" ] || echo "MODE MISMATCH $path";; 100644) [ ! -x "$path" ] || echo "MODE MISMATCH $path";; esac
  fi
done > /tmp/verify_restore_$$.txt
echo "tracked blobs checked: $(git ls-tree -r HEAD | awk '$2=="blob"' | wc -l); mismatches: $(wc -l < /tmp/verify_restore_$$.txt)"
cat /tmp/verify_restore_$$.txt; rm -f /tmp/verify_restore_$$.txt
echo "gitlinks (pin / checkout):"
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read -r pin path; do
  if [ -e "$path/.git" ]; then co=$(git -C "$path" rev-parse HEAD); else co=uninitialised; fi
  echo "  $path $pin $co $( [ "$pin" = "$co" ] && echo MATCH || echo "-" )"
done
git submodule status

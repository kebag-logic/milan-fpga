#!/bin/sh
# Verifies the review clone is at the exact head with no tracked, untracked or
# ignored change, the index equals the head tree, every tracked file's bytes
# and mode match, and the submodule gitlinks equal their checkouts.
# Usage: restore_check.sh <checkout>
G=/usr/bin/git
cd "$1" || exit 2
echo "HEAD $($G rev-parse HEAD)"
echo "HEAD tree $($G rev-parse 'HEAD^{tree}')"
echo "index tree $($G write-tree)"
$G diff-index --quiet --cached HEAD; echo "index vs HEAD rc=$?"
$G diff-files --quiet; echo "worktree vs index rc=$?"
echo "porcelain --ignored lines: $($G status --porcelain --ignored --untracked-files=all | wc -l)"
$G status --porcelain --ignored --untracked-files=all | head -20
# re-hash every tracked regular file and compare with its blob id and mode
bad=0; n=0
$G ls-files -s > /tmp/r429_lsfiles.$$
while read -r mode oid stage path; do
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then h=$(readlink -n "$path" | $G hash-object --stdin)
  else h=$($G hash-object --no-filters -- "$path"); fi
  [ "$h" = "$oid" ] || { bad=$((bad+1)); echo "BYTES $path"; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then bad=$((bad+1)); echo "MODE $path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then bad=$((bad+1)); echo "MODE $path"; fi
done < /tmp/r429_lsfiles.$$
rm -f /tmp/r429_lsfiles.$$
echo "tracked files re-hashed: $n, mismatches: $bad"
echo "submodule gitlinks (tree) vs checkouts:"
$G ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r oid path; do
  if [ ! -e "$path/.git" ]; then echo "$path gitlink $oid not initialized (no checkout)"; continue; fi
  co=$($G -C "$path" rev-parse HEAD 2>/dev/null || echo none)
  echo "$path gitlink $oid checkout $co $( [ "$oid" = "$co" ] && echo MATCH || echo DIFF )"
done

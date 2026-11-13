#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer-owned: prove a review clone is byte-exact at its head after probes. Re-hash every tracked file and compare
# with HEAD's blob ids and modes, check the index and the work tree against HEAD, list untracked and ignored files,
# and print each submodule's checked-out commit against its gitlink.
# usage: verify_clone.sh CLONE EXPECTED_HEAD
set -u
C=$1 H=$2
cd "$C" || exit 2
echo "head $(git rev-parse HEAD) expected $H tree $(git rev-parse HEAD^{tree})"
git ls-tree -r HEAD | awk '$2=="blob"{print $1" "$3" "$4}' > /tmp/vc.$$.tree
n=0 bad=0
while read -r mode sha path; do
  n=$((n+1))
  got=$(git hash-object --no-filters -- "$path" 2>/dev/null || echo missing)
  if [ "$got" != "$sha" ]; then bad=$((bad+1)); echo "BLOB MISMATCH $path"; fi
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then bad=$((bad+1)); echo "MODE $path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then bad=$((bad+1)); echo "MODE $path"; fi
  if [ "$mode" = 120000 ] && [ ! -L "$path" ]; then bad=$((bad+1)); echo "LINK $path"; fi
done < /tmp/vc.$$.tree
rm -f /tmp/vc.$$.tree
echo "tracked blobs $n mismatches $bad"
git diff --quiet HEAD && echo "worktree vs HEAD: clean" || echo "worktree vs HEAD: DIRTY"
git diff --cached --quiet HEAD && echo "index vs HEAD: clean" || echo "index vs HEAD: DIRTY"
echo "untracked: $(git ls-files --others --exclude-standard | wc -l)"
echo "ignored: $(git ls-files --others --ignored --exclude-standard | wc -l)"
git ls-files --others --ignored --exclude-standard | head -20
git ls-tree -r HEAD | awk '$2=="commit"{print $3" "$4}' | while read -r sha path; do
  if [ -e "$path/.git" ]; then
    cur=$(git -C "$path" rev-parse HEAD); d=$(git -C "$path" status --porcelain | wc -l)
    echo "gitlink $path $sha checked-out $cur dirty $d $( [ "$cur" = "$sha" ] && echo OK || echo DIFFERS)"
  else
    echo "gitlink $path $sha not initialized"
  fi
done

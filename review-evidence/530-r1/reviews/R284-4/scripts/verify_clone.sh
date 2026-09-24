#!/usr/bin/env bash
# Verify a review clone is byte-exact at the expected head: HEAD, tree, index
# tree, every tracked blob's bytes and mode, no flags, no leftovers, gitlinks.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
echo "HEAD=$(git rev-parse HEAD) expect $H"; [ "$(git rev-parse HEAD)" = "$H" ] || echo "HEAD MISMATCH"
echo "tree=$(git rev-parse HEAD^{tree}) expect $T"; [ "$(git rev-parse HEAD^{tree})" = "$T" ] || echo "TREE MISMATCH"
echo "index tree=$(git write-tree)"; [ "$(git write-tree)" = "$T" ] || echo "INDEX MISMATCH"
git update-index -q --really-refresh
bad=0; n=0
while read -r mode type sha path; do
  [ "$type" = blob ] || continue; n=$((n+1))
  got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
  [ "$got" = "$sha" ] || { echo "BYTES DIFFER: $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE: $path"; bad=$((bad+1)); }
  else [ -x "$path" ] && [ ! -L "$path" ] && { echo "MODE: $path"; bad=$((bad+1)); }; fi
done < <(git ls-tree -r "$H")
echo "tracked blobs checked: $n, mismatches: $bad"
echo "assume-unchanged/skip-worktree flags: $(git ls-files -v | grep -c '^[a-z]\|^S')"
echo "status (untracked+ignored), expect empty:"; git status --porcelain --ignored --ignore-submodules=none
echo "gitlinks:"; git submodule status
for s in protocol-processor gptp-processor third_party/verilog-axis; do echo "$s dirty-lines=$(git -C $s status --porcelain --ignored | wc -l)"; done

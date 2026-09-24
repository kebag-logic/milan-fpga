#!/bin/sh
# Verify a review clone is byte-exact at the expected head.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -u
C=$1; H=$2; T=$3; rc=0
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) expect $H"; [ "$(git rev-parse HEAD)" = "$H" ] || rc=1
echo "tree $(git rev-parse HEAD^{tree}) expect $T"; [ "$(git rev-parse HEAD^{tree})" = "$T" ] || rc=1
it=$(git write-tree); echo "index tree $it"; [ "$it" = "$T" ] || rc=1
s=$(git status --porcelain --ignored=matching --untracked-files=all | grep -v '^!! external/$' ); echo "status entries: $(printf '%s' "$s" | grep -c . )"; [ -z "$s" ] || { printf '%s\n' "$s" | head; rc=1; }
flags=$(git ls-files -v | grep -c '^[a-z]\|^S'); echo "assume-unchanged/skip-worktree flags: $flags"; [ "$flags" = 0 ] || rc=1
# byte and mode check of every tracked regular file / symlink against HEAD
bad=$(git ls-tree -r HEAD | awk '$2!="commit"' | while read -r mode type obj path; do
  h=$(git hash-object --no-filters -- "$path" 2>/dev/null)
  if [ -L "$path" ]; then m=120000; elif [ -x "$path" ]; then m=100755; else m=100644; fi
  [ "$h" = "$obj" ] && [ "$m" = "$mode" ] || echo "$path"; done | wc -l)
n=$(git ls-tree -r HEAD | awk '$2!="commit"' | wc -l)
echo "tracked blobs checked: $n  mismatched: $bad"; [ "$bad" = 0 ] || rc=1
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read -r sha p; do
  if [ -e "$p/.git" ]; then act=$(git -C "$p" rev-parse HEAD); d=$(git -C "$p" status --porcelain | wc -l); echo "gitlink $p pinned $sha checked-out $act dirty $d"; [ "$act" = "$sha" ] && [ "$d" = 0 ] || echo "GITLINK MISMATCH $p";
  else echo "gitlink $p pinned $sha not initialised"; fi; done
git submodule status | grep -q '^[+U]' && { echo "submodule drift"; rc=1; }
echo "RESULT: $([ $rc = 0 ] && echo PASS || echo FAIL)"; exit $rc

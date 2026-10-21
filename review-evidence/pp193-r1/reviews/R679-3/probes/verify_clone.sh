#!/bin/sh
# Verify a review clone is byte-exact at the expected head.
# usage: verify_clone.sh <clone> <head sha> <tree sha>
# Prints HEAD/tree, ignored/untracked/modified status, index-vs-HEAD, every
# tracked file's working bytes and mode against its index entry, and gitlinks.
set -u
c=$1; want_head=$2; want_tree=$3
cd "$c" || exit 2
rc=0
head=$(git rev-parse HEAD); tree=$(git rev-parse HEAD^{tree})
echo "HEAD $head"; echo "tree $tree"
[ "$head" = "$want_head" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$tree" = "$want_tree" ] || { echo "TREE MISMATCH"; rc=1; }
st=$(git status --porcelain --ignored --untracked-files=all)
echo "status entries (ignored included): $(printf '%s' "$st" | grep -c . )"
[ -z "$st" ] || { printf '%s\n' "$st" | head -20; rc=1; }
git diff --cached --quiet HEAD || { echo "INDEX != HEAD"; rc=1; }
git ls-tree -r HEAD | awk '{print $1, $3, $4}' > /tmp/vc_tree.$$
git ls-files -s | awk '{print $1, $2, $4}' > /tmp/vc_index.$$
cmp -s /tmp/vc_tree.$$ /tmp/vc_index.$$ || { echo "INDEX ENTRIES != TREE"; rc=1; }
n=0; bad=0
while read -r mode blob path; do
  n=$((n+1))
  case $mode in
    160000) echo "gitlink $path $blob"; continue ;;
    120000) got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin) ;;
    *) got=$(git hash-object "$path") ;;
  esac
  [ "$got" = "$blob" ] || { echo "BYTES $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE $path"; bad=$((bad+1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE $path"; bad=$((bad+1)); fi
done < /tmp/vc_tree.$$
rm -f /tmp/vc_tree.$$ /tmp/vc_index.$$
echo "tracked entries $n, byte/mode mismatches $bad"
echo "gitlinks: $(git ls-tree -r HEAD | grep -c '^160000')"
[ "$bad" -eq 0 ] || rc=1
echo "verify rc $rc"
exit $rc

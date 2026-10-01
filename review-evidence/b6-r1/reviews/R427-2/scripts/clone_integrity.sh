#!/bin/bash
# Verify the review clone is exactly the head under review: HEAD, index tree,
# every tracked blob's bytes and mode, no assume-unchanged/skip-worktree flags,
# no untracked or modified files, and the gitlinks equal the head tree's.
# Usage: clone_integrity.sh <clone> <head-sha> <tree-sha>
set -u
c=$1; head=$2; tree=$3
cd "$c" || exit 2
rc=0
h=$(git rev-parse HEAD); echo "HEAD $h"; [ "$h" = "$head" ] || { echo "HEAD MISMATCH"; rc=1; }
t=$(git rev-parse 'HEAD^{tree}'); echo "HEAD tree $t"; [ "$t" = "$tree" ] || { echo "TREE MISMATCH"; rc=1; }
it=$(git write-tree); echo "index tree $it"; [ "$it" = "$tree" ] || { echo "INDEX MISMATCH"; rc=1; }
flags=$(git ls-files -v | grep -c -E '^[a-zS] ' || true); echo "assume-unchanged/skip-worktree entries: $flags"; [ "$flags" = 0 ] || rc=1
st=$(git status --porcelain=v1 --untracked-files=all --ignored=no | wc -l); echo "status entries: $st"; [ "$st" = 0 ] || { git status --short | head; rc=1; }
# Bytes and modes of every tracked regular file and symlink against HEAD's blobs.
n=0; bad=0
git ls-tree -r HEAD | awk '$2=="blob"{print $1" "$3" "substr($0, index($0,"\t")+1)}' > /tmp/r427-2-blobs.$$
while read -r mode sha path; do
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$sha" ] || { echo "SYMLINK DIFF $path"; bad=$((bad+1)); }
  else
    [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || { echo "BYTES DIFF $path"; bad=$((bad+1)); }
    x=no; [ -x "$path" ] && x=yes
    want=no; [ "$mode" = 100755 ] && want=yes
    [ "$x" = "$want" ] || { echo "MODE DIFF $path"; bad=$((bad+1)); }
  fi
done < /tmp/r427-2-blobs.$$
echo "tracked blobs checked: $(wc -l < /tmp/r427-2-blobs.$$), differing: $bad"
rm -f /tmp/r427-2-blobs.$$
[ "$bad" = 0 ] || rc=1
echo "gitlinks (head tree):"; git ls-tree -r HEAD | awk '$1=="160000"'
echo "gitlinks (index):"; git ls-files -s | awk '$1=="160000"'
diff <(git ls-tree -r HEAD | awk '$1=="160000"{print $3" "$4}') <(git ls-files -s | awk '$1=="160000"{print $2" "$4}') || { echo "GITLINK INDEX MISMATCH"; rc=1; }
echo "RESULT $( [ $rc = 0 ] && echo PASS || echo FAIL )"
exit $rc

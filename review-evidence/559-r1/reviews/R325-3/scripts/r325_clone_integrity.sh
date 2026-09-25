#!/bin/sh
# [R325] R325-3: prove the review clone is the exact published head, byte for
# byte: HEAD/tree ids, index == HEAD tree (paths, modes, blob ids, stage 0),
# no assume-unchanged/skip-worktree flags, every tracked file's on-disk bytes
# and mode hash to its recorded blob, and the submodule gitlinks.
set -eu
C=$1
cd "$C"
export GIT_NO_REPLACE_OBJECTS=1
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
test "$(git rev-parse HEAD)" = b02af0480d3a3061df24683d522799d1759f7c33
test "$(git rev-parse 'HEAD^{tree}')" = 8c9f216b462e2f0fd7b8da9c73e3f817a8555d32
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/r325-tree.$$
git ls-files -s | awk '{print $1, $2, $3, $4}' > /tmp/r325-idx.$$
awk '$3 != 0 {bad=1} END {exit bad}' /tmp/r325-idx.$$ && echo "index: all records stage 0"
awk '{print $1, $2, $4}' /tmp/r325-idx.$$ | sort | cmp - /tmp/r325-tree.$$ && echo "index == HEAD tree ($(wc -l < /tmp/r325-tree.$$) records)"
flags=$(git ls-files -v | grep -vc '^H ' || true); echo "non-H index flags (assume-unchanged/skip-worktree/etc): $flags"; test "$flags" = 0
n=0; bad=0
while read -r mode blob path; do
  case $mode in
    160000) continue ;;
    120000) h=$(readlink "$path" | tr -d '\n' | git hash-object --stdin) ; [ -L "$path" ] || bad=$((bad+1)) ;;
    100755) h=$(git hash-object --no-filters -- "$path"); [ -x "$path" ] && [ ! -L "$path" ] || bad=$((bad+1)) ;;
    100644) h=$(git hash-object --no-filters -- "$path"); [ ! -x "$path" ] && [ ! -L "$path" ] || bad=$((bad+1)) ;;
  esac
  [ "$h" = "$blob" ] || { echo "MISMATCH $path"; bad=$((bad+1)); }
  n=$((n+1))
done < /tmp/r325-tree.$$
echo "tracked files hashed from disk: $n, mismatches (bytes or mode): $bad"; test "$bad" = 0
echo "gitlinks:"; git ls-tree -r HEAD | awk '$1=="160000"{print "  "$3, $4}'
git submodule status
git status --porcelain --untracked-files=all --ignored | sed 's/^/  status: /'
rm -f /tmp/r325-tree.$$ /tmp/r325-idx.$$
echo "CLONE INTEGRITY OK"

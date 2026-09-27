#!/usr/bin/env bash
# Verify a checkout holds exact head bytes: HEAD/tree, index tree, every tracked
# blob re-hashed with its mode, no index flags, no status lines (incl. ignored), gitlinks.
# Usage: scripts/verify_clone.sh <checkout> <commit> <tree>
set -u
cd "$1" || exit 2
fail=0
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
[ "$(git rev-parse HEAD)" = "$2" ] || { echo "HEAD mismatch"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$3" ] || { echo "tree mismatch"; fail=1; }
it=$(git write-tree); echo "index tree $it"; [ "$it" = "$3" ] || { echo "index tree mismatch"; fail=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  read -r mode _type blob <<< "$meta"
  n=$((n+1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $blob"; continue; fi
  if [ "$mode" = 120000 ]; then h=$(readlink -n -- "$path" | git hash-object --stdin)
  else h=$(git hash-object -- "$path"); fi
  fm=100644; [ -L "$path" ] && fm=120000 || { [ -x "$path" ] && fm=100755; }
  if [ "$h" != "$blob" ] || [ "$fm" != "$mode" ]; then echo "MISMATCH $path"; bad=$((bad+1)); fi
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked entries $n, blob/mode mismatches $bad"; [ $bad -eq 0 ] || fail=1
flags=$(git ls-files -t | grep -vc '^H ' || true); echo "non-H index flags $flags"; [ "$flags" -eq 0 ] || fail=1
st=$(git status --porcelain --ignored | wc -l); echo "status lines incl. ignored $st"; [ "$st" -eq 0 ] || fail=1
echo "gitlinks in tree: $(git ls-tree -r HEAD | awk '$1==160000' | wc -l); .gitmodules: $([ -f .gitmodules ] && echo present || echo absent)"
echo "verify rc=$fail"; exit $fail

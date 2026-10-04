#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# verify_clone.sh CLONE HEAD TREE : the review clone is exactly HEAD's bytes.
# Checks HEAD and its tree id, every index record's mode and blob against HEAD's tree,
# every working file's blob hash (bypassing the index's stat cache and its
# assume-unchanged / skip-worktree flags), no untracked or ignored files, and the
# gitlink (mode 160000) set, which must equal HEAD's.
set -u
c=$1; want_head=$2; want_tree=$3
export GIT_NO_REPLACE_OBJECTS=1
cd "$c" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$want_head" ] || { echo "FAIL HEAD"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$want_tree" ] || { echo "FAIL tree"; fail=1; }
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/r453_tree.$$
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/r453_index.$$
cmp -s /tmp/r453_tree.$$ /tmp/r453_index.$$ || { echo "FAIL index records differ from HEAD's tree"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' | head -5)
[ -z "$flags" ] || { echo "FAIL index flags: $flags"; fail=1; }
n=0
while read -r mode blob path; do
  if [ "$mode" = 160000 ]; then continue; fi
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  [ "$got" = "$blob" ] || { echo "FAIL bytes $path"; fail=1; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "FAIL mode $path"; fail=1; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "FAIL mode $path"; fail=1; fi
  n=$((n + 1))
done < /tmp/r453_tree.$$
extra=$(git status --porcelain --ignored --untracked-files=all | head -5)
[ -z "$extra" ] || { echo "FAIL worktree not clean: $extra"; fail=1; }
links=$(awk '$1 == "160000"' /tmp/r453_tree.$$ | wc -l)
rm -f /tmp/r453_tree.$$ /tmp/r453_index.$$
echo "files hashed: $n; gitlinks in HEAD: $links (none required at this head)"
[ "$fail" = 0 ] && echo "CLONE OK: HEAD $want_head tree $want_tree" || echo "CLONE FAIL"
exit "$fail"

#!/usr/bin/env bash
# Verify the review clone is byte-exact at the reviewed head after probes:
# HEAD and tree ids, no tracked/untracked/ignored-tracked changes, every
# tracked file's working-tree blob id and mode equal to the index and HEAD,
# the index equal to HEAD's tree, and the submodule gitlinks and checkouts.
# Usage: verify_clone.sh <clone> <expected head sha> <expected tree sha>
set -euo pipefail
C="$1"; H="$2"; T="$3"
cd "$C"
rc=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD ok $H" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] && echo "tree ok $T" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$T" ] && echo "index tree ok (git write-tree == $T)" || { echo "INDEX MISMATCH"; rc=1; }
st="$(git status --porcelain=v1 --untracked-files=all)"
[ -z "$st" ] && echo "status clean (tracked and untracked)" || { echo "STATUS DIRTY:"; echo "$st"; rc=1; }
# every tracked regular file / symlink: hash the working copy and compare with HEAD's blob and mode
git ls-tree -r --full-tree HEAD | awk '$2=="blob"{print $1" "$3" "$4}' > /tmp/r366_lstree.$$
n=0; bad=0
while read -r mode sha path; do
  n=$((n+1))
  if [ "$mode" = "120000" ]; then w=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else w=$(git hash-object --no-filters "$path"); fi
  fm=$([ -L "$path" ] && echo 120000 || { [ -x "$path" ] && echo 100755 || echo 100644; })
  if [ "$w" != "$sha" ] || [ "$fm" != "$mode" ]; then bad=$((bad+1)); echo "BLOB/MODE MISMATCH $path"; fi
done < /tmp/r366_lstree.$$
rm -f /tmp/r366_lstree.$$
echo "tracked blobs checked: $n, mismatches: $bad"; [ "$bad" -eq 0 ] || rc=1
git ls-tree -r HEAD | awk '$2=="commit"{print $3" "$4}' | while read -r sha path; do
  actual=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo absent)
  dirty=$(git -C "$path" status --porcelain 2>/dev/null | wc -l)
  echo "gitlink $path $sha checkout=$actual dirty_entries=$dirty $([ "$actual" = "$sha" ] && echo ok || echo '(not checked out / differs)')"
done
exit $rc

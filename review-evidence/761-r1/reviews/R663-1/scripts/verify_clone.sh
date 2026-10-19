#!/usr/bin/env bash
# Verify a review clone is byte-identical to the reviewed head.
# Usage: verify_clone.sh <clone> <head_sha> <tree_sha>
# Checks: HEAD and tree ids; index tree == HEAD tree; every tracked regular
# file's blob hash and mode equal the HEAD entry (no stat shortcut); no
# untracked or ignored file; submodule gitlinks at the recorded commits.
set -u
C=$1; H=$2; T=$3; bad=0
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD mismatch"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "tree mismatch"; bad=1; }
[ "$(git write-tree)" = "$T" ] || { echo "index tree differs from HEAD tree"; bad=1; }
n=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; type=$2; oid=$3
  if [ "$type" = commit ]; then
    # an uninitialised submodule is an empty directory with no .git of its own
    if [ -e "$path/.git" ]; then have=$(git -C "$path" rev-parse HEAD)
    else have=uninitialised; fi
    echo "gitlink $path recorded=$oid checkout=$have"
    if [ "$have" != uninitialised ] && [ "$have" != "$oid" ]; then bad=1; fi
    continue
  fi
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$oid" ] || { echo "symlink differs: $path"; bad=1; }
    continue
  fi
  [ "$(git hash-object --no-filters "$path")" = "$oid" ] || { echo "bytes differ: $path"; bad=1; }
  x=100644; [ -x "$path" ] && x=100755
  [ "$x" = "$mode" ] || { echo "mode differs: $path ($x vs $mode)"; bad=1; }
done < <(git ls-tree -r HEAD)
extra=$(git status --porcelain --ignored --untracked-files=all | wc -l)
[ "$extra" -eq 0 ] || { echo "status not clean ($extra entries)"; git status --porcelain --ignored | head; bad=1; }
echo "tracked files checked: $n; problems: $bad"
exit $bad

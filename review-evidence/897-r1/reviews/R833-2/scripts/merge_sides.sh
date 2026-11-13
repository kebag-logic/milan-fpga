#!/bin/sh
# Usage: merge_sides.sh <repo> <old_base> <branch_tip> <new_base> <merge>
# For every file the branch changed from old_base, compare the merge's diff
# from new_base with the branch's own diff from old_base (hunk bodies only,
# line numbers stripped). Also list files where merge differs from new_base
# that the branch never touched.
set -u
R=$1; OB=$2; BT=$3; NB=$4; M=$5
cd "$R" || exit 2
body() { git diff -U0 "$1" "$2" -- "$3" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) '; }
rc=0
for f in $(git diff --name-only "$OB" "$BT"); do
  a=$(body "$OB" "$BT" "$f" | sha256sum | cut -c1-16)
  b=$(body "$NB" "$M" "$f" | sha256sum | cut -c1-16)
  if [ "$a" = "$b" ]; then echo "SAME   $f"; else echo "DIFFER $f"; rc=1; fi
done
echo "--- files changed by merge vs new base not in branch diff:"
comm -13 <(git diff --name-only "$OB" "$BT" | sort) <(git diff --name-only "$NB" "$M" | sort)
echo "--- files changed by merge vs branch tip (expected: base side) not in base diff:"
comm -13 <(git diff --name-only "$OB" "$NB" | sort) <(git diff --name-only "$BT" "$M" | sort)
exit $rc

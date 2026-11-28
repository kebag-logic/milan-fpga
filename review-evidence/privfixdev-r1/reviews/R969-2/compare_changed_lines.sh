#!/bin/sh
# Compare the removed/added line content per file between two diffs (ignores hunk offsets).
# usage: compare_changed_lines.sh <repo> <baseA> <headA> <baseB> <headB>
set -eu
R=$1; cd "$R"
for f in $(git diff --name-only "$2" "$3" | sort); do
  a=$(git diff -U0 "$2" "$3" -- "$f" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) ' | sha256sum | cut -c1-16)
  b=$(git diff -U0 "$4" "$5" -- "$f" | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) ' | sha256sum | cut -c1-16)
  [ "$a" = "$b" ] && s=SAME || s=DIFF
  echo "$s $a $b $f"
done

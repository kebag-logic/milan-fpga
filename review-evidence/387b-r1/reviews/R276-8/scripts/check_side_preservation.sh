#!/usr/bin/env bash
# For each file both sides changed, check the composed tree carries each
# side's change unchanged: the diff (other parent -> candidate) must equal
# the diff (merge base -> this side), hunk bodies compared with line numbers
# stripped. Usage: check_side_preservation.sh <clone> <base> <p1> <p2> <cand> files...
set -u
REPO=$1 B=$2 P1=$3 P2=$4 C=$5; shift 5
cd "$REPO" || exit 2
norm() { sed -E -e '/^(diff --git|index |--- |\+\+\+ )/d' -e 's/^@@ -[0-9,]+ \+[0-9,]+ @@.*/@@/'; }
rc=0
for f in "$@"; do
  a=$(git diff --no-color --no-ext-diff -U0 "$B" "$P2" -- "$f" | norm | sha256sum | cut -c1-16)
  b=$(git diff --no-color --no-ext-diff -U0 "$P1" "$C" -- "$f" | norm | sha256sum | cut -c1-16)
  c=$(git diff --no-color --no-ext-diff -U0 "$B" "$P1" -- "$f" | norm | sha256sum | cut -c1-16)
  d=$(git diff --no-color --no-ext-diff -U0 "$P2" "$C" -- "$f" | norm | sha256sum | cut -c1-16)
  s1=SAME; [ "$a" = "$b" ] || { s1=DIFF; rc=1; }
  s2=SAME; [ "$c" = "$d" ] || { s2=DIFF; rc=1; }
  printf '%s\tsecond-parent-side:%s(%s/%s)\tfirst-parent-side:%s(%s/%s)\n' "$f" "$s1" "$a" "$b" "$s2" "$c" "$d"
done
exit $rc

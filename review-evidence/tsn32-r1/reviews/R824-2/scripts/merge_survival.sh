#!/bin/bash
# Compare each parent's change with what the merged head carries over the other parent (changed lines only).
# usage: merge_survival.sh REPO BASE OURS THEIRS HEAD PATHS...
set -u
R=$1 B=$2 O=$3 T=$4 H=$5; shift 5
lines() { git -C "$R" diff --no-color -U0 "$1" "$2" -- "$@" | grep -E '^[+-][^+-]' ; }
for p in "$@"; do
  echo "== $p: the walk's change (base..ours) against the head over main (theirs..head)"
  diff <(lines $B $O $p) <(lines $T $H $p) && echo "   identical"
  echo "== $p: main's change (base..theirs) against the head over the walk (ours..head)"
  diff <(lines $B $T $p) <(lines $O $H $p) && echo "   identical"
done

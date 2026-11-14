#!/bin/sh
# usage: merge_sides_check.sh <clone> ; per-file comparison of each side's own diff with the merged diff from the other side
# base cec88385, #898 side 3bebf03a, #902 side 7398ec0a, head f098f893
set -eu
cd "$1"
norm() { grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' || true; }
side() { # $1 own-from $2 own-to $3 merged-from
  git diff --name-only "$1" "$2" | sort | while read -r f; do
    a=$(git diff "$1" "$2" -- "$f" | norm | sha256sum | cut -c1-12)
    b=$(git diff "$3" f098f893d57e0fa3ec95a7e459313c5cfe4f4224 -- "$f" | norm | sha256sum | cut -c1-12)
    [ "$a" = "$b" ] && s=SAME || s=DIFF; echo "$s $a $b $f"; done; }
echo "## #898 side"; side cec88385 3bebf03a 7398ec0a
echo "## #902 side"; side cec88385 7398ec0a 3bebf03a

#!/bin/sh
# For each shared file, every line each side added against the merge base must be
# present (verbatim, as a full line) in the candidate blob.
# Usage: added_lines_survive.sh <repo> <base> <side1> <side2> <candidate> <file>...
repo=$1 base=$2 s1=$3 s2=$4 cand=$5; shift 5
G="/usr/bin/git -C $repo"
for f in "$@"; do
  $G show "$cand:$f" > /tmp/r397_cand.$$ 2>/dev/null
  for side in $s1 $s2; do
    total=0 missing=0
    $G diff -U0 "$base" "$side" -- "$f" 2>/dev/null | grep '^+' | grep -v '^+++' | cut -c2- > /tmp/r397_add.$$
    while IFS= read -r line; do
      total=$((total+1))
      grep -qxF -- "$line" /tmp/r397_cand.$$ || { missing=$((missing+1)); echo "  MISSING [$side] $f: $line"; }
    done < /tmp/r397_add.$$
    echo "$f side=$side added=$total missing_in_candidate=$missing"
  done
done
rm -f /tmp/r397_cand.$$ /tmp/r397_add.$$

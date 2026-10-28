#!/bin/sh
# Classify every file changed since the merge base by side, and check one-sided files equal their side.
# Usage: sides.sh <repo> <base> <s1> <s2> <head>
set -eu
R=$1 B=$2 S1=$3 S2=$4 H=$5
cd "$R"
git diff --name-only "$B" "$S1" | sort > /tmp/s1.$$
git diff --name-only "$B" "$S2" | sort > /tmp/s2.$$
echo "S1-only: $(comm -23 /tmp/s1.$$ /tmp/s2.$$ | wc -l)  S2-only: $(comm -13 /tmp/s1.$$ /tmp/s2.$$ | wc -l)  both: $(comm -12 /tmp/s1.$$ /tmp/s2.$$ | wc -l)"
bad=0
for f in $(comm -23 /tmp/s1.$$ /tmp/s2.$$); do git diff --quiet "$S1" "$H" -- "$f" || { echo "S1-only differs at head: $f"; bad=1; }; done
for f in $(comm -13 /tmp/s1.$$ /tmp/s2.$$); do git diff --quiet "$S2" "$H" -- "$f" || { echo "S2-only differs at head: $f"; bad=1; }; done
echo "both-sided:"; comm -12 /tmp/s1.$$ /tmp/s2.$$
git diff --name-only "$B" "$H" | sort > /tmp/h.$$
sort -u /tmp/s1.$$ /tmp/s2.$$ > /tmp/u.$$
echo "head-changed not in either side:"; comm -23 /tmp/h.$$ /tmp/u.$$
echo "either-side not changed at head:"; comm -13 /tmp/h.$$ /tmp/u.$$
rm -f /tmp/s1.$$ /tmp/s2.$$ /tmp/h.$$ /tmp/u.$$
echo "one-sided-mismatch=$bad"

#!/bin/sh
# Usage: check_tree_provenance.sh <repo> <head> <branch_parent> <dev_parent> <base>
# For every path in the union of trees, classify head entry (mode+oid) as matching branch, dev, both, or neither.
set -eu
cd "$1"; H=$2; B=$3; D=$4; M=$5
t=$(mktemp -d)
for r in H B D M; do eval c=\$$r; git ls-tree -r --full-tree "$c" | awk '{print $4"\t"$1" "$3}' | sort > "$t/$r"; done
cut -f1 "$t/H" "$t/B" "$t/D" "$t/M" | sort -u > "$t/paths"
join -a1 -e NONE -t "$(printf '\t')" -o 0,2.2 "$t/paths" "$t/H" > "$t/jH"
join -a1 -e NONE -t "$(printf '\t')" -o 0,2.2 "$t/paths" "$t/B" > "$t/jB"
join -a1 -e NONE -t "$(printf '\t')" -o 0,2.2 "$t/paths" "$t/D" > "$t/jD"
join -a1 -e NONE -t "$(printf '\t')" -o 0,2.2 "$t/paths" "$t/M" > "$t/jM"
paste "$t/jH" "$t/jB" "$t/jD" "$t/jM" | awk -F'\t' '{
 h=$2;b=$4;d=$6;m=$8;
 if(h==b&&h==d) c="same";
 else if(h==d&&b==m) c="dev-only-change";
 else if(h==b&&d==m) c="branch-only-change";
 else c="OTHER";
 n[c]++; if(c!="same") print c"\t"$1 }
 END{for(k in n) print "COUNT\t"k"\t"n[k] > "/dev/stderr"}'
rm -rf "$t"

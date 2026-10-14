#!/bin/sh
# Usage: merge_provenance.sh <repo-root>
# Re-derives the round-8 merge facts for PR #715 from git objects only.
set -eu
cd "$1"
B=9b32002cc0c3aafae9e864af7b4f08c1089a188a   # round-7 head
D=fa8209889411e8ca95757174c981f720dbcd95a2   # dev merged in round 8
M=f3bb2014d065141930ae1a473c966b419d1040aa   # merge commit
H=d5cd863561ba1ee7bc6342fb1b00f57dd786bd97   # head under review
C=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc   # dev merged in round 7 (merge-base of B and D)
T=$(mktemp -d)
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
echo "merge parents: $(git log -1 --format=%P $M)"
echo "merge-base(B,D): $(git merge-base $B $D)"
echo "merge-tree(B,D): $(git merge-tree --write-tree $B $D | head -1)  merge commit tree: $(git rev-parse $M^{tree})"
git diff --name-only $D $M | sort > "$T/own_at_merge"
git diff --name-only $C $B | sort > "$T/own_r7"
echo "paths differing from dev at merge: $(wc -l < "$T/own_at_merge"); same set as round-7 own paths: $(cmp -s "$T/own_at_merge" "$T/own_r7" && echo yes || echo no)"
echo "own paths byte-identical to round-7 head at merge: $(git diff --quiet $B $M -- $(cat "$T/own_at_merge") && echo yes || echo no)"
git diff --name-only $C $D | sort > "$T/dev_delta"
echo "dev delta since round-7 merge-base: $(wc -l < "$T/dev_delta") paths; overlap with own paths: $(comm -12 "$T/dev_delta" "$T/own_r7" | wc -l)"
git diff --full-index --binary $C $D > "$T/a"
git diff --full-index --binary $B $M > "$T/b"
if cmp -s "$T/a" "$T/b"; then same=yes; else same=no; fi
echo "merge delta patch (B..M) == dev delta patch (C..D): $same"
for c in $B $D $M $H; do echo "gitlinks $c:"; git ls-tree -r $c | awk '$2=="commit"{print "  "$3" "$4}'; done
echo "head commit changes vs merge:"; git diff --stat $M $H
echo "commit subjects:"; git log --format='  %h parents=%p %s' -2 $H
rm -rf "$T"

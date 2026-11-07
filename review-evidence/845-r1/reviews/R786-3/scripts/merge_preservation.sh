#!/bin/sh
# Usage: merge_preservation.sh <clone> <outdir>
# Re-derives the four sync checks at head 43410ce1 against 853ca25a.
set -eu
C=$1; O=$2; mkdir -p "$O"; cd "$C"
MB=87e9d03aa2a4797957ac0124d0c7851a2eec234c; OURS=853ca25ae00fe26b09e019fbfe70893666617fc1
THEIRS=697e17a48e00073c9cd40f40049cd1f0f8ddb033; MERGE=f7e94a0751ff8c3f72d86f9878d89527273294ca
HEAD=43410ce1ec16e08fff22c35115d1fea9a6ed78de
git diff --name-only $MB $THEIRS | sort > "$O/side849.txt"
git diff --name-only $MB $OURS | sort > "$O/side847.txt"
git diff --name-only $OURS $HEAD | sort > "$O/delta.txt"
echo "delta outside 849/842 side:"; comm -23 "$O/delta.txt" "$O/side849.txt"
echo "overlap:"; comm -12 "$O/side847.txt" "$O/side849.txt"
echo "849-only paths differing from 697e17a4:"; git diff --name-only $THEIRS $HEAD -- $(comm -23 "$O/side849.txt" "$O/side847.txt")
echo "847 paths differing from 853ca25a:"; git diff --name-only $OURS $HEAD -- $(cat "$O/side847.txt")
T=$(mktemp -d); f=tb/verilator/milan_dp/README.md
git show $MB:$f > $T/b; git show $OURS:$f > $T/o; git show $THEIRS:$f > $T/t; git show $MERGE:$f > $T/m
git merge-file -p $T/o $T/b $T/t > $T/x && cmp $T/x $T/m && echo "README: merge == clean three-way"
git show $OURS:CHANGELOG.md > $T/co; git show $HEAD:CHANGELOG.md > $T/ch
git diff $MB $THEIRS -- CHANGELOG.md | sed -n 's/^+\([^+].*\)$/\1/p' | while IFS= read -r l; do grep -qxF -- "$l" $T/ch || echo "MISSING 849 line: $l"; done
git diff $MB $OURS -- CHANGELOG.md | sed -n 's/^+\([^+].*\)$/\1/p' | while IFS= read -r l; do grep -qxF -- "$l" $T/ch || echo "MISSING 847 line: $l"; done
grep -n '^## ' $T/ch | sed -n '2,4p'
echo "gitlinks equal:"; [ "$(git ls-tree -r $OURS | awk '$2=="commit"')" = "$(git ls-tree -r $HEAD | awk '$2=="commit"')" ] && echo yes
rm -rf $T

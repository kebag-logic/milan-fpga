#!/bin/sh
# Usage: delta_compare.sh <repo>
# Checks that the merge 9405010f (b5d17214 + dev 45c0b56c) adds exactly dev's
# #835 step (123f57a9..45c0b56c, first parent of dev) except the hand-resolved
# docs/findings/README.md, by (a) file-set equality, (b) per-file blob
# equality of the change, (c) an independent merge-tree replay.
set -u
cd "$1" || exit 2
H=9405010ff5def3275eecda7271a4b1ccc1aa2be0 O=b5d17214f811b48836ecc0cac5adb361454ccfd5
D=45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c B=123f57a922bf07476cd69f91867f3b6f07080804
A=ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36
rc=0
echo "dev first-parent chain from 45c0b56c:"; git log --first-parent --format='  %H %s' -3 $D
echo "merge-base(b5d17214, 45c0b56c) = $(git merge-base $O $D) (expected $B)"
[ "$(git merge-base $O $D)" = "$B" ] || rc=1
echo "literal ac0a01e3..45c0b56c spans $(git diff --name-only $A $D | wc -l) files (#825 + #835); #825's step was absorbed by b5d17214, so the #835 step is 123f57a9..45c0b56c"
echo "== (a) files changed b5d17214..9405010f vs 123f57a9..45c0b56c"
git diff --name-only $O $H > /tmp/.dc_pr.$$; git diff --name-only $B $D > /tmp/.dc_dev.$$
paste /tmp/.dc_pr.$$ /tmp/.dc_dev.$$ | sed 's/^/  /'
cmp -s /tmp/.dc_pr.$$ /tmp/.dc_dev.$$ && echo "  file sets: EQUAL" || { echo "  file sets: DIFFER"; rc=1; }
echo "== (b) per file: does head == dev blob (i.e. the PR-side file equalled the merge base)?"
for f in $(cat /tmp/.dc_dev.$$); do
  o=$(git rev-parse $O:$f) b=$(git rev-parse $B:$f) h=$(git rev-parse $H:$f) d=$(git rev-parse $D:$f)
  if [ "$h" = "$d" ]; then s="head==dev"; elif [ "$o" != "$b" ]; then s="both sides edited (3-way)"; else s="UNEXPECTED"; rc=1; fi
  echo "  $f: $s"
done
rm -f /tmp/.dc_pr.$$ /tmp/.dc_dev.$$
echo "== (c) independent replay: git merge-tree --write-tree b5d17214 45c0b56c"
out=$(git merge-tree --write-tree --name-only $O $D); T=$(echo "$out" | head -1)
echo "$out" | sed 's/^/  /'
echo "  replay tree vs head, files differing:"; git diff --name-only $T $H | sed 's/^/    /'
[ "$(git diff --name-only $T $H)" = "docs/findings/README.md" ] || rc=1
echo "== (d) head vs live dev: name-status (must be #854's own files plus b5d17214's two generator sources)"
git diff --name-status $D $H | sed 's/^/  /'
echo "  of those, head blob == a853461d blob:"
for f in $(git diff --name-only $D $H); do
  [ "$(git rev-parse $H:$f)" = "$(git rev-parse a853461d:$f 2>/dev/null)" ] && echo "    same  $f" || echo "    moved $f"
done
echo "== hdl/ tb/ syn/ scripts/ third_party/ or gitlink paths in b5d17214..9405010f: $(git diff --name-only $O $H -- hdl tb syn scripts third_party sw | wc -l)"
echo "RESULT: $([ $rc = 0 ] && echo PASS || echo FAIL)"
exit $rc

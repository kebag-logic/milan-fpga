#!/bin/sh
# Verify a clone is byte-exact at a head: usage tree_integrity.sh <clone> <head> <tree>
set -u
cd "$1" || exit 2
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $h"; echo "tree $t"
[ "$h" = "$2" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$t" = "$3" ] || { echo "TREE MISMATCH"; rc=1; }
it=$(git write-tree 2>/dev/null); echo "index tree $it"; [ "$it" = "$3" ] || { echo "INDEX MISMATCH"; rc=1; }
git update-index -q --really-refresh >/dev/null 2>&1
d=$(git diff --name-only HEAD --ignore-submodules=none); [ -z "$d" ] && echo "tracked bytes+modes: clean vs HEAD" || { echo "DIFF: $d"; rc=1; }
f=$(git ls-files -v | grep -E '^[a-z]|^S' | head -5); [ -z "$f" ] && echo "no assume-unchanged/skip-worktree flags" || { echo "FLAGS: $f"; rc=1; }
u=$(git status --porcelain --ignored --untracked-files=all | head -5); [ -z "$u" ] && echo "nothing untracked or ignored" || { echo "STATUS: $u"; rc=1; }
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$s" | awk '{print $3}'); have=$(git -C "$s" rev-parse HEAD)
  dirty=$(git -C "$s" status --porcelain --untracked-files=all | head -3)
  echo "gitlink $s want $want have $have dirty:[${dirty}]"
  [ "$want" = "$have" ] && [ -z "$dirty" ] || rc=1
done
echo "external gitlink: $(git ls-tree HEAD external | awk '{print $3}') (not initialised; not a build input)"
echo "RESULT rc=$rc"; exit $rc

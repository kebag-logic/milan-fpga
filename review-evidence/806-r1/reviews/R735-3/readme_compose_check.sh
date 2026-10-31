#!/bin/sh
# Usage: readme_compose_check.sh <repo> ; checks composed milan_dp README against both merge parents
set -u
cd "$1"
F=tb/verilator/milan_dp/README.md
MB=$(git merge-base 71d6ed07a59ec35b703b658edc9157d6b454d131 0c45ebf28e2c11352aa4ad40d46780143b1a77ab)
echo "merge-base $MB"
# 1. every line added by either side appears in the candidate exactly as many times as in that side
for side in 71d6ed07a59ec35b703b658edc9157d6b454d131 0c45ebf28e2c11352aa4ad40d46780143b1a77ab; do
  git diff -U0 $MB $side -- $F | grep '^+' | grep -v '^+++' | cut -c2- > /tmp/added.$$
  n=0; bad=0
  while IFS= read -r l; do n=$((n+1)); c=$(git show HEAD:$F | grep -cxF -- "$l"); s=$(git show $side:$F | grep -cxF -- "$l"); [ "$c" = "$s" ] || { bad=$((bad+1)); echo "MISMATCH side=$side cand=$c side=$s: $l" | cut -c1-160; }; done < /tmp/added.$$
  git diff -U0 $MB $side -- $F | grep '^-' | grep -v '^---' | cut -c2- > /tmp/removed.$$
  r=0; rb=0
  while IFS= read -r l; do r=$((r+1)); c=$(git show HEAD:$F | grep -cxF -- "$l"); [ "$c" = 0 ] || { rb=$((rb+1)); echo "REMOVED-LINE-PRESENT side=$side: $l" | cut -c1-160; }; done < /tmp/removed.$$
  echo "side $side: added $n lines, $bad mismatches; removed $r lines, $rb still present"
done
# 2. mutant table numbering 1..N unique and contiguous
git show HEAD:$F | grep -E '^\| [0-9]+ \| ' | awk -F'|' '{gsub(/ /,"",$2); print $2}' > /tmp/rows.$$
echo "mutant rows: $(wc -l < /tmp/rows.$$), unique $(sort -u /tmp/rows.$$ | wc -l), max $(sort -n /tmp/rows.$$ | tail -1), contiguous=$( [ "$(sort -n /tmp/rows.$$ | tr '\n' ' ')" = "$(seq 1 $(sort -n /tmp/rows.$$ | tail -1) | tr '\n' ' ')" ] && echo yes || echo no)"
# 3. every obj_ binary named in the legs table is a Makefile target and its listed source exists
git show HEAD:$F | grep -oE '^\| `obj_[a-z0-9_]+` \| `[a-z_0-9]+\.cpp`' | sed -E 's/^\| `(obj_[a-z0-9_]+)` \| `([^`]+)`/\1 \2/' | while read o s; do
  t=$(grep -cE "(^|[[:space:]])$o([[:space:]/:]|$)" tb/verilator/milan_dp/Makefile); [ -f tb/verilator/milan_dp/$s ] && e=yes || e=NO
  echo "$o src=$s exists=$e makefile_refs=$t"
done
# 4. make targets named in the README exist in the Makefile
for t in $(git show HEAD:$F | grep -oE 'make [a-z0-9-]+' | awk '{print $2}' | sort -u); do
  grep -qE "^$t:|^\.PHONY:.*[[:space:]]$t([[:space:]]|$)|^$t[[:space:]]*:" tb/verilator/milan_dp/Makefile && echo "target $t present" || echo "target $t not in milan_dp/Makefile"
done

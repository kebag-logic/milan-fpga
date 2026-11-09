#!/usr/bin/env bash
# Portable re-run of this round's merge, line-set, conflict-row, figure and gitlink checks.
# usage: r766_7_checks.sh <clone of kebag-logic/milan-fpga with e70ae2cb, ac0a01e3, 72816d26, 0a75aa77> <output dir>
set -eu
C=$1; O=$2; mkdir -p "$O"; cd "$C"
H=e70ae2cb2dd0746060612493cb6724522b8701bc; DEV=ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36
R6=72816d26a7e2a29db5bc198ff65056ee4c5790b4; OLD=0a75aa774b89ac89351700f63dd8cbb89694af6c
test "$(git rev-parse $H^1) $(git rev-parse $H^2)" = "$R6 $DEV" && echo "parents OK" > "$O/parents.txt"
git diff --stat $DEV $H > "$O/diff_dev_head.stat"
for p in "r6 $OLD $R6" "r7 $DEV $H"; do set -- $p
  git diff -U0 $2 $3 | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' | sort > "$O/lines_$1.txt"; done
diff "$O/lines_r6.txt" "$O/lines_r7.txt" > "$O/lines_r6_vs_r7.diff" && echo "line sets identical" >> "$O/parents.txt"
T=$(git merge-tree --write-tree --name-only $R6 $DEV | head -1 || true)
git diff $T $H > "$O/conflict_resolution.diff" || true
f=docs/findings/README.md
for rev in $DEV $R6 $H; do echo "$rev 234=$(git show $rev:$f | grep '^| \[234_' | sha256sum | cut -c1-16) 649=$(git show $rev:$f | grep '^| \[649_' | sha256sum | cut -c1-16)"; done > "$O/readme_rows.txt"
git diff -U0 $DEV $H | grep '^+' | grep -v '^+++' > "$O/branch_added_lines.txt"
S="docs/design/AREA_BUDGET.md docs/design/MARK_II_AREA_PLAN.md docs/findings/234_PP_SHADOW_AREA_BASELINE.md syn/ooc/pp_resource_baseline.json docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md"
grep -oE '[+-]?[0-9][0-9,]*\.?[0-9]*( %| ns)?' "$O/branch_added_lines.txt" | sed 's/^[+]//' | awk 'length($0)>=3' | sort -u |
while read -r n; do o=0; w=0; for s in $S; do git show $OLD:$s 2>/dev/null | grep -qF -- "$n" && o=1; git show $DEV:$s 2>/dev/null | grep -qF -- "$n" && w=1; done; [ $o != $w ] && echo "MOVED? '$n' old=$o new=$w"; done > "$O/figure_moves.txt" || true
for p in $(git ls-tree -r $H | awk '$2=="commit"{print $4}'); do a=$(git rev-parse $H:$p); b=$(git rev-parse $DEV:$p); echo "$p $a $([ $a = $b ] && echo =dev || echo DIFF)"; done > "$O/gitlinks.txt"
echo done

#!/bin/sh
# Planted controls for fit_check.py: each copies the three pages, plants one
# wrong figure, and requires fit_check.py to fail naming it.
# usage: plant_check.sh <tree> <links-head> <links-prev> <fit-receipts> <scratch> <out>
set -u
tree=$1 lh=$2 lp=$3 fr=$4 sc=$5 out=$6
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
plant() {
  name=$1 file=$2 from=$3 to=$4
  t=$sc/plant-$name
  rm -rf "$t"; mkdir -p "$t/docs/design"
  cp "$tree"/docs/design/SPLIT_CONTROL_MEMORY.md "$tree"/docs/design/MARK_II_AREA_PLAN.md \
     "$tree"/docs/design/AREA_BUDGET.md "$t/docs/design/"
  python3 -I -c 'import sys,pathlib; p=pathlib.Path(sys.argv[1]); s=p.read_text(); assert s.count(sys.argv[2])>=1; p.write_text(s.replace(sys.argv[2],sys.argv[3],1))' \
    "$t/docs/design/$file" "$from" "$to"
  python3 -I "$here/fit_check.py" "$t" "$lh" "$lp" "$fr/ctrl_memory_ooc.tsv" \
    "$fr/size-head-8x8_i2.txt" "$fr/size-prev-8x8_i2.txt" > "$out/$name.log" 2>&1
  rc=$?
  echo "$name rc=$rc $(grep -m1 '^FAIL' "$out/$name.log")"
}
plant stale-ledger-total MARK_II_AREA_PLAN.md '| -10 | -2 | -11 | 114 |' '| -10 | -2 | -11 | 113 |'
plant stale-lut-cells SPLIT_CONTROL_MEMORY.md '| 266 / 34 |' '| 328 / 40 |'
plant stale-headroom SPLIT_CONTROL_MEMORY.md 'with the unused bytes inside them, 5,064 B.' 'with the unused bytes inside them, 7,112 B.'
plant stale-budget-arith AREA_BUDGET.md '`87.5 - 6.5 + 6 - 18 + 54 + 2 = 125`' '`87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`'

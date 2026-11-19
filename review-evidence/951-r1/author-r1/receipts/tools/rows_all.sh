#!/bin/bash
# rows_all.sh: for each finished leg pair (point x arm, base and head), the probe comparison (probe_cmp.py) and each
# group's pass distributions (rows_cmp.py), into cmp/rows/.
S=<scratch>; O=$S/cmp/rows; mkdir -p $O
for p in 1x1 8x8-1if; do for a in none valid-destinations; do
  B=$S/meas/base/$p/$a/results H=$S/meas/head/$p/$a/results
  [ -f $B/results.json ] && [ -f $H/results.json ] || continue
  python3 -I $S/bin/probe_cmp.py $B/results.json $H/results.json > $O/$p-$a-probes.txt
  : > $O/$p-$a-passes.txt
  for l in $(cd $H && ls *.log); do echo "== $p $a ${l%.log}" >> $O/$p-$a-passes.txt; python3 -I $S/bin/rows_cmp.py $B/$l $H/$l >> $O/$p-$a-passes.txt; done
  echo "$p $a: $(grep -E '^verdicts changed|^misses each side' $O/$p-$a-probes.txt | tr '\n' ' ')"
done; done

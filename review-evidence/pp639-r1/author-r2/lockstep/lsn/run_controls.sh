#!/bin/sh
cd "$(dirname "$0")"
out=results-$1; mkdir -p $out
for c in ctl_*.sv; do
  nm=${c%.sv}
  ./build.sh $c 2 obj_$nm || { echo "BUILD FAIL $nm"; exit 3; }
  for s in 1 2 3 4 5 6 7 8; do
    m=0; [ $s -gt 4 ] && m=1
    ./obj_$nm/sim $s 1000000 $m 2 > $out/${nm}_s$s.log 2>&1
    echo "$nm seed=$s rc=$?" >> $out/summary.txt
  done
done

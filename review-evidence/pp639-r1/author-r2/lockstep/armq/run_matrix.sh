#!/bin/sh
# run_matrix.sh <tag>: the head extract at four shapes, then every control at 1x1
cd "$(dirname "$0")"
tag=$1
out=results-$tag; rm -rf $out; mkdir -p $out
for aw in 6 7 5 8; do
  ./build.sh dut.sv $aw obj_dut_$aw || { echo "BUILD FAIL dut $aw"; exit 3; }
  for s in 1 2 3 4 5 6 7 8; do
    m=0; [ $s -gt 4 ] && m=1
    ./obj_dut_$aw/sim $s 1000000 $m > $out/dut_aw${aw}_s$s.log 2>&1
    echo "dut aw=$aw seed=$s rc=$?" >> $out/summary.txt
  done
done
for c in ctl_*.sv; do
  n=${c%.sv}
  ./build.sh $c 6 obj_$n || { echo "BUILD FAIL $n"; exit 3; }
  for s in 1 2 3 4 5 6 7 8; do
    m=0; [ $s -gt 4 ] && m=1
    ./obj_$n/sim $s 1000000 $m > $out/${n}_s$s.log 2>&1
    echo "$n seed=$s rc=$?" >> $out/summary.txt
  done
done
echo done >> $out/summary.txt

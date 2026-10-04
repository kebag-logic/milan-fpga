#!/bin/sh
# run_matrix.sh <tag>: the candidate at five shapes, then every control at 2 sinks
cd "$(dirname "$0")"
tag=$1
out=results-$tag; rm -rf $out; mkdir -p $out
for n in 2 9 8 1 3; do
  ./build.sh dut_listener.sv $n obj_dut_$n || { echo "BUILD FAIL dut $n"; exit 3; }
  for s in 1 2 3 4 5 6 7 8; do
    m=0; [ $s -gt 4 ] && m=1
    ./obj_dut_$n/sim $s 1000000 $m $n > $out/dut_n${n}_s$s.log 2>&1
    echo "dut n=$n seed=$s rc=$?" >> $out/summary.txt
  done
done
for c in ctl_*.sv; do
  nm=${c%.sv}
  ./build.sh $c 2 obj_$nm || { echo "BUILD FAIL $nm"; exit 3; }
  for s in 1 2 3 4 5 6 7 8; do
    m=0; [ $s -gt 4 ] && m=1
    ./obj_$nm/sim $s 1000000 $m 2 > $out/${nm}_s$s.log 2>&1
    echo "$nm seed=$s rc=$?" >> $out/summary.txt
  done
done
echo done >> $out/summary.txt

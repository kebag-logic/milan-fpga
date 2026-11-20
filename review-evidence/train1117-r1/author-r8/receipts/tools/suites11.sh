#!/bin/bash
# suites11.sh CLONE GROUP: the RTL suites #927 touches, at CLONE (RULING-1118c item 1). GROUP a selects one set so
# the sets run in parallel units: dp (milan_dp: split, split-mutants, split-cdc, dynmap, maprec8, maprec4),
# render (milan_dp_render: tdm8render, tdm8render-mutants), meter (aaf_clock_meter: all, mutants),
# mbx (mbx: all, dma-mutants). Each target's rc is printed; the set's rc is 1 if any failed.
. <scratch>/bin/env.sh
C=$1 G=$2
case $G in
  dp) D=milan_dp; TG="split split-mutants split-cdc dynmap maprec8 maprec4";;
  render) D=milan_dp_render; TG="tdm8render tdm8render-mutants";;
  meter) D=aaf_clock_meter; TG="all mutants";;
  mbx) D=mbx; TG="all dma-mutants";;
  *) echo "unknown group $G"; exit 2;;
esac
cd "$C/tb/verilator/$D" || exit 2
echo "HEAD $(git rev-parse --short=8 HEAD) $D start $(date +%T)"
rc=0
for t in $TG; do
  echo "== make $t $(date +%T)"; make -j8 $t; r=$?; echo "== $D $t rc=$r $(date +%T)"; [ $r = 0 ] || rc=1
done
echo "END rc=$rc $(date +%T)"; exit $rc

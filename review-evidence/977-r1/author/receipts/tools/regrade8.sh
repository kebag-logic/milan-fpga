#!/bin/bash
# regrade8.sh POINT VARIANT...: run.py --regrade at round 8's head (r8/meas, ea52ec11) of each VARIANT's every-arm logs at
# POINT against its round-8 build (r8/b/<point>/<variant>, byte-identical in image and model to round 7's). Each group's
# log, script and journal are linked into r8/regrade/<point>/<variant>: round 7's pool runs first
# (r7/arms/<point>/<variant>/s-<group>), then round 8's reruns of the groups ea52ec11 rescripted, which replace them
# (r8/arms/<point>/<variant>/s-<group>).
set -u
T=<scratch>; C=$T/r8/meas P=$1; shift
for v in "$@"; do
  O=$T/r8/regrade/$P/$v; mkdir -p $O
  for d in $T/r7/arms/$P/$v/s-* $T/r8/arms/$P/$v/s-*; do
    [ -d "$d" ] || continue
    for f in $d/*.log $d/*.txt $d/*.journal; do [ -e "$f" ] && ln -sf $f $O/$(basename $f); done
  done
  (cd $C && python3 -B tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $T/r8/b/$P/$v --reuse-build \
     --variant $v --out $O --regrade --record-budget-findings --record-share-findings > $O.out 2>&1)
  echo "REGRADE $P $v rc=$? $(grep -h 'groups graded' $O.out | cut -c1-220)"
done

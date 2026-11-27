#!/bin/bash
# twin.sh CLONE: the twin and its plants, the maps leg and its plant, each target's rc.
cd "$1" || exit 3
echo "HEAD $(git rev-parse --short=8 HEAD) start $(date +%T)"
rc=0
for t in twin twin-plants twin-maps twin-maps-plants; do
  make -C tb/verilator/milan_dp -j8 $t > "<scratch>/units/twin-$t.out" 2>&1; r=$?
  echo "TARGET $t rc=$r $(date +%T) $(tail -n 2 <scratch>/units/twin-$t.out | tr '\n' ' ' | cut -c1-200)"
  [ $r -ne 0 ] && rc=1
done
echo "END rc=$rc $(date +%T)"; exit $rc

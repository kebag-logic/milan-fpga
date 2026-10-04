#!/usr/bin/env bash
# Scratch: build every control at shapes 2/2, 9/9, 3/5 and run 6 seeds x 300,000 cycles each.
set -u
L=$VALIDATION_STORAGE/pp230-a523/lockstep
cd $L
for c in $(ls controls); do
  for shape in "n2 2 2 6 5 23 37" "n9 9 9 7 5 23 37" "n35 3 5 7 4 17 29" "n1 1 1 6 5 23 37"; do
    set -- $shape
    o=$L/cb/$c-$1
    ./build.sh $L/controls/$c $o $2 $3 $4 $5 $6 $7 > /dev/null 2>&1 || { echo "$c $1 BUILD-FAIL"; continue; }
    tot=0; runs=0
    for sd in 101 102 103 104 105 106; do
      out=$($o/obj/Vlockstep $sd 300000 $((sd % 2)))
      m=$(echo "$out" | sed -n 's/.*mismatch_cycles=\([0-9]*\) internal_mismatch_cycles=\([0-9]*\).*/\1 \2/p')
      set -- $m
      tot=$((tot + $1 + $2)); runs=$((runs + 1))
    done
    echo "$c $shape -> mismatch_cycles(top+internal)=$tot over $runs runs"
    rm -rf $o/obj
  done
done

#!/bin/sh
# Robustness probe: the committed walk arms at shapes beyond the four the
# Makefile runs, and at further random-reset seeds. usage: <tree> <receipt-dir>
set -u
tree=$1; out=$2; mkdir -p "$out"
cd "$tree/tb/srp_stream_fsms" || exit 2
rc=0
for s in 4x4 8x8 16x16 1x9 9x1 2x3 3x2 5x16; do
  make --no-print-directory walk SHAPE=$s > "$out/walk-$s.log" 2>&1 || rc=1
  tail -1 "$out/walk-$s.log"
done
for s in 1x1 2x2 3x5 9x9; do
  [ -x obj_walk_$s/Vsrp_walk_sim ] || make --no-print-directory walk SHAPE=$s > /dev/null 2>&1
  for seed in 1 2 3 4 5 6 7 8; do
    ./obj_walk_$s/Vsrp_walk_sim +verilator+rand+reset+2 +verilator+seed+$seed > "$out/seed-$s-$seed.log" 2>&1 || rc=1
    echo "$s seed $seed: $(tail -1 "$out/seed-$s-$seed.log")"
  done
done
echo "rc=$rc"
exit $rc

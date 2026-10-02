#!/bin/sh
# Run the R421-3 random-press probe binary (built from a tree with
# r421_3_random.py applied) over seeds, at most 8 at a time.
# Usage: run_random.sh BIN OUTDIR STEPS
BIN=$1; OUT=$2; STEPS=$3
mkdir -p "$OUT"
for st in 0 1; do
  for s in 0x11 0x22 0x33 0x44 0x55 0x66 0x77 0x88; do
    echo "$s $st"
  done
done | xargs -P 8 -n 2 sh -c 'R421_SEED=$0 R421_STALL=$1 R421_STEPS='"$STEPS"' "'"$BIN"'" > "'"$OUT"'/seed_$0_stall_$1.log" 2>&1; echo "seed $0 stall $1 rc=$?"'

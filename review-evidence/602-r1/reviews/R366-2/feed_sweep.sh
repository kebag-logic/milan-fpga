#!/bin/sh
# R366-2: run the clean head gmstep binary at every GMSTEP_FEED_DELAY 0..41, 8 at a time.
# Usage: feed_sweep.sh <obj dir with Vmilan_dp_gmstep and aemi.bin> <suite dir> <out dir>
OBJ=$1; SUITE=$2; OUT=$3
mkdir -p "$OUT"
seq 0 41 | xargs -P 8 -I{} sh -c "cd '$SUITE' && '$OBJ/Vmilan_dp_gmstep' '$OBJ/aemi.bin' {} > '$OUT/feed_{}.log' 2>&1; echo \"feed {} rc=\$?\" >> '$OUT/rc.txt'"

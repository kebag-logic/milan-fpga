#!/bin/sh
# Free-running passages (sel low) across one tick, [G9] geometry, with
# 0..W edges of marker delivery jitter.   passweep.sh <lockprobe_binary> <out>
set -eu
BIN=$1; OUT=$2
{
  for j in 0 1 2; do
    for seed in 0x74A197 0x1234 0xBEEF 0x5A5A5; do
      echo "2063 $j $seed plan 10000000 1"
      echo "20 $j $seed fast 10000000 1"
    done
  done
} | LP_PASS=1 xargs -P 8 -L 1 "$BIN" | sort > "$OUT"
cat "$OUT"

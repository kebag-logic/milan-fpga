#!/bin/sh
# Run the raced-lock probe over engagement phases x jitter widths x rate
# directions, 8 jobs at a time.   sweep.sh <lockprobe_binary> <out_file> [jitters]
set -eu
BIN=$1; OUT=$2; JITS=${3:-"0 1 2 4"}
LEADS="0 1 2 3 5 8 12 15 16 17 20 40 60 1041 2023 2043 2063 2066 2067 2068 2070 2075 2080 2081 2082 2083"
{
  for rate in plan fast; do
    for j in $JITS; do
      for l in $LEADS; do
        echo "$l $j ${SEED:-0x74A197} $rate ${SETTLE:-200000000} 5"
      done
    done
  done
} | xargs -P 8 -L 1 "$BIN" | sort -t= -k2,2n > "$OUT"
grep -c VERDICT=CLEAN "$OUT" || true
grep -c VERDICT=COUNTS "$OUT" || true

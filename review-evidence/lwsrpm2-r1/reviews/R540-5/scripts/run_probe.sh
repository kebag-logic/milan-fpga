#!/bin/sh
# Usage: run_probe.sh SRC OUTDIR PROFILE(0|1)  -- build probe_r5 against SRC with sanitizers and run it.
SRC=$1; OUT=$2; M=$3; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
cc -std=c11 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer -DLWSRP_MILAN=$M \
  -I"$SRC/src/include" -I"$SRC/src" -I"$SRC/tests/unit" "$HERE/probe_r5.c" \
  "$SRC/src/core/mrp_mad.c" "$SRC/src/core/mrp_pdu.c" "$SRC/src/modules/msrp.c" \
  "$SRC/src/ports/timer.c" "$SRC/tests/unit/fault_alloc.c" -o "$OUT/probe_r5_$M" || exit 3
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 "$OUT/probe_r5_$M"

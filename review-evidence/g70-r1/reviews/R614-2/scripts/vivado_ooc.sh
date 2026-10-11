#!/bin/sh
# Run `make ooc` in an exported tree under the shared exclusive Vivado lock,
# then copy the logs, the six reports and the make transcript to OUTDIR.
# Usage: vivado_ooc.sh TREE OUTDIR [LOCK]
set -u
TREE=$1
OUT=$2
LOCK=${3:-$VIVADO_LOCK}
mkdir -p "$OUT"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/start.txt"
flock -x -w 540 "$LOCK" make -j16 -C "$TREE" ooc > "$OUT/make_ooc.txt" 2>&1
RC=$?
echo "$RC" > "$OUT/rc.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/end.txt"
for f in ucpu_ooc.log engine_ooc.log ucpu_util.rpt ucpu_util_hier.rpt ucpu_timing.rpt \
         engine_util.rpt engine_util_hier.rpt engine_timing.rpt; do
    [ -f "$TREE/syn/ooc/work/$f" ] && cp "$TREE/syn/ooc/work/$f" "$OUT/$f"
done
cat "$OUT/rc.txt"
exit "$RC"

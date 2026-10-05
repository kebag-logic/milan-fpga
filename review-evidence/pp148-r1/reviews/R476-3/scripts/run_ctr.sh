#!/bin/sh
# Run tb/pp_top/ctr_mutants.py from a git-archive extraction with the pinned simulator.
# Usage: run_ctr.sh TREE OUTDIR JOBS [ONLY]
# Writes OUTDIR/driver.log and OUTDIR/rc; arm logs go to OUTDIR/logs/.
set -u
TREE=$1 OUT=$2 JOBS=$3 ONLY=${4:-}
VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
export VERILATOR
mkdir -p "$OUT/logs"
{
  echo "tree: $TREE"; echo "verilator: $VERILATOR"; "$VERILATOR" --version
  echo "start: $(date -u +%FT%TZ)"
} > "$OUT/driver.log" 2>&1
if [ -n "$ONLY" ]; then
  python3 "$TREE/tb/pp_top/ctr_mutants.py" --output "$OUT/logs" --jobs "$JOBS" --only "$ONLY" >> "$OUT/driver.log" 2>&1
else
  python3 "$TREE/tb/pp_top/ctr_mutants.py" --output "$OUT/logs" --jobs "$JOBS" >> "$OUT/driver.log" 2>&1
fi
rc=$?
echo "end: $(date -u +%FT%TZ)" >> "$OUT/driver.log"
echo "$rc" > "$OUT/rc"

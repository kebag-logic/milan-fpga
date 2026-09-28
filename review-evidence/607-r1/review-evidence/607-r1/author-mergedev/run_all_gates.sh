#!/bin/sh
# Run every gate mode in sequence, one writer in the lane at a time; each mode keeps its own receipt.
set -u
here=$(cd "$(dirname "$0")" && pwd)
logs=$VALIDATION_STORAGE/607-a427
for mode in pins hooks builder live docs; do
    python3 -B "$here/run_gates.py" "$mode" > "$logs/driver-$mode.log" 2>&1
    echo "MODE $mode rc=$?"
done
echo "ALL MODES DONE"

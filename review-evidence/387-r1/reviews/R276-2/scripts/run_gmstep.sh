#!/bin/sh
# Run a built gmstep binary from the suite directory (its ROMs load by
# relative name) at one feed delay; prints the checker output.
# Usage: run_gmstep.sh <clone> <mdir> <feed delay>
set -u
repo=$1; mdir=$2; delay=$3
cd "$repo/tb/verilator/milan_dp"
"$mdir/Vmilan_dp_gmstep" "$mdir/aemi.bin" "$delay"
echo "EXIT=$?"

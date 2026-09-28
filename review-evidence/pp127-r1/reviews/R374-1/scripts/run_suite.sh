#!/usr/bin/env bash
# Usage: run_suite.sh <tree> <suite> [RUN_ARGS]  -- builds one tb/<suite> with the
# pinned simulator, capped at 8 compile jobs; prints the log to stdout.
set -u
VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator}
tree=$1; suite=$2; args=${3:-}
cd "$tree/tb/$suite" || exit 2
rm -rf obj_dir
vf=$(make -pn 2>/dev/null | sed -n 's/^VFLAGS = //p' | head -1 | sed 's/-j 0/-j 8/')
make VERILATOR="$VERILATOR" VFLAGS="$vf" RUN_ARGS="$args" 2>&1
echo "EXIT=$?"

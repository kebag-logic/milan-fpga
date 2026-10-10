#!/usr/bin/env bash
# run_gmstep.sh <clone-root> <log-dir>
# Builds and runs the parent's milan_dp gmstep leg at the clone's head with the
# pinned simulator; the model directory is outside the clone.
set -u
root=$1; logs=$2
mkdir -p "$logs"
export PYTHONDONTWRITEBYTECODE=1
mdir=$(realpath --relative-to="$root/tb/verilator/milan_dp" "$(dirname "$logs")/../scratch/obj_gmstep_head")
make -C "$root/tb/verilator/milan_dp" gmstep \
  VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=8 \
  GMSTEP_MDIR="$mdir" > "$logs/gmstep-head.log" 2>&1
echo $? > "$logs/gmstep-head.rc"

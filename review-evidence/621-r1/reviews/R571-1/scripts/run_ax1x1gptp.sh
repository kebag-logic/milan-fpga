#!/usr/bin/env bash
# run_ax1x1gptp.sh <clone-root> <log-dir> : the physical-clock ax1x1gptp leg
# (default windows) at the clone's head with the pinned simulator.
set -u
export PYTHONDONTWRITEBYTECODE=1
make -C "$1/tb/verilator/milan_dp" ax1x1gptp \
  VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator > "$2/ax1x1gptp-head.log" 2>&1
echo $? > "$2/ax1x1gptp-head.rc"

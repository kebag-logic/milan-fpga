#!/usr/bin/env bash
# run_phc.sh <clone-root> <name> <work-dir> <log-dir> [phc_step.py args...]
# Runs the parent's real-counter PHC step regression with the pinned simulator
# and records its output and exit status as <log-dir>/<name>.log / .rc.
set -u
root=$1; name=$2; work=$3; logs=$4; shift 4
export VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
export VERILATOR_JOBS=${VERILATOR_JOBS:-2}
export PYTHONDONTWRITEBYTECODE=1
rm -rf "$work"; mkdir -p "$work" "$logs"
python3 -I "$root/tb/verilator/gptp_plane/phc_step.py" --work "$work" "$@" > "$logs/$name.log" 2>&1
echo $? > "$logs/$name.rc"

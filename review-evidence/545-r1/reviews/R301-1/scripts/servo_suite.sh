#!/usr/bin/env bash
# Extract the exact head tree subset into scratch and run the mmcm_servo
# default target (unit, rails, #539 step, #545 slew suite, slew mutants).
set -u
REPO=${REPO:-$REVIEWS/r301-1-545}
PKT=${PKT:-$REVIEWS/545-r301-1-packet}
HEAD=fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4
VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
T="$PKT/scratch/tree"
rm -rf "$T"; mkdir -p "$T"
git -C "$REPO" archive "$HEAD" hdl tb/common tb/verilator/mmcm_servo tb/verilator/mmcm_servo_autorepair | tar -x -C "$T"
"$VERILATOR" --version
make -C "$T/tb/verilator/mmcm_servo" VERILATOR="$VERILATOR" 2>&1

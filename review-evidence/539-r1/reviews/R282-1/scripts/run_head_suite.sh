#!/bin/sh
# Build and run tb/verilator/mmcm_servo (unit, rails, phc_step) at the exact head,
# from a git-archive export, with the pinned simulator and -j 8.
set -eu
. "$(dirname "$0")/env.sh"
W="$PKT/scratch/head"
rm -rf "$W"; mkdir -p "$W"
git -C "$CLONE" archive "$HEAD_SHA" hdl tb/common tb/verilator/mmcm_servo tb/verilator/mmcm_servo_autorepair | tar -x -C "$W"
"$VERILATOR" --version
make -C "$W/tb/verilator/mmcm_servo" VERILATOR="$VERILATOR" VFLAGS="$VFLAGS_R" run
echo "mmcm_servo exit=$?"
make -C "$W/tb/verilator/mmcm_servo_autorepair" VERILATOR="$VERILATOR" VFLAGS="$VFLAGS_R" run
echo "mmcm_servo_autorepair exit=$?"

#!/bin/sh
# Export the exact head into a disposable tree and run tb/verilator/mmcm_servo
# (unit, rails, silicon-scale step harness) with at most 8 build jobs.
# Usage: run_servo_suite.sh <repo> <scratch_dir> <verilator>
set -eu
REPO=${1:?repo}; S=${2:?scratch}; VL=${3:?verilator}
H=324eb343a870973b64706779d0183ae342dcb3d7
rm -rf "$S/servo_head"; mkdir -p "$S/servo_head"
git -C "$REPO" archive "$H" hdl tb/verilator/mmcm_servo tb/common | tar -x -C "$S/servo_head"
"$VL" --version
cd "$S/servo_head/tb/verilator/mmcm_servo"
make VERILATOR="$VL" VFLAGS='--cc --exe --build -j 8 -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"' run
echo "SERVO_SUITE rc=$?"

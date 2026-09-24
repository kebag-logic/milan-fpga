#!/bin/sh
# Disposable probe: raise STEP_DET_NS_C above the 20 us link-up step in an exported copy; the step suite must fail.
# Usage: run_mutant_stepdet.sh <export-dir-from-run_servo_suite> <verilator> <newvalue, e.g. 24576>
set -eu
D=$1; V=$2; N=$3
sed -i "s/localparam logic \[31:0\] STEP_DET_NS_C = 32'd4096;/localparam logic [31:0] STEP_DET_NS_C = 32'd$N;/" "$D/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
grep -n "STEP_DET_NS_C =" "$D/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
cd "$D/tb/verilator/mmcm_servo" && rm -rf obj_phc
VF='--cc --exe --build -j 8 -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
MAKEFLAGS= make VERILATOR="$V" VFLAGS="$VF" phc_step_build >/dev/null
./obj_phc/Vphc_step || echo "step suite rc=$? (non-zero expected)"

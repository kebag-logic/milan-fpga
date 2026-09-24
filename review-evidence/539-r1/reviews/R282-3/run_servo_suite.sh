#!/bin/sh
# Rebuild and run the three mmcm_servo harnesses at an exact commit in a disposable export.
# Usage: run_servo_suite.sh <repo> <commit> <verilator> <outdir>   (jobs capped at 8)
set -eu
R=$1; C=$2; V=$3; O=$4
rm -rf "$O" && mkdir -p "$O"
git -C "$R" archive "$C" hdl tb/verilator/mmcm_servo tb/common | tar -x -C "$O"
cd "$O/tb/verilator/mmcm_servo"
VF='--cc --exe --build -j 8 -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
MAKEFLAGS= make VERILATOR="$V" VFLAGS="$VF" all

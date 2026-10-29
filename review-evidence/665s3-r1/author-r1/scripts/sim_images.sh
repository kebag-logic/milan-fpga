#!/bin/bash
# The split boot simulation at both points, then the images at the four points with the simulation's runtime.
# (The self-test's plants ran at this head in [A697]'s session; its log is kept.)
# usage: sim_images.sh CLONE BUILD_ROOT LOG_DIR
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697b/scripts
C=$1 B=$2 L=$3
mkdir -p "$L"
bash $S/gate.sh "$C" "$L/split_boot-1x1.log" . python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-1x1"
bash $S/gate.sh "$C" "$L/split_boot-8x8.log" . python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-8x8" --shape endstation_ax7101_8x8
bash $S/images.sh "$C" "$B" "$B/images" "$L"

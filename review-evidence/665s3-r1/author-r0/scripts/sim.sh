#!/bin/bash
# The split boot simulation at both points and its self-test, one after another, from a clone.
# usage: sim.sh CLONE BUILD_ROOT LOG_DIR
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697/scripts
C=$1 B=$2 L=$3
mkdir -p "$L"
bash $S/gate.sh "$C" "$L/split_boot-1x1.log" . python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-1x1"
bash $S/gate.sh "$C" "$L/split_boot-8x8.log" . python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-8x8" --shape endstation_ax7101_8x8
bash $S/gate.sh "$C" "$L/split_boot-selftest.log" . python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-plants" --self-test

#!/bin/bash
# The split boot simulation at both points, each regraded from its saved log and status, then its native
# controls alone and its self-test (the native controls, then both plants), one after another, from a clone.
# usage: boot.sh CLONE BUILD_ROOT LOG_DIR
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697d/scripts
C=$1 B=$2 L=$3
mkdir -p "$L"
R=tb/verilator/ctrl_split_boot/run.py
bash $S/gate.sh "$C" "$L/split_boot-1x1.log" . python3 -B $R --build-dir "$B/boot-1x1"
bash $S/gate.sh "$C" "$L/split_boot-1x1-regrade.log" . python3 -B $R --build-dir "$B/boot-1x1" --regrade
bash $S/gate.sh "$C" "$L/split_boot-8x8.log" . python3 -B $R --build-dir "$B/boot-8x8" --shape endstation_ax7101_8x8
bash $S/gate.sh "$C" "$L/split_boot-8x8-regrade.log" . python3 -B $R --build-dir "$B/boot-8x8" \
    --shape endstation_ax7101_8x8 --regrade
bash $S/gate.sh "$C" "$L/split_boot-native-controls.log" . python3 -B $R --build-dir "$B/boot-native" --native-controls
bash $S/gate.sh "$C" "$L/split_boot-selftest.log" . python3 -B $R --build-dir "$B/boot-plants" --self-test
for p in 1x1 8x8; do cp "$B/boot-$p/sim.status" "$L/split_boot-$p.sim.status"; done
echo "boot done $(date)" > "$L/boot.done"

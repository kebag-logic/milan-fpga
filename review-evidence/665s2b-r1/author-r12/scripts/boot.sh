#!/bin/bash
# The split boot simulation at both shapes, the regrade, the controls and the planted self-test, from a checkout.
# usage: boot.sh CHECKOUT OUT
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/env.sh
C=$1 B=$2
L=$VALIDATION_STORAGE/665s2b-a683o/logs
cd "$C"
go() { n=$1; shift; { echo "HEAD $(git -C "$C" rev-parse HEAD)"; echo "\$ $*"; "$@"; echo "rc=$?"; } > "$L/boot-$n.log" 2>&1; }
go 1x1 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/1x1" &
go 8x8 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/8x8" --shape endstation_ax7101_8x8 &
wait
go native python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/native" --native-controls
go plants python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/plants" --self-test

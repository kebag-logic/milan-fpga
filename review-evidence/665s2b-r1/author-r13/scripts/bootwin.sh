#!/bin/bash
# The round-12 head's boot with only the product's flash window added, at both shapes.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p; C=$T/HB; L=$T/logs
cd $C
go() { n=$1; shift; { echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; echo "\$ $*"; "$@"; echo "rc=$?"; } > "$L/bootwin-$n.log" 2>&1; }
go 1x1 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $T/boot-HB/1x1 &
go 8x8 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $T/boot-HB/8x8 --shape endstation_ax7101_8x8 &
wait

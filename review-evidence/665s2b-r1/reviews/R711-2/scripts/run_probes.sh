#!/bin/bash
# Reviewer probes: the patched harness at 8x8/2if, then the boot simulation with the product's uncached flash window.
PK=$(cd "$(dirname "$0")/.." && pwd)
. $PK/scripts/env.sh
S=$PK/scratch; L=$S/logs; mkdir -p $L
( cd $S/probe && python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/b/x8 \
    --groups x-links-quiet,x-links-same,x-links-1ms,x-links-2ms,x-save-0,x-save-1,x-save-2,x-save-3,x-save-4,x-save-5 \
    --record-budget-findings --record-share-findings --jobs 10 > $L/x8.log 2>&1; echo $? > $L/x8.rc ) &
until [ -x $S/b/x8/native/Vsim ] || [ -f $L/x8.rc ]; do python3 -c 'import time; time.sleep(10)'; done
( cd $S/probe-boot && python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/b/boot-u8 --shape endstation_ax7101_8x8 > $L/boot-u8.log 2>&1; echo $? > $L/boot-u8.rc ) &
until [ -x $S/b/boot-u8/native/Vsim ] || [ -f $L/boot-u8.rc ]; do python3 -c 'import time; time.sleep(10)'; done
( cd $S/probe-boot && python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/b/boot-u1 > $L/boot-u1.log 2>&1; echo $? > $L/boot-u1.rc ) &
wait

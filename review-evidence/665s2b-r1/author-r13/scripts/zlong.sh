#!/bin/bash
# The head's save alone, run to 5.2 s after its change (R711-2's z-save, its wait lengthened), on the reproduction's build.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
cd $T/P0
{ python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $T/builds/P0-A8 --reuse-build --out $T/builds/P0-A8/results-zlong --groups z-save --record-budget-findings --record-share-findings --jobs 1; echo "rc=$?"; } > $T/logs/P0-zlong.log 2>&1

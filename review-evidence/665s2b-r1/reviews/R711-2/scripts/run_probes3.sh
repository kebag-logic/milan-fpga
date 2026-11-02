#!/bin/bash
# Reviewer probes, third batch: one whole save at 8x8/2if on the reused build.
PK=$(cd "$(dirname "$0")/.." && pwd)
. $PK/scripts/env.sh
S=$PK/scratch; L=$S/logs
cd $S/probe && python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/b/x8 --reuse-build \
    --out $S/b/x8/results3 --groups z-save --record-budget-findings --record-share-findings --jobs 2 > $L/z8.log 2>&1; echo $? > $L/z8.rc

#!/bin/bash
# Reviewer probes, second batch: reuse the patched harness's 8x8 build.
PK=$(cd "$(dirname "$0")/.." && pwd)
. $PK/scripts/env.sh
S=$PK/scratch; L=$S/logs
cd $S/probe && python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/b/x8 --reuse-build \
    --out $S/b/x8/results2 --groups y-links,y-save-0,y-save-1,y-save-2,y-save-3,y-save-4,y-save-5,y-save-6,y-save-7 \
    --record-budget-findings --record-share-findings --jobs 10 > $L/y8.log 2>&1; echo $? > $L/y8.rc

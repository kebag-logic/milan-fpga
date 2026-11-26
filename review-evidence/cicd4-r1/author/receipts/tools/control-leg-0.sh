#!/bin/bash
set -euo pipefail
export TMPDIR=$VALIDATION_STORAGE/cicd4-a839/tmp CCACHE_DIR=$VALIDATION_STORAGE/ccache
cd $LANES/cicd-1008
perf stat -e cycles:u,instructions:u,task-clock -o $MANAGEMENT/2026-09-23/cicd4-a839/receipts/local/control-0.perf.txt -- /usr/bin/time -v python3 -u sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4 --campaign-shard 0 4 --build-dir $VALIDATION_STORAGE/cicd4-a839/control-0 > $MANAGEMENT/2026-09-23/cicd4-a839/receipts/local/control-0.log 2> $MANAGEMENT/2026-09-23/cicd4-a839/receipts/local/control-0.time

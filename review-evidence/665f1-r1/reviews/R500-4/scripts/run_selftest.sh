#!/bin/sh
# Re-run (foreground) of the lane self-test at the review head: the 1x1 shape's
# 42 checks, then all planted defects (the clock defect is graded at the Arty
# shape it names). Usage: run_selftest.sh <clone> <packet>
set -u
CLONE=$1; P=$2
export TMPDIR=$P/scratch/tmp
cd "$CLONE" || exit 2
python3 -u sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test \
  --config configs/endstation_ax7101_1x1_tdm8.yaml > "$P/receipts/selftest.log" 2>&1
echo $? > "$P/receipts/selftest.rc"

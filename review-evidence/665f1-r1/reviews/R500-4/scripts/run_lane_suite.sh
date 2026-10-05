#!/bin/sh
# Run the #665 F1 lane suite at the review head: one process per shape, plus
# the self-test (1x1 shape, then every planted defect), each with its own log
# and rc file. Usage: run_lane_suite.sh <clone> <packet>
set -u
CLONE=$1; P=$2
export TMPDIR=$P/scratch/tmp
cd "$CLONE" || exit 2
for s in endstation_arty_current endstation_ax7101_1x1_tdm8 endstation_arty_4x4 endstation_arty_8ch endstation_ax7101_8x8; do
  ( python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --config configs/$s.yaml \
      > "$P/receipts/suite_$s.log" 2>&1; echo $? > "$P/receipts/suite_$s.rc" ) &
done
( python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test \
    --config configs/endstation_ax7101_1x1_tdm8.yaml > "$P/receipts/selftest.log" 2>&1; \
  echo $? > "$P/receipts/selftest.rc" ) &
wait

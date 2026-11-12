#!/bin/bash
# Early checks on clone E1 (the current head), before the final pass: the firmware coverage gate and the firmware
# suites (every arm, no campaign), each its log and rc.
T=<scratch>
. $T/scripts/env.sh
cd $T/E1 || exit 3
export TMPDIR=$T/tmp/early MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p $TMPDIR
python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 8 > $T/logs/early-coverage.log 2>&1; echo $? > $T/logs/early-coverage.log.rc
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 8 > $T/logs/early-suites.log 2>&1; echo $? > $T/logs/early-suites.log.rc

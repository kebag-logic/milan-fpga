#!/bin/bash
# dev 6714181d's rtl-fast firmware-unit commands, at the merged content (builder export).
cd $VALIDATION_STORAGE/645-a531/round2c/functional/builder || exit 2
O=$VALIDATION_STORAGE/645-a531/round2c/functional/firmware-unit-m
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$VALIDATION_STORAGE/645-a531/round2c/tmp
run() { n=$1; shift; echo "$(date +%T) START $n $*" >> $O/driver.log; "$@" > $O/$n.log 2>&1; rc=$?; echo $rc > $O/$n.rc; echo "$(date +%T) DONE $n $rc" >> $O/driver.log; }
run tally-selftest python3 sw/firmware/gtest/tally_selftest.py
run ctrl-firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py
run ctrl-nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
run coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4

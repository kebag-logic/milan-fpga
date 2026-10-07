#!/bin/bash
# dev 910f338d's rtl-fast firmware-unit commands at the 886e1620 content (builder export).
cd $VALIDATION_STORAGE/645-a531/round2c/functional/builder || exit 2
O=$VALIDATION_STORAGE/645-a531/round2c/functional/gates-j/firmware
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$VALIDATION_STORAGE/645-a531/round2c/tmp
run() { n=$1; shift; echo "$(date +%T) START $n $*" >> $O/driver.log; "$@" > $O/$n.log 2>&1; rc=$?; echo $rc > $O/$n.rc; echo "$(date +%T) DONE $n $rc" >> $O/driver.log; }
run tally-selftest python3 sw/firmware/gtest/tally_selftest.py
run rv32-sdk-selftest python3 scripts/ci_rv32_sdk_selftest.py
run fw-rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
run ctrl-firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
run ctrl-nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
run coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
rc=0; for f in $O/*.rc; do [ "$(cat $f)" = 0 ] || rc=1; done; exit $rc

#!/bin/bash
# Gates that read what the dev d51b373a merge changed (sw/firmware/ctrl,
# ctrl_nvm, gtest), at 701b8332 in the merge export: the mbx suite through the
# two-slot simulator shim, then dev's rtl-fast firmware-unit commands.
W=$VALIDATION_STORAGE/645-a531/round2d/functional
cd $W/merge || exit 2
O=$W/merge-gates
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$VALIDATION_STORAGE/645-a531/round2d/tmp MAKEFLAGS=-j8 VERILATOR_JOBS=2
export VERILATOR=$W/run-simulator-limited PATH=$W/shims:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
run() { n=$1; shift; echo "$(date +%T) START $n $*" >> $O/driver.log; "$@" > $O/$n.log 2>&1; rc=$?; echo $rc > $O/$n.rc; echo "$(date +%T) DONE $n $rc" >> $O/driver.log; }
run mbx timeout 7200 make -C tb/verilator/mbx
run tally-selftest python3 sw/firmware/gtest/tally_selftest.py
run rv32-sdk-selftest python3 scripts/ci_rv32_sdk_selftest.py
run fw-rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
run ctrl-firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
run ctrl-nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
run coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
rc=0; for f in $O/*.rc; do [ "$(cat $f)" = 0 ] || rc=1; done; exit $rc

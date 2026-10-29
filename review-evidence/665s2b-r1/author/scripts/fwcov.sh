#!/bin/bash
# fw_coverage.py --check, then the RV32 self-test, in one checkout, each through gate.sh.
# usage: fwcov.sh CHECKOUT LOGPREFIX
S=$MANAGEMENT/2026-09-23/665s2b-a683l/scripts
bash $S/gate.sh "$1" "$2-fw_coverage-check.log" . python3 sw/firmware/gtest/fw_coverage.py --check
bash $S/gate.sh "$1" "$2-fw_rv32_selftest.log" . python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32

#!/usr/bin/env bash
# Scratch: the hosted firmware-unit job's firmware steps under one capture, in the CI-parity container, each timed.
# usage: fullcap.sh <tree> <capture>
set -u
tree=$1; cap=$2
cd "$tree" || exit 2
c() { local start=$SECONDS; python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$cap" -- "$@"; echo "rc=$? after $((SECONDS - start)) s: $*"; }
date -u +%FT%TZ
c python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
c python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
c python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
c python3 sw/firmware/gtest/fw_coverage.py --selftest
c python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
date -u +%FT%TZ
echo DONE

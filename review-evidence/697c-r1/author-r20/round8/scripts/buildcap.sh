#!/usr/bin/env bash
# Scratch: the four firmware builders' commands of ctrl_configs.BUILDERS (their builds), each under one capture,
# timed, as the gate's standalone run makes them.
# usage: buildcap.sh <tree> <capture>
set -u
tree=$1; cap=$2
cd "$tree" || exit 2
c() { local start=$SECONDS; python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$cap" -- "$@" > "$cap.$(basename "$2").log" 2>&1; echo "rc=$? after $((SECONDS - start)) s: $*"; }
date -u +%FT%TZ
c python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
c python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
c python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4
c python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
date -u +%FT%TZ
echo DONE

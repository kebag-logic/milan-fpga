#!/usr/bin/env bash
# #799: the local firmware gate set (docs/testing/CI_WORKFLOWS.md, the firmware block), one at a time in a clean
# clone at <rev>, --jobs 8 inside this session's unit. ctrl_boundary runs under the LiteX interpreter.
# usage: fw_all.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692; C=$X/clone-fw-${rev:0:8}; O=$X/r/firmware-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O" "$X/home-fw"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export HOME=$X/home-fw
git rev-parse HEAD > "$O/head.txt"
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table.txt"; }
run fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
run tally_selftest python3 sw/firmware/gtest/tally_selftest.py --mutants
run test_ctrl_firmware_shards python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
run fw_coverage_selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run test_ctrl_firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 8
run test_ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8
run fw_coverage_check python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8
run ctrl_boundary "$LITEX_PYTHON" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo FW-DONE >> "$O/table.txt"

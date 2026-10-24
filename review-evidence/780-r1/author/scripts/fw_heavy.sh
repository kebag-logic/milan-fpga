#!/usr/bin/env bash
# #780: the rest of the local firmware gate set (docs/testing/CI_WORKFLOWS.md, the firmware block), one at a time
# in the clean clone at the head, --jobs 8 inside this session's unit. ctrl_boundary runs under the LiteX
# interpreter (it imports migen through sw/litex/test_ctrl_memory.py).
set -u
X=$VALIDATION_STORAGE/scratch/780-a670; O=$X/r/firmware; D=$(cd "$(dirname "$0")" && pwd)
cd $X/clone-fw || exit 2
source $D/env.sh; source $D/fw_env.sh; export HOME=$X/home-fw
run() { n=$1; shift; s=$(date +%s); "$@" > $O/$n.log 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> $O/table.txt; }
run test_ctrl_firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 8
run test_ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8
run fw_coverage_check python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8
run ctrl_boundary "$LITEX_PYTHON" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
git status --porcelain --untracked-files=no > $O/clone-status-after.txt
echo FW-HEAVY-DONE >> $O/table.txt

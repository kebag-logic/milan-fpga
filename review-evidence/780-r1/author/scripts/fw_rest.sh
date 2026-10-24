#!/usr/bin/env bash
# #780: the two firmware gates the host reset cut (fw_coverage --check, ctrl_boundary), in the clean clone at the head.
set -u
X=$VALIDATION_STORAGE/scratch/780-a670; O=$X/r/firmware; D=$(cd "$(dirname "$0")" && pwd)
cd $X/clone-fw || exit 2
source $D/env.sh; source $D/fw_env.sh; export HOME=$X/home-fw
run() { n=$1; shift; s=$(date +%s); "$@" > $O/$n.log 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> $O/table.txt; }
run fw_coverage_check python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8
run ctrl_boundary "$LITEX_PYTHON" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
git status --porcelain --untracked-files=no > $O/clone-status-after.txt
echo FW-HEAVY-DONE >> $O/table.txt

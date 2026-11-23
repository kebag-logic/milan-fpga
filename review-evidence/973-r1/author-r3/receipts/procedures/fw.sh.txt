#!/bin/bash
# fw.sh CLONE SHARD JOBS BUILD: one shard of the firmware gate (test_ctrl_firmware.py --require-rv32 --self-test) on CLONE.
export MAKEFLAGS="-j$3 --no-print-directory"
cd "$1" && echo "HEAD $(git rev-parse --short=8 HEAD) dirty $(git status --porcelain --untracked-files=no | wc -l) shard $2/4 start $(date +%T)" && \
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs "$3" --shard "$2/4" --build-dir "$4"; rc=$?
echo "END rc=$rc $(date +%T)"; exit $rc

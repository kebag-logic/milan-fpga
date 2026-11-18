#!/bin/bash
# fw.sh CLONE SHARD JOBS: one firmware shard of test_ctrl_firmware.py on CLONE (--require-rv32 --self-test).
. <scratch>/bin/env.sh
export MAKEFLAGS="-j$3 --no-print-directory"
cd "$1" && echo "HEAD $(git rev-parse --short=8 HEAD) shard $2/4 start $(date +%T)" && \
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs "$3" --shard "$2/4"; rc=$?
echo "END rc=$rc $(date +%T)"; exit $rc

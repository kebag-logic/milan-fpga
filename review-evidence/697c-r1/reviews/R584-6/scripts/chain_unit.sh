#!/bin/bash
# Replica of firmware-unit's firmware steps under one capture, then its boundary step.
# Usage: chain_unit.sh <packet-root> <checkout>
set -u; P=$1; cd "$2"; source $P/scripts/env.sh
C=$P/scratch/capA; rm -rf $C; L=$P/logs/unit
step(){ n=$1; shift; echo "== $n: $*"; "$@" > $L.$n.log 2>&1; echo $? > $L.$n.rc; echo "rc=$(cat $L.$n.rc)"; }
step 1 python3 sw/firmware/ctrl/test/ctrl_capture.py --out $C -- python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
step 2 python3 sw/firmware/ctrl/test/ctrl_capture.py --out $C -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
step 3 python3 sw/firmware/ctrl/test/ctrl_capture.py --out $C -- python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
step 4 python3 sw/firmware/ctrl/test/ctrl_capture.py --out $C -- python3 sw/firmware/gtest/fw_coverage.py --selftest
step 5 python3 sw/firmware/ctrl/test/ctrl_capture.py --out $C -- python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
step 6 python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture $C --without verilator
echo done > $L.done

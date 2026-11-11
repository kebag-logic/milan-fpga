#!/bin/sh
# Run the three ctrl_configs.py readers at a candidate tree; argv: TREE RECEIPTS_DIR. Needs MILAN_RV32_CC.
T=$1; R=$2; cd "$T" || exit 2
( python3 -E -s sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 6 > "$R/ctrl_firmware.log" 2>&1; echo $? > "$R/ctrl_firmware.rc" ) &
( python3 -E -s sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 6 > "$R/ctrl_nvm.log" 2>&1; echo $? > "$R/ctrl_nvm.rc" ) &
( python3 -E -s sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator > "$R/ctrl_boundary.log" 2>&1; echo $? > "$R/ctrl_boundary.rc" ) &
wait

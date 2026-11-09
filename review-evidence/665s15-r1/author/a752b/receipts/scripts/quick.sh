#!/bin/bash
# The touched tests on the lane's working tree, each with its rc. usage: quick.sh OUT_DIR
set -u
OUT=$1; cd $LANE
run() { local name=$1; shift; "$@" > "$OUT/$name.log" 2>&1; echo "$name rc=$?" >> "$OUT/rc.txt"; }
: > "$OUT/rc.txt"
run builder-39-40 python3 sw/builder/test_builder.py --gates test_simulation_shape_option,test_shipped_shape_outputs_unchanged
run soc-options python3 sw/builder/test_soc_options.py
run ctrl-memory python3 sw/litex/test_ctrl_memory.py
run mailbox-selftest python3 sw/mailbox/gen_mailbox.py --selftest
run mailbox-check python3 sw/mailbox/gen_mailbox.py --check --crosscheck
run record-space python3 scripts/check_nvm_record_space.py
run record-space-self python3 scripts/check_nvm_record_space.py --self-test
run nvm-firmware python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 8
run harness-selftest python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
echo done >> "$OUT/rc.txt"

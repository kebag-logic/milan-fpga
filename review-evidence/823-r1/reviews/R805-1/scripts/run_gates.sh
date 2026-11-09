#!/usr/bin/env bash
# Run the round's focused gates at the reviewed head, concurrently; one log and rc file each.
# usage: run_gates.sh <clone> <receipt-dir> <scratch-dir>
set -u
C=$1; R=$2; S=$3
mkdir -p "$R" "$S"
cd "$C" || exit 2
export MILAN_RV32_CC=${MILAN_RV32_CC:-$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc}
export PYTHONDONTWRITEBYTECODE=1
run() { local n=$1; shift; ( "$@" >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc" ) & }
run layout3        python3 scripts/nvm_layout3.py
run klj3           python3 scripts/check_nvm_klj3.py
run klj3_self      python3 scripts/check_nvm_klj3.py --self-test
run fmt32          python3 scripts/check_nvm_format_32x32.py
run fmt32_self     python3 scripts/check_nvm_format_32x32.py --self-test
run record_space   python3 scripts/check_nvm_record_space.py
run flash_port     python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --self-test
run split_target   python3 tb/verilator/nvm_split_target/target_selftest.py
run ctrl_memory    python3 sw/litex/test_ctrl_memory.py
run builder_g39    python3 sw/builder/test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output
run ctrl_nvm       python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8
run hosttest       python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
run diffcheck      git diff --check a9d69c77 HEAD
wait
run fw_coverage    python3 sw/firmware/gtest/fw_coverage.py --check
wait
echo ALLDONE > "$R/ALLDONE"

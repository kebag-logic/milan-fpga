#!/bin/sh
# Usage: run_gates.sh <clone> <packet>. Runs the format's gates at the clone's head, one log and rc per gate.
C=$1; P=$2; R=$P/receipts; export TMPDIR=$P/scratch/tmp
cd "$C" || exit 2
run() { name=$1; shift; ( "$@" ) > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
run layout3        python3 scripts/nvm_layout3.py
run klj3_selftest  python3 scripts/check_nvm_klj3.py --self-test
run drift_gate     python3 scripts/check_nvm_format_32x32.py
run drift_selftest python3 scripts/check_nvm_format_32x32.py --self-test
run flash_map      python3 sw/litex/flash_map.py
run fw_coverage    python3 sw/firmware/gtest/fw_coverage.py --check
run builder_g39    python3 sw/builder/test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output
run hdl_diff       git diff --name-only 1d6bf5556ae28764361d85012b86394eb467d294 HEAD -- '*.sv' '*.svh' '*.v' '*.vh' '*.vhd' hdl syn protocol-processor gptp-processor third_party external configs/generated

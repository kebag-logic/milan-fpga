#!/bin/sh
# Run the PR's quick reproducible gates concurrently at the clone given as $1,
# writing one log and one rc file per gate into $2.
set -u
T=$1; O=$2; mkdir -p "$O"; cd "$T" || exit 2
run() { n=$1; shift; ( "$@" > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc" ) & }
run layout3            python3 scripts/nvm_layout3.py
run klj3_selftest      python3 scripts/check_nvm_klj3.py --self-test
run fmt_gate           python3 scripts/check_nvm_format_32x32.py
run fmt_selftest       python3 scripts/check_nvm_format_32x32.py --self-test
run flash_map          python3 sw/litex/flash_map.py
run fw_cov             python3 sw/firmware/gtest/fw_coverage.py --check
run builder_g38_39     python3 sw/builder/test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output
wait
git diff --name-only 1d6bf555 HEAD -- '*.sv' '*.svh' '*.v' '*.vh' '*.vhd' hdl syn protocol-processor gptp-processor third_party external configs/generated > "$O/hdl_diff.log" 2>&1; echo $? > "$O/hdl_diff.rc"
for f in "$O"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

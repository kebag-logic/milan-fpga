#!/bin/bash
# The gates this change touches, one log and one rc per gate, never piped, on a clean clone of the head, in order.
set -u
H=$1
S=$MANAGEMENT/2026-09-23/665s2b-a683o/scripts
T=$VALIDATION_STORAGE/665s2b-a683o
W=$T/lane-wt
G=$T/lane-logs
mkdir -p "$G"
[ -d "$W" ] || "$S/clone.sh" "$W" "$H" > "$G/clone.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp-lane MAKEFLAGS="-j8 --no-print-directory"
mkdir -p "$TMPDIR"
BASE=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin
export PATH=$BASE:$PATH VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc" >> "$G/summary.txt"; }
run diffcheck "git diff --check f4c9ad4f06f185378fd2646298aab51dd108e86f HEAD"
run diffcheck_merge "git diff --check a68536fa4cf8ce65c513874722de2e3ba83c2d00 HEAD"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run fw_coverage "python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8"
run fw_rv32_selftest "python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32"
run gen_mailbox "python3 sw/mailbox/gen_mailbox.py --check --crosscheck"
run gen_mailbox_selftest "python3 sw/mailbox/gen_mailbox.py --selftest"
run census "python3 sw/mailbox/publication_census.py --check --selftest --jobs 8"
run lint_rtl "python3 scripts/lint_rtl.py --check"
run soc_options "python3 sw/builder/test_soc_options.py"
run ctrl_memory "python3 sw/litex/test_ctrl_memory.py"
run boundary_a "python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator"
run boundary_b "python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator"
run behave "cd tests && behave --no-capture -f plain"
run test_builder "python3 sw/builder/test_builder.py --require-rv32"
run boot_1x1 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $T/boot-final/1x1"
run boot_8x8 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $T/boot-final/8x8 --shape endstation_ax7101_8x8"
run boot_native "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $T/boot-final/native --native-controls"
run boot_plants "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $T/boot-final/plants --self-test"
git status --short > "$G/tree-after.txt"
echo done >> "$G/summary.txt"

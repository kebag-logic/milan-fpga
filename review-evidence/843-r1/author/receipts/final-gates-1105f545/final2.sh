#!/usr/bin/env bash
# final lane gates at <sha> on a fresh clean clone, one log and one rc per gate, never piped
set -u
H=$1; BASE=$2; S=<scratch>; W=$S/clone-final2; O=$S/final-gates2
mkdir -p "$O" "$S/tmp-final"
[ -d "$W" ] || bash $S/scripts/make_clone.sh "$W" "$H" > "$O/clone.log" 2>&1 || exit 3
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain)" || exit 5
SDK=<data>/scratch/803-a693/sdk/br-milan-rv32/host
export HOME=<home> VERILATOR=<data>/tools/pinned-verilator-5.050/verilator TMPDIR=$S/tmp-final MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c
export PATH=<data>/tmp/sync-a723b/venv-docs/bin:<data>/scratch/a662/make43/bin:<data>/tools/sv2v-v0.0.12:<data>/tools/pinned-verilator-5.050:$SDK/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
run() { id=$1; shift; s=$(date +%s); { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$O/$id.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s) - s ))" > "$O/$id.rc"; echo "$id rc=$rc"; }
run diffcheck "git diff --check $BASE HEAD"
run fw_selftest "python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test"
run fw_coverage_check "python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8"
run fw_coverage_selftest "python3 sw/firmware/gtest/fw_coverage.py --selftest"
run docs_inventory_check "python3 scripts/docs_inventory.py --check"
run docs_inventory_selftest "python3 scripts/docs_inventory.py --selftest"
run behave "cd tests && behave"
run lint_rtl "python3 scripts/lint_rtl.py --check"
run em_dash "<data>/tools/md-venv/bin/python3 scripts/check_em_dash.py --base $BASE"
run builder "python3 sw/builder/test_builder.py --require-rv32"
run xvlog_gate "PATH=<home>/Xilinx/2026.1/Vivado/bin:$PATH <home>/milan-fpga-management/2026-09-23/vivado-slot.sh python3 scripts/xvlog_gate.py --check"
run fw_service_budget "make -C tb/verilator/fw_service_budget"
git status --porcelain > "$O/tree-after.txt"
echo done > "$O/DONE"

#!/usr/bin/env bash
# Reproduces this round's executed evidence. Usage: run_r935_4.sh <clone at 57f32b28> <packet dir>
# Each long run writes its own log and rc file; the gate and the self-test may run concurrently.
set -u
ROOT=$(cd "$1" && pwd); OUT=$(cd "$2" && pwd); R="$OUT/receipts"; W="$OUT/scratch"
mkdir -p "$R" "$W"
cd "$ROOT/tb/verilator/ctrl_service_budget" && python3 -I -B model_counts.py > "$R/model_counts.log" 2>&1; echo $? > "$R/model_counts.rc"
python3 -I -B "$OUT/probe_model_counts.py" "$ROOT" > "$R/probe_model_counts.log" 2>&1; echo $? > "$R/probe_model_counts.rc"
cd "$ROOT" && python3 -B scripts/check_py_idiom.py > "$R/check_py_idiom.log" 2>&1; echo $? > "$R/check_py_idiom.rc"
cd "$ROOT" && python3 -B scripts/gen_toc.py --check > "$R/gen_toc_check.log" 2>&1; echo $? > "$R/gen_toc_check.rc"
cd "$ROOT" && python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$W/gate/build" \
    > "$R/firmware_gate.log" 2>&1; echo $? > "$R/firmware_gate.rc"
cd "$ROOT/tb/verilator/ctrl_service_budget" && python3 -B run.py --self-test > "$R/run_selftest.log" 2>&1; echo $? > "$R/run_selftest.rc"
cd "$ROOT" && PYTHONHASHSEED=0 python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$W/ledger/build" \
    > "$R/plat_ledger_not_run.log" 2>&1; echo $? > "$R/plat_ledger_not_run.rc"
cd "$ROOT" && { git rev-parse HEAD 'HEAD^{tree}'; git write-tree; git status --porcelain --ignore-submodules=none; git submodule status; } \
    > "$R/tree_restore_check.log" 2>&1

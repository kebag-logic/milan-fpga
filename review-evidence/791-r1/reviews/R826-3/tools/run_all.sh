#!/bin/bash
# run_all.sh: the review's concurrent runs. Needs R (this packet), C (exact-head clone), PY, RV32_BIN,
# VERILATOR_WRAPPER, VERILATOR_ROOT set; each run writes receipts/<area>/<name>.{log,rc}.
set -u
. "$R/tools/env.sh"
export PYTHONPATH=$R/tools/noguard PYTHONDONTWRITEBYTECODE=1
cd "$C"
run() { local out=$1; shift; mkdir -p "$(dirname "$R/receipts/$out")"; ( "$@" > "$R/receipts/$out.log" 2>&1; echo $? > "$R/receipts/$out.rc" ) & }
run tcm/run "$PY" -B sw/litex/test_ctrl_memory.py
run sims/region-self-test "$PY" -B tb/verilator/ctrl_region_decode/run.py --build-dir "$R/scratch/region-self" --self-test
run probes/guard_probe2-at-head "$PY" -B "$R/tools/guard_probe2.py" "$C"
run probes/guard_probe2-at-596e2ae3 "$PY" -B "$R/tools/guard_probe2.py" "$R/scratch/parent"
run probes/decode-arm-at-head "$PY" -B "$R/tools/decode_arm.py" "$C"
run probes/decode-arm-at-596e2ae3 "$PY" -B "$R/tools/decode_arm.py" "$R/scratch/parent"
run probes/decode-arm-head-fix-reverted "$PY" -B "$R/tools/decode_arm.py" "$R/scratch/reverted"
wait

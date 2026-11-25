#!/bin/sh
# suites and campaigns, concurrent, 14 jobs at most
export TREE OUT VERILATOR=${VERILATOR:?pinned 5.050 wrapper} VERILATOR_JOBS=4
export PATH=$(dirname "$VERILATOR"):$PATH PYTHONDONTWRITEBYTECODE=1
R=$(dirname "$0")/run_probe.sh
setsid "$R" suite-leaf make -C tb/verilator/input_loopback VERILATOR=$VERILATOR MDIR="$S/obj_leaf" &
setsid "$R" suite-parent make -C tb/verilator/input_loopback_dp VERILATOR=$VERILATOR WORK="$S/obj_parent" &
setsid "$R" planner-selftest python3 scripts/suite_shards.py --selftest &
setsid "$R" gate-workflows python3 scripts/ci_gate_workflows.py --check &
setsid "$R" suite-workflows python3 scripts/ci_suite_workflows.py --check &
wait

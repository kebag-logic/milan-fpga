#!/bin/sh
export TREE OUT VERILATOR=${VERILATOR:?pinned 5.050 wrapper} VERILATOR_JOBS=4
export PATH=$(dirname "$VERILATOR"):$PATH PYTHONDONTWRITEBYTECODE=1
R=$(dirname "$0")/run_probe.sh
"$R" leaf-mutants python3 tb/verilator/input_loopback/mutants.py --output "$S/mut_leaf" &
"$R" parent-mutants python3 tb/verilator/input_loopback_dp/mutants.py --output "$S/mut_parent" &
"$R" pieces-selftest python3 scripts/ci_suite_pieces_selftest.py &
"$R" measure-evidence python3 scripts/measure_test_evidence.py --check &
wait

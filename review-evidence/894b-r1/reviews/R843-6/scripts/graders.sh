#!/bin/bash
# Every ctrl_service_budget grader at a tree, one output file each, run concurrently. usage: graders.sh TREE OUT
set -u
C=$1 O=$2; mkdir -p "$O"; cd "$C" || exit 3
B=tb/verilator/ctrl_service_budget
run() { n=$1; shift; ( "$@" > "$O/$n.txt" 2>&1; echo "$n rc=$?" > "$O/$n.rc" ) & }
run flip_check python3 -B $B/flip_grade.py --check
run flip_1x1 python3 -B $B/flip_grade.py --check --point 1x1/1if
run flip_8x8_2if python3 -B $B/flip_grade.py --check --point 8x8/2if
run flip_8x8_1if python3 -B $B/flip_grade.py --check --point 8x8/1if
run load_check python3 -B $B/load_grade.py --check
run shape_costs python3 -B $B/shape_costs.py --check --selftest
run flip_selftest python3 -B $B/flip_grade.py --selftest
run rows_tiers_selftest python3 -B $B/rows_tiers.py --selftest
run load_selftest python3 -B $B/load_grade.py --selftest
run rows_tiers_report python3 -B $B/rows_tiers.py
wait
cat "$O"/*.rc > "$O/rc.txt"

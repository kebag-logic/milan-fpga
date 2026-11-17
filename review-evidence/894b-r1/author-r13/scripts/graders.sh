#!/bin/bash
# Every grader's output at a tree, one file each, for a before/after comparison. usage: graders.sh TREE OUT
set -u
C=$1 O=$2; mkdir -p "$O"; cd "$C" || exit 3
B=tb/verilator/ctrl_service_budget
run() { n=$1; shift; "$@" > "$O/$n.txt" 2>&1; echo "$n rc=$?" >> "$O/rc.txt"; }
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

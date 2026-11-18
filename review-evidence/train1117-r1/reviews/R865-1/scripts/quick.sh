#!/bin/bash
# The docs, idiom, hygiene, TOC and CPU-budget harness checks at a clone's head; one log and rc per check into <out>.
# usage: quick.sh <clone> <out>
c=$1; o=$2; mkdir -p "$o"; cd "$c" || exit 99
run() { n=$1; shift; "$@" > "$o/$n.log" 2>&1; echo $? > "$o/$n.rc"; echo "$n rc=$(cat "$o/$n.rc")"; }
MDPY=${MDPY:-python3}
run docs_check python3 -B scripts/docs_check.py
run py_idiom python3 -B scripts/check_py_idiom.py
run hygiene python3 -B scripts/check_hygiene.py --check
run toc_check "$MDPY" -B scripts/gen_toc.py --check
run toc_anchors "$MDPY" -B scripts/gen_toc.py --verify-anchors
run diff_check git diff --check cb96336d7a...HEAD
run flip_1x1 python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
run flip_8x8_1if python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
run flip_all python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check
run load_check python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
run fw_coverage python3 -B sw/firmware/gtest/fw_coverage.py --check
run resgate_baseline python3 -B syn/ooc/pp_resource_gate.py check-baseline
run resgate_selftest python3 -B syn/ooc/pp_resource_gate.py --selftest

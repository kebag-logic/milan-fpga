#!/bin/bash
# Scratch: the parent's light consumer gates, one log and rc file each.
cd $VALIDATION_STORAGE/c8-a504/parent-dev || exit 2
G=$VALIDATION_STORAGE/c8-a504/gates-dev
run() { name=$1; shift; "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc"; echo "$name rc=$(cat $G/$name.rc)"; }
run check_cpp_idiom python3 -B scripts/check_cpp_idiom.py
run check_py_idiom python3 -B scripts/check_py_idiom.py
run check_rtl_source_lists python3 -B scripts/check_rtl_source_lists.py
run pp_srcs python3 -B scripts/pp_srcs.py --check --selftest
run check_port_contracts python3 -B scripts/check_port_contracts.py
run measure_naming python3 -B scripts/measure_naming.py --check
run measure_test_evidence python3 -B scripts/measure_test_evidence.py --check
run docs_check python3 -B scripts/docs_check.py
run lint_rtl python3 -B scripts/lint_rtl.py --check

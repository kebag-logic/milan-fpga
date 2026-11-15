#!/bin/sh
# Run the pure-Python model gates at an extracted head tree (its tsn-c-stack and lwSRP submodules copied in).
# usage: sh model_gates.sh TREE OUT
T=$1; O=$2; B=tb/verilator/ctrl_service_budget; mkdir -p "$O"; cd "$T" || exit 2
python3 -I $B/flip_grade.py --check --point 1x1/1if > "$O/flip_1x1.txt" 2>&1; echo $? > "$O/flip_1x1.rc"
python3 -I $B/load_grade.py --check > "$O/load_check.txt" 2>&1; echo $? > "$O/load_check.rc"
python3 -I $B/load_grade.py --selftest > "$O/load_selftest.txt" 2>&1; echo $? > "$O/load_selftest.rc"
python3 -I $B/record_classes.py --selftest > "$O/record_classes_selftest.txt" 2>&1; echo $? > "$O/record_classes_selftest.rc"
python3 -I $B/flip_grade.py --selftest > "$O/flip_selftest.txt" 2>&1; echo $? > "$O/flip_selftest.rc"
python3 -I -c "import sys, pathlib; sys.path.insert(0, '$B'); import queued_bound, paced_rows, rows_tiers; r = pathlib.Path('.'); w = rows_tiers.solve('last', rows_tiers.point_inputs(r, '1x1/1if'), rows_tiers.BUILT)[0]; print('last', w, 'ruled', queued_bound.ruled(w), 'stated', queued_bound.stated(r)); s = queued_bound.statements(r) + paced_rows.statements(r) + rows_tiers.tx_statements(r); print('pace', paced_rows.choice(r), 'statements', s); print('controls escaped', queued_bound.controls(r) + paced_rows.controls(r)); sys.exit(1 if s else 0)" > "$O/rules.txt" 2>&1; echo $? > "$O/rules.rc"

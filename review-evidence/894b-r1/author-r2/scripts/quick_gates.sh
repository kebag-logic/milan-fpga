#!/bin/bash
# The model's, the table's and the style gates at a clean clone, one log and rc each, never piped. usage: quick_gates.sh CLONE OUT
set -u
C=$1 O=$2; mkdir -p $O; cd $C || exit 3
run() { id=$1; shift; { echo "# head $(git rev-parse HEAD) gate $id: $*"; bash -c "$*"; } > $O/$id.log 2>&1; echo $? > $O/$id.rc; echo "$id rc=$(cat $O/$id.rc)" >> $O/summary.txt; }
run shape_costs "python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check --selftest"
run flip_check_1x1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if"
run flip_check_8x8_1if "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if"
run flip_check_8x8_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/2if"
run flip_selftest "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest"
run load_check "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check"
run load_selftest "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest"
run rows_tiers_selftest "python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest"
run tier_grid "python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if"
run docs_check "python3 -B scripts/docs_check.py"
run em_dash "/data-2/milan/tmp/894-a773/venv-md/bin/python3 -B scripts/check_em_dash.py --base 66adb9a987b56c2b1a12ce92d058e0bc1a57bc3a"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run diffcheck_lane_start "git diff --check 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 HEAD"
run ctrl_hot_check "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check"
git status --short --untracked-files=all > $O/tree-after.txt

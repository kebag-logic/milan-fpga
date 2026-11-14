#!/bin/sh
# grade_tree.sh TREE OUTDIR: the flip check at 1x1/1if, the pace rule, tier_grid at 1x1/1if and the load gate on TREE.
T=$1; O=$2; mkdir -p "$O"; cd "$T/tb/verilator/ctrl_service_budget" || exit 2
python3 -I flip_grade.py --check --point 1x1/1if > "$O/flip-1x1.log" 2>&1; echo $? > "$O/flip-1x1.rc"
python3 -I tier_grid.py --point 1x1/1if > "$O/tier_grid-1x1.log" 2>&1; echo $? > "$O/tier_grid-1x1.rc"
python3 -I load_grade.py --check > "$O/load_grade.log" 2>&1; echo $? > "$O/load_grade.rc"
python3 -I -c "import sys; sys.path.insert(0,'.'); from pathlib import Path; import paced_rows; r=Path('$T'); print('choice', paced_rows.choice(r)); print('statements', paced_rows.statements(r))" > "$O/pace.log" 2>&1; echo $? > "$O/pace.rc"

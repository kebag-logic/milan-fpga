#!/bin/sh
# In a scratch tree (a git archive of the head with its submodules), charge the retained retry at most once a
# centisecond in rows_grade.demand, run flip_grade.py --selftest and --check --point 1x1/1if, and restore the file.
# usage: rows_charge_selftest.sh <scratch-tree>
set -u
T=$1; F=$T/tb/verilator/ctrl_service_budget/rows_grade.py
cp "$F" "$F.orig"
python3 -I - "$F" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read()
old = "out['item.retained'] = min(passes, srp_in) * c['item.retained']"
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, "out['item.retained'] = min(passes, srp_in, ticks) * c['item.retained']"))
PY
out=$(python3 -B "$T/tb/verilator/ctrl_service_budget/flip_grade.py" --selftest); rc=$?; echo "$out" | tail -1; echo "selftest rc $rc"
python3 -B "$T/tb/verilator/ctrl_service_budget/flip_grade.py" --check --point 1x1/1if | tail -8
mv "$F.orig" "$F"

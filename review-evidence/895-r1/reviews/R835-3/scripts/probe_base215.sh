#!/bin/sh
# probe_base215.sh CLONE OUT: export CLONE's HEAD (with the tsn-c-stack and lwSRP submodules) twice under OUT,
# raise poll_grade.py's 1x1/1if polls' base 205 -> 215 us in the second (the head's measured 20,456 CPU cycles plus
# 5 %, rounded up to 5 us), and grade both trees with grade_tree.sh plus the slice rule and rows_tiers' self-test.
set -e
C=$1; O=$2; H=$(cd "$(dirname "$0")" && pwd)
for t in head probe-base215; do
  rm -rf "$O/$t"; mkdir -p "$O/$t"; (cd "$C" && git archive HEAD) | tar -x -C "$O/$t"
  for m in third_party/tsn-c-stack third_party/lwSRP; do
    rm -rf "$O/$t/$m"; mkdir -p "$O/$t/$m"; (cd "$C/$m" && git archive HEAD) | tar -x -C "$O/$t/$m"
  done
done
sed -i 's/STATED_US = {1: dict(base=205,/STATED_US = {1: dict(base=215,/' "$O/probe-base215/tb/verilator/ctrl_service_budget/poll_grade.py"
diff "$O/head/tb/verilator/ctrl_service_budget/poll_grade.py" "$O/probe-base215/tb/verilator/ctrl_service_budget/poll_grade.py" || true
for t in head probe-base215; do
  sh "$H/grade_tree.sh" "$O/$t" "$O/out-$t" &
done
wait
for t in head probe-base215; do
  (cd "$O/$t/tb/verilator/ctrl_service_budget" && python3 -I -c "import sys; sys.path.insert(0,'.'); from pathlib import Path; import rows_tiers as rt; r=Path('$O/$t'); print('slice_choice', rt.slice_choice(r), 'ruled', rt.ruled(r), 'built', rt.built_constants(r,1)[0])" > "$O/out-$t/ruled.log" 2>&1
   python3 -I rows_tiers.py --selftest > "$O/out-$t/rows_tiers-selftest.log" 2>&1; echo $? > "$O/out-$t/rows_tiers-selftest.rc") &
done
wait

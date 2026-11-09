#!/usr/bin/env bash
# run_gates.sh <clean-copy-1> <clean-copy-2> <receipts> <verilator>: the changed gates at the head, two independent
# copies so the suite and drops-mutant do not share generated files. Each writes <id>.log and <id>.rc.
set -u
c1=$1; c2=$2; out=$3; V=$4
( cd "$c1/tb/verilator/pp_shadow" && make -j4 VERILATOR="$V" VERILATOR_JOBS=2 > "$out/pp_shadow_suite.log" 2>&1; echo $? > "$out/pp_shadow_suite.rc" ) &
( cd "$c2/tb/verilator/pp_shadow" && VERILATOR="$V" VERILATOR_JOBS=4 python3 drops_mutant.py > "$out/drops_mutant.log" 2>&1; echo $? > "$out/drops_mutant.rc" ) &
wait
cd "$c1"
python3 syn/ooc/pp_resource_gate.py check-baseline > "$out/check_baseline.log" 2>&1; echo $? > "$out/check_baseline.rc"
python3 syn/ooc/pp_resource_gate.py --selftest > "$out/gate_selftest.log" 2>&1; echo $? > "$out/gate_selftest.rc"
python3 scripts/docs_inventory.py --check > "$out/docs_inventory.log" 2>&1; echo $? > "$out/docs_inventory.rc"
git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD > "$out/diff_check.log" 2>&1; echo $? > "$out/diff_check.rc"

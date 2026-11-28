#!/bin/bash
# Round 5's harness gates at the checkout's head. usage: harness5.sh (cwd = checkout root)
G=$VALIDATION_STORAGE/arty4x4-a863/gates5; T=$VALIDATION_STORAGE/arty4x4-a863/tools; S=tb/verilator/ctrl_service_budget
X=$VALIDATION_STORAGE/arty4x4-a863/r5/census4-extract
run() { local name=$1; shift; "$@" > $G/$name.log 2>&1; echo "$name rc=$?" | tee -a $G/harness5.rc; }
: > $G/harness5.rc
git rev-parse HEAD >> $G/harness5.rc
run egress-mii-selftest python3 -I -B $S/egress_mii.py --selftest
run egress-mii-structural-1x1 python3 -I -B $S/egress_mii.py --structural
run egress-mii-structural-4x4 python3 -I -B $S/egress_mii.py --structural --point arty-4x4
run egress-mii-extract python3 -I -B $S/egress_mii.py $X/answering-every-port/ $X/answering-later/ $X/answering-ports/ $X/declaring-outputs/ $X/none/ $X/shutdown-entry/ $X/talker-notices/ $X/valid-destinations/
run egress-fixed-selftest python3 -I -B $S/egress_fixed.py --selftest
run egress-fixed-100 python3 -I $S/egress_fixed.py $G/fixed100 100000000
run egress-fixed-80 python3 -I $S/egress_fixed.py $G/fixed80
run record-classes-selftest python3 -I -B $S/record_classes.py --selftest
run ledger-selftest python3 -I -B $S/egress_ledger.py --selftest
run ledger-extract python3 -I -B $S/egress_ledger.py --point arty-4x4 $X/answering-every-port/results $X/answering-later/results $X/answering-ports/results $X/declaring-outputs/results $X/none/results $X/shutdown-entry/results $X/talker-notices/results $X/valid-destinations/results
run arty-grade-1x1 python3 -I -B $S/arty_grade.py --point arty-1x1
run arty-grade-4x4 python3 -I -B $S/arty_grade.py --point arty-4x4
run arty-grade-selftest python3 -I -B $S/arty_grade.py --selftest
run rows-tiers-selftest python3 -I -B $S/rows_tiers.py --selftest
run load-grade-selftest python3 -I -B $S/load_grade.py --selftest
run shape-costs-selftest python3 -I -B $S/shape_costs.py --selftest
run kept-grade-selftest python3 -I -B $S/kept_grade.py --selftest
run mutants python3 -B $T/mutants5.py $G/mutants
run service-selftest python3 -B $T/service-selftest5.py

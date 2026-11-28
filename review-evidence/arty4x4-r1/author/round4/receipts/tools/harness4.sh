#!/bin/bash
# Round 4's harness gates at the checkout's head: the service self-test (8 partitions), the ledger and Arty grades,
# and the firmware coverage ratchet. usage: harness4.sh (cwd = checkout root)
G=$VALIDATION_STORAGE/arty4x4-a863/gates4; T=$VALIDATION_STORAGE/arty4x4-a863/tools
run() { local name=$1; shift; "$@" > $G/$name.log 2>&1; echo "$name rc=$?" | tee -a $G/harness4.rc; }
: > $G/harness4.rc
git rev-parse HEAD >> $G/harness4.rc
run ledger-selftest python3 -I -B tb/verilator/ctrl_service_budget/egress_ledger.py --selftest
run ledger-census4 python3 -I -B tb/verilator/ctrl_service_budget/egress_ledger.py --point arty-4x4 $VALIDATION_STORAGE/arty4x4-a863/c4q/*/results
run arty-grade-1x1 python3 -B tb/verilator/ctrl_service_budget/arty_grade.py --point arty-1x1
run arty-grade-selftest python3 -I -B tb/verilator/ctrl_service_budget/arty_grade.py --selftest
run arty-grade-4x4 python3 -B tb/verilator/ctrl_service_budget/arty_grade.py --point arty-4x4
run fw-coverage-selftest python3 -B sw/firmware/gtest/fw_coverage.py --selftest
run fw-coverage-check python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4
run service-selftest python3 -B $T/service-selftest4.py

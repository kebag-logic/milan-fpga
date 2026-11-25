#!/bin/sh
export PATH=$(dirname "$VERILATOR"):$PATH
R=$(dirname "$0")/run_probe.sh
"$R" egress-selftest python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --selftest &
"$R" bounds python3 tb/verilator/input_loopback/bounds.py --output "$S/bounds" &
"$R" builder-contract python3 sw/builder/test_input_loopback.py &
"$R" idiom python3 scripts/check_py_idiom.py &
"$R" failfast-selftest python3 scripts/ci_fail_fast_selftest.py &
wait

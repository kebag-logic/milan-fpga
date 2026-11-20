#!/usr/bin/env bash
# selftests.sh <repo> <outdir>: the CPU-budget harness self-tests and checks the delta's
# message texts feed, each with its own log and rc, run concurrently (at most 12 at once).
set -u
R=$1 O=$2; mkdir -p "$O"; cd "$R"
B=tb/verilator/ctrl_service_budget
run() { local n=$1; shift; ( echo "CMD $*"; echo "HEAD $(git rev-parse HEAD) START $(date -Iseconds)"; "$@"; echo "rc=$?" ) > "$O/$n.log" 2>&1; tail -n1 "$O/$n.log" | sed 's/rc=//' > "$O/$n.rc"; }
run flip_selftest     python3 -B $B/flip_grade.py --selftest &
run flip_check        python3 -B $B/flip_grade.py --check &
run flip_check_1x1    python3 -B $B/flip_grade.py --check --point 1x1/1if &
run flip_check_8x8    python3 -B $B/flip_grade.py --check --point 8x8/1if &
run load_check        python3 -B $B/load_grade.py --check &
run load_selftest     python3 -B $B/load_grade.py --selftest &
run rows_tiers        python3 -B $B/rows_tiers.py --selftest &
run record_classes    python3 -I $B/record_classes.py --selftest &
run shape_check       python3 -I $B/shape_costs.py --check &
run shape_selftest    python3 -I $B/shape_costs.py --selftest &
run queued_bound      python3 -B $B/queued_bound.py --selftest &
run ctrl_hot_check    python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check &
wait
run ctrl_hot_selftest python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test &
run ctrl_memory       ${HOME}/litex-milan/venv/bin/python3 sw/litex/test_ctrl_memory.py &
wait
echo "porcelain-after $(git status --porcelain | wc -l)" > "$O/porcelain.txt"

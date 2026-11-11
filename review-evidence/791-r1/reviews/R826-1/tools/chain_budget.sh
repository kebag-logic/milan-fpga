#!/usr/bin/env bash
# chain_budget.sh: S2's CPU budget harness on the exact-head clone, serially, generation guarded; logs and rcs in receipts/budget.
set -u
. "${R:?packet directory}/tools/env.sh"; export PYTHONPATH=$R/tools/noguard
C=${CLONE:?exact-head clone}; B=$R/scratch/build; O=$R/receipts/budget; mkdir -p "$B" "$O"
step() { local name=$1; shift; echo "$(date +%T) start $name" >> "$O/chain.log"; ( cd "$C" && /usr/bin/time -v "$@" ) > "$O/$name.log" 2>&1; echo $? > "$O/$name.rc"; echo "$(date +%T) $name rc $(cat "$O/$name.rc")" >> "$O/chain.log"; }
step self-test "$PY" -B tb/verilator/ctrl_service_budget/run.py --self-test
step 1x1 "$PY" -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$B/budget-1x1" --record-budget-findings
step 8x8 "$PY" -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$B/budget-8x8" --record-budget-findings
echo "$(date +%T) chain done" >> "$O/chain.log"

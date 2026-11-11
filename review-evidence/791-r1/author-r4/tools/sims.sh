#!/usr/bin/env bash
# sims.sh: the split boot at 1x1 and 8x8, S2's harness self-test and its 1x1 (one interface) and 8x8 (two
# interfaces) points, on a clean clone of the final head, each rc beside its log.
set -u
S=/data-2/milan/tmp/791-a765c; F=$S/final; CL=$S/clones/head-sims; PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0 PATH=$WORKSPACE_HOME/br-milan-rv32/host/bin:$PATH
mkdir -p "$F"
step() { local name=$1; shift; echo "$(date +%T) start $name"; ( cd "$CL" && "$@" ) > "$F/$name.log" 2>&1; echo $? > "$F/$name.rc"; echo "$(date +%T) $name rc $(cat "$F/$name.rc")"; }
rm -rf "$F/boot-1x1" "$F/boot-8x8" "$F/budget-1x1" "$F/budget-8x8"
step boot-1x1 "$PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$F/boot-1x1"
step boot-8x8 "$PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$F/boot-8x8" --shape endstation_ax7101_8x8
step budget-selftest "$PY" -B tb/verilator/ctrl_service_budget/run.py --self-test
step budget-1x1 "$PY" -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$F/budget-1x1" --record-budget-findings
step budget-8x8 "$PY" -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$F/budget-8x8" --record-budget-findings
echo "$(date +%T) sims done"

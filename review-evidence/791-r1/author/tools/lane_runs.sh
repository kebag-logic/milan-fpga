#!/usr/bin/env bash
# lane_runs.sh <chain>: the lane's own runs on the final head's clean clone, each with its rc beside its log.
# chain sims: the split boot at 8x8, S2's harness at 1x1 (one interface) and 8x8 (two interfaces), S2's self-test.
# chain litex: the all-fabric compare (base against head), then test_ctrl_memory.py.
set -u
S=/data-2/milan/tmp/791-a765; F=$S/final; CL=$S/clones/final; PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
T=$MANAGEMENT/2026-09-23/791-a765/tools
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0 PATH=$WORKSPACE_HOME/br-milan-rv32/host/bin:$PATH
step() { local name=$1; shift; echo "$(date +%T) start $name"; ( cd "$CL" && "$@" ) > "$F/$name.log" 2>&1; echo $? > "$F/$name.rc"; echo "$(date +%T) $name rc $(cat "$F/$name.rc")"; }
case $1 in
  sims)
    rm -rf "$F/boot-8x8"; mv "$F/boot-8x8.log" "$F/boot-8x8-attempt2-ro-home.log" 2>/dev/null; rm -f "$F/boot-8x8.rc"
    step boot-8x8 "$PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$F/boot-8x8" --shape endstation_ax7101_8x8
    step budget-1x1 "$PY" -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$F/budget-1x1" --record-budget-findings
    step budget-8x8 "$PY" -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$F/budget-8x8" --record-budget-findings
    step budget-selftest "$PY" -B tb/verilator/ctrl_service_budget/run.py --self-test ;;
  litex)
    rm -rf "$S/allfabric"
    step allfabric "$PY" "$T/allfabric_compare.py" "$S/clones/base" "$S/clones/final-af" "$S/allfabric" "$F/allfabric-receipt"
    mkdir -p "$F/tcm-tmp"; step tcm env TMPDIR="$F/tcm-tmp" "$PY" -B sw/litex/test_ctrl_memory.py ;;
esac
echo "$(date +%T) chain $1 done"

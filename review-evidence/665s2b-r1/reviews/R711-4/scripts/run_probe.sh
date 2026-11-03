#!/bin/bash
# usage: run_probe.sh TREE BUILD_DIR LOG GROUPS [extra run.py args]; writes LOG and LOG.rc
set -u
T=$1 B=$2 L=$3 G=$4; shift 4
export PATH=$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
reuse=(); [ -f "$B/build.json" ] && reuse=(--reuse-build)
start=$(date +%s)
python3 -B "$T/tb/verilator/ctrl_service_budget/run.py" --point "${POINT:-8x8}" --build-dir "$B" "${reuse[@]}" --groups "$G" \
  --record-budget-findings --record-share-findings --jobs "${JOBS:-11}" "$@" > "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L"
echo $rc > "$L.rc"

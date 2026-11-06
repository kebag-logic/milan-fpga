#!/bin/bash
# Build the answering arm at one point and run only hooks-counters at the exact head.
# usage: VERILATOR_DIR=<dir> LITEX_BIN=<dir> RV32_BIN=<dir> sim_counters.sh <clone> <point> <out-root>
set -u
clone=$1 point=$2 out=$3
export PATH=$VERILATOR_DIR:$LITEX_BIN:$RV32_BIN:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
cd "$clone" || exit 2
python3 -B tb/verilator/ctrl_service_hooks/run.py --point "$point" --arm answering --groups hooks-counters --build-dir "$out/b-$point" --record-findings --jobs 2 > "$out/$point.log" 2>&1
echo $? > "$out/$point.rc"

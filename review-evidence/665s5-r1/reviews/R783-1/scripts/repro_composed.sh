#!/bin/sh
# Reviewer reproduction of three composed rows at 1x1, answering arm, product clock, on a clean scratch clone
# at the head under review. usage: repro_composed.sh <clean clone> <build dir>
set -u
cd "$1" || exit 2
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
echo "HEAD $(git rev-parse HEAD); changed paths $(git status --porcelain | wc -l)"
start=$(date +%s)
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --arm answering --build-dir "$2" --record-findings \
  --groups backlog,backlog-owed,hooks-load-counters --jobs 3
echo "rc=$?"
echo "elapsed=$(( $(date +%s) - start ))s"

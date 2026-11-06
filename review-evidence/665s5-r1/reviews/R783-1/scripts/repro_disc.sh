#!/bin/sh
# Reviewer reproduction of the backlog-adp group (the composed H-DISC fit) at 1x1, answering arm, product clock,
# reusing the reviewer's own clean build. usage: repro_disc.sh <clean clone> <build dir> <out dir>
set -u
cd "$1" || exit 2
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
echo "HEAD $(git rev-parse HEAD); changed paths $(git status --porcelain | wc -l)"
start=$(date +%s)
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --arm answering --build-dir "$2" --reuse-build \
  --out "$3" --record-findings --groups backlog-adp --jobs 1
echo "rc=$?"
echo "elapsed=$(( $(date +%s) - start ))s"

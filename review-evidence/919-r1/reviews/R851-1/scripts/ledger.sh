#!/usr/bin/env bash
# ledger.sh NAME BUILD_DIR [plat_ledger.py args]: the platform ledger on the review clone, detached; receipts/NAME.{log,rc}
set -u
P=${PACKET:?export PACKET, this packet directory}
TREE=${TREE:-${CLONE:?export CLONE, the review clone at the exact head}}
name=$1; dir=$2; shift 2
export PATH=${RV32_SDK:?export RV32_SDK, the pinned RV32 SDK host directory}/bin:${TOOLS:?export TOOLS, the pinned tools directory}/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true TMPDIR=$P/scratch/tmp
export RCFILE="$P/receipts/$name.rc"; rm -f "$RCFILE"
cd "$TREE" && nohup setsid bash -c '
  echo "head $(git rev-parse HEAD) dirty $(git status --porcelain | wc -l)"; s=$(date +%s)
  ${LITEX:?export LITEX, the product LiteX tree with its venv}/venv/bin/python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$1" "${@:2}"
  rc=$?; echo "elapsed=$(( $(date +%s) - s ))s rc=$rc"; echo $rc > "$RCFILE"
' _ "$dir" "$@" > "$P/receipts/$name.log" 2>&1 < /dev/null &

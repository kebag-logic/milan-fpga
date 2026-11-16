#!/usr/bin/env bash
# boot.sh NAME SHAPE BUILD_DIR [run.py args]: the split boot simulation of the review clone, detached;
# output to receipts/NAME.log, exit status to receipts/NAME.rc.
set -u
P=${PACKET:?export PACKET, this packet directory}
TREE=${TREE:-${CLONE:?export CLONE, the review clone at the exact head}}
name=$1; shape=$2; dir=$3; shift 3
V=${TOOLS:?export TOOLS, the pinned tools directory}/pinned-verilator-5.050
export PATH=${RV32_SDK:?export RV32_SDK, the pinned RV32 SDK host directory}/bin:$V:${TOOLS:?export TOOLS, the pinned tools directory}/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$V/verilator COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$P/scratch/tmp MAKEFLAGS="-j${JOBS:-6} --no-print-directory"
export RCFILE="$P/receipts/$name.rc"
mkdir -p "$TMPDIR"
rm -f "$RCFILE"
cd "$TREE" && nohup setsid bash -c '
  echo "head $(git rev-parse HEAD) dirty $(git status --porcelain | wc -l)"; date -Iseconds; s=$(date +%s)
  ${LITEX:?export LITEX, the product LiteX tree with its venv}/venv/bin/python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$1" --shape "$2" "${@:3}"
  rc=$?; date -Iseconds; echo "elapsed=$(( $(date +%s) - s ))s rc=$rc"; echo $rc > "$RCFILE"
' _ "$dir" "$shape" "$@" > "$P/receipts/$name.log" 2>&1 < /dev/null &

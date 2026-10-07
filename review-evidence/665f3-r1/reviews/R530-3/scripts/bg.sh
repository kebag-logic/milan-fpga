#!/bin/bash
# [R530] bg.sh NAME CMD... : run CMD in $CLONE in the background; log to $PACKET/receipts/NAME.log, rc to NAME.rc.
# PACKET defaults to this script's parent directory; CLONE to the current directory.
# MILAN_RV32_CC defaults to the pinned SDK extracted under $PACKET/scratch.
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
R=${CLONE:-$PWD}
name=$1; shift
export MILAN_RV32_CC=${MILAN_RV32_CC:-$P/scratch/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc}
rm -f "$P/receipts/$name.rc"
( cd "$R" && { echo "# $(date -Is) cwd=$R head=$(git rev-parse HEAD 2>/dev/null)"; echo "# cmd: $*"; } > "$P/receipts/$name.log"
  cd "$R" && "$@" >> "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &

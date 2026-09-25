#!/bin/sh
# Usage: run_leg.sh <tree> <receipt-dir> <name> <make args...>
# Runs one make target (LEGDIR, default tb/verilator/milan_dp) in an exported candidate tree with the pinned
# simulator and records the command, rc and full log as a receipt.
set -u
TREE=$1; OUT=$2; NAME=$3; shift 3
VERILATOR_BIN=${VERILATOR_BIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
PATH=$(dirname "$VERILATOR_BIN"):$PATH
export PATH
LEGDIR=${LEGDIR:-tb/verilator/milan_dp}
LOG=$OUT/$NAME.log
{
  echo "# cmd: make -C $LEGDIR VERILATOR=$VERILATOR_BIN $*"
  echo "# tree: $TREE"
  echo "# verilator: $($VERILATOR_BIN --version)"
  echo "# start: $(date -u +%FT%TZ)"
} > "$LOG"
make -C "$TREE/$LEGDIR" VERILATOR="$VERILATOR_BIN" "$@" >> "$LOG" 2>&1
RC=$?
echo "# end: $(date -u +%FT%TZ) rc=$RC" >> "$LOG"
echo "$NAME rc=$RC"
exit $RC

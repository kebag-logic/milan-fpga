#!/bin/sh
# usage: PACKET=<packet> VERILATOR=<pinned 5.050> bg.sh <name> <cwd> <cmd...>
# Runs one command and writes $PACKET/receipts/<name>.log and <name>.rc.
P=${PACKET:?set PACKET}
name=$1; shift; cwd=$1; shift
export TMPDIR=$P/scratch/tmp
export VERILATOR=${VERILATOR:?set VERILATOR}
( cd "$cwd" && { echo "# cmd: $*"; echo "# cwd: $cwd"; echo "# start: $(date -Is)"; "$@"; rc=$?; echo "# end: $(date -Is) rc=$rc"; echo $rc > "$P/receipts/$name.rc"; } ) > "$P/receipts/$name.log" 2>&1

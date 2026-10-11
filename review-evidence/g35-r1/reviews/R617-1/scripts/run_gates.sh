#!/bin/sh
# Run the four donor gates at the clone head, concurrently, each with its own
# log and rc file. Usage: run_gates.sh <clone> <receipt-dir>
# The pinned simulator wrapper directory is prepended to PATH so that both
# Makefile builds and the mutation drivers (which call `verilator`) use it.
set -u
CLONE=$1; OUT=$2
PIN=${PIN:-$VALIDATION_TOOLS/pinned-verilator-5.050}
mkdir -p "$OUT"
export PATH="$PIN:$PATH"
cd "$CLONE" || exit 2
verilator --version > "$OUT/verilator_version.txt" 2>&1
git rev-parse HEAD HEAD^{tree} > "$OUT/head.txt"
for g in contract lint docs tb; do
  ( make -j16 "$g" > "$OUT/gate_$g.log" 2>&1; echo $? > "$OUT/gate_$g.rc" ) &
done
wait

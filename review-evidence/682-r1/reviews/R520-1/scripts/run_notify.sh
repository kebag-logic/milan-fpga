#!/bin/sh
# Usage: run_notify.sh <tree> <outdir>  - builds and runs tb/verilator/milan_dp `make notify`
set -u
TREE=$1; OUT=$2; mkdir -p "$OUT"
: "${VERILATOR:?set VERILATOR}"
export VERILATOR VERILATOR_JOBS=${VERILATOR_JOBS:-4} PYTHONHASHSEED=0
{ "$VERILATOR" --version; git -C "$TREE" rev-parse HEAD; git -C "$TREE/protocol-processor" rev-parse HEAD; git -C "$TREE" status --short; sha256sum "$TREE/tb/verilator/milan_dp/sim_nxn.cpp"; date -Is; } > "$OUT/identity.txt" 2>&1
cd "$TREE/tb/verilator/milan_dp" || exit 99
make notify VERILATOR="$VERILATOR" VERILATOR_JOBS="$VERILATOR_JOBS" > "$OUT/notify.log" 2>&1
echo $? > "$OUT/rc"; date -Is >> "$OUT/identity.txt"

#!/bin/sh
# Usage: run_bank_contract.sh CLONE WORK OUT
set -eu
C=$1; W=$2; O=$3
PIN=${PIN:-$VALIDATION_TOOLS/pinned-verilator-5.050}
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$W" "$O"
"$PIN/verilator" --version > "$O/version.txt"
"$PIN/verilator" --cc --exe --build -j 16 --top-module KL_gptp_rx_parser -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC --Mdir "$W/obj" -CFLAGS "-std=c++17 -O2" "$C/hdl/ucpu/gptp_ucpu_pkg.sv" "$C/hdl/wire/KL_gptp_rx_parser.sv" "$HERE/bank_contract.cpp" -o Vbank > "$O/build.log" 2>&1
set +e
"$W/obj/Vbank" > "$O/result.csv" 2>&1
rc=$?
echo "$rc" > "$O/run.rc"
cat "$O/result.csv"
exit "$rc"

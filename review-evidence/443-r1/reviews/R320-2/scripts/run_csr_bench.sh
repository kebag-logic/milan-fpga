#!/usr/bin/env bash
# Build and run tb/verilator/csr (all five executables) in a DISPOSABLE tree.
# usage: run_csr_bench.sh <tree> <verilator> [milan_csr.sv override]
# The suite's own VFLAGS with "-j 0" replaced by "-j 8" (reviewer job cap).
set -u
tree=$1; vl=$2; src=${3:-}
cd "$tree/tb/verilator/csr" || exit 2
make clean >/dev/null
vflags='--cc --exe --build -j 8 +incdir+$(RTL_DIR)/common/csr -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
extra=()
[ -n "$src" ] && extra=("SRCS=$src")
make VERILATOR="$vl" "VFLAGS=$vflags" "${extra[@]}" run

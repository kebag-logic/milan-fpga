#!/bin/sh
# Usage: run_default_timed.sh <clone-copy> <receipt-dir> <shim-bin-dir>
# Cold default render suite, serial outer make -C, four CPUs, VERILATOR_JOBS=2
# (the shape PR #672 and the author used).
set -u
clone=$1; out=$2; bin=$3
export PATH="$bin:$PATH" VERILATOR="$bin/verilator" VERILATOR_JOBS=2
cd "$clone" || exit 99
make -C tb/verilator/milan_dp_render clean >/dev/null 2>&1
{ verilator --version; git rev-parse HEAD; date -u +%FT%TZ; nproc; } > "$out/default.env"
start=$(date +%s.%N)
env -u MAKEFLAGS taskset -c 12-15 make -C tb/verilator/milan_dp_render > "$out/default.log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "rc=$rc elapsed=$(echo "$end - $start" | bc)" > "$out/default.rc"

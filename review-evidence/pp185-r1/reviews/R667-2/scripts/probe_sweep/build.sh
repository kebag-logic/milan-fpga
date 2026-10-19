#!/usr/bin/env bash
# Build the sweep probe against TREE's KL_aecp_notify into OUT.
# Usage: build.sh TREE OUT VERILATOR [extra verilator args...]
set -eu
T=$1; O=$2; V=$3; shift 3
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
"$V" --cc --exe --build -j 4 --top-module KL_aecp_notify \
  -GN_CTRL_P=4 -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 \
  -Wno-fatal -Wno-lint -Wno-style \
  -CFLAGS "-std=c++17 -O2" --Mdir "$O" "$@" \
  "$T/hdl/common/pp_pkg.sv" "$T/hdl/aecp/KL_aecp_notify.sv" "$D/sweep.cpp" -o sweep

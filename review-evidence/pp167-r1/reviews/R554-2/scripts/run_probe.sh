#!/usr/bin/env bash
# usage: run_probe.sh VERILATOR TREE_DIR BUILD_DIR TAG
# Builds scripts/probe_fail_offset.cpp against TREE_DIR's KL_aecp_notify at the
# tb/aecp_notify default shape (N_CTRL_P=2, one stream in/out, N_IF_P=1) and runs it.
set -euo pipefail
V=$1; T=$2; B=$3; TAG=$4
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$B"
"$V" --cc --exe --build -j 4 --top-module KL_aecp_notify \
  -GN_CTRL_P=2 -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 \
  -Wno-fatal -Wno-lint -Wno-style \
  --Mdir "$B" -CFLAGS "-std=c++17 -O2" \
  "$T/hdl/common/pp_pkg.sv" "$T/hdl/aecp/KL_aecp_notify.sv" "$HERE/probe_fail_offset.cpp" \
  -o Vprobe >"$B/build.log" 2>&1
"$B/Vprobe" "$TAG"

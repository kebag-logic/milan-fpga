#!/usr/bin/env bash
# Build probe P2 against a tree's KL_pp_originator. Args: SRC_TREE WORK_DIR
set -euo pipefail
SRC=$1; W=$2; HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"; cp "$HERE/p2_originator.cpp" "$W/"
cd "$W"
${VERILATOR:-verilator} --cc --exe --build -j 4 --top-module KL_pp_originator -Wno-fatal -Wno-lint -Wno-style \
  -CFLAGS "-std=c++17 -O2" "$SRC/hdl/common/pp_pkg.sv" "$SRC/hdl/packet_engine/KL_pp_originator.sv" \
  p2_originator.cpp -o Vp2 >build.log 2>&1 || { tail -30 build.log; exit 3; }
./obj_dir/Vp2 | grep '^\[probe'

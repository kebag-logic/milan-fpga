#!/usr/bin/env bash
# Build reviewer_probes.cpp against one processor tree's talker and run it.
# Usage: run_probes.sh <processor-tree> <build-dir>   (needs PINNED_VERILATOR)
set -euo pipefail
pp=$(cd "$1" && pwd) build=$2 here=$(cd "$(dirname "$0")" && pwd)
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
rm -rf "$build"; mkdir -p "$build"
"$PINNED_VERILATOR" --cc --exe --build -j 8 --Mdir "$build/obj" \
  --top-module KL_acmp_talker -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -CFLAGS "-std=c++17 -O2 -I$pp/tb -I$pp/tb/acmp_talker" \
  "$pp/hdl/common/pp_pkg.sv" "$pp/hdl/srp/srp_pkg.sv" "$pp/hdl/acmp/KL_acmp_talker.sv" \
  "$here/reviewer_probes.cpp" -o probes >"$build/build.log" 2>&1 \
  || { tail -30 "$build/build.log"; exit 3; }
"$build/obj/probes" | grep -E '^(PROBE|PROBES|BEHAVIOR)'

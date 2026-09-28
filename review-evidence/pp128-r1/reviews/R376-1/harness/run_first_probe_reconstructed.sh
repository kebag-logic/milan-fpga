#!/usr/bin/env bash
# Build and run the published first-probe harness source against a processor
# revision and the parent's MAAP shim, using the reviewer-reconstructed top.
# Usage: run_first_probe_reconstructed.sh <processor-tree> <shim.sv> <harness.cpp> <build-dir>
# Needs PINNED_VERILATOR (the pinned Verilator 5.050 wrapper).
set -euo pipefail
pp=$(cd "$1" && pwd) shim=$(readlink -f "$2") cpp=$(readlink -f "$3") build=$4
here=$(cd "$(dirname "$0")" && pwd)
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
rm -rf "$build"; mkdir -p "$build"
sha256sum "$pp/hdl/acmp/KL_acmp_talker.sv" "$shim" "$cpp" "$here/first_probe_top.sv"
"$PINNED_VERILATOR" --cc --exe --build -j 8 --Mdir "$build/obj" \
  --top-module first_probe_top --prefix VKL_acmp_talker \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
  -CFLAGS "-std=c++17 -O2 -I$pp/tb -I$pp/tb/acmp_talker" \
  "$pp/hdl/common/pp_pkg.sv" "$pp/hdl/srp/srp_pkg.sv" \
  "$pp/hdl/acmp/KL_acmp_talker.sv" "$shim" "$here/first_probe_top.sv" \
  "$cpp" -o first_probe >"$build/build.log" 2>&1 \
  || { tail -30 "$build/build.log"; exit 3; }
"$build/obj/first_probe"

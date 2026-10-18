#!/usr/bin/env bash
# run.sh <tree> <build-dir>: build the probe against <tree>/hdl/srp/KL_srp_domain.sv and run it
set -eu
tree="$1"; b="$2"; here="$(cd "$(dirname "$0")" && pwd)"
export PATH="<tools>/pinned-verilator-5.050:$PATH"
verilator --version
sha256sum "$tree/hdl/srp/KL_srp_domain.sv" "$here/probe.cpp"
rm -rf "$b"; mkdir -p "$b"
verilator --cc --exe --build -j 4 -Wno-fatal --top-module KL_srp_domain -Mdir "$b/obj" \
  "$tree/hdl/srp/KL_srp_domain.sv" "$here/probe.cpp" > "$b/build.log" 2>&1
"$b/obj/VKL_srp_domain"

#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build the reviewer cross-source probe against a source tree's own
# KL_srp_admission.sv + tb/srp_admission/srp_admission_wrap.sv.
# Usage: run.sh <source-tree> <verilator> <build-dir> <N> [admission.sv override]
set -uo pipefail
SRC=$1; VL=$2; B=$3; N=$4; ADM=${5:-$SRC/hdl/srp/KL_srp_admission.sv}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$B"; mkdir -p "$B"
"$VL" --cc --exe --build -j 8 --top-module srp_admission_wrap -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  -GN_SOURCES_P="$N" --Mdir "$B" \
  -CFLAGS "-std=c++17 -O2 -DTB_SOURCES=$N" \
  "$ADM" "$SRC/tb/srp_admission/srp_admission_wrap.sv" "$HERE/probe_main.cpp" \
  -o Vprobe >"$B/build.log" 2>&1 || { echo "BUILD FAILED"; tail -20 "$B/build.log"; exit 2; }
"$B/Vprobe"

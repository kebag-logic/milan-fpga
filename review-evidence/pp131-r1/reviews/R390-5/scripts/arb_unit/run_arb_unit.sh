#!/bin/sh
# Build and run the reviewer's arbiter unit probe against the arbiter of a
# given tree (the exact head, or a mutant copy).
# Usage: run_arb_unit.sh <tree> <build-dir> <verilator>
set -u
T=$(realpath "$1"); B=$(realpath -m "$2"); VL=$3
HERE=$(dirname "$(realpath "$0")")
rm -rf "$B"; mkdir -p "$B"
cp "$HERE/arb_unit.cpp" "$B/"
cd "$B" && "$VL" --cc --exe --build -j 2 --top-module KL_pp_nvm_mgr_arb --prefix Varb \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  "$T/hdl/packet_engine/KL_pp_nvm_mgr_arb.sv" arb_unit.cpp -o arb_unit > build.log 2>&1 \
  || { echo "BUILD FAILED"; tail -20 build.log; exit 2; }
./obj_dir/arb_unit; echo "rc=$?"

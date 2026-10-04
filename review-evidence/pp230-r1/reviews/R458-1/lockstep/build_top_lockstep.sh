#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build the committed tb/srp_top harness against the lockstep KL_srp_top.
# usage: build_top_lockstep.sh <base_tree> <head_tree> <work_dir>
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
BASE=$1; HEAD=$2; W=$3
VERILATOR=${VERILATOR:-verilator}
mkdir -p "$W"
python3 "$HERE/gen_top_lockstep.py" "$BASE" "$HEAD" "$W"
cp "$HEAD"/tb/srp_top/*.cpp "$HEAD"/tb/srp_top/*.sv "$W"/
[ -n "$(ls "$HEAD"/tb/srp_top/*.hpp 2>/dev/null)" ] && cp "$HEAD"/tb/srp_top/*.hpp "$W"/
HDL="$HEAD/hdl"
cd "$W"
# the committed wrapper reads DUT internals; point them at the head copy
sed -i 's/u_dut\./u_dut.u_new./g' srp_top_wrap.sv
"$VERILATOR" --cc --exe --build -j 4 --top-module srp_top_wrap \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -Wno-MULTIDRIVEN -Wno-BLKSEQ -Wno-UNOPTFLAT \
  --x-initial unique --x-assign unique \
  -CFLAGS "-std=c++17 -O2 -I$W -I$HEAD/tb/srp_top" \
  "$HDL/common/pp_pkg.sv" "$HDL/srp/srp_pkg.sv" "$HDL/common/KL_pp_prng.sv" \
  "$HDL/common/KL_pp_timer_service.sv" "$HDL/packet_engine/KL_pp_tx_slots.sv" \
  srp_ref/*.sv srp_new/*.sv KL_srp_top_lockstep.sv srp_top_wrap.sv \
  sim_main.cpp "$HERE/rand_init.cpp" -o Vsrp_top_sim > build.log 2>&1
echo "built $W/obj_dir/Vsrp_top_sim"

#!/bin/sh
# build.sh <tree> <out> [depth]: builds the fuzz harness against a tree's encoder wrap
T=$1; O=$2; D=${3:-12}; V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
H=$(dirname "$(readlink -f "$0")")
mkdir -p "$O"; sed "s/KL_srp_encoder u_enc (/KL_srp_encoder #(.DEPTH_P($D)) u_enc (/" "$T/tb/srp_encoder/srp_tb_wrap.sv" > "$O/srp_tb_wrap.sv"
cd "$O" && "$V" --cc --exe --build -j 4 --top-module srp_tb_wrap -Wno-fatal -Wno-lint -CFLAGS "-std=c++17 -O2" \
 "$T/hdl/common/pp_pkg.sv" "$T/hdl/packet_engine/KL_pp_tx_slots.sv" "$T/hdl/srp/KL_srp_encoder.sv" "$T/hdl/srp/KL_srp_domain.sv" "$T/hdl/srp/KL_srp_vlan.sv" srp_tb_wrap.sv "$H/fuzz_main.cpp" -o Vsrp_sim > build.log 2>&1 || { tail -20 build.log; exit 1; }

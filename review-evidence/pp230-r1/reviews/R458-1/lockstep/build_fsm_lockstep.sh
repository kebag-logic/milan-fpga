#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build ls_fsm at N contexts. usage: build_fsm_lockstep.sh <ref_dir> <new_dir> <head_tree> <N> <work>
# <ref_dir>/<new_dir> hold the renamed modules written by gen_top_lockstep.py
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
REF=$1; NEW=$2; HEAD=$3; N=$4; W=$5
VERILATOR=${VERILATOR:-verilator}
mkdir -p "$W"; cd "$W"
"$VERILATOR" --cc --exe --build -j 2 --top-module ls_fsm -GN="$N" \
  -Wno-fatal -Wno-WIDTH -Wno-UNUSED -Wno-DECLFILENAME -Wno-MULTIDRIVEN -Wno-PROCASSINIT \
  --x-initial unique --x-assign unique \
  -CFLAGS "-std=c++17 -O2" \
  "$HEAD/hdl/common/pp_pkg.sv" "$HEAD/hdl/srp/srp_pkg.sv" \
  "$REF/KL_srp_talker_fsm_ref.sv" "$REF/KL_srp_listener_fsm_ref.sv" "$REF/KL_srp_admission_ref.sv" \
  "$NEW/KL_srp_talker_fsm_new.sv" "$NEW/KL_srp_listener_fsm_new.sv" "$NEW/KL_srp_admission_new.sv" \
  "$HERE/ls_fsm.sv" "$HERE/ls_fsm_main.cpp" -o Vls_fsm > build.log 2>&1
echo "built $W/obj_dir/Vls_fsm (N=$N)"

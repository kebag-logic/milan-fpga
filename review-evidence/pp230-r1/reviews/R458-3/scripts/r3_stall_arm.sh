#!/usr/bin/env bash
# Build the disposable R458-3 stall arm (walk_main.cpp + r3_offer_not_accepted) against an hdl/srp.
# usage: r3_stall_arm.sh <hdl tree root> <dir with walk_main.cpp, srp_walk_wrap.sv, verilator_harness.hpp> <M> <N> <out>
set -u
H=$1; D=$2; M=$3; N=$4; O=$5
verilator --cc --exe --build -j 0 --top-module srp_walk_wrap --x-initial unique -Wno-fatal -Wno-lint -Wno-style \
  -GN_SOURCES_P=$M -GN_SINKS_P=$N -CFLAGS "-std=c++17 -O2 -I$D -DTB_SOURCES=$M -DTB_SINKS=$N" --Mdir $O \
  $H/hdl/common/pp_pkg.sv $H/hdl/srp/srp_pkg.sv $H/hdl/srp/KL_srp_talker_fsm.sv $H/hdl/srp/KL_srp_listener_fsm.sv \
  $D/srp_walk_wrap.sv $D/walk_main.cpp -o Vw > $O.build.log 2>&1 || { echo "BUILD-FAIL $O"; tail -5 $O.build.log; exit 3; }
$O/Vw +verilator+rand+reset+2 +verilator+seed+230

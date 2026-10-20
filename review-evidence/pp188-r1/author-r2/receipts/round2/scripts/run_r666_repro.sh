#!/usr/bin/env bash
# usage: run_r666_repro.sh <scratch tree with the R666-1 probe patch>: build the
# pp_top model once, run the ACMP phase stalled and with REVIEW_NO_TX_STALL, and
# the stream suite; each run's log, rc and seconds beside the tree.
set -u
. <scratch>/scripts/env.sh
W=$1
cd "$W/tb/pp_top" || exit 2
make gsi-build VERILATOR="$VERILATOR" > "$W.build.log" 2>&1; echo $? > "$W.build.rc"
./obj_dir/Vpp_top_sim --acmp-only > "$W.stall.log" 2>&1; echo $? > "$W.stall.rc"
REVIEW_NO_TX_STALL=1 ./obj_dir/Vpp_top_sim --acmp-only > "$W.no-stall.log" 2>&1; echo $? > "$W.no-stall.rc"
cd "$W/tb/srp_stream_fsms" || exit 2
make RUN_ARGS=suite VERILATOR="$VERILATOR" > "$W.fsms.log" 2>&1; echo $? > "$W.fsms.rc"
echo done > "$W.done"

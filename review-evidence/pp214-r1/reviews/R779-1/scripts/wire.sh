#!/bin/bash
# usage: wire.sh <head|base-rtl>: build the frame-dumping copy and run the groups PR #213 graded end to end
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
export PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH DUMP_FRAMES=1
v=$1; t=$PKT/scratch/wire/$v/tb/srp_top
make -C "$t" run RUN_ARGS=share > "$PKT/scratch/wire/$v.share.log" 2>&1; echo $? > "$PKT/scratch/wire/$v.share.rc"
"$t/obj_dir/Vsrp_top_sim" link > "$PKT/scratch/wire/$v.link.log" 2>&1; echo $? > "$PKT/scratch/wire/$v.link.rc"
"$t/obj_dir/Vsrp_top_sim" domjoin > "$PKT/scratch/wire/$v.domjoin.log" 2>&1; echo $? > "$PKT/scratch/wire/$v.domjoin.rc"

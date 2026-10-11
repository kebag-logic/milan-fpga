#!/bin/sh
# R601-1 extra-shape lockstep probe for KL_chan_map_capture.
# Usage: shape_probe.sh <tree> <outdir>
# Builds the lane's own chmap lockstep harness (reference vs shipping, same
# flags as the Makefile's LS_FLAGS) at the SHIPPING 8x8 capture parameters:
# N_SLOTS_P=32, N_LB_STREAMS_P=1, N_LB_CH_P=2 (milan_datapath with
# LOOPBACK_P=0, configs/endstation_ax7101_8x8.yaml loopback_lane: false).
# Only the [LS] lines (every output identical in every cycle) are meaningful
# here: the [SK] value oracles assume an 8-channel loopback bucket.
set -u
TREE=$1; OUT=$2
PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH; export PATH
D="$TREE/tb/verilator/chmap_capture"
mkdir -p "$OUT"
cd "$D" || exit 2
verilator --cc --exe --build -j 8 --top-module chmap_lockstep_wrap \
  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -Wno-DECLFILENAME -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
  --Mdir "$OUT/obj_ship8x8" -GN_SLOTS_P=32 -GN_LB_STREAMS_P=1 -GN_LB_CH_P=2 \
  -CFLAGS "-DSLOTS_TB=32 -DNLB_TB=1 -Wall -Wextra" \
  reference/KL_chan_map_capture_ref.sv ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv \
  chmap_lockstep_wrap.sv sim_lockstep.cpp -o Vchmap_lockstep > "$OUT/ship8x8.build.log" 2>&1
echo "build rc=$?" >> "$OUT/ship8x8.build.log"
"$OUT/obj_ship8x8/Vchmap_lockstep" > "$OUT/ship8x8.run.log" 2>&1
echo "run rc=$?" >> "$OUT/ship8x8.run.log"
grep '\[LS\]' "$OUT/ship8x8.run.log"
tail -1 "$OUT/ship8x8.run.log"

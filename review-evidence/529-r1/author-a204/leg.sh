#!/bin/sh
# Build (and optionally run) one milan_dp sim_nxn leg with the pinned
# simulator, through the suite's own exported source list and flag set.
#   leg.sh <nxn|nxn8|nxndv|nxn4c|notify> <abs-mdir> [abs-dp-src] [run]
set -eu
LANE=$LANES/529-crf-input-counters
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
cd "$LANE/tb/verilator/milan_dp"
leg=$1; mdir=$2; dp=${3:-}; run=${4:-}
if [ -n "$dp" ]; then
  SRCS=$(make -s print-srcs VERILATOR_JOBS=8 DP_SRC="$dp")
else
  SRCS=$(make -s print-srcs VERILATOR_JOBS=8)
fi
FL=$(make -s print-dp-vflags VERILATOR_JOBS=8)
CFG=../../../configs/generated
case $leg in
  nxn)    ARGS="+incdir+$CFG/endstation_arty_4x4 $FL --Mdir $mdir -GN_STREAMS=4"; BIN=Vmilan_dp_nxn ;;
  nxn4c)  ARGS="+incdir+$CFG/endstation_arty_4x4 $FL --Mdir $mdir -GN_STREAMS=4 -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 -GAUDIO_IF_I2S_PAIR_P=1"; BIN=Vmilan_dp_nxn4c ;;
  nxn8)   ARGS="+incdir+$CFG/endstation_ax7101_8x8 $FL --Mdir $mdir -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS \"-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra\""; BIN=Vmilan_dp_nxn8 ;;
  notify) ARGS="+incdir+$CFG/endstation_ax7101_1x1_tdm8 $FL --Mdir $mdir -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 -CFLAGS \"-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra\""; BIN=Vmilan_dp_notify ;;
  *) echo "unknown leg $leg" >&2; exit 2 ;;
esac
eval verilator $ARGS $SRCS sim_nxn.cpp -o $BIN
if [ "$run" = run ]; then
  "$mdir/$BIN"
fi

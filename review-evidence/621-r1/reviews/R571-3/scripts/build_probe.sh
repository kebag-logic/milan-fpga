#!/bin/sh
# Build one probe harness against the exact-head RTL, same flags as phc_step.py.
# Usage: build_probe.sh <repo root> <probe dir containing sim_phc_step.cpp> <jobs>
set -eu
ROOT=$1; DIR=$2; JOBS=$3
V=${VERILATOR:-verilator}
D=$ROOT/gptp-processor/hdl
cp "$ROOT/tb/verilator/gptp_plane/gptp_plane_wrap.sv" "$DIR/"
# The harness includes ../../common/verilator_harness.hpp relative to itself.
mkdir -p "$DIR/../../common"
cp "$ROOT/tb/common/verilator_harness.hpp" "$DIR/../../common/"
"$V" --cc --exe --build -j "$JOBS" --top-module gptp_plane_wrap --Mdir "$DIR/obj" \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -GCLK_HZ_P=8000000 -GPHC_INCR_P=2097152000 \
  -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
  "$DIR/gptp_plane_wrap.sv" "$ROOT/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv" \
  "$D/ucpu/gptp_ucpu_pkg.sv" "$D/ucpu/KL_gptp_ucpu.sv" "$D/wire/KL_gptp_rx_parser.sv" \
  "$D/wire/KL_gptp_tx_slot.sv" "$D/common/KL_gptp_timer.sv" "$D/top/KL_gptp_engine.sv" \
  "$DIR/sim_phc_step.cpp" -o phc_step

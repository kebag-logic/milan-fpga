#!/bin/sh
# Reviewer probe (R593-2): build and run the gptp_shadow-stimulus dual differential.
# Usage: run_shadow_dual.sh <exact-head tree copy> <verilator> <dev dir>
# Run from the directory make_shadow_dual.py wrote.
set -eu
TREE=$1; VERILATOR=$2; DEV=$3
S=$TREE/tb/verilator/gptp_shadow
H=$TREE/hdl; GP=$TREE/gptp-processor; AX=$TREE/third_party/verilog-axis/rtl
python3 -I "$GP/hdl/ucode/gen_gptp_ucode.py" --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex
"$VERILATOR" --cc --exe --build -j 8 --top-module gptp_shadow_wrap \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
  -Wno-PINCONNECTEMPTY -Wno-IMPLICIT \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$S -Wall -Wextra" \
  gptp_shadow_wrap.sv gptp_shadow_wrap_head.sv \
  "$DEV/gptp_shadow_wrap_dev.sv" "$DEV/KL_gptp_shadow_dev.sv" "$DEV/KL_gptp_txret_dev.sv" \
  "$DEV/KL_gptp_engine_dev.sv" "$DEV/KL_gptp_timer_dev.sv" \
  "$H/ieee8021as/ptp_timestamp/timestamp_counter.sv" \
  "$H/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv" \
  "$H/ieee8021as/gptp_plane/KL_gptp_txticket.sv" "$H/ieee8021as/gptp_plane/KL_gptp_txret.sv" \
  "$H/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv" "$H/ieee8021as/gptp_plane/KL_gptp_shadow.sv" \
  "$H/common/KL_link_guard.sv" "$H/common/cdc_pulse.sv" "$H/common/cdc_handshake.sv" \
  "$AX/axis_fifo.v" "$GP/hdl/ucpu/gptp_ucpu_pkg.sv" "$GP/hdl/ucpu/KL_gptp_ucpu.sv" \
  "$GP/hdl/wire/KL_gptp_rx_parser.sv" "$GP/hdl/wire/KL_gptp_tx_slot.sv" \
  "$GP/hdl/common/KL_gptp_timer.sv" "$GP/hdl/top/KL_gptp_engine.sv" \
  sim_main.cpp -o Vshadow_dual
./obj_dir/Vshadow_dual

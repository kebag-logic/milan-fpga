#!/bin/sh
# Reviewer probe (R593-2): build and run the dual-instance differential.
# Usage: run_dual.sh <exact-head tree copy> <verilator> [extra verilator flags...]
# Run from <tree>/tb/verilator/gptp_dual after make_dual.py and the dev copies.
set -eu
TREE=$1; VERILATOR=$2; shift 2
G=$TREE/tb/verilator/gptp_tables
H=$TREE/hdl; GP=$TREE/gptp-processor; AX=$TREE/third_party/verilog-axis/rtl
python3 -I "$GP/hdl/ucode/gen_gptp_ucode.py" --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex
"$VERILATOR" --cc --exe --build -j 8 --top-module gptp_tables_wrap \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
  -Wno-PINCONNECTEMPTY -Wno-PINMISSING -Wno-MULTIDRIVEN \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 "$@" \
  -CFLAGS "-std=c++17 -O2 -I$G -Wall -Wextra" \
  gptp_tables_wrap.sv "$TREE/tb/verilator/gptp_shadow/gptp_shadow_wrap.sv" \
  dev/gptp_shadow_wrap_dev.sv dev/KL_gptp_shadow_dev.sv dev/KL_gptp_txret_dev.sv \
  dev/KL_gptp_engine_dev.sv dev/KL_gptp_timer_dev.sv \
  "$H/ieee8021as/ptp_timestamp/timestamp_counter.sv" \
  "$H/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv" \
  "$H/ieee8021as/gptp_plane/KL_gptp_txticket.sv" "$H/ieee8021as/gptp_plane/KL_gptp_txret.sv" \
  "$H/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv" "$H/ieee8021as/gptp_plane/KL_gptp_shadow.sv" \
  "$H/common/KL_link_guard.sv" "$H/common/cdc_pulse.sv" "$H/common/cdc_handshake.sv" \
  "$AX/axis_fifo.v" "$GP/hdl/ucpu/gptp_ucpu_pkg.sv" "$GP/hdl/ucpu/KL_gptp_ucpu.sv" \
  "$GP/hdl/wire/KL_gptp_rx_parser.sv" "$GP/hdl/wire/KL_gptp_tx_slot.sv" \
  "$GP/hdl/common/KL_gptp_timer.sv" "$GP/hdl/top/KL_gptp_engine.sv" \
  sim_main.cpp -o Vdual
./obj_dir/Vdual

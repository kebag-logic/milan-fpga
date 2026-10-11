#!/bin/sh
# Reviewer probe (R593-2): the exact-head gptp_tables suite built with
# --x-initial unique and run with random initial state, so every
# un-reset memory (including the converted ledger, result and deadline RAMs)
# starts with random contents instead of zero.
# Usage: run_xinit.sh <exact-head tree copy> <verilator> <build dir> <seed>...
set -eu
TREE=$1; VERILATOR=$2; BUILD=$3; shift 3
G=$TREE/tb/verilator/gptp_tables
H=$TREE/hdl; GP=$TREE/gptp-processor; AX=$TREE/third_party/verilog-axis/rtl
mkdir -p "$BUILD"; cd "$BUILD"
python3 -I "$GP/hdl/ucode/gen_gptp_ucode.py" --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex
"$VERILATOR" --cc --exe --build -j 8 --top-module gptp_tables_wrap --x-initial unique \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
  -Wno-PINCONNECTEMPTY -Wno-PINMISSING \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$G -Wall -Wextra" \
  "$G/waivers.vlt" "$G/gptp_tables_wrap.sv" "$TREE/tb/verilator/gptp_shadow/gptp_shadow_wrap.sv" \
  "$H/ieee8021as/ptp_timestamp/timestamp_counter.sv" \
  "$H/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv" \
  "$H/ieee8021as/gptp_plane/KL_gptp_txticket.sv" "$H/ieee8021as/gptp_plane/KL_gptp_txret.sv" \
  "$H/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv" "$H/ieee8021as/gptp_plane/KL_gptp_shadow.sv" \
  "$H/common/KL_link_guard.sv" "$H/common/cdc_pulse.sv" "$H/common/cdc_handshake.sv" \
  "$AX/axis_fifo.v" "$GP/hdl/ucpu/gptp_ucpu_pkg.sv" "$GP/hdl/ucpu/KL_gptp_ucpu.sv" \
  "$GP/hdl/wire/KL_gptp_rx_parser.sv" "$GP/hdl/wire/KL_gptp_tx_slot.sv" \
  "$GP/hdl/common/KL_gptp_timer.sv" "$GP/hdl/top/KL_gptp_engine.sv" \
  "$G/sim_main.cpp" -o Vxinit
for seed in "$@"; do
  echo "=== seed $seed"
  ./obj_dir/Vxinit +verilator+rand+reset+2 +verilator+seed+$seed || echo "rc $?"
done

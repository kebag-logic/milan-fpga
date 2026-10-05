#!/usr/bin/env bash
# Reviewer cross-check (not the #638 recipe): KL_aecp_notify alone through
# sv2v + yosys synth_xilinx at the 1x1 binding the lane's Vivado module run used.
# Usage: yosys_notify_area.sh TREE OUTDIR LABEL
set -euo pipefail
tree=$1; out=$2; label=$3
mkdir -p "$out"
G="-DN_CTRL_P=16"
sv2v --top=KL_aecp_notify "$tree/hdl/common/pp_pkg.sv" "$tree/hdl/aecp/KL_aecp_notify.sv" \
  > "$out/$label-notify.v"
yosys -q -l "$out/$label-yosys.log" -p "read_verilog $out/$label-notify.v; \
  chparam -set N_CTRL_P 16 -set N_STREAM_IN_P 2 -set N_STREAM_OUT_P 2 \
    -set TL_TIMEOUT_MS_P 300000 -set LOCK_TIMEOUT_MS_P 60000 -set TMR_SLOTS_P 61 \
    -set TMR_REGMON_BASE_P 7 -set TMR_LOCK_SLOT_P 43 -set TMR_IDENT_SLOT_P 44 \
    -set EN_IDENTIFY_NOTIF_P 0 KL_aecp_notify; \
  synth_xilinx -top KL_aecp_notify -flatten; stat" > /dev/null

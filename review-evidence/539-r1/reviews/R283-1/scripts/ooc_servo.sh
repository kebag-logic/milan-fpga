#!/bin/sh
# Out-of-context area of KL_mmcm_drp_servo, the syn/yosys/ooc.sh recipe for
# this one top (sv2v --top, then synth_xilinx -family xc7 -top -flatten; stat),
# without the ROM generation that script does for the datapath tops.
# usage: ooc_servo.sh <src-tree> <out-dir>
set -eu
SRC=$1; OUT=$2
mkdir -p "$OUT"
C="$SRC/hdl/common"
sv2v --top=KL_mmcm_drp_servo "$C/cdc_pulse.sv" "$C/cdc_handshake.sv" \
  "$SRC/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv" > "$OUT/servo.v"
yosys -q -p "read_verilog $OUT/servo.v; synth_xilinx -family xc7 -top KL_mmcm_drp_servo -flatten; tee -o $OUT/stat.txt stat" > "$OUT/yosys.log" 2>&1
sha256sum "$SRC/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv" "$OUT/servo.v"
grep -E 'LUT[1-6]|FDRE|FDSE|FDCE|FDPE|CARRY4|DSP48E1|cells' "$OUT/stat.txt"

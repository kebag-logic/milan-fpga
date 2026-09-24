#!/bin/sh
# Standalone servo area at base and head, the ooc.sh recipe (sv2v, then
# yosys synth_xilinx -family xc7 -top KL_mmcm_drp_servo -flatten; stat).
set -u
. "$(dirname "$0")/env.sh"
for rev in "$BASE_SHA" "$HEAD_SHA"; do
  W="$PKT/scratch/ooc/$rev"; rm -rf "$W"; mkdir -p "$W"
  git -C "$CLONE" archive "$rev" hdl/common/cdc_pulse.sv hdl/common/cdc_handshake.sv hdl/ieee1722/crf/KL_mmcm_drp_servo.sv | tar -x -C "$W"
  sv2v --top=KL_mmcm_drp_servo "$W/hdl/common/cdc_pulse.sv" "$W/hdl/common/cdc_handshake.sv" "$W/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv" > "$W/servo.v" || { echo "sv2v FAIL $rev"; continue; }
  (cd "$W" && yosys -q -p "read_verilog servo.v; synth_xilinx -family xc7 -top KL_mmcm_drp_servo -flatten; tee -o stat.txt stat" > yosys.log 2>&1) || echo "yosys FAIL $rev"
  echo "== $rev"
  grep -E "LUT[1-6]|FDRE|FDSE|FDCE|FDPE|CARRY4|DSP48E1|Number of cells|cells$" "$W/stat.txt" | sed 's/^ */  /'
done

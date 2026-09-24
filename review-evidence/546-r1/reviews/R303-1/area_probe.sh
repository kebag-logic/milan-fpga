#!/bin/sh
# Focused OOC area probe: synth_xilinx -family xc7 -flatten on the two touched
# modules, base tree vs head tree. Usage: area_probe.sh <base_root> <head_root> <tmpdir>
set -eu
for side in "$1" "$2"; do
  for top in KL_crf_rx; do  # the servo needs an SV front-end this host lacks
    st="$3/stat_$(basename "$side")_$top.txt"
    yosys -q -p "read_verilog -sv $side/hdl/ieee1722/crf/$top.sv $side/hdl/common/cdc_pulse.sv $side/hdl/common/cdc_handshake.sv; synth_xilinx -family xc7 -flatten -top $top; tee -q -o $st stat" >/dev/null 2>&1 || echo "yosys rc=$? for $side $top"
    printf '%s %s ' "$(basename "$side")" "$top"
    awk '$2 ~ /^LUT[1-6]$/{l+=$1} $2 ~ /^FD[RSCP]E$/{f+=$1} $2=="CARRY4"{c+=$1} $2 ~ /^RAMB18/{r+=$1} $2 ~ /^DSP48/{d+=$1} END{printf "LUT=%d FF=%d CARRY4=%d RAMB18=%d DSP=%d\n",l,f,c,r,d}' "$st"
  done
done

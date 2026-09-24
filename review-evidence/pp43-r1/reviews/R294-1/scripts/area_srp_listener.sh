#!/usr/bin/env bash
# R294 area probe A1: generic Xilinx-7 mapping (yosys synth_xilinx) of
# KL_srp_listener_fsm alone, head vs base, N_SINKS_P = 1 and 8.
# All module outputs are ports here, so this isolates the LUT cost of the
# new FailureInformation comparators; it does NOT model the top-level
# pruning of the previously unconnected bridge output.
# Usage: area_srp_listener.sh <head-tree> <base-tree> <outdir>
set -euo pipefail
head=$1; base=$2; out=$3; mkdir -p "$out"
for tag in head base; do
  tree=$head; [ "$tag" = base ] && tree=$base
  sv2v "$tree/hdl/common/pp_pkg.sv" "$tree/hdl/srp/srp_pkg.sv" \
       "$tree/hdl/srp/KL_srp_listener_fsm.sv" > "$out/$tag-srp_listener.v"
  for n in 1 8; do
    yosys -q -l "$out/$tag-n$n.log" -p "read_verilog $out/$tag-srp_listener.v; \
      chparam -set N_SINKS_P $n KL_srp_listener_fsm; \
      synth_xilinx -family xc7 -flatten -top KL_srp_listener_fsm; stat" >/dev/null
    cells=$(awk '/^[0-9]+\. Printing statistics/ {buf=""} {buf=buf $0 "\n"} END {printf "%s", buf}' "$out/$tag-n$n.log")
    luts=$(echo "$cells" | awk '$2 ~ /^LUT[1-6]$/ {s+=$1} END {print s+0}')
    ffs=$(echo "$cells" | awk '$2 ~ /^FD[A-Z]*$/ {s+=$1} END {print s+0}')
    echo "$tag N_SINKS_P=$n LUT=$luts FF=$ffs"
  done
done

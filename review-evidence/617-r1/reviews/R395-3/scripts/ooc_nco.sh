#!/usr/bin/env bash
# ooc_nco.sh NCO_SV OUTDIR TAG: syn/yosys/ooc.sh's per-top recipe (sv2v, then
# synth_xilinx -family xc7 -flatten; stat) applied to KL_media_nco alone, at
# CLK_FREQ_HZ_P 50 MHz and 100 MHz (chparam, as OOC_CHPARAM does).
set -euo pipefail
src=$1; out=$2; tag=$3
mkdir -p "$out"
sv2v "$src" > "$out/$tag.v"
for hz in 50000000 100000000; do
  yosys -q -p "read_verilog $out/$tag.v; chparam -set CLK_FREQ_HZ_P $hz KL_media_nco; synth_xilinx -family xc7 -top KL_media_nco -flatten; tee -o $out/$tag-$hz.stat stat" > /dev/null
  printf "%s %s: " "$tag" "$hz"
  awk '/LUT[1-6]|FDRE|FDSE|FDCE|FDPE|CARRY4|DSP48E1|RAMB/ {printf "%s=%s ", $2, $1}' "$out/$tag-$hz.stat"; echo
done

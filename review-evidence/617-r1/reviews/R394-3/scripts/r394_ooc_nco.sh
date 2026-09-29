#!/usr/bin/env bash
# r394_ooc_nco.sh OUTDIR NCO_SRC TAG [NAME=VALUE ...] : KL_media_nco alone, sv2v then yosys
# `synth_xilinx -family xc7 -top KL_media_nco -flatten` (the syn/yosys/ooc.sh recipe for a leaf top,
# which does not list this top), at CLK_FREQ_HZ_P = 50 MHz and 100 MHz, plus any extra chparam
# (milan_datapath binds TRIMW_P=18); writes TAG_<hz>.stat.txt and prints LUT/FF/CARRY4/DSP.
set -euo pipefail
out=$1; src=$2; tag=$3; shift 3
chp=""; for kv in "$@"; do chp="$chp chparam -set ${kv%%=*} ${kv#*=} KL_media_nco;"; done
mkdir -p "$out"
sv2v --top=KL_media_nco "$src" > "$out/$tag.v"
for hz in 50000000 100000000; do
  yosys -q -p "read_verilog $out/$tag.v; chparam -set CLK_FREQ_HZ_P $hz KL_media_nco;$chp synth_xilinx -family xc7 -top KL_media_nco -flatten; tee -o $out/${tag}_$hz.stat.txt stat" > /dev/null
  s=$out/${tag}_$hz.stat.txt
  luts=$(grep -E '^\s+[0-9]+\s+LUT[1-6]$' "$s" | awk '{t+=$1} END {print t+0}')
  ff=$(grep -E '^\s+[0-9]+\s+FD' "$s" | awk '{t+=$1} END {print t+0}')
  c4=$(grep -E '^\s+[0-9]+\s+CARRY4$' "$s" | awk '{t+=$1} END {print t+0}')
  dsp=$(grep -E '^\s+[0-9]+\s+DSP48E1$' "$s" | awk '{t+=$1} END {print t+0}')
  echo "$tag $hz ${*:-module defaults}: LUT $luts FF $ff CARRY4 $c4 DSP48E1 $dsp"
done
rm -f "$out/$tag.v"

#!/usr/bin/env bash
# R294 area probe A2: yosys synth_xilinx (xc7) of protocol_processor_top at a
# chosen stream shape, for one extracted tree. Reviewer estimate only: this is
# NOT the Vivado OOC instrument in syn/ooc and not a routed result.
# Usage: area_top.sh <tree> <n_in> <n_out> <outdir> <tag>
set -euo pipefail
tree=$1; nin=$2; nout=$3; out=$4; tag=$5
mkdir -p "$out/$tag"; w=$out/$tag
sv2v $(find "$tree/hdl" -name '*_pkg.sv' | sort) \
     $(find "$tree/hdl" -name '*.sv' ! -name '*_pkg.sv' | sort) > "$w/all.v"
( cd "$tree/hdl/aecp/ucode" && python3 gen_ucode.py -o "$w/ucode.hex" >/dev/null )
( cd "$tree/hdl/acmp/rom" && python3 gen_ltn_rom.py -o "$w/ltn_rom.hex" >/dev/null )
cd "$w"
yosys -q -l "$w/yosys.log" -p "read_verilog all.v; \
  chparam -set N_STREAM_IN_P $nin -set N_STREAM_OUT_P $nout protocol_processor_top; \
  synth_xilinx -family xc7 -flatten -top protocol_processor_top; stat" >/dev/null
cells=$(awk '/^[0-9]+\. Printing statistics/ {buf=""} {buf=buf $0 "\n"} END {printf "%s", buf}' "$w/yosys.log")
luts=$(echo "$cells" | awk '$2 ~ /^LUT[1-6]$/ {s+=$1} END {print s+0}')
ffs=$(echo "$cells" | awk '$2 ~ /^FD[A-Z]*$/ {s+=$1} END {print s+0}')
brams=$(echo "$cells" | awk '$2 ~ /^RAMB/ {s+=$1} END {print s+0}')
lutram=$(echo "$cells" | awk '$2 ~ /^RAM[0-9]/ {s+=$1} END {print s+0}')
echo "$tag in=$nin out=$nout LUT=$luts FF=$ffs RAMB=$brams LUTRAMcells=$lutram"

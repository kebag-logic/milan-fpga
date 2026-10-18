#!/usr/bin/env bash
# domain_area.sh <tree> <workdir>: KL_srp_domain alone, sv2v 0.0.12 then Yosys synth_xilinx
# (xc7, flattened); the Yosys run is in <workdir> so its scratch files stay out of every tree
set -eu
tree="$1"; w="$2"
export PATH="<tools>/sv2v-v0.0.12:$PATH"
rm -rf "$w"; mkdir -p "$w"
sv2v --version; yosys -V
sha256sum "$tree/hdl/srp/KL_srp_domain.sv"
sv2v "$tree/hdl/srp/KL_srp_domain.sv" > "$w/KL_srp_domain.v"
cd "$w"
yosys -q -p "read_verilog KL_srp_domain.v; synth_xilinx -family xc7 -flatten -top KL_srp_domain; tee -o stat.txt stat" > yosys.log 2>&1
grep -E '^ +[0-9]+ +(FD|LUT)' stat.txt
awk '$2 ~ /^FD/ {f+=$1} $2 ~ /^LUT/ {l+=$1} END {print "FF", f, "LUT", l}' stat.txt

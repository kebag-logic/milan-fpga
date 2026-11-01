#!/bin/bash
# usage: obs_synth.sh <clone> <tag> <work>: sv2v plus Xilinx mapping of the observer at its GMII defaults,
# with `ready` a free input (what the head ships) and, on the head, with it tied at 1.
set -u
c=$1; t=$2; w=$3; G=$c/hdl/ieee8021as/gptp_plane; K=$c/hdl/common
mkdir -p "$w"
sv2v "$G/KL_gptp_gmii_launch.sv" "$K/cdc_handshake.sv" "$K/cdc_pulse.sv" > "$w/$t.v" 2>"$w/$t.sv2v.err"; echo "$t sv2v rc=$?"
yosys -q -l "$w/$t.free.log" -p "read_verilog $w/$t.v; synth_xilinx -top KL_gptp_gmii_launch -flatten -noiopad; tee -o $w/$t.free.stat stat" >/dev/null 2>&1; echo "$t free yosys rc=$?"
if grep -q gmii_tready_i "$w/$t.v"; then
sed 's/gmii_tready_i/gmii_tready_w/g; 0,/^module KL_gptp_gmii_launch/!b' "$w/$t.v" > "$w/$t.tied.v"
python3 -I - "$w/$t.v" "$w/$t.tied.v" <<'PY'
import re,sys
s=open(sys.argv[1]).read()
s=re.sub(r"\binput\s+wire\s+gmii_tready_i\s*;", "wire gmii_tready_i = 1'b1;", s)
s=re.sub(r"\binput\s+gmii_tready_i\s*;", "wire gmii_tready_i = 1'b1;", s)
s=re.sub(r"(module KL_gptp_gmii_launch\b.*?\()(.*?)(\);)", lambda m:m.group(1)+re.sub(r"\s*gmii_tready_i\s*,","",m.group(2))+m.group(3), s, count=1, flags=re.S)
open(sys.argv[2],"w").write(s)
PY
yosys -q -l "$w/$t.tied.log" -p "read_verilog $w/$t.tied.v; synth_xilinx -top KL_gptp_gmii_launch -flatten -noiopad; tee -o $w/$t.tied.stat stat" >/dev/null 2>&1; echo "$t tied yosys rc=$?"
fi

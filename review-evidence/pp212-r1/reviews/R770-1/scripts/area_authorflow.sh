#!/usr/bin/env bash
# Usage: area_authorflow.sh TREE NAME TOP "PARAMS" OUTDIR
# The published author flow (receipts/area/area.sh): sv2v of every hdl source,
# then `read_verilog all.v; hierarchy -check -top TOP PARAMS; synth_xilinx
# -family xc7 -flatten -top TOP; stat`, run here for one shape.
set -euo pipefail
tree=$(cd "$1" && pwd); name=$2; top=$3; params=$4; mkdir -p "$5"; out=$(cd "$5" && pwd)
work="$out/work-$name"; rm -rf "$work"; mkdir -p "$work"
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -I -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -I -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
cd "$work"
yosys -q -l "$out/$name.log" -p "read_verilog all.v; hierarchy -check -top $top $params; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/$name.stat stat" >/dev/null
rm -rf "$work"
awk '/LUT[1-6]$/{l+=$1} /FD[RSCPE][RSCPE]$/{f+=$1} /INV$/{i=$1} END {printf "LUT1-6 %d FF %d INV %d\n", l, f, i}' "$out/$name.stat"

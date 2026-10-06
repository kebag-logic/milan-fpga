#!/usr/bin/env bash
# Netlist statistics of one module, processor sources lowered by sv2v exactly as
# syn/yosys/run.sh lowers them (packages first, then every other .sv, sorted).
# usage: yosys_stats.sh <tree> <outdir> <top>
# Writes <outdir>/<top>.stat.json (stat -json), <outdir>/<top>.noattr.v
# (write_verilog -noattr after proc; opt_clean) and <outdir>/<top>.log.
set -euo pipefail
tree=$(readlink -f "$1"); out=$(readlink -f -m "$2"); top=$3
mkdir -p "$out"
if [ ! -s "$out/all.v" ]; then
  ( cd "$tree" && sv2v $(find hdl -name '*_pkg.sv' | sort) \
                       $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) ) > "$out/all.v.tmp"
  mv "$out/all.v.tmp" "$out/all.v"
  ( cd "$tree/hdl/aecp/ucode" && python3 gen_ucode.py -o "$out/ucode.hex" >/dev/null )
  ( cd "$tree/hdl/acmp/rom" && python3 gen_ltn_rom.py -o "$out/ltn_rom.hex" >/dev/null )
fi
cd "$out"
yosys -q -l "$top.log" -p "read_verilog -defer all.v; hierarchy -check -top $top; proc; opt_clean; \
  tee -q -o $top.stat.json stat -json; write_verilog -noattr $top.noattr.v"

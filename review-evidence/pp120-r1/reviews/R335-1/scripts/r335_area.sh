#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Scoped area comparison: synth_xilinx (xc7, flattened) of the descriptor
# store and the AECP engine at base and head. Not the repository's synthesis
# bank; the whole-processor figure is the executor's/manager's receipt.
# Usage: r335_area.sh <base-tree> <head-tree> <out-dir>
set -uo pipefail
out=$(mkdir -p "$3" && cd "$3" && pwd)
run() {  # <tree> <label> <top>
  local w="$out/work-$2-$3"; mkdir -p "$w"
  ( cd "$1" && sv2v $(find hdl -name '*_pkg.sv' | sort) \
      $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$w/all.v" )
  ( cd "$1/hdl/aecp/ucode" && python3 gen_ucode.py -o "$w/ucode.hex" >/dev/null )
  ( cd "$1/hdl/acmp/rom" && python3 gen_ltn_rom.py -o "$w/ltn_rom.hex" >/dev/null )
  ( cd "$w" && yosys -q -l "$out/$2-$3.yosys.log" -p "read_verilog all.v; \
      hierarchy -check -top $3; synth_xilinx -family xc7 -flatten -top $3; \
      tee -o $out/$2-$3.stat.txt stat" >/dev/null 2>&1; echo "rc=$?" >> "$out/$2-$3.stat.txt" )
}
for top in KL_aecp_desc_store KL_aecp_engine; do
  run "$1" base "$top" & run "$2" head "$top" &
done
wait
rm -rf "$out"/work-*

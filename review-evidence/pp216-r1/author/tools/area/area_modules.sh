#!/usr/bin/env bash
# area_modules.sh <tree> <outdir>: yosys synth_xilinx (xc7) of KL_srp_top at two sources and two sinks WITHOUT
# flattening, so the stat is per module (a diagnostic of where cells go; the gate figure is area.sh's flattened one)
set -euo pipefail
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
cd "$work"
yosys -q -l "$out/modules_2x2.log" -p "read_verilog all.v; hierarchy -check -top KL_srp_top -chparam N_SOURCES_P 2 -chparam N_SINKS_P 2; synth_xilinx -family xc7 -top KL_srp_top; tee -o $out/modules_2x2.stat stat" >/dev/null

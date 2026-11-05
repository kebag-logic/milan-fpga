#!/usr/bin/env bash
# area.sh <tree> <outdir> [shape...]: sv2v lowering of the processor tree, then
# yosys synth_xilinx -family xc7 -flatten of the requested shapes; one stat
# file per shape. Shapes: listener_n2 listener_n8 srp_top_2x2 srp_top_8x8.
set -euo pipefail
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd); shift 2
shapes=${*:-listener_n2 listener_n8 srp_top_2x2 srp_top_8x8}
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
cd "$work"
for s in $shapes; do
  case $s in
    listener_n2) top=KL_srp_listener_fsm; p="-chparam N_SINKS_P 2";;
    listener_n8) top=KL_srp_listener_fsm; p="";;
    srp_top_2x2) top=KL_srp_top; p="-chparam N_SOURCES_P 2 -chparam N_SINKS_P 2";;
    srp_top_8x8) top=KL_srp_top; p="";;
  esac
  yosys -q -l "$out/$s.log" -p "read_verilog all.v; hierarchy -check -top $top $p; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/$s.stat stat" >/dev/null &
done
wait

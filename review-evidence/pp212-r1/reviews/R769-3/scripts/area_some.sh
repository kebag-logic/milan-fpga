#!/usr/bin/env bash
# area_some.sh <tree> <outdir> <name>...: area.sh's flow for the named shapes only
# (listener_n2, listener_n8, srp_top_2x2, srp_top_8x8)
set -euo pipefail
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd); shift 2
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
cd "$work"
for name in "$@"; do
  case $name in
    listener_n2) top=KL_srp_listener_fsm; params="-chparam N_SINKS_P 2" ;;
    listener_n8) top=KL_srp_listener_fsm; params="" ;;
    srp_top_2x2) top=KL_srp_top; params="-chparam N_SOURCES_P 2 -chparam N_SINKS_P 2" ;;
    srp_top_8x8) top=KL_srp_top; params="" ;;
  esac
  yosys -q -l "$out/$name.log" -p "read_verilog all.v; hierarchy -check -top $top $params; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/$name.stat stat" >/dev/null
done

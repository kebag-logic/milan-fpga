#!/usr/bin/env bash
# area_2x2.sh <tree> <outdir> [listener_n2]: sv2v + yosys synth_xilinx -family xc7 -flatten
# of KL_srp_top at 2 sources x 2 sinks (and optionally the listener at N=2),
# the same lowering as the author's published area.sh. Prints LUT1-6 and FF sums.
set -euo pipefail
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
cd "$work"
run() { yosys -q -l "$out/$1.log" -p "read_verilog all.v; hierarchy -check -top $2 $3; synth_xilinx -family xc7 -flatten -top $2; tee -o $out/$1.stat stat" >/dev/null; }
run srp_top_2x2 KL_srp_top "-chparam N_SOURCES_P 2 -chparam N_SINKS_P 2" &
if [ "${3:-}" = listener_n2 ]; then run listener_n2 KL_srp_listener_fsm "-chparam N_SINKS_P 2" & fi
wait
for s in "$out"/*.stat; do
  awk -v n="$(basename "$s" .stat)" '$2 ~ /^LUT[1-6]$/ {l+=$1} $2 ~ /^FD/ {f+=$1} END {print n, "LUT", l, "FF", f}' "$s"
done

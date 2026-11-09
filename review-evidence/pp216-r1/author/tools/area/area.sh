#!/usr/bin/env bash
# area.sh <tree> <outdir>: yosys synth_xilinx (xc7, flattened) of the SRP top at two sources and two sinks and at the
# default eight and eight, and of the SRP encoder, Domain and VLAN participants alone, from the sv2v lowering the
# processor's syn/yosys/run.sh gate uses. One stat per shape and a summary.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
cd "$work"
run() {
  local name=$1 top=$2 params=$3
  yosys -q -l "$out/$name.log" -p "read_verilog all.v; hierarchy -check -top $top $params; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/$name.stat stat" >/dev/null &
}
run encoder KL_srp_encoder ""
run domain KL_srp_domain ""
run vlan KL_srp_vlan ""
run srp_top_2x2 KL_srp_top "-chparam N_SOURCES_P 2 -chparam N_SINKS_P 2"
run srp_top_8x8 KL_srp_top ""
wait
python3 "$here/area_summary.py" "$out"

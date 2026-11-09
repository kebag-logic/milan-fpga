#!/usr/bin/env bash
# area.sh <tree> <outdir>: the processor's yosys flow (syn/yosys/run.sh: the sv2v lowering of every hdl/ source,
# the generated ROMs, synth_xilinx -family xc7 -flatten) of protocol_processor_top at 2x2 (N_STREAM_IN_P =
# N_STREAM_OUT_P = 2) and at its default 8x8, and of KL_aecp_engine and KL_adp_engine alone. One stat per run.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
sha256sum "$work/all.v" "$work/ucode.hex" "$work/ltn_rom.hex" | sed "s#$work/##" > "$out/inputs.sha256"
cd "$work"
run() {
  local name=$1 top=$2 params=$3
  yosys -q -l "$out/$name.log" -p "read_verilog all.v; hierarchy -check -top $top $params; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/$name.stat stat" >/dev/null
}
run adp_engine KL_adp_engine "" &
run aecp_engine KL_aecp_engine "" &
wait
run top_2x2 protocol_processor_top "-chparam N_STREAM_IN_P 2 -chparam N_STREAM_OUT_P 2" &
run top_8x8 protocol_processor_top "" &
wait
python3 "$here/area_summary.py" "$out"

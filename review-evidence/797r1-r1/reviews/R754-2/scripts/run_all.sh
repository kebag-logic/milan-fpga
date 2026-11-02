#!/bin/sh
# Rebuild the independent measurement and rerun the plants.
# Usage: run_all.sh <clone> <out-dir> <python-with-pinned-wavedrom> <verilator>
set -eu
clone=$1; out=$2; py=$3; vl=$4; here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out/receipts" "$out/sim"
python3 -I "$here/gen_wrapper.py" "$clone/hdl/common/csr/milan_csr.sv" "$out/sim/tb_top.sv" "$out/sim/portmap.json"
python3 -I -c "
import json,sys
m=json.load(open(sys.argv[1]));hs={'i_lctx_wr_rdy','i_tctx_wr_rdy','i_lctx_rd_valid','i_tctx_rd_valid','i_lctx_snap_ok','i_tctx_snap_ok','i_ptp_tod_valid','i_pp_ack'}
open(sys.argv[2],'w').write(''.join(f'{n} {p} {w} {int(n in hs)}\n' for n,(p,w) in m['inputs'].items()))" "$out/sim/portmap.json" "$out/sim/ports.txt"
ib=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))['in_bits'])" "$out/sim/portmap.json")
ob=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))['out_bits'])" "$out/sim/portmap.json")
"$vl" --cc --exe --build -j 16 -O2 -Wno-fatal -Wno-lint -Wno-style --top-module tb_top -I"$clone/hdl/common/csr" \
  -I"$clone/configs/generated/endstation_ax7101_1x1_tdm8" -CFLAGS "-DIN_BITS=$ib -DOUT_BITS=$ob -O2" --Mdir "$out/sim/obj" \
  "$out/sim/tb_top.sv" "$clone/hdl/common/csr/milan_csr.sv" "$here/sim_main.cpp"
for m in reset word input directed; do "$out/sim/obj/Vtb_top" "$m" "$out/sim/ports.txt" > "$out/receipts/sim_$m.txt"; done
"$out/sim/obj/Vtb_top" bit "$out/sim/ports.txt" > "$out/sim/sim_bit.txt"
python3 -I "$here/compare_page.py" "$clone/docs/reference/REGISTER_MAP.md" "$out/receipts" "$out/sim/sim_bit.txt" "$out/sim/portmap.json" > "$out/receipts/compare_page.txt"
python3 -I "$here/attrib.py" "$clone/docs/reference/REGISTER_MAP.md" "$out/receipts" "$out/sim/sim_bit.txt" "$out/sim/portmap.json" "$here" > "$out/receipts/attribution.txt"
python3 -I "$here/mutants.py" "$clone" "$out" "$py" > "$out/receipts/mutants.tsv"

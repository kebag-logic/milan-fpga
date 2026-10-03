#!/bin/sh
# R445-1: the D3 writer alone at the 8x8 diagnostic shape (9 in, 9 out, 99
# names), base against head, same instrument as ooc_writer.sh.
# Usage: ooc_writer_8x8.sh BASE_TREE HEAD_TREE OUTDIR
set -e
out=$3; mkdir -p "$out"
for t in base head; do
  [ $t = base ] && tree=$1 || tree=$2
  sv2v "$tree/hdl/aecp/KL_aecp_nvm_writer.sv" > "$out/$t.v"
  np=""; grep -q 'parameter .*\bN_NAME_P\b' "$out/$t.v" && np="-set N_NAME_P 99"
  yosys -q -p "read_verilog $out/$t.v; chparam -set N_STREAM_IN_P 9 -set N_STREAM_OUT_P 9 $np KL_aecp_nvm_writer; \
     synth_xilinx -flatten -family xc7 -top KL_aecp_nvm_writer; tee -o $out/$t.stat stat" >/dev/null
  python3 - "$out/$t.stat" "$t" <<'PY'
import re, sys
s = open(sys.argv[1]).read()
n = lambda p: sum(int(m) for m in re.findall(r"^\s*(\d+)\s+(?:[\d.]+\s+)?" + p + r"\s*$", s, re.M))
lut = sum(n(f"LUT{k}") for k in range(1, 7)); ff = sum(n(c) for c in ("FDRE","FDSE","FDCE","FDPE"))
print(f"{sys.argv[2]} writer 8x8: LUT {lut} RAM32M {n('RAM32M')} FF {ff}")
PY
done

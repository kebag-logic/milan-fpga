#!/bin/sh
# R445-1: one-module synthesis count of the D3 writer and the descriptor
# store, base against head, at the parent's 1x1 shape (2 in, 2 out, 38 or 39
# names), with sv2v then Yosys `synth_xilinx -flatten -family xc7` (the
# instrument the PR body names). Synthesis counts only; no placement.
# Usage: ooc_writer.sh BASE_TREE HEAD_TREE OUTDIR NAMES
set -e
base=$1; head=$2; out=$3; names=${4:-38}
mkdir -p "$out"
synth() {  # tree tag module params...
  st=$1; tag=$2; mod=$3; shift 3
  v="$out/$tag-$mod.v"
  case $mod in
    KL_aecp_nvm_writer) sv2v "$st/hdl/aecp/KL_aecp_nvm_writer.sv" > "$v" ;;
    KL_aecp_desc_store) sv2v "$st/hdl/aecp/KL_aecp_desc_store.sv" > "$v" ;;
  esac
  cp=""
  for p in "$@"; do
    k=${p%%=*}; val=${p#*=}
    grep -q "parameter .*\b$k\b" "$v" && cp="$cp -set $k $val"
  done
  yosys -q -l "$out/$tag-$mod.log" -p "read_verilog $v; chparam$cp $mod; \
      synth_xilinx -flatten -family xc7 -top $mod; tee -o $out/$tag-$mod.stat stat" >/dev/null
}
for t in base head; do
  eval tree=\$$t
  synth "$tree" $t KL_aecp_nvm_writer N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_NAME_P=$names
  synth "$tree" $t KL_aecp_desc_store N_STREAM_IN_P=2 N_STREAM_OUT_P=2 NAME_ENTRIES_P=$names
done
for f in "$out"/*.stat; do
  python3 - "$f" <<'EOF'
import re, sys
s = open(sys.argv[1]).read()
def n(pat):
    return sum(int(m) for m in re.findall(r"^\s*(\d+)\s+(?:[\d.]+\s+)?" + pat + r"\s*$", s, re.M))
lut = sum(n(f"LUT{k}") for k in range(1, 7))
ff = sum(n(c) for c in ("FDRE", "FDSE", "FDCE", "FDPE"))
r32 = n("RAM32M"); r64 = n("RAM64M"); r32x1d = n("RAM32X1D"); r64x1d = n("RAM64X1D")
eq = lut + 4 * r32 + 4 * r64 + 2 * r32x1d + 2 * r64x1d
print(f"{sys.argv[1].split('/')[-1]:40s} LUT {lut:5d}  RAM32M {r32:3d}  RAM64M {r64:3d}  "
      f"RAM32X1D {r32x1d} RAM64X1D {r64x1d}  LUT-eq {eq:5d}  FF {ff:5d}")
EOF
done

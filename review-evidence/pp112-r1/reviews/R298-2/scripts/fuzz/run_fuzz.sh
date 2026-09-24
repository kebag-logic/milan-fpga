#!/usr/bin/env bash
# Usage: run_fuzz.sh <tree> <variant-A-file> <out-dir> <N> <EQ 0|1> <seed> <episodes> [<variant-B-file>]
# Optional <variant-B-file> replaces the derived u_b (its module is renamed KL_srp_admission_eq).
# Builds fz_wrap with DUT_A = the module in <variant-A-file> and u_b = the
# "validity terms removed" variant derived from <tree>'s KL_srp_admission.sv.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tree=$1; afile=$2; out=$3; n=$4; eq=$5; seed=$6; eps=$7; bfile=${8:-}
mkdir -p "$out"; b="$out/build_N${n}_eq${eq}"; rm -rf "$b"; mkdir -p "$b"
sed -e 's/module KL_srp_admission #(/module KL_srp_admission_eq #(/' \
    -e 's/endmodule : KL_srp_admission/endmodule : KL_srp_admission_eq/' \
    -e 's/ \&\& slope_valid_r\[aidx_r\]//' "$tree/hdl/srp/KL_srp_admission.sv" > "$b/eq.sv"
[ "$(grep -c 'slope_valid_r\[aidx_r\]' "$b/eq.sv")" = 1 ] || { echo "eq variant anchor mismatch"; exit 3; }
if [ -n "$bfile" ]; then sed -e 's/module KL_srp_admission #(/module KL_srp_admission_eq #(/' -e 's/endmodule : KL_srp_admission/endmodule : KL_srp_admission_eq/' "$bfile" > "$b/eq.sv"; fi
amod=$(grep -o 'module [A-Za-z_0-9]*' "$afile" | head -1 | cut -d' ' -f2)
verilator --cc --exe --build -j 8 --top-module fz_wrap -Wno-fatal -Wno-lint -Wno-style \
  -GN=$n "+define+DUT_A=$amod" --Mdir "$b" \
  -CFLAGS "-std=c++17 -O2 -DFZ_N=$n $( [ "$eq" = 1 ] && echo -DEQ_CHECK )" \
  "$afile" "$b/eq.sv" "$here/fz_wrap.sv" "$here/fz_main.cpp" -o Vfz > "$b/build.log" 2>&1
"$b/Vfz" "$seed" "$eps"

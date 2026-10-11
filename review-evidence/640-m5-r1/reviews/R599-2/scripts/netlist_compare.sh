#!/usr/bin/env bash
# Usage: netlist_compare.sh <treeA> <treeB> <outdir>
# Lowers hdl/common/csr/milan_csr.sv of each tree with sv2v (1x1 shipping shape
# include) into <outdir>/<A|B>/milan_csr.v (same file name, so source-location
# names agree), synthesises it with Yosys' generic flow from inside that
# directory, and compares the lowered sources and the netlists byte for byte.
set -euo pipefail
a=$1 b=$2 out=$3; mkdir -p "$out/A" "$out/B"; : > "$out/summary.txt"
for t in A B; do
  tree=$a; [ $t = B ] && tree=$b
  sv2v -I"$tree/hdl/common/csr" -I"$tree/configs/generated/endstation_ax7101_1x1_tdm8" \
       "$tree/hdl/common/csr/milan_csr.sv" > "$out/$t/milan_csr.v" 2> "$out/$t/sv2v.err"
  echo "sv2v $t rc=$?" >> "$out/summary.txt"
  (cd "$out/$t" && yosys -q -l yosys.log -p "read_verilog -sv milan_csr.v; synth -top milan_csr -flatten; opt_clean -purge; tee -o stat.txt stat; write_verilog -noattr netlist.v; write_json netlist.json" > /dev/null 2>&1)
  echo "yosys $t rc=$?" >> "$out/summary.txt"
done
for f in milan_csr.v netlist.v netlist.json stat.txt; do
  cmp "$out/A/$f" "$out/B/$f"
  echo "$f: IDENTICAL" >> "$out/summary.txt"
done
(cd "$out" && sha256sum A/milan_csr.v B/milan_csr.v A/netlist.v B/netlist.v A/netlist.json B/netlist.json) >> "$out/summary.txt"
cat "$out/A/stat.txt" >> "$out/summary.txt"

#!/usr/bin/env bash
# How Yosys 0.66 rejects an active elaboration guard in each form the flows feed it.
# Arg 1: work dir. Prints each case's rc and its ERROR line.
set -u
W=$1; mkdir -p "$W"; cd "$W" || exit 2
mk() {  # $1 file, $2 guard statement at generate scope
  printf 'module t #(parameter P = %s)(input clk, output reg q);\nif (P > 1) begin : g\n%s\nend\nalways @(posedge clk) q <= ~q;\nendmodule\n' \
    "$3" "$2" > "$1"
}
mk native_active.v   '$error("native guard message P too large");' 2
mk native_inactive.v '$error("native guard message P too large");' 1
mk restored_active.v 'initial $error("Error [elaboration] restored guard message");' 2
mk restored_inactive.v 'initial $error("Error [elaboration] restored guard message");' 1
for f in native_active native_inactive restored_active restored_inactive; do
  for mode in "" "-sv"; do
    out=$(yosys -q -p "read_verilog $mode $f.v; hierarchy -check -top t" 2>&1); rc=$?
    echo "$f read_verilog${mode:+ $mode}: rc=$rc $(printf '%s\n' "$out" | grep -m1 -E 'ERROR|rror' | cut -c1-150)"
  done
done

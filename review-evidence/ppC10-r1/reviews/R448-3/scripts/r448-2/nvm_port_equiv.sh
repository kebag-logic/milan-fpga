#!/usr/bin/env bash
# No-logic check for KL_pp_nvm_port.sv between two trees: sv2v + yosys
# (proc; opt; clean) netlists at MAX_PAYLOAD_P = 1024 and 65527, compared as
# text with attributes stripped.
# usage: nvm_port_equiv.sh <tree-a> <tree-b> <out-dir>
set -uo pipefail
a=$1 b=$2 out=$3; mkdir -p "$out"; w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
for t in a b; do
  eval src=\$$t
  sv2v "$src/hdl/packet_engine/KL_pp_nvm_port.sv" > "$w/$t.v" || exit 2
  for v in 1024 65527; do
    yosys -q -p "read_verilog $w/$t.v; chparam -set MAX_PAYLOAD_P $v KL_pp_nvm_port; hierarchy -check -top KL_pp_nvm_port; proc; opt -full; clean -purge; rename -enumerate; write_verilog -noattr $w/$t-$v.nl.v" || exit 3
    grep -v '^/\*' "$w/$t-$v.nl.v" > "$out/$t-$v.nl.v"
  done
done
for v in 1024 65527; do
  if cmp -s "$out/a-$v.nl.v" "$out/b-$v.nl.v"; then r=IDENTICAL; else r=DIFFERENT; fi
  echo "MAX_PAYLOAD_P=$v: $r ($(sha256sum < "$out/a-$v.nl.v" | cut -c1-16) vs $(sha256sum < "$out/b-$v.nl.v" | cut -c1-16), $(wc -l < "$out/a-$v.nl.v") lines)"
done

#!/usr/bin/env bash
# R449-2: KL_pp_nvm_port's yosys netlist (sv2v, proc, opt, write_verilog
# -noattr) at two revisions and two MAX_PAYLOAD_P values, then sha256 + diff.
# Usage: port_netlist.sh <git-clone> <rev-a> <rev-b> <work-dir>
set -u
repo=$1 a=$2 b=$3 w=$4; F=hdl/packet_engine/KL_pp_nvm_port.sv
mkdir -p "$w"
for r in "$a" "$b"; do
  git -C "$repo" show "$r:$F" > "$w/$r.sv"
  sv2v "$w/$r.sv" > "$w/$r.v" || exit 1
  for p in 1024 65527; do
    yosys -q -p "read_verilog -defer $w/$r.v; chparam -set MAX_PAYLOAD_P $p KL_pp_nvm_port; hierarchy -check -top KL_pp_nvm_port; proc; opt; opt_clean -purge; rename -enumerate; write_verilog -noattr $w/$r.$p.nl.v" > "$w/$r.$p.log" 2>&1
    echo "$r MAX_PAYLOAD_P=$p yosys rc=$? sha256=$(sha256sum < "$w/$r.$p.nl.v" | cut -c1-16)"
  done
done
for p in 1024 65527; do
  cmp -s "$w/$a.$p.nl.v" "$w/$b.$p.nl.v" && echo "MAX_PAYLOAD_P=$p: netlists identical" || echo "MAX_PAYLOAD_P=$p: netlists DIFFER"
done

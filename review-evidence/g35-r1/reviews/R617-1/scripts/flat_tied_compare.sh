#!/bin/bash
# Parser-scope analogue of the parent's flattened view: base vs head parser,
# rx_err_i tied 0, flatten; opt; opt_clean; then strip src attributes and
# canonicalise names, and compare the written netlists byte for byte.
# Usage: flat_tied_compare.sh <equiv-work-dir> <out-dir>   (after equiv_parser.sh)
set -u
W=$1; O=$2; mkdir -p "$O"
for m in gold gate; do
  yosys -q -l "$O/flat_$m.log" -p "
    read_verilog -DTIE $W/$m.v $W/wrap_$m.v
    hierarchy -top t_$m; proc; flatten; opt; opt_clean
    rename t_$m t
    attrmap -remove src
    rename -enumerate -pattern n%
    tee -o $O/flat_$m.stat stat
    write_verilog -noattr $O/flat_$m.v" >/dev/null 2>&1
  echo "$m rc=$?"
done
sha256sum "$O/flat_gold.v" "$O/flat_gate.v"
if cmp -s "$O/flat_gold.v" "$O/flat_gate.v"; then echo "FLAT TIED NETLIST: byte-identical after src strip"; else echo "FLAT TIED NETLIST: differs"; diff "$O/flat_gold.v" "$O/flat_gate.v" | head -20; fi
diff <(grep -v "===\|^$" "$O/flat_gold.stat" | sed 's/t_gold//') <(grep -v "===\|^$" "$O/flat_gate.stat" | sed 's/t_gate//') >/dev/null && echo "STAT identical"

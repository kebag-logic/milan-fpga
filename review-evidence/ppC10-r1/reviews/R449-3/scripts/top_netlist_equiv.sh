#!/usr/bin/env bash
# R449-3: elaborated-netlist equivalence of protocol_processor_top between two
# revisions (the declaration reorder must be netlist-neutral at the merge).
# For each revision: git archive -> sv2v (run.sh's order) -> yosys
# read_verilog; hierarchy -check -top protocol_processor_top; proc; opt_clean;
# write_verilog -noattr; then compare the two netlists byte for byte.
# usage: top_netlist_equiv.sh <repo> <scratch> <revA> <revB>
set -euo pipefail
repo=$1 sc=$2 a=$3 b=$4
for r in "$a" "$b"; do
  d="$sc/netlist-$r"; rm -rf "$d"; mkdir -p "$d/t" "$d/w"
  git -C "$repo" archive "$r" | tar -x -C "$d/t"
  ( cd "$d/t"
    sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$d/w/all.v"
    ( cd hdl/aecp/ucode && python3 gen_ucode.py -o "$d/w/ucode.hex" >/dev/null )
    ( cd hdl/acmp/rom && python3 gen_ltn_rom.py -o "$d/w/ltn_rom.hex" >/dev/null ) )
  ( cd "$d/w" && yosys -q -p "read_verilog all.v; hierarchy -check -top protocol_processor_top; proc; opt_clean; write_verilog -noattr top.v; stat" > stat.txt 2>&1 )
  echo "$r: $(sha256sum < "$d/w/top.v" | cut -c1-64) $(wc -c < "$d/w/top.v") bytes; cells $(grep -m1 -E 'cells' "$d/w/stat.txt" | tr -s ' ')"
done
A="$sc/netlist-$a/w/top.v" B="$sc/netlist-$b/w/top.v"
if cmp -s "$A" "$B"; then echo "IDENTICAL netlists (raw)"; exit 0; fi
echo "raw netlists differ in $(diff "$A" "$B" | grep -c '^[<>]') lines (yosys embeds all.v line numbers and creation counters in generated names)"
# Normalise only the source-line numbers and creation counters yosys bakes
# into generated names, then compare the sorted line multisets.
norm() { sed -E 's/all\.v:[0-9]+/all.v:L/g; s/\$[0-9]+/$N/g; s/_[0-9]+_/_N_/g' "$1" | sort; }
n=$(diff <(norm "$A") <(norm "$B") | grep -c '^[<>]' || true)
if [ "$n" -eq 0 ]; then echo "EQUAL after normalising line numbers and counters (sorted line multiset, $(wc -l < "$A") lines)"; else
  echo "DIFFERENT after normalisation: $n lines"; exit 1; fi

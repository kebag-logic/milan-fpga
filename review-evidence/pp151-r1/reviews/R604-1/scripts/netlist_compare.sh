#!/usr/bin/env bash
# Compare base/head netlists from netlists.sh: canonical (already masked) and,
# for a case that differs, with write_verilog's own _NNNN_ wire numbers masked too;
# stat (cell/wire counts by type) compared exactly.
# Usage: netlist_compare.sh <base-out> <head-out>
B=$1 H=$2
for f in "$H"/*.canon; do n=$(basename "$f" .canon)
  if cmp -s "$B/$n.canon" "$H/$n.canon"; then c=IDENTICAL
  elif cmp -s <(sed -E 's/_[0-9]+_/_N_/g' "$B/$n.canon" | sort) <(sed -E 's/_[0-9]+_/_N_/g' "$H/$n.canon" | sort); then c=IDENTICAL-UP-TO-WIRE-NUMBERING
  else c=DIFFER; fi
  if cmp -s "$B/$n.statc" "$H/$n.statc"; then s=stat-identical; else s=STAT-DIFFER; fi
  echo "$n $c $s $(wc -l < "$H/$n.canon") lines"
done

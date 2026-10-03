#!/usr/bin/env bash
# Preprocess every hdl/**/*.sv at two extracted trees with comments stripped (verilator -E -P)
# and report which files differ. Usage: rtl_preproc_compare.sh <base-tree> <head-tree> <verilator>
set -u
base=$1; head=$2; vl=${3:-verilator}
cd "$base" || exit 2
diffs=0
while IFS= read -r f; do
  a=$("$vl" -E -P -Ihdl/common -Ihdl "$f" 2>/dev/null | sed '/^\s*$/d' | sha256sum | cut -c1-16)
  b=$(cd "$head" && "$vl" -E -P -Ihdl/common -Ihdl "$f" 2>/dev/null | sed '/^\s*$/d' | sha256sum | cut -c1-16)
  if [ "$a" != "$b" ]; then echo "DIFFERS $f base=$a head=$b"; diffs=$((diffs+1)); fi
done < <(cd "$base" && find hdl -name '*.sv' | sort)
echo "files differing after comment strip: $diffs"

#!/usr/bin/env bash
# Scratch (never committed): the recipe's "Hierarchical mapping comparison" for
# one combination and shape: the flattened run's converted source and numeric
# parameters, mapped again without -flatten, then pp_baseline_mapping.py.
#   run_yosys_hier.sh <A|B> <ax7101|ax8x8>
set -u
combo=$1; shape=$2
S=$VALIDATION_STORAGE/234-a516
L=$LANES/234-area
out=$S/$combo/work/$shape-yosys
script="read_verilog $out/KL_pp_shadow.ooc.v; "
for item in $(cat "$S/$combo/work/$shape-ooc/baseline_chparam.txt"); do
  script+="chparam -set ${item%%=*} ${item#*=} KL_pp_shadow; "
done
script+="synth_xilinx -family xc7 -top KL_pp_shadow; stat; write_json hierarchical.json"
printf '%s\n' "$script" > "$out/hierarchical.ys"
date -Is > "$out/hierarchical.log.start"
rc=0
( cd "$out" && LD_PRELOAD=/usr/lib/libjemalloc.so.2 yosys -s hierarchical.ys > hierarchical.log 2>&1 ) || rc=$?
echo "$rc" > "$out/hierarchical.log.rc"
mrc=0
python3 "$L/syn/ooc/pp_baseline_mapping.py" "$out/hierarchical.json" "$out/KL_pp_shadow.ooc.json" \
  "$S/$combo/work/$shape-ooc/baseline_cells.tsv" > "$S/$combo/work/$shape-mapping.tsv" 2> "$S/$combo/work/$shape-mapping.err" || mrc=$?
echo "$mrc" > "$S/$combo/work/$shape-mapping.rc"
date -Is > "$out/hierarchical.log.end"

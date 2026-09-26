#!/usr/bin/env bash
# Recipe "Hierarchical mapping comparison" for one shape (the recipe's PYMAP body
# per shape), detached; caller polls <work>/<shape>-yosys/hier_rc.txt.
# Usage: run_yosys_hier_detached.sh <work> <shape>
set -euo pipefail
work="$1"; shape="$2"
output="$work/$shape-yosys"
script="read_verilog $output/KL_pp_shadow.ooc.v; "
for item in $(cat "$work/$shape-ooc/baseline_chparam.txt"); do
  script+="chparam -set ${item%%=*} ${item#*=} KL_pp_shadow; "
done
script+="synth_xilinx -family xc7 -top KL_pp_shadow; stat; write_json hierarchical.json"
printf '%s\n' "$script" > "$output/hierarchical.ys"
rm -f "$output/hier_rc.txt"
cd "$output"
setsid nohup bash -c 'yosys -s hierarchical.ys > hierarchical.log 2>&1; echo $? > hier_rc.txt' < /dev/null > /dev/null 2>&1 &
echo "launched pid $!"

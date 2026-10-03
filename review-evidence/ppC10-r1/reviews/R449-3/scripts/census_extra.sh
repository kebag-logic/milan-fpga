#!/usr/bin/env bash
# R449-3: census probes beyond round 2's forms, in a scratch copy of the head.
# usage: census_extra.sh <src-tree> <work-dir> <case>
# cases:
#   bbox         `(* blackbox *) module KL_r4493_bbox`, not in tops       -> census red, named
#   bbox-top     the same, added to tops                                  -> rc 0
#   wbox         `(* whitebox *) module KL_r4493_wbox` + fault, not in tops -> census red, named
#   esc          `module \KL_r4493_esc$q` (escaped identifier), not in tops  -> census red, named
#   attr2        two attribute instances then `module`, on the line before, with a fault
#   firstfail    a fault in the FIRST top (KL_aecp_desc_mem_guard) plus a
#                plain undeclared-in-tops module: the census must still run
#   mut-sel      run.sh mutated to `select -list *` (no boxes), + bbox     -> must NOT be red by census (mutant check)
#   mut-nocensus run.sh's census call removed, + attr form (one line)      -> must be rc 0 (mutant check)
# Writes <work-dir>/{gate.log,rc}.
set -u
src=$1 w=$2 case=$3
rm -rf "$w"; mkdir -p "$w"; cp -a "$src/." "$w/tree"; t="$w/tree"
run="$t/syn/yosys/run.sh"; f="$t/hdl/top/KL_r4493_probe.sv"
fault="  r4493_absent_module u_r4493_absent ();"
addtop() { sed -i -E "s/^tops=\(/tops=($1 /" "$run"; }
case "$case" in
  bbox|bbox-top|mut-sel)
    printf '(* blackbox *) module KL_r4493_bbox (input wire clk_i);\nendmodule\n' > "$f"
    [ "$case" = bbox-top ] && addtop KL_r4493_bbox
    [ "$case" = mut-sel ] && sed -i 's/select -list =\*/select -list */' "$run" ;;
  wbox)
    printf '(* whitebox *) module KL_r4493_wbox (input wire clk_i);\n%s\nendmodule\n' "$fault" > "$f" ;;
  esc)
    printf 'module \\KL_r4493_esc$q (input wire clk_i);\n%s\nendmodule\n' "$fault" > "$f" ;;
  attr2)
    printf '(* keep_hierarchy = "yes" *) (* r4493 = 1 *)\nmodule KL_r4493_attr2 (input wire clk_i);\n%s\nendmodule\n' "$fault" > "$f" ;;
  firstfail)
    printf 'module KL_r4493_plain (input wire clk_i);\nendmodule\n' > "$f"
    python3 - "$t/hdl/aecp/KL_aecp_desc_mem_guard.sv" "$fault" <<'PY'
import sys
p, text = sys.argv[1:3]
s = open(p).read(); j = s.rindex('endmodule')
open(p, 'w').write(s[:j] + text + '\n' + s[j:])
PY
    ;;
  mut-nocensus)
    printf '(* keep_hierarchy = "yes" *) module KL_r4493_attr (input wire clk_i);\n%s\nendmodule\n' "$fault" > "$f"
    sed -i 's/ || census$//' "$run"; grep -q '|| census$' "$run" && { echo "mutation not applied" > "$w/gate.log"; echo 9 > "$w/rc"; exit 0; } ;;
  *) echo "unknown case $case" >&2; exit 2 ;;
esac
( cd "$t" && ./syn/yosys/run.sh ) > "$w/gate.log" 2>&1
echo $? > "$w/rc"
echo "$case rc=$(cat "$w/rc")"

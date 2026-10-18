#!/usr/bin/env bash
# Sequential equivalence of a module's base and head RTL (issue #181 evidence, round 2).
# usage: equiv.sh <name> <gold.sv> <gate.sv> <module> <seq> [gold-extra-verilog] [-- chparam args...]
# gold-extra-verilog is spliced into the gold netlist before its endmodule (a
# named observation wire only; it adds no state and drives nothing).
# EQUIV_SKIP: space-separated internal net names left out of the matching (the
# changed combinational nets themselves); every port and register is matched.
# Exit 0 = every equivalence point proven; otherwise the proof failed.
set -euo pipefail
. <data>/tmp/pp181-a635/env.sh
name=$1; gold=$2; gate=$3; mod=$4; seq=$5; extra=${6:-}
shift 6 || shift $#
[ "${1:-}" = "--" ] && shift
chp="$*"
tree=<data>/lanes/pp181-cut
w=<data>/tmp/pp181-a635/r2/proofs/run-$name
rm -rf "$w"; mkdir -p "$w"; cd "$w"
pkgs=$(find $tree/hdl -name '*_pkg.sv' | sort)
sv2v $pkgs "$gold" > gold_raw.v
sv2v $pkgs "$gate" > gate_raw.v
sed "s/^module $mod\b/module gold/" gold_raw.v > gold.v
sed "s/^module $mod\b/module gate/" gate_raw.v > gate.v
if [ -n "$extra" ]; then
  python3 -I - "$extra" <<'PY'
import sys
t = open("gold.v").read()
i = t.rindex("endmodule")
open("gold.v", "w").write(t[:i] + sys.argv[1] + "\n" + t[i:])
PY
fi
{
  echo "read_verilog${EQUIV_MEM2REG:+ -mem2reg} gold.v gate.v"
  [ -n "$chp" ] && echo "chparam $chp gold gate"
  echo "hierarchy -check"
  echo "proc; opt_clean"
  echo "memory${EQUIV_MEM_NOMAP:+ -nomap}; opt_clean"
  echo "flatten; opt_clean"
  echo "async2sync"
  : > skip.txt; for n in ${EQUIV_SKIP:-}; do echo "$n" >> skip.txt; done
  echo "equiv_make -blacklist skip.txt gold gate eq"
  echo "hierarchy -top eq"
  echo "equiv_simple -seq $seq"
  echo "equiv_induct -seq $seq"
  echo "equiv_status -assert"
} > equiv.ys
yosys -q -l equiv.log -s equiv.ys

#!/usr/bin/env bash
# Prove KL_aecp_notify's occupancy invariant by temporal induction (issue #181 evidence):
#   after a reset cycle, cmdq_nempty_r == (cmdq_count_r != 0) in every cycle.
# usage: inv.sh <name> <notify.sv> [chparam args...]   exit 0 = proven
set -euo pipefail
. <data>/tmp/pp181-a635/env.sh
name=$1; src=$2; shift 2
chp="$*"
tree=<data>/lanes/pp181-cut
w=<data>/tmp/pp181-a635/equiv/inv-$name
rm -rf "$w"; mkdir -p "$w"; cd "$w"
pkgs=$(find $tree/hdl -name '*_pkg.sv' | sort)
sv2v $pkgs "$src" > dut_raw.v
# one observation wire, spliced before endmodule: it drives nothing
python3 -I - <<'PY'
t = open("dut_raw.v").read()
i = t.rindex("endmodule")
w = "(* keep *) wire inv_ok = (cmdq_nempty_r == (cmdq_count_r != 5'd0));\n"
open("dut.v", "w").write(t[:i] + w + t[i:])
PY
{
  echo "read_verilog -mem2reg dut.v"
  [ -n "$chp" ] && echo "chparam $chp KL_aecp_notify"
  echo "hierarchy -check -top KL_aecp_notify"
  echo "proc; opt_clean -keep_inv"
  echo "memory; flatten; opt_clean"
  echo "opt_clean"
  echo "async2sync; dffunmap"
  echo "sat -tempinduct -prove inv_ok 1 -set-at 1 rst_n 0 -seq 1 -maxsteps 1 -verify KL_aecp_notify"
} > inv.ys
sed -i 's/ -keep_inv//' inv.ys
yosys -q -l inv.log -s inv.ys

#!/usr/bin/env bash
# Reproduce the HDL engineer guide's section 2.1 table for the front ends present here:
# Verilator lint (lint_hdl.sh flags), sv2v 0.0.12 + Yosys, sv2v 0.0.13 + Yosys.
# usage: forms_probe.sh WORKDIR BIN012 BIN013
# Each probe module has one guard `if (P > 1)`; P=2 violates, P=1 passes.
set -uo pipefail
work=$1 bin012=$2 bin013=$3
mkdir -p "$work"; cd "$work" || exit 2
gen() {  # $1 name, $2 guard text
  cat > "$1.sv" <<EOF
module $1 #(parameter int P = 1) (input logic a_i, output logic y_o);
  assign y_o = a_i;
$2
endmodule
EOF
}
gen m_fatal_mod   '  if (P > 1) begin : g_chk $fatal(1, "probe guard P=%0d", P); end'
gen m_error_mod   '  if (P > 1) begin : g_chk $error("probe guard P=%0d", P); end'
gen m_warning_mod '  if (P > 1) begin : g_chk $warning("probe guard P=%0d", P); end'
gen m_info_mod    '  if (P > 1) begin : g_chk $info("probe guard P=%0d", P); end'
gen m_fatal_init  '  initial begin : g_chk if (P > 1) $fatal(1, "probe guard P=%0d", P); end'
for m in m_fatal_mod m_error_mod m_warning_mod m_info_mod m_fatal_init; do
  for p in 2 1; do
    out=$(PATH="$bin013:$PATH" verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
          -Wno-UNUSEDPARAM --top-module $m -GP=$p $m.sv 2>&1); rc=$?
    echo "verilator $m P=$p rc=$rc :: $(grep -m1 -E '^%|probe' <<<"$out" || echo '(no diagnostic)')"
    for v in 012 013; do
      b=bin$v; b=${!b}
      PATH="$b:$PATH" sv2v $m.sv > $m.$v.v 2>sv2v.err || { echo "sv2v$v $m failed: $(head -1 sv2v.err)"; continue; }
      out=$(PATH="$b:$PATH" yosys -q -p "read_verilog -defer $m.$v.v; chparam -set P $p $m; hierarchy -check -top $m; proc; opt_clean" 2>&1); rc=$?
      echo "sv2v0.$v+yosys $m P=$p rc=$rc :: $(grep -m1 -E 'ERROR|Warning|probe' <<<"$out" || echo '(no diagnostic)')"
    done
  done
done

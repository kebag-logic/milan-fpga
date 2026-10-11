#!/usr/bin/env bash
# Independent one-guard probe: each severity form, at module scope and in an
# initial block, violating (P=1) and passing (P=0), through Verilator lint
# (scripts/lint_hdl.sh flags) and sv2v + Yosys (the syn/yosys/run.sh flow).
# Usage: probe_forms.sh <workdir> <bin-dir-with-sv2v-0.0.12> <bin-dir-with-sv2v-0.0.13>
set -u
W=$1 B12=$2 B13=$3; mkdir -p "$W"; cd "$W" || exit 2
for task in fatal error warning info; do
  if [ $task = fatal ]; then call="\$fatal(1, \"probe: P=%0d violates\", P);"; else call="\$$task(\"probe: P=%0d violates\", P);"; fi
  cat > m_${task}_mod.sv <<SV
module probe #(parameter int P = 0) (input logic a_i, output logic b_o);
  assign b_o = a_i;
  if (P != 0) begin : g_chk
    $call
  end
endmodule
SV
  cat > m_${task}_init.sv <<SV
module probe #(parameter int P = 0) (input logic a_i, output logic b_o);
  assign b_o = a_i;
  initial begin : g_chk
    if (P != 0)
      $call
  end
endmodule
SV
done
for f in m_*.sv; do
  for p in 1 0; do
    out=$(PATH=$B12:$PATH verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module probe -GP=$p $f 2>&1); rc=$?
    echo "== $f P=$p verilator rc=$rc :: $(grep -m1 -E '^%' <<<"$out")"
    for b in 12 13; do
      bin=$B12; [ $b = 13 ] && bin=$B13
      PATH=$bin:$PATH sv2v $f > ${f%.sv}.sv2v$b.v 2>&1
      out=$(PATH=$bin:$PATH yosys -q -p "read_verilog -defer ${f%.sv}.sv2v$b.v; chparam -set P $p probe; hierarchy -check -top probe; proc; opt_clean" 2>&1); rc=$?
      echo "== $f P=$p sv2v0.0.$b+yosys rc=$rc :: $(grep -m1 -E 'ERROR|Warning' <<<"$out")"
    done
  done
done

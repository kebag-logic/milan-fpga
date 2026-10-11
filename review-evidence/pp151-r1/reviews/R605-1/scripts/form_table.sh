#!/usr/bin/env bash
# Reviewer re-measurement of the HDL engineer guide's section 2.1 table, on
# reviewer-written one-guard probes (not the author's probe files): each form
# violating (P=0) and passing (P=1), through Verilator 5.050 lint with
# scripts/lint_hdl.sh's flags, and sv2v (0.0.12, 0.0.13) + Yosys with
# syn/yosys/run.sh's elaboration step. Vivado is not installed here.
# usage: form_table.sh <workdir> <tc012-dir> <tc013-dir>
set -u
work=$1; tc012=$2; tc013=$3
mkdir -p "$work"; cd "$work" || exit 2
forms=(fatal_mod error_mod warning_mod info_mod fatal_init)
for f in "${forms[@]}"; do
  case $f in
    fatal_mod)   body='  if (P < 1) begin : g_check
    $fatal(1, "probe: P=%0d must be at least 1", P);
  end' ;;
    error_mod)   body='  if (P < 1) begin : g_check
    $error("probe: P=%0d must be at least 1", P);
  end' ;;
    warning_mod) body='  if (P < 1) begin : g_check
    $warning("probe: P=%0d must be at least 1", P);
  end' ;;
    info_mod)    body='  if (P < 1) begin : g_check
    $info("probe: P=%0d must be at least 1", P);
  end' ;;
    fatal_init)  body='  initial begin : g_check
    if (P < 1) $fatal(1, "probe: P=%0d must be at least 1", P);
  end' ;;
  esac
  cat > "r605_$f.sv" <<EOF
module r605_$f #(parameter int unsigned P = 1) (
    input  wire  a_i,
    output logic y_o
);
$body
  assign y_o = a_i;
endmodule
EOF
done
verdict() { # rc, output -> word
  if [ "$1" -eq 0 ]; then echo "elaborates"; else echo "refused: $(grep -m1 -E '%(Warning|Error)|ERROR' <<<"$2" | sed 's/^ *//' | cut -c1-110)"; fi
}
printf '| form | P | Verilator 5.050 lint | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 |\n|---|---|---|---|---|\n'
for f in "${forms[@]}"; do
  for p in 0 1; do
    out=$(PATH="$tc012:$PATH" verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
          -Wno-UNUSEDPARAM --top-module "r605_$f" -GP=$p "r605_$f.sv" 2>&1); rc=$?
    v=$(verdict $rc "$out")
    cols=()
    for tc in "$tc012" "$tc013"; do
      PATH="$tc:$PATH" sv2v "r605_$f.sv" > "lowered_$(basename "$tc")_$f.v" 2>&1
      out=$(PATH="$tc:$PATH" yosys -q -p "read_verilog -defer lowered_$(basename "$tc")_$f.v; chparam -set P $p r605_$f; hierarchy -check -top r605_$f; proc; opt_clean" 2>&1); rc=$?
      cols+=("$(verdict $rc "$out")")
    done
    printf '| %s | %s | %s | %s | %s |\n' "$f" "$p" "$v" "${cols[0]}" "${cols[1]}"
  done
done

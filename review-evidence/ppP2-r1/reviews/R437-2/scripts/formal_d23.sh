#!/usr/bin/env bash
# D23's equivalence claim, proven: owed_r is set only in S_IDLE, S_FIN, S_WHDR,
# S_WEREQ or S_RHREQ, for every input sequence (rst_n included), by Yosys's
# built-in SAT temporal induction from the all-zero (reset) state, at
# MEM_TIMEOUT_CYC_P = 3 and 100. With the invariant, the `if (!owed_r)` guards
# of S_WWREQ and S_RPREQ can never be false, so dropping them is equivalent.
# Negative control: drop S_RHREQ from the allowed set (owed_r IS reachable
# there); the same command must then FAIL with a base-case model.
# usage: formal_d23.sh CLONE OUTDIR   (needs sv2v and yosys)
set -euo pipefail
clone=$1; out=$2; mkdir -p "$out"; cd "$out"
git -C "$clone" show c0715410418b47ffaccf5feed55b71617fcfaf82:hdl/packet_engine/KL_pp_nvm_port.sv > port.sv
python3 - <<'EOF'
s = open('port.sv').read()
s = s.replace("    input  wire         dev_err_i        //! one-cycle pulse: device command failed\n);",
              "    input  wire         dev_err_i,       //! one-cycle pulse: device command failed\n    output logic        inv_o\n);")
s = s.replace("endmodule\n",
              "  assign inv_o = owed_r && !((state_r == S_IDLE) || (state_r == S_FIN) || (state_r == S_WHDR)\n"
              "                           || (state_r == S_WEREQ) || (state_r == S_RHREQ));\nendmodule\n")
open('port_inv.sv', 'w').write(s)
open('port_neg.sv', 'w').write(s.replace("|| (state_r == S_WEREQ) || (state_r == S_RHREQ));", "|| (state_r == S_WEREQ));"))
EOF
prove() { # $1 tag, $2 sv, $3 tmo
  sv2v "$2" > "$1.v"
  cat > "$1.ys" <<EOF
read_verilog -sv $1.v
chparam -set MEM_TIMEOUT_CYC_P $3 KL_pp_nvm_port
prep -top KL_pp_nvm_port
flatten
memory_map
opt -fast
sat -tempinduct -prove inv_o 0 -set-init-zero -maxsteps 40 -show-inputs -show-outputs
EOF
  yosys -q -l "$1.log" "$1.ys" >/dev/null 2>&1 || true
  echo "$1: $(grep -E 'SUCCESS|FAIL!' "$1.log" | tail -1)"
}
prove inv_3 port_inv.sv 3
prove inv_100 port_inv.sv 100
prove neg_3 port_neg.sv 3

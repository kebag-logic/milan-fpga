#!/usr/bin/env bash
# Out-of-context cost of KL_pp_nvm_port: sv2v then Yosys synth_xilinx (flatten),
# main 2ebd4fe8 vs head 70bf017d, the head at MEM_TIMEOUT_CYC_P default and 1.
set -euo pipefail
REPO=$1; OUT=$2; W=$3
mkdir -p "$W" "$OUT"
for rev in 2ebd4fe8d31e88c44559e934bd624e1c50515ad5 70bf017d62d60b4401126c7b1bb087f4cb115c5a; do
  git -C "$REPO" show "$rev:hdl/packet_engine/KL_pp_nvm_port.sv" > "$W/port_${rev:0:8}.sv"
done
yosys -V > "$OUT/ooc_tools.txt"; sv2v --version >> "$OUT/ooc_tools.txt" 2>&1 || true
run() { # name src chparam
  local name=$1 src=$2 cp=$3
  sv2v "$W/$src" > "$W/$name.v"
  yosys -q -p "read_verilog $W/$name.v; ${cp} synth_xilinx -top KL_pp_nvm_port -flatten; tee -o $OUT/ooc_$name.stat stat" > "$W/$name.ylog" 2>&1
}
run main port_2ebd4fe8.sv "" &
run head_default port_70bf017d.sv "" &
run head_tmo1 port_70bf017d.sv "chparam -set MEM_TIMEOUT_CYC_P 1 KL_pp_nvm_port;" &
run head_tmo2e31m1 port_70bf017d.sv "chparam -set MEM_TIMEOUT_CYC_P 2147483647 KL_pp_nvm_port;" &
wait
for n in main head_default head_tmo1 head_tmo2e31m1; do
  printf '%-16s ' "$n"; awk '/LUT[1-6]|FDRE|FDSE|FDCE|FDPE|CARRY4/ {printf "%s=%s ", $2, $1}' "$OUT/ooc_$n.stat"; echo
done

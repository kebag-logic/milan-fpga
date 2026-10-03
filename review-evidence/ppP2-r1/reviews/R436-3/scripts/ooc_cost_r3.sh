#!/usr/bin/env bash
# Out-of-context cost of KL_pp_nvm_port (R436-3): R436-2's recipe (sv2v, then
# Yosys synth_xilinx -flatten), round 2's c0715410 against the exact head
# 527662d6 at MEM_TIMEOUT_CYC_P default, 1, 2^31 - 1 and 125,000,000; main
# 631eeb34 at the default for the cumulative figure.
#   ooc_cost_r3.sh <repo> <out dir> <work dir>
set -euo pipefail
REPO=$1; OUT=$2; W=$3
mkdir -p "$W" "$OUT"
for rev in 631eeb342ca1e3fa80e734077a56a943aee76ff1 c0715410418b47ffaccf5feed55b71617fcfaf82 \
           527662d659b4ead97675744d12a43af1ea92b9b3; do
  git -C "$REPO" show "$rev:hdl/packet_engine/KL_pp_nvm_port.sv" > "$W/port_${rev:0:8}.sv"
done
yosys -V > "$OUT/ooc_tools.txt"; sv2v --version >> "$OUT/ooc_tools.txt" 2>&1 || true
run() { # name src chparam
  local name=$1 src=$2 cp=$3
  sv2v "$W/$src" > "$W/$name.v"
  yosys -q -p "read_verilog $W/$name.v; ${cp} synth_xilinx -top KL_pp_nvm_port -flatten; tee -o $OUT/ooc_$name.stat stat" > "$W/$name.ylog" 2>&1
}
P1="chparam -set MEM_TIMEOUT_CYC_P 1 KL_pp_nvm_port;"
PM="chparam -set MEM_TIMEOUT_CYC_P 2147483647 KL_pp_nvm_port;"
P125="chparam -set MEM_TIMEOUT_CYC_P 125000000 KL_pp_nvm_port;"
run main port_631eeb34.sv "" &
run r2_default port_c0715410.sv "" &
run r2_tmo1 port_c0715410.sv "$P1" &
run r2_tmo2e31m1 port_c0715410.sv "$PM" &
run r2_tmo125m port_c0715410.sv "$P125" &
run head_default port_527662d6.sv "" &
run head_tmo1 port_527662d6.sv "$P1" &
run head_tmo2e31m1 port_527662d6.sv "$PM" &
run head_tmo125m port_527662d6.sv "$P125" &
wait
for n in main r2_default head_default r2_tmo1 head_tmo1 r2_tmo2e31m1 head_tmo2e31m1 r2_tmo125m head_tmo125m; do
  printf '%-16s ' "$n"; awk '/LUT[1-6]|FDRE|FDSE|FDCE|FDPE|CARRY4/ {printf "%s=%s ", $2, $1}' "$OUT/ooc_$n.stat"; echo
done

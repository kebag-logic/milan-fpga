#!/usr/bin/env bash
# Out-of-context cost of KL_pp_nvm_port (R436-2): sv2v then Yosys synth_xilinx
# -flatten, main 631eeb34 against the head c0715410 at MEM_TIMEOUT_CYC_P
# default, 1 and 2^31 - 1; the round-1 head 70bf017d at the default for the
# round-1 to round-2 delta. The same recipe as R436-1's ooc_cost.sh.
#   ooc_cost.sh <repo> <out dir> <work dir>
set -euo pipefail
REPO=$1; OUT=$2; W=$3
mkdir -p "$W" "$OUT"
for rev in 631eeb342ca1e3fa80e734077a56a943aee76ff1 c0715410418b47ffaccf5feed55b71617fcfaf82 \
           70bf017d62d60b4401126c7b1bb087f4cb115c5a; do
  git -C "$REPO" show "$rev:hdl/packet_engine/KL_pp_nvm_port.sv" > "$W/port_${rev:0:8}.sv"
done
yosys -V > "$OUT/ooc_tools.txt"; sv2v --version >> "$OUT/ooc_tools.txt" 2>&1 || true
run() { # name src chparam
  local name=$1 src=$2 cp=$3
  sv2v "$W/$src" > "$W/$name.v"
  yosys -q -p "read_verilog $W/$name.v; ${cp} synth_xilinx -top KL_pp_nvm_port -flatten; tee -o $OUT/ooc_$name.stat stat" > "$W/$name.ylog" 2>&1
}
run main port_631eeb34.sv "" &
run head_default port_c0715410.sv "" &
run head_tmo1 port_c0715410.sv "chparam -set MEM_TIMEOUT_CYC_P 1 KL_pp_nvm_port;" &
run head_tmo2e31m1 port_c0715410.sv "chparam -set MEM_TIMEOUT_CYC_P 2147483647 KL_pp_nvm_port;" &
run r1_default port_70bf017d.sv "" &
wait
for n in main head_default head_tmo1 head_tmo2e31m1 r1_default; do
  printf '%-16s ' "$n"; awk '/LUT[1-6]|FDRE|FDSE|FDCE|FDPE|CARRY4/ {printf "%s=%s ", $2, $1}' "$OUT/ooc_$n.stat"; echo
done

#!/usr/bin/env bash
# Out-of-context cost of KL_pp_nvm_port: sv2v, then Yosys synth_xilinx (xc7),
# at round 2 c0715410 and at head 527662d6, each at MEM_TIMEOUT_CYC_P =
# 100,000,000 (default), 1 (smallest legal), 2^31 - 1 (largest legal) and 125,000,000.
# usage: ooc_cost.sh CLONE OUTDIR
set -euo pipefail
clone=$1; out=$2; mkdir -p "$out"
synth() { # $1 tag, $2 rtl file, $3 chparam args
  sv2v "$2" > "$out/$1.v"
  yosys -q -l "$out/$1.yosys.log" -p "read_verilog $out/$1.v; $3 hierarchy -check -top KL_pp_nvm_port; synth_xilinx -family xc7 -flatten -top KL_pp_nvm_port; stat" >/dev/null
  echo "== $1"
  grep -E '^\s+[0-9]+\s+(LUT[1-6]|FD[CPRSE]+|CARRY4|MUXF[78])\b|Number of cells|cells$' "$out/$1.yosys.log" | tail -20
}
git -C "$clone" show c0715410418b47ffaccf5feed55b71617fcfaf82:hdl/packet_engine/KL_pp_nvm_port.sv > "$out/base.sv"
git -C "$clone" show 527662d659b4ead97675744d12a43af1ea92b9b3:hdl/packet_engine/KL_pp_nvm_port.sv > "$out/head.sv"
for v in base head; do
  synth ${v}_default "$out/$v.sv" ""
  synth ${v}_1 "$out/$v.sv" "chparam -set MEM_TIMEOUT_CYC_P 1 KL_pp_nvm_port;"
  synth ${v}_max "$out/$v.sv" "chparam -set MEM_TIMEOUT_CYC_P 2147483647 KL_pp_nvm_port;"
  synth ${v}_125M "$out/$v.sv" "chparam -set MEM_TIMEOUT_CYC_P 125000000 KL_pp_nvm_port;"
done
# LUT/FF/CARRY4 totals per run
for t in base_default base_1 base_max base_125M head_default head_1 head_max head_125M; do
  awk -v t=$t '/Number of cells|cells$/{n++} n==1 && /LUT[1-6]/{l+=$1} n==1 && /FDRE|FDSE|FDCE|FDPE/{f+=$1} n==1 && /CARRY4/{c+=$1} END{printf "%s LUT=%d FF=%d CARRY4=%d\n", t, l, f, c}' "$out/$t.yosys.log"
done

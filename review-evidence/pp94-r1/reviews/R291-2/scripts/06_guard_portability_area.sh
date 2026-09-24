#!/usr/bin/env bash
# Guard-only portability (sv2v + yosys elaboration) and an independent open-tool
# area cross-check (yosys synth_xilinx, xc7). Not the Vivado OOC figure.
source "$(dirname "$0")/00_env.sh"
W=$PKT/scratch/yosys; rm -rf "$W"; mkdir -p "$W"; cd "$W"   # ABC drops abc.history in the cwd
sv2v "$TREE/hdl/aecp/KL_aecp_desc_mem_guard.sv" > "$W/guard.v"
yosys -q -p "read_verilog $W/guard.v; hierarchy -check -top KL_aecp_desc_mem_guard; proc; opt_clean" && echo "YOSYS OK  KL_aecp_desc_mem_guard"
yosys -p "read_verilog $W/guard.v; synth_xilinx -family xc7 -top KL_aecp_desc_mem_guard; stat" 2>&1 | sed -n '/Printing statistics/,$p' | grep -E 'LUT|FD|cells|CARRY|RAM|DSP' 

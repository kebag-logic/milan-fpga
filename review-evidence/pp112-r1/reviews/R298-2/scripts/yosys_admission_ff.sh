#!/usr/bin/env bash
# Usage: yosys_admission_ff.sh <tree> <out-prefix>: generic synth of KL_srp_admission (N=8), cell stats
set -euo pipefail
tree=$(cd "$1" && pwd); out=$(cd "$(dirname "$2")" && pwd)/$(basename "$2")
# Amended after the recorded run only to run inside the output directory, so
# ABC's history file is not written to the caller's directory. No other change.
cd "$(dirname "$out")"
sv2v "$tree/hdl/srp/KL_srp_admission.sv" > "$out.v"
yosys -q -p "read_verilog $out.v; synth -top KL_srp_admission -flatten; opt_clean -purge; tee -o $out.stat stat" > "$out.log" 2>&1

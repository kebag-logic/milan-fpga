#!/usr/bin/env bash
# The #530 item 2 reproduction: build obj_crflic against a scratch copy of
# milan_datapath.sv whose stream gate reads the raw admission verdict again.
# usage: run_crflic_gate_reverted.sh <repo> <verilator> <scratch>
set -uo pipefail
repo=$1; ver=$2; scratch=$3; mkdir -p "$scratch"
src="$repo/hdl/milan/milan_datapath.sv"; mut="$scratch/milan_datapath.gate-reverted.sv"
sed 's/assign lwsrp_stream_gate = pp_cd_srp_active_w\[/assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[/' "$src" > "$mut"
diff "$src" "$mut"
"$(dirname "$0")/run_crflic.sh" "$repo" "$ver" "$scratch/obj_crflic_reverted" DP_SRC="$mut"

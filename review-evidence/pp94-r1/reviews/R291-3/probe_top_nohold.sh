#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Product-top bench with the guard's two request holds deleted (disposable
# probe tree from run_probes.sh). Expect A12 to fail; restores the file after.
#   probe_top_nohold.sh <packet> <verilator>
set -uo pipefail
PKT=$(readlink -f "$1"); VL=$2; T=$PKT/scratch/tree; R=$PKT/receipts
G=$T/hdl/aecp/KL_aecp_desc_mem_guard.sv
[ "$(grep -c ' && !owed_r' "$G")" = 2 ] || { echo "REFUSED: hold arms"; exit 3; }
sed -i 's/ && !owed_r//' "$G"
git -C "$T" diff --stat >"$R/top-nohold.diff"
make -C "$T/tb/pp_top" clean >/dev/null 2>&1
make -C "$T/tb/pp_top" VERILATOR="$VL" >"$R/top-nohold.log" 2>&1; rc=$?
git -C "$T" checkout -- hdl/aecp/KL_aecp_desc_mem_guard.sv
echo "top-nohold make rc=$rc; restored: $(git -C "$T" status --porcelain | wc -l) modified tracked files" | tee "$R/top-nohold-rc.txt"
grep -E '^FAIL|checks:' "$R/top-nohold.log" | tee -a "$R/top-nohold-rc.txt"

#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe P1c (attribution): rerun probe P1 with one of the PR's new
# walk-failure routes reverted to the pre-PR behaviour.
#   B02: a zero-byte DEVICE err is again a per-record default (pre-PR)
#   B01: no read deadline (pre-PR)
# Usage: run_p1_counterfactual.sh <repo> <commit> <outdir> B01|B02
set -euo pipefail
repo=$1; commit=$2; out=$3; which=$4
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$out/src"; mkdir -p "$out/src"
git -C "$repo" archive "$commit" | tar -x -C "$out/src"
python3 "$here/p1_failed_walk_get.py" "$out/src/tb/acmp_nvm/sim_main.cpp"
python3 - "$out/src/hdl/acmp/KL_acmp_nvm_shadow.sv" "$which" <<'PY'
import sys
p, which = sys.argv[1], sys.argv[2]; s = open(p).read()
edits = {
  "B02": [("&& (nvm_err_cause_i != CAUSE_UNFRAMED_C);", "&& 1'b0;"),
          ("&& (nvm_err_cause_i == CAUSE_UNFRAMED_C))", ")")],
  "B01": [("assign rs_tmo_w   = rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1));",
           "assign rs_tmo_w   = 1'b0;")],
}[which]
for old, new in edits:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
open(p, "w").write(s); print("reverted", which, "in", p)
PY
cd "$out/src/tb/acmp_nvm"
make -s ltn_rom.hex
make -s run VERILATOR="${VERILATOR:-verilator}" > build-and-suite.log 2>&1 || true
R278_PROBE=1 ./obj_dir/Vacmp_nvm_sim

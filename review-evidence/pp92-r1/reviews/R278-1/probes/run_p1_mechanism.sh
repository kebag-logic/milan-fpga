#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe P1m (mechanism only, NOT a proposed fix): rerun probe P1 with
# the binding manager's capture compare ignoring field-only differences
# between two UNBOUND records. If P1's failures vanish, the erasure comes
# from the shadow keeping a rejected sink's NVM fields while valid is 0.
# Usage: run_p1_mechanism.sh <repo> <commit> <outdir>
set -euo pipefail
repo=$1; commit=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$out/src"; mkdir -p "$out/src"
git -C "$repo" archive "$commit" | tar -x -C "$out/src"
python3 "$here/p1_failed_walk_get.py" "$out/src/tb/acmp_nvm/sim_main.cpp"
python3 - "$out/src/hdl/acmp/KL_acmp_nvm_shadow.sv" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = """  assign c1_diff_w  = (SHW_W_C'(c1_proj_r) != cmp_data_w)
                    || (c1_vld_r != valid_r[c1_sink_r]);"""
new = """  assign c1_diff_w  = ((c1_vld_r || valid_r[c1_sink_r]) && (SHW_W_C'(c1_proj_r) != cmp_data_w))
                    || (c1_vld_r != valid_r[c1_sink_r]);"""
assert s.count(old) == 1; open(p, "w").write(s.replace(old, new)); print("mutated", p)
PY
cd "$out/src/tb/acmp_nvm"
make -s ltn_rom.hex
make -s run VERILATOR="${VERILATOR:-verilator}" > build-and-suite.log 2>&1 || true
tail -1 build-and-suite.log
R278_PROBE=1 ./obj_dir/Vacmp_nvm_sim

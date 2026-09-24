#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe P1 runner. Usage: run_p1.sh <repo> <commit> <outdir>
# Extracts <commit> of <repo> into <outdir>/src (a disposable copy), applies
# p1_failed_walk_get.py to its tb/acmp_nvm bench and runs only the probe.
# VERILATOR must name Verilator 5.050 (the CI pin).
set -euo pipefail
repo=$1; commit=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$out/src"; mkdir -p "$out/src"
git -C "$repo" archive "$commit" | tar -x -C "$out/src"
python3 "$here/p1_failed_walk_get.py" "$out/src/tb/acmp_nvm/sim_main.cpp"
cd "$out/src/tb/acmp_nvm"
"${VERILATOR:-verilator}" --version
make -s ltn_rom.hex
make -s run VERILATOR="${VERILATOR:-verilator}" > build-and-suite.log 2>&1 || true
R278_PROBE=1 ./obj_dir/Vacmp_nvm_sim

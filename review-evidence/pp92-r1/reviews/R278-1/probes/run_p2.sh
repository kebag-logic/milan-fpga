#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe P2 runner. Usage: run_p2.sh <repo> <commit> <outdir>
set -euo pipefail
repo=$1; commit=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$out/src"; mkdir -p "$out/src"
git -C "$repo" archive "$commit" | tar -x -C "$out/src"
python3 "$here/p2_pp_top_bw3_get.py" "$out/src/tb/pp_top/sim_main.cpp"
cd "$out/src/tb/pp_top"
V="${VERILATOR:-verilator}"
# a probe target beside the suite's own, same variables, first build only
printf '\nr278-probe: fixture-guards ltn_rom.hex ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim > build.log 2>&1\n\tR278_PROBE=1 ./obj_dir/Vpp_top_sim\n' >> Makefile
make -s r278-probe VERILATOR="$V"

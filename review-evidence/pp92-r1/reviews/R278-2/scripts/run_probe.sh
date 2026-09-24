#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# run_probe.sh <P1|P2|P3> <commit> <outdir-under-scratch>
# Extracts <commit> of the review clone into a disposable copy, applies the
# probe's injector to that copy's bench, builds with the pinned simulator and
# runs only the probe. The probe's own tally line is its verdict.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
probe=$1; commit=$2; out=$3
"$here/extract.sh" "$commit" "$out"
"$V" --version
case "$probe" in
  P1|P3)
    inj=$here/p1_failed_walk_get.py; env=R278_PROBE
    [ "$probe" = P3 ] && { inj=$here/p3_unbound_rule_edges.py; env=R278_P3; }
    python3 "$inj" "$out/tb/acmp_nvm/sim_main.cpp"
    cd "$out/tb/acmp_nvm"
    make run VERILATOR="$V" > build-and-suite.log 2>&1 || true
    grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' build-and-suite.log | tail -1 | sed 's/^/suite (unpatched cases) /'
    env "$env=1" ./obj_dir/Vacmp_nvm_sim ;;
  P2)
    python3 "$here/p2_pp_top_bw3_get.py" "$out/tb/pp_top/sim_main.cpp"
    cd "$out/tb/pp_top"
    printf '\nr278-probe: fixture-guards ltn_rom.hex ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim > build.log 2>&1\n\tR278_PROBE=1 ./obj_dir/Vpp_top_sim\n' >> Makefile
    make -s r278-probe VERILATOR="$V" ;;
esac

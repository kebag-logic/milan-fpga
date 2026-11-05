#!/bin/sh
# Build the bootsa leg (and, with a 3rd arg "probe", the probe harness) against
# one datapath source into a scratch objdir, through the Makefile's own recipe.
# Usage: build_variants.sh <repo> <objdir> <datapath.sv> [probe <probe.cpp>]
set -eu
REPO=$1; MD=$2; DP=$3
V=${VERILATOR:-verilator}   # a Verilator 5.050 binary or wrapper
cd "$REPO/tb/verilator/milan_dp"
make -s VERILATOR=$V VERILATOR_JOBS=8 BOOTSA_MDIR="$MD" DP_SRC="$DP" bootsa-build
if [ "${4:-}" = probe ]; then
  cmd=$(make -n VERILATOR=$V VERILATOR_JOBS=8 BOOTSA_MDIR="$MD" DP_SRC="$DP" bootsa-build | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep -- "sim_boot_sa.cpp -o Vmilan_dp_bootsa")
  cmd=$(printf '%s' "$cmd" | sed "s#sim_boot_sa.cpp -o Vmilan_dp_bootsa#$5 -o Vmilan_dp_bootsa_probe#")
  sh -c "$cmd"
fi

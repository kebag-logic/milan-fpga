#!/bin/sh
# Build and run only the committed 4x4 sim_nxn leg (obj_nxn) of the milan_dp
# `run` recipe, in TREE, with the pinned Verilator capped at $VL_JOBS.
# Usage: nxn_leg.sh TREE PACKET_DIR   (VL_REAL, VL_JOBS in the environment)
set -eu
TREE="$1"; P="$2"; VL="$P/scripts/vl-capped.sh"
cd "$TREE/tb/verilator/milan_dp"
make ltn_rom.hex ucode.hex gptp_ucode.hex
# The exact obj_nxn command line of `make -n run`, verilator substituted.
cmd=$(make -n run VERILATOR=VLX 2>/dev/null | grep -- '--Mdir obj_nxn -GN_STREAMS=4 ' | head -1)
[ -n "$cmd" ]
rm -rf obj_nxn
eval "$(printf '%s' "$cmd" | sed "s#^VLX #$VL #")"
./obj_nxn/Vmilan_dp_nxn

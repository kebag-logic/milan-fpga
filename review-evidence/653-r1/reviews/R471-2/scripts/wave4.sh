#!/bin/bash
# Wave 4: the other four sim_nxn.cpp elaborations of the milan_dp suite.
. "$(dirname "$0")/env.sh"
D=$SCR/nxn/tb/verilator/milan_dp
# generate the shared inputs once, then build/run the four shapes in parallel
make -C $D -f Makefile -f $PKT/scripts/nxn_extra.mk ltn_rom.hex ucode.hex gptp_ucode.hex VERILATOR="$VERILATOR" > $REC/nxn_prereq.log 2>&1
for t in nxn-4x4 nxn-dv nxn-8x8 nxn-4c; do
  run "$t" make -C $D -f Makefile -f $PKT/scripts/nxn_extra.mk $t VERILATOR="$VERILATOR" VERILATOR_JOBS=4
done
wait

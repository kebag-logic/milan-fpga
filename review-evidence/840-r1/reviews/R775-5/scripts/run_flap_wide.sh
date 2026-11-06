#!/bin/sh
# usage: run_flap_wide.sh <milan_dp dir> <log dir>
# Expects kAdvertiseBoundMs already set to 8000 in the copy of sim_boot_sa.cpp.
# Rebuilds the flap probe with that widened bound and runs
# it with no flap and with a 3 s flap, with and without the MAC stalled.
d=$1; l=$2
PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH; export PATH
VERILATOR_JOBS=4; export VERILATOR_JOBS
cd "$d" || exit 9
make -s bootsa-build BOOTSA_MDIR=obj_wide > "$l/flap_wide.build.log" 2>&1 || { echo build-failed > "$l/flap_wide.rc"; exit 1; }
( ./obj_wide/Vmilan_dp_bootsa > "$l/flap_wide_control.log" 2>&1; echo $? > "$l/flap_wide_control.rc" ) &
( BOOTSA_FLAP_AT=45000 BOOTSA_FLAP_LEN=300000 ./obj_wide/Vmilan_dp_bootsa > "$l/flap_wide_300k.log" 2>&1; echo $? > "$l/flap_wide_300k.rc" ) &
( BOOTSA_FLAP_AT=45000 BOOTSA_FLAP_LEN=300000 BOOTSA_FLAP_STALL=1 ./obj_wide/Vmilan_dp_bootsa > "$l/flap_wide_300k_stall.log" 2>&1; echo $? > "$l/flap_wide_300k_stall.rc" ) &
wait
echo done > "$l/flap_wide.rc"

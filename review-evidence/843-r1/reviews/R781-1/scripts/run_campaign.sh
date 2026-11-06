#!/usr/bin/env bash
# Concurrent focused runs and planted mutants for the PR #846 review.
# usage: run_campaign.sh <packet dir>   (copies of the head clone in
# <packet>/scratch/{h,hl,m1..m4}; logs and rc files to <packet>/receipts/runs)
set -u
P=$1; S=$P/scratch; R=$P/receipts/runs; mkdir -p "$R"
export VERILATOR=<data>/tools/pinned-verilator-5.050/verilator
export PATH=<data>/tools/pinned-verilator-5.050:$PATH
export MAKEFLAGS="-j2 --no-print-directory" VERILATOR_JOBS=2
G='test_rom_clock_contract,test_baremetal_profile_contract,test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board'
job() { local name=$1 dir=$2; shift 2
  ( cd "$dir" && "$@" ) > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
job H-milan_dp-gptp      $S/h  make -C tb/verilator/milan_dp gptp VERILATOR=$VERILATOR &
job H-milan_dp-gptp-lat  $S/hl make -C tb/verilator/milan_dp gptp-lat VERILATOR=$VERILATOR &
job H-gptp_shadow        $S/h  make -C tb/verilator/gptp_shadow run VERILATOR=$VERILATOR &
job H-gptp_plane         $S/h  make -C tb/verilator/gptp_plane run VERILATOR=$VERILATOR &
job H-builder-gates      $S/hl python3 sw/builder/test_builder.py --gates $G &
job M1-milan_dp-gptp     $S/m1 make -C tb/verilator/milan_dp gptp VERILATOR=$VERILATOR &
job M1-builder-gates     $S/m1 python3 sw/builder/test_builder.py --gates test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board &
job M2-milan_dp-gptp-lat $S/m2 make -C tb/verilator/milan_dp gptp-lat VERILATOR=$VERILATOR &
job M2-builder-26c       $S/m2 python3 sw/builder/test_builder.py --gates test_gptp_clock_accuracy_per_board &
job M3-gptp_shadow       $S/m3 make -C tb/verilator/gptp_shadow run VERILATOR=$VERILATOR &
job M4-gptp_plane        $S/m4 make -C tb/verilator/gptp_plane run VERILATOR=$VERILATOR &
wait
echo ALL-DONE > "$R/ALL.done"

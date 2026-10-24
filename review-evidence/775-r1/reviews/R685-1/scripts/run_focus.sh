#!/usr/bin/env bash
# Focused suite runs: head avtp_rxmon + crf_rx (with mutant drivers), base-RTL harness runs.
# usage: run_focus.sh <scratch-dir> <receipts-dir> ; pinned verilator first on PATH
set -u
S=$1; R=$2
run() { local name=$1; shift; ( cd "$1" && shift && "$@" ) > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
run head-avtp_rxmon  "$S/head/tb/verilator/avtp_rxmon" make &
run head-crf_rx      "$S/head/tb/verilator/crf_rx" make &
run base-avtp_rxmon-nx "$S/base/tb/verilator/avtp_rxmon" bash -c 'make nx-build && ./obj_nx/Vavtp_rxmon_nx_sim' &
run base-crf_rx-unit "$S/base/tb/verilator/crf_rx" bash -c 'make unit-build discontinuity-build && { ./obj_unit/Vcrf_rx_sim; a=$?; ./obj_discontinuity/Vdiscontinuity; b=$?; echo "unit_rc=$a disc_rc=$b"; exit $((a|b)); }' &
wait

#!/bin/sh
# Reviewer receipt driver: build and run tb/adp_engine and the ADP mutant campaign
# from exported trees of the exact head, with the pinned Verilator on PATH.
# usage: run_head.sh PACKET_DIR WHAT   (WHAT = suite | campaign)
K=$1
WHAT=$2
S=$K/scratch
R=$K/receipts
export PATH="$S/bin:$PATH"
export TMPDIR="$S/tmp"
case "$WHAT" in
  suite)
    make -C "$S/head/tb/adp_engine" run > "$R/head-adp_engine-run.log" 2>&1
    echo $? > "$R/head-adp_engine-run.rc" ;;
  campaign)
    make -C "$S/camp/tb/adp_engine" mutants JOBS=6 MUTANT_OUTPUT="$S/camp-out" \
      > "$R/head-campaign-jobs6.log" 2>&1
    echo $? > "$R/head-campaign-jobs6.rc" ;;
esac

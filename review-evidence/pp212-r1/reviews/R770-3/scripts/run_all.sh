#!/usr/bin/env bash
# Reviewer gate set at the exact head; every job writes receipts/<name>.log and .rc.
# usage: run_all.sh <packet-dir>   (VERILATOR must name the pinned Verilator 5.050)
set -u
P=$1; S=$P/scratch; R=$P/receipts
export VERILATOR=${VERILATOR:?set VERILATOR to the pinned Verilator 5.050}
export PATH=$(dirname "$VERILATOR"):$PATH TMPDIR=$S/tmp
ARMS=settled-link-flush-dropped,settled-link-unpublished,link-withdraw-dropped,link-clock-indicates,settled-link-keeps-lv-slot,link-begin-dropped,lv-expiry-masked,r-sink-receive-priority-lost,unarmed-indicates,unarmed-latency-strobe,unarmed-link-flush-dropped,unarmed-unregistered,keep-declares-seed-type,listener-reprobe-abandons-leave,listener-settle-compare-dropped,listener-teardown-keeps-declaring,presettle-removed,pt-link-flush-dropped,rebind-same-not-kept,seed-no-registered-strobe,keep-on-link-clock,top-listener-link-unwired
( cd $S/clean/tb/srp_stream_fsms && make > $R/suite-srp_stream_fsms.log 2>&1; echo $? > $R/suite-srp_stream_fsms.rc ) &
( cd $S/clean2/tb/srp_top && make > $R/suite-srp_top.log 2>&1; echo $? > $R/suite-srp_top.rc ) &
( cd $S/clean3 && python3 -B tb/srp_top/mutants.py --output $S/camp-out --only $ARMS --jobs 10 > $R/campaign-r3-arms.log 2>&1; echo $? > $R/campaign-r3-arms.rc ) &
( bash $P/scripts/area_2x2.sh $S/clean4 $R/area-head-2x2 listener_n2 > $R/area-head-2x2.log 2>&1; echo $? > $R/area-head-2x2.rc ) &
wait

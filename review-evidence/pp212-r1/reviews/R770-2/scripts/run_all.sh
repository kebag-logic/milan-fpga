#!/usr/bin/env bash
# Reviewer gate set at the exact head; every job writes <name>.log and <name>.rc.
# usage: run_all.sh <packet-dir>
set -u
P=$1; S=$P/scratch; R=$P/receipts
export VERILATOR=${VERILATOR:?set VERILATOR to the pinned Verilator 5.050}
export TMPDIR=$S/tmp
ARMS=presettle-removed,pt-seed-dropped,pt-alloc-any-event,pt-fcode-first-only,pt-lat-on-alloc-only,pt-type-on-alloc-only,seed-on-teardown,pt-rlv-on-lv-ends,rebind-same-not-kept,keep-ignores-da,keep-ignores-vlan,keep-declares-seed-type,keep-latency-strobe-dropped,unarmed-registrar-deaf,keep-ignores-expiry,unarmed-indicates,unarmed-fail-chg,unarmed-unregistered,unarmed-latency-strobe,unarmed-publishes-latency,unarmed-dbg-registrar,pt-link-flush-dropped,link-begin-dropped,unarmed-link-flush-dropped,keep-on-link-clock,top-listener-link-unwired,pt-expiry-sign-bit,seed-deadline-rebuild-drops-now,pt-leaveall-any-lane,pt-leaveall-ignored,pt-leavetimer-never-expires,pt-never-holds,pt-rlv-ignored,seed-from-current-state,seed-keeps-expiry-strobe,seed-lv-fresh-deadline,seed-lv-unguarded,seed-no-registered-strobe
( cd $S/clean/tb/srp_stream_fsms && make > $R/suite-srp_stream_fsms.log 2>&1; echo $? > $R/suite-srp_stream_fsms.rc ) &
( cd $S/clean2/tb/srp_top && make > $R/suite-srp_top.log 2>&1; echo $? > $R/suite-srp_top.rc ) &
( cd $S/probe/tb/srp_stream_fsms && make RUN_ARGS=suite > $R/probe-srp_stream_fsms.log 2>&1; echo $? > $R/probe-srp_stream_fsms.rc ) &
( cd $S/clean3 && python3 tb/srp_top/mutants.py --output $S/camp-out --only $ARMS --jobs 8 > $R/campaign-r2-arms.log 2>&1; echo $? > $R/campaign-r2-arms.rc ) &
wait

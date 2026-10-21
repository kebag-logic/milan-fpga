#!/usr/bin/env bash
# targeted dev campaign: every label with a stream-FSM suite row, on the uncommitted tree
. <scratch>/r4/scripts/env.sh
cd <scratch>/r4/dev/camp
t0=$(date +%s)
python3 tb/srp_top/mutants.py --output <scratch>/r4/dev/camp-out --jobs 2 --only talker-lost-txla,listener-lost-txla,licence-ignores-join,lv-expiry-masked,lv-expiry-last,lv-expiry-dropped,listener-rebind-abandons-leave,listener-declaration-not-held,listener-park-never-retires,listener-reprobe-abandons-leave,listener-reprobe-parks-own-stream,listener-csid-ram-ignores-park,listener-rebind-back-keeps-park,listener-lo-not-owed,listener-park-retires-on-txla,listener-parked-applies-rx,listener-unrecorded-applicant-owes,listener-settle-compare-dropped,listener-rider-not-quiet,listener-teardown-applies-lv,listener-handover-drops-state,listener-withdraw-ignores-riders,listener-teardown-keeps-declaring,listener-group-order-reversed,listener-rider-settle-hands-over,listener-type-not-combined,listener-handover-forgets-walk-mark,listener-settle-parks-shared-stream,listener-group-op-during-settle,listener-parked-outside-groups,listener-settle-skips-leave-copies,listener-merge-keeps-park,listener-retire-skips-group-mark,listener-park-drops-matcher-pairs,listener-repark-takes-matcher-pairs,listener-two-parks-grouped,listener-walk-ends-owing-a-transmit,listener-walk-marks-only-served-slots,listener-walk-marks-group-only-on-retire,listener-walk-done-before-second-pass > <scratch>/r4/dev/camp.log 2>&1
echo $? > <scratch>/r4/dev/camp.rc
echo $(( $(date +%s) - t0 )) > <scratch>/r4/dev/camp.sec

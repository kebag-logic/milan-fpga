#!/bin/bash
# Run every probe plant (at most two at a time) against an exported copy of the head.
. "$(dirname "$0")/env.sh"
REPO=$S/probe-repo; LW=$R/third_party/lwSRP
run() { python3 -I $P/scripts/probe_mutants.py $REPO $LW $S/probe-$1 $1 > $P/receipts/probe-$1.log 2>&1; echo "$1 rc=$?" >> $P/receipts/probes.summary; }
: > $P/receipts/probes.summary
run control-none & run srp-poll-drops-tx & wait
run srp-pass-drops-rx-and-poll & wait
run srp-rx-max-zero & run srp-event-max-zero & wait
run attach-acmp-always & wait
run attach-no-tick & wait

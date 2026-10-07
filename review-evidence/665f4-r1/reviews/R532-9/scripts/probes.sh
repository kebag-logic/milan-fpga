#!/bin/bash
# usage: probes.sh PACKET REPO LWSRP -- run every probe plant, six at a time, against the head.
P=$1; R=$2; LW=$3
run() { python3 -I $P/scripts/probe_mutants.py $R $LW $P/scratch/probe-$1 $1 > $P/receipts/r8probes/probe-$1.log 2>&1; echo "$1 rc=$?" >> $P/receipts/r8probes/probes.summary; }
mkdir -p $P/receipts/r8probes; : > $P/receipts/r8probes/probes.summary
for n in control-none srp-poll-drops-tx srp-pass-drops-rx-and-poll srp-rx-max-zero srp-event-max-zero attach-acmp-always attach-no-tick code-poll-extra-read code-send-extra-read; do
  run $n &
  while [ "$(jobs -r | wc -l)" -ge 6 ]; do sleep 2; done
done
wait

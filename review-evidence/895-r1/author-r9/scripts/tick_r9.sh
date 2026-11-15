#!/bin/bash
# tick_r9.sh SECONDS: for up to SECONDS, every 60 s, one pass of round 9's full-pass starters (lane 895): the sweep
# first (sweep_shard.py, the next shard on its own pick8 range), then the gate queue (disp_once.py, at most GATE_MAX gate units,
# MemAvailable above 20 GB). Stops early once a unit of this round ends (a new rc file). Prints what started and the
# state of every gate unit and sweep shard.
set -u
S9=$MANAGEMENT/2026-09-23/895-a775/round9/scripts
T=/data-2/milan/tmp/895-a775/r9
U=$T/units
end=$(( $(date +%s) + $1 ))
before=$(ls $U/*.rc 2>/dev/null | wc -l)
while [ $(date +%s) -lt $end ]; do
  python3 $S9/sweep_shard.py $T/sweep/full-native.json $T/sweep/out 4 2>&1 | grep -v "waiting\|every shard" | sed "s/^/$(date +%T) /"
  python3 $S9/gates/disp_once.py "${GATE_MAX:-4}" 20 $T/gates.queue 2>&1 | grep started
  python3 $S9/gates/pool_start.py $T/gates.queue ${POOL_UNITS:-lane-c W-docs-gates-2}
  now=$(ls $U/*.rc 2>/dev/null | wc -l)
  [ "$now" != "$before" ] && { echo "$(date +%T) units ended: $before -> $now rc files"; break; }
  sleep 60
done
python3 $S9/gates/disp_once.py 0 20 $T/gates.queue 2>&1 | tail -2
systemctl --user list-units 'milan-895r9sweep-*' --no-legend --plain --all 2>/dev/null | awk '{print $1, $4}' | tr '\n' ' '; echo

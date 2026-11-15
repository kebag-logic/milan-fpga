#!/bin/bash
# tick_r10.sh SECONDS: for up to SECONDS, every 60 s, one pass of round 10's gate starters (lane 895): the gate queue
# (disp_once.py, at most GATE_MAX gate units on pick8 ranges), then the session pool for the units POOL_UNITS names
# (pool_start.py, at most two there). Stops early once a unit of this round ends. Prints what started and each gate
# unit's state.
set -u
S10=$MANAGEMENT/2026-09-23/895-a775/round10/scripts
T=/data-2/milan/tmp/895-a775/r10
U=$T/units
end=$(( $(date +%s) + $1 ))
before=$(ls $U/*.rc 2>/dev/null | wc -l)
while [ $(date +%s) -lt $end ]; do
  python3 $S10/gates/disp_once.py "${GATE_MAX:-4}" 20 $T/gates.queue 2>&1 | grep started
  python3 $S10/gates/pool_start.py $T/gates.queue ${POOL_UNITS:-}
  now=$(ls $U/*.rc 2>/dev/null | wc -l)
  [ "$now" != "$before" ] && { echo "$(date +%T) units ended: $before -> $now rc files"; break; }
  sleep 60
done
python3 $S10/gates/disp_once.py 0 20 $T/gates.queue 2>&1 | tail -2

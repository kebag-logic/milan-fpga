#!/bin/bash
# poll.sh SECONDS: for up to SECONDS, every 60 s, one pass of the leg starter and of the gate dispatcher (lane 895
# round 5); stops early once a unit of this lane has started or ended. Prints what changed.
set -u
M=$MANAGEMENT/2026-09-23/895-a775/round5/scripts
U=/data-2/milan/tmp/895-a775/r5/units
end=$(( $(date +%s) + $1 ))
before=$(ls $U/*.rc 2>/dev/null | wc -l):$(systemctl --user list-units 'milan-895-a775-r5-*' --no-legend --plain --state=active | wc -l)
while [ $(date +%s) -lt $end ]; do
  a=$(bash $M/tick_r5.sh 2>&1 | grep started)
  c=$(python3 $M/sweep_launch.py 2>&1 | grep -v "waiting\|launched already")
  [ -n "$c" ] && echo "$(date +%T) $c"
  b=$(python3 $M/gates/disp_once.py 6 20 /data-2/milan/tmp/895-a775/r5/gates/queue.txt 2>&1 | grep started)
  now=$(ls $U/*.rc 2>/dev/null | wc -l):$(systemctl --user list-units 'milan-895-a775-r5-*' --no-legend --plain --state=active | wc -l)
  [ -n "$a$b" ] && echo "$a $b"
  [ "$now" != "$before" ] && { echo "$(date +%T) units changed: rc files:active $before -> $now"; break; }
  sleep 60
done
systemctl --user list-units 'milan-895-a775-r5-*' --no-legend --plain --state=active | awk '{print $1}' | tr '\n' ' '; echo

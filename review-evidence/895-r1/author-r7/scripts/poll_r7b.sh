#!/bin/bash
# poll.sh SECONDS: for up to SECONDS, every 60 s, one pass of round 7B's leg starter (lane 895); stops early once a unit
# of this round has ended (a new rc file). Prints what started and the units running.
set -u
S6=$MANAGEMENT/2026-09-23/895-a775/round7/scripts
U=/data-2/milan/tmp/895-a775/r7b/units
end=$(( $(date +%s) + $1 ))
before=$(ls $U/*.rc 2>/dev/null | wc -l)
while [ $(date +%s) -lt $end ]; do
  bash $S6/tick_r7b.sh 2>&1 | grep started
  now=$(ls $U/*.rc 2>/dev/null | wc -l)
  [ "$now" != "$before" ] && { echo "$(date +%T) units ended: $before -> $now rc files"; break; }
  sleep 60
done
systemctl --user list-units 'milan-895-a775-r7b-*' --no-legend --plain --state=active | awk '{print $1}' | sed 's/milan-895-a775-r7b-//' | tr '\n' ' '; echo
for f in /data-2/milan/tmp/895-a775/legs/R7B-*.log; do n=$(basename $f .log); printf "%s:%s " $n "$(cat ${f%.log}.rc 2>/dev/null || echo run)"; done; echo

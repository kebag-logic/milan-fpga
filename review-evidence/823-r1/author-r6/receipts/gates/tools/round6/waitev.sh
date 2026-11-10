#!/usr/bin/env bash
# waitev.sh <seconds>: return early when a driver fails a step or starts a job, an extra ends, or a shard unit ends.
S=<scratch>
snap() { echo "$(cat $S/drive5-*.log 2>/dev/null | grep -c 'rc=[1-9]')|$(cat $S/drive3-a.log $S/drive3-b.log $S/drive4-c.log 2>/dev/null | grep -c '^==')|$(ls $S/gates/run/logs/*.rc 2>/dev/null | wc -l)|$(systemctl --user list-units 'milan-823-a753f-*' --no-legend --plain --state=active | wc -l)"; }
a=$(snap); end=$((SECONDS + $1))
while [ $SECONDS -lt $end ]; do sleep 15; b=$(snap); [ "$a" != "$b" ] && { echo "changed: $a -> $b"; exit 0; }; done
echo "no change: $a"

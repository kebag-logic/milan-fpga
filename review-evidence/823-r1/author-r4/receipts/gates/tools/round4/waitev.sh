#!/usr/bin/env bash
# waitev.sh <seconds>: return early when something of this round changes state worth a look.
S=<scratch>
snap() { echo "$(cat $S/drive-*.log 2>/dev/null | grep -c "rc=[1-9]")|$(wc -l < $S/waiter.log)|$(systemctl --user list-units "milan-823-a753d-*" --no-legend --plain | wc -l)|$(ls $S/gates/run/logs/*.rc 2>/dev/null | wc -l)"; }
a=$(snap); end=$((SECONDS + $1))
while [ $SECONDS -lt $end ]; do sleep 15; b=$(snap); [ "$a" != "$b" ] && { echo "changed: $a -> $b"; exit 0; }; done
echo "no change: $a"

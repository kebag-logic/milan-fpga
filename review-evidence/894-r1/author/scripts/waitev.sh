#!/bin/bash
# Wait up to SECONDS for something to need attention: a dispatched gate unit ending, a leg or sweep shard ending, the
# scratch disk under 8 GB or MemAvailable under 22 GB; then print the state. usage: waitev.sh SECONDS
T=/data-2/milan/tmp/894-a773
ended() { grep -c ended $T/gates-out/dispatch.txt; }
legs() { ls $T/units/L1A.rc $T/units/L1N.rc $T/units/L8A.rc $T/units/L8N.rc 2>/dev/null | wc -l; }
shards() { systemctl --user list-units 'milan-894-a773-sweep-shard*' --no-legend --plain | wc -l; }
e0=$(ended) l0=$(legs) s0=$(shards)
end=$((SECONDS + $1))
while [ $SECONDS -lt $end ]; do
    [ "$(ended)" -gt "$e0" ] || [ "$(legs)" -gt "$l0" ] || [ "$(shards)" -lt "$s0" ] && break
    [ "$(df --output=avail -k /data-2 | tail -1)" -lt 8000000 ] && break
    [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -lt 22000000 ] && break
    sleep 15
done
date +%T
tail -n 4 $T/gates-out/dispatch.txt
for L in L1A L1N L8A L8N; do echo "$L logs=$(ls $T/builds/$L/results/*.log 2>/dev/null | wc -l) rc=$(cat $T/units/$L.rc 2>/dev/null)"; done
echo "sweep shards active: $(shards)"
df -h /data-2 | tail -1
grep MemAvailable /proc/meminfo

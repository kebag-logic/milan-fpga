#!/bin/bash
# launch.sh: reserve four CPU ranges (placeholder units, released at launch), then run native-shards.py
G=<scratch>/gates; M=<management>/2026-09-23
log=$G/sweep/launch4.txt; ranges=()
while [ ${#ranges[@]} -lt 4 ]; do
  r=$(/usr/bin/python3 $M/cpu_ranges.py pick)
  if [ -n "$r" ]; then
    k=${#ranges[@]}
    systemd-run --user --unit=milan-665s11-a761-res$k --collect /usr/bin/taskset -c $r /usr/bin/sleep 86400 >> $log 2>&1
    ranges+=("$r"); echo "$(date +%T) reserved $r (MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB)" >> $log
  else
    sleep 60
  fi
done
until [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -gt 31457280 ]; do sleep 60; done
for k in 0 1 2 3; do systemctl --user stop milan-665s11-a761-res$k >> $log 2>&1; done
a=${ranges[2]%-*}; c2="$a-$((a + 3))"
echo "$(date +%T) launching on ${ranges[0]} ${ranges[1]} $c2 ${ranges[3]}" >> $log
/usr/bin/python3 $M/native-shards.py 665s11-a761-sw $G/sweep/full-native.json $G/sweep/out4 4 ${ranges[0]} ${ranges[1]} $c2 ${ranges[3]} >> $log 2>&1
echo "$(date +%T) native-shards rc=$?" >> $log

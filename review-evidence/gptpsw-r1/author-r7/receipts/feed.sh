#!/usr/bin/env bash
# feed.sh <jobs...>: within ~9 minutes, launch each job (in order) the moment cpu_ranges.py pick returns a range
T=/data-2/milan/tmp/opt-a837-r2; P=$MANAGEMENT/2026-09-23/cpu_ranges.py
end=$((SECONDS+540))
for job in "$@"; do
  [ -e $T/logs/started-$job ] && continue
  until r=$(python3 $P pick 2>/dev/null); do [ $SECONDS -ge $end ] && { echo "waiting: $job and after"; exit 3; }; sleep 15; done
  $T/bin/launch.sh $job "$r" && echo "$(date +%T) $job $r" | tee $T/logs/started-$job; sleep 5
done
echo all-started

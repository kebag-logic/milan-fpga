#!/usr/bin/env bash
# unit_waiter.sh <name> <list>: poll cpu_ranges.py pick every 2 s; on a free range run drive.sh over <list> at the head
# as gate unit milan-823-a753f-<name> on that range (MemoryMax 10G, not niced), root gates/final5, log drive5-<name>.log.
S=<scratch>; T=$S/gates/tools; H=2905c8749a4573450b9999dd546bb20ae5c7fc38; N=$1; L=$2
while :; do
  R=$(python3 <management>/2026-09-23/cpu_ranges.py pick 2>/dev/null | tail -1)
  [ -n "$R" ] && break; sleep 2
done
echo "$(date +%T) $N on $R"
systemd-run --user --unit=milan-823-a753f-$N --collect --property=MemoryMax=10G --setenv=HOME=<home> \
  --setenv=PATH=/usr/local/bin:/usr/bin:/bin /usr/bin/taskset -c "$R" /bin/bash -c "bash $T/drive.sh $H $S/gates/final5 $L > $S/drive5-$N.log 2>&1"
echo "$(date +%T) launched rc=$?"

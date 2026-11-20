#!/bin/bash
# repin.sh: re-apply each active unit's booked CPUs (pins.txt, written by bgunit.sh) to every process of the unit; the
# host resets task affinity (seen 2026-11-17), which leaves the units invisible to cpu_ranges.busy.
P=<scratch>/bin/pins.txt
declare -A pin; while read -r u c; do pin[$u]=$c; done < $P
for u in "${!pin[@]}"; do
  [ "$(systemctl --user is-active $u 2>/dev/null)" = active ] || continue
  cg=$(systemctl --user show -p ControlGroup --value $u)
  n=0; for pid in $(cat /sys/fs/cgroup$cg/cgroup.procs 2>/dev/null); do taskset -a -cp ${pin[$u]} $pid >/dev/null 2>&1 && n=$((n+1)); done
  echo "$u ${pin[$u]} $n"
done

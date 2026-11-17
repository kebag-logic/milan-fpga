#!/bin/bash
# repin.sh <unit-suffix>: move one of my units that fell back to the session pool (96-127) onto a range booked through
# cpu_ranges.py pick: every process of the unit's cgroup, twice over for children forked meanwhile; then its CPU weight
# back to 100. Each process moved is listed with its arguments in r4/repin-<suffix>.txt. Does nothing when none is free.
set -u
S=<scratch>; u=milan-sync1115-a787-$1.service
case "$(taskset -cp "$(systemctl --user show -p MainPID --value "$u")" 2>/dev/null)" in *": 96-127"|*": 0-127") ;; *) echo "$1 on a booked range"; exit 0 ;; esac
# None free: back onto the session pool (bgunit.sh's fallback), where a host event left the unit unpinned (0-127).
r=$(python3 <management>/2026-09-23/cpu_ranges.py pick) || { r=96-127; echo "$1: no range free"; }
cg=$(systemctl --user show -p ControlGroup --value "$u")
for pass in 1 2; do
  for p in $(cat "/sys/fs/cgroup$cg/cgroup.procs"); do
    echo "$p $(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | cut -c1-120)" >> "$S/r4/repin-$1.txt"
    taskset -acp "$r" "$p" >/dev/null 2>&1
  done
done
[ "$r" = 96-127 ] || systemctl --user set-property --runtime "$u" CPUWeight=100
echo "$1 moved to $r: main $(taskset -cp "$(systemctl --user show -p MainPID --value "$u")")"

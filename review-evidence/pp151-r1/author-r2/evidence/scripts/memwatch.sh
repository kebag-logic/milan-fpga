#!/usr/bin/env bash
# samples this unit's anon and total memory every 10 s into a file until killed
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
while :; do echo "$(date +%T) anon=$(awk '/^anon /{print int($2/1048576)}' $CG/memory.stat)M cur=$(( $(cat $CG/memory.current)/1048576 ))M oom=$(awk '/^oom_kill /{print $2}' $CG/memory.events)" >> "$1"; sleep 10; done

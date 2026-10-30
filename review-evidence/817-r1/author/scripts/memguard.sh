#!/usr/bin/env bash
# #817: protect the lane's service unit (24 GB cap) from the suite workers. Every 5 s, if the unit's memory
# passes the limit, terminate the process groups of suite workers 1 and 2 (worker 0 is left running) and log it.
# Records the unit's peak. Stops when <stop-file> exists.
# usage: memguard.sh <limit-MB> <log> <stop-file>
set -u
limit=$1; log=$2; stop=$3
C=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-817-a709.service
peak=0
while [ ! -e "$stop" ]; do
  cur=$(( $(cat $C/memory.current) / 1048576 ))
  [ "$cur" -gt "$peak" ] && { peak=$cur; echo "$(date -u +%T) peak ${peak} MB" >> "$log"; }
  if [ "$cur" -gt "$limit" ]; then
    for p in $(pgrep -f "^timeout [0-9]+ make -C $VALIDATION_STORAGE/scratch/817-a709/clone-suites-[12]/"); do
      echo "$(date -u +%T) unit ${cur} MB > ${limit}: TERM $(ps -o cmd= -p "$p")" >> "$log"
      kill -TERM -- "-$(ps -o pgid= -p "$p" | tr -d ' ')"
    done
  fi
  sleep 5
done

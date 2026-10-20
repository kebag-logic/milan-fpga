#!/usr/bin/env bash
# keeps this unit's MemoryCurrent under 9 GB: every 3 s, reclaim page cache past 7 GB;
# in an emergency (anon past 8.5 GB) pause the parent stream's process group until anon
# falls under 6.5 GB. Logs every action to memguard.log.
S=<scratch>; U=$(sed -n 's#^0::/##p' /proc/self/cgroup); D=/sys/fs/cgroup/$U
L="$S/memguard.log"; paused=""
while :; do
  cur=$(cat "$D/memory.current"); anon=$(awk '$1=="anon"{print $2}' "$D/memory.stat")
  if [ "$cur" -gt 7000000000 ]; then
    echo 2G > "$D/memory.reclaim" 2>/dev/null
    echo "$(date +%T) reclaim at cur=$cur anon=$anon -> $(cat "$D/memory.current")" >> "$L"
  fi
  if [ -z "$paused" ] && [ "$anon" -gt 8500000000 ] && [ -f "$S/jobs/P.pid" ]; then
    paused=$(cat "$S/jobs/P.pid"); kill -STOP -- "-$paused" 2>/dev/null
    echo "$(date +%T) PAUSE P group $paused at anon=$anon" >> "$L"
  elif [ -n "$paused" ] && [ "$anon" -lt 6500000000 ]; then
    kill -CONT -- "-$paused" 2>/dev/null
    echo "$(date +%T) RESUME P group $paused at anon=$anon" >> "$L"; paused=""
  fi
  sleep 3
done

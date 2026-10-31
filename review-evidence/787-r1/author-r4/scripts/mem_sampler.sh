#!/usr/bin/env bash
# #787 round 4: sample the lane unit's MemoryCurrent (bytes) and the host's MemAvailable (kB) every 15 s.
# usage: mem_sampler.sh <out.tsv>
out=$1
while :; do
  printf '%s\t%s\t%s\n' "$(date -u +%FT%TZ)" \
    "$(systemctl --user show milan-787-a700e.service -p MemoryCurrent --value)" \
    "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" >> "$out"
  sleep 15
done

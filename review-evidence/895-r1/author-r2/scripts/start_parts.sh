#!/bin/bash
# Start queued harness parts (lane 895 round 2) on free 8-wide CPU ranges, one unit each, while ranges are free and
# MemAvailable is above 20 GB. usage: start_parts.sh QUEUE   (lines: BUILD POINT PART; a started line is removed)
set -u
Q=$1
M=$MANAGEMENT/2026-09-23
C=${CLONE:-/data-2/milan/tmp/895-a775/r2/L}
while read -r b p k; do
  [ -z "${b:-}" ] && continue
  avail=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
  [ "$avail" -gt 20 ] || { echo "MemAvailable $avail GB: wait"; break; }
  R=$(python3 $M/cpu_ranges.py pick) || { echo "no free range"; break; }
  bash $M/895-a775/scripts/unit.sh "r2-${b}-p$k" "$R" 10G -- "CLONE=$C bash $M/895-a775/scripts/part.sh $b $p $k" >/dev/null 2>&1 \
    && echo "$(date +%T) started $b part $k on $R" && sed -i "0,/^$b $p $k\$/{/^$b $p $k\$/d}" "$Q"
  sleep 2
done < <(cat "$Q")

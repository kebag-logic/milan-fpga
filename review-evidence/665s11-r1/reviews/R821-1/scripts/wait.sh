#!/bin/sh
# wait.sh SECONDS NAME...: wait up to SECONDS for every NAME's rc file; print each status and log tail.
PK=$(cd "$(dirname "$0")/.." && pwd)
limit=$1; shift
end=$(( $(date +%s) + limit ))
for name in "$@"; do
  while [ ! -f "$PK/receipts/$name.rc" ] && [ "$(date +%s)" -lt "$end" ]; do
    python3 -c 'import time; time.sleep(10)'
  done
done
for name in "$@"; do
  if [ -f "$PK/receipts/$name.rc" ]; then echo "$name rc=$(cat "$PK/receipts/$name.rc")"; else echo "$name RUNNING"; fi
  tail -n 3 "$PK/receipts/$name.log" 2>/dev/null
done

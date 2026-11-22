#!/bin/sh
# wait_rc.sh <receipt-dir> <seconds> <name...>: wait at most <seconds> for each <name>.rc, then print each status
dir=$1; limit=$2; shift 2
end=$(( $(date +%s) + limit ))
for n in "$@"; do
  while [ ! -f "$dir/$n.rc" ] && [ "$(date +%s)" -lt "$end" ]; do sleep 10; done
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$dir/$n.rc" 2>/dev/null || echo running)"; done

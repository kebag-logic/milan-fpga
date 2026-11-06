#!/usr/bin/env bash
# waitfor.sh <seconds> <condition...>: return when the condition command succeeds, or after <seconds>; prints which.
d=$(( $(date +%s) + $1 )); shift
until "$@" >/dev/null 2>&1; do
  [ "$(date +%s)" -ge "$d" ] && { echo "waitfor: still waiting after deadline"; exit 0; }
  sleep 15
done
echo "waitfor: condition met"

#!/usr/bin/env bash
# Poll for campaign rc files for at most MAX_S seconds; print what is done.
# usage: wait_rc.sh RECEIPTS MAX_S name...
r=$1; max=$2; shift 2
end=$(( $(date +%s) + max ))
while :; do
  pending=0
  for n in "$@"; do [ -f "$r/$n.rc" ] || pending=$((pending+1)); done
  [ "$pending" -eq 0 ] && break
  [ "$(date +%s)" -ge "$end" ] && break
  sleep 15
done
for n in "$@"; do
  if [ -f "$r/$n.rc" ]; then echo "$n rc=$(cat "$r/$n.rc")"; else echo "$n PENDING"; fi
done

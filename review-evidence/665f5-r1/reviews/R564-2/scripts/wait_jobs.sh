#!/usr/bin/env bash
# Foreground wait (bounded) for named jobs' rc files. Usage: wait_jobs.sh <receipts> <max-seconds> <names...>
receipts=$1; limit=$2; shift 2; start=$(date +%s)
while :; do
  pending=(); for n in "$@"; do [ -f "$receipts/$n.rc" ] || pending+=("$n"); done
  [ ${#pending[@]} -eq 0 ] && break
  [ $(( $(date +%s) - start )) -ge "$limit" ] && { echo "still running: ${pending[*]}"; break; }
  sleep 15
done
for n in "$@"; do [ -f "$receipts/$n.rc" ] && echo "$n rc=$(cat "$receipts/$n.rc")"; done
free -g | sed -n 2p

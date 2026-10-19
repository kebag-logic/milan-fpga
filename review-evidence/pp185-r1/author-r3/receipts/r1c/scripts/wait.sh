#!/usr/bin/env bash
# usage: wait.sh <max-seconds> <file> [file ...]   returns when every file exists or time is up
max="$1"; shift; end=$(( $(date +%s) + max ))
while :; do
  all=1; for f in "$@"; do [ -e "$f" ] || all=0; done
  [ "$all" -eq 1 ] && { echo "ready"; exit 0; }
  [ "$(date +%s)" -ge "$end" ] && { echo "waiting"; exit 0; }
  timeout 20 tail -f /dev/null
done

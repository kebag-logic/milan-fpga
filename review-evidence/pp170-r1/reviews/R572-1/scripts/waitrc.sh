#!/usr/bin/env bash
# Usage: waitrc.sh <max-seconds> <rcfile...> : wait (foreground) for rc files
end=$(( $(date +%s) + $1 )); shift
while :; do
  missing=0; for f in "$@"; do [ -f "$f" ] || missing=$((missing+1)); done
  [ $missing -eq 0 ] && break
  [ $(date +%s) -ge $end ] && { echo "still running: $missing"; break; }
  sleep 10
done
for f in "$@"; do printf '%s rc=%s\n' "$f" "$(cat "$f" 2>/dev/null || echo PENDING)"; done

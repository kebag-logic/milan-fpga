#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# waitrc.sh SECONDS RCFILE...   wait (at most SECONDS) until every RCFILE exists
end=$(( $(date +%s) + $1 )); shift
while :; do
  missing=0; for f in "$@"; do [ -f "$f" ] || missing=$((missing+1)); done
  [ $missing = 0 ] && { echo "all done"; break; }
  [ $(date +%s) -ge $end ] && { echo "still running: $missing"; break; }
  sleep 10
done
for f in "$@"; do [ -f "$f" ] && echo "$f: $(cat "$f")"; done

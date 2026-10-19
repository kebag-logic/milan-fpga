#!/usr/bin/env bash
# round 2: wait for the final-head marker (one line, the final head SHA, written once the
# head campaigns' records are settled), then run the parent head pass at that SHA
S=<data>/tmp/pp185-a647; F="$S/r2/rec/final-head.txt"
while [ ! -e "$F" ]; do timeout 30 tail -f /dev/null; done
exec "$S/scripts/r2_parent_head.sh" "$(head -1 "$F")"

#!/bin/bash
# Run harness legs two at a time. usage: queue.sh CHECKOUT LEGFILE
# Each LEGFILE line: NAME POINT FETCH_L1 [extra run.py args...]
C=$1 F=$2
L=$MANAGEMENT/2026-09-23/665s2c-a685/scripts/leg.sh
grep -v '^#' "$F" | xargs -P 2 -L 1 bash -c 'exec "$0" "$@"' "$L" "$C"
echo "queue done $(date +%s)" >> $VALIDATION_STORAGE/665s2c-a685/logs/queue-$(basename "$F").done

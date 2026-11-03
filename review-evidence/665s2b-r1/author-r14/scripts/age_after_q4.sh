#!/bin/bash
# Queue 8 (AGE-A8 at the held fix's head) on queue 4's range once queue 4 is stopped.
T=$VALIDATION_STORAGE/665s2b-a683q
until grep -q 'stopped queue 4' $T/logs/queue-4.txt 2>/dev/null; do sleep 10; done
exec $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/queues.sh 8

#!/bin/bash
# Stop queue 4 once D-A8 ends, so its AGE-A8 at the old head does not run (it reruns at the held fix's head).
T=$VALIDATION_STORAGE/665s2b-a683q
until grep -q 'end D-A8' $T/logs/queue-4.txt 2>/dev/null; do sleep 10; done
systemctl --user stop milan-665s2b-a683q-q4.service
echo "$(date +%H:%M:%S) stopped queue 4 after D-A8" >> $T/logs/queue-4.txt

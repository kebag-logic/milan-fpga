#!/bin/bash
T=$VALIDATION_STORAGE/665s2b-a683q
until grep -q 'end D-A1' $T/logs/queue-r5.txt 2>/dev/null; do sleep 10; done
systemctl --user stop milan-665s2b-a683q-r5.service
echo "$(date +%H:%M:%S) stopped queue r5 after D-A1 (D-B1 runs in r6)" >> $T/logs/queue-r5.txt

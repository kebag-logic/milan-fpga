#!/bin/bash
T=$VALIDATION_STORAGE/665s2b-a683q
until grep -q 'end N-B1' $T/logs/queue-r5.txt 2>/dev/null; do sleep 5; done
systemctl --user stop milan-665s2b-a683q-r5.service
echo "$(date +%H:%M:%S) stopped queue r5 after N-B1 (D-A1 runs in r7, D-B1 in r6)" >> $T/logs/queue-r5.txt

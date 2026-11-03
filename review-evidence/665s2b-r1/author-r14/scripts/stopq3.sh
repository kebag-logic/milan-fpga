#!/bin/bash
# Stop queue 3 once N-A1 ends: the legs after it measured an image the store's mark fix replaces.
T=$VALIDATION_STORAGE/665s2b-a683q
until grep -q 'end N-A1' $T/logs/queue-3.txt 2>/dev/null; do sleep 10; done
systemctl --user stop milan-665s2b-a683q-q3.service
echo "$(date +%H:%M:%S) stopped queue 3 after N-A1" >> $T/logs/queue-3.txt

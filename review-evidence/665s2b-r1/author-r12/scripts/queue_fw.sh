#!/bin/bash
# Wait for the earlier self-test units to end, then queue the final-head shards.
H=$1
while systemctl --user is-active -q milan-665s2b-a683o-fw1 || systemctl --user is-active -q milan-665s2b-a683o-fw3; do python3 -c 'import time; time.sleep(20)'; done
for k in 0 1 2 3; do
    (setsid nohup $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/start_when_free.sh fwf$k $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/fwfinal.sh $H $k > $VALIDATION_STORAGE/665s2b-a683o/logs/start-fwf$k.log 2>&1 &)
    python3 -c 'import time; time.sleep(6)'
done

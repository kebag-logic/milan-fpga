#!/usr/bin/env bash
# route_queue.sh <head>: wait until no route (milan_soc.py) runs on the host, then run route.sh <head>, so this lane
# never routes beside another route; build-dev.sh's preflight refuses again if one started in between.
set -u
while pgrep -f 'milan_soc.py' > /dev/null; do sleep 30; done
echo "queue released $(date -Iseconds)" > <scratch>/route-${1:0:8}.queue
exec /usr/bin/bash <scratch>/tools/route.sh "$1"

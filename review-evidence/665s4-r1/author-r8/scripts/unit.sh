#!/bin/sh
# unit.sh NAME CHECKOUT COMMAND...: job.sh as its own capped unit, inside this lane's CPUs, detached.
exec systemd-run --user --quiet --unit="milan-665s4-a698i-$1" --property=MemoryMax=10G --property=MemoryHigh=8G \
  --property=CPUAffinity=88-95 --property=Nice=10 --collect \
  /bin/sh $MANAGEMENT/2026-09-23/665s4-a698i/scripts/job.sh "$@"

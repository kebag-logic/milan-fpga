#!/bin/bash
# Start one heavy job as its own transient unit. usage: unit.sh NAME CPU_RANGE MEMORY_MAX LOG -- CMD...
set -u
NAME=$1 RANGE=$2 MEM=$3 LOG=$4; shift 4
[ "$1" = "--" ] && shift
exec systemd-run --user --unit="milan-665s15-a752b-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$HOME --setenv=PATH=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  --working-directory=$SCRATCH \
  /usr/bin/taskset -c "$RANGE" /bin/bash -c 'source $SCRATCH/scripts/env.sh; exec /usr/bin/time -v "$@" > "'"$LOG"'" 2>&1' _ "$@"

#!/bin/bash
# Start one job as its own transient unit on a CPU range. usage: gunit.sh NAME CPU_RANGE MEMORY_MAX -- CMD...
set -u
NAME=$1 RANGE=$2 MEM=$3; shift 3
[ "$1" = "--" ] && shift
exec systemd-run --user --unit="milan-665s15-a752b-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$HOME --setenv=PATH=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$RANGE" "$@"

#!/bin/bash
# Start one heavy job as its own transient unit on a booked CPU range. usage: unit.sh NAME CPU_RANGE MEMORY_MAX -- CMD...
set -u
NAME=$1 RANGE=$2 MEM=$3; shift 3
[ "$1" = "--" ] && shift
exec systemd-run --user --unit="milan-665s2b-a683zj-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=<home> --setenv=PATH=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$RANGE" "$@"

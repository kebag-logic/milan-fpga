#!/bin/bash
# Start one job as its own transient unit on a CPU range. usage: unit30.sh NAME CPU_RANGE MEMORY_MAX -- CMD...
set -u
NAME=$1 RANGE=$2 MEM=$3; shift 3
[ "$1" = "--" ] && shift
exec systemd-run --user --unit="milan-665s2b-a683zo-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$RANGE" "$@"

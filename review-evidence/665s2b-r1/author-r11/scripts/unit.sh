#!/bin/bash
# Start one heavy job as its own transient unit on a booked CPU range.
# usage: unit.sh NAME CPU_RANGE MEMORY_MAX [VAR=VALUE ...] -- CMD...
set -u
NAME=$1 RANGE=$2 MEM=$3; shift 3
envs=()
while [ $# -gt 0 ] && [ "$1" != "--" ]; do envs+=(--setenv="$1"); shift; done
shift
exec systemd-run --user --unit="milan-665s2b-a683m-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  "${envs[@]}" /usr/bin/taskset -c "$RANGE" "$@"

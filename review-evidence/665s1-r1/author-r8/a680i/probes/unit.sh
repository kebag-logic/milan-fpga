#!/bin/bash
# Run one command in its own transient unit on the lane's CPUs, with a memory cap.
# usage: unit.sh NAME CPUS MEMMAX CMD...
set -u
NAME=$1 CPUS=$2 MEM=$3; shift 3
systemd-run --user --unit="milan-665s1-a680i-$NAME" --collect --property=MemoryMax=$MEM \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$CPUS" "$@"

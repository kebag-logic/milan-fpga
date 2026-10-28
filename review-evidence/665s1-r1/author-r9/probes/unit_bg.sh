#!/bin/bash
# Start one command in its own transient unit on the given CPUs, with a memory cap, and return.
# usage: unit_bg.sh NAME CPUS MEMMAX CMD...   (poll: systemctl --user is-active milan-665s1-a680l-NAME)
set -u
NAME=$1 CPUS=$2 MEM=$3; shift 3
systemd-run --user --unit="milan-665s1-a680l-$NAME" --collect --property=MemoryMax=$MEM \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$CPUS" "$@"

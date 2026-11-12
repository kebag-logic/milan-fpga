#!/bin/bash
# Start one heavy job of lane 895 as its own transient unit on a booked CPU range.
# usage: unit.sh NAME CPU_RANGE MEMORY_MAX -- CMD...   (rc in units/NAME.rc, output in units/NAME.log)
set -u
NAME=$1 RANGE=$2 MEM=$3; shift 3
[ "$1" = "--" ] && shift
U=/data-2/milan/tmp/895-a775/units
exec systemd-run --user --unit="milan-895-a775-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$RANGE" /bin/bash -c ". $MANAGEMENT/2026-09-23/895-a775/scripts/env.sh; cd $LANES/895-talker; $* > $U/$NAME.log 2>&1; echo \$? > $U/$NAME.rc"

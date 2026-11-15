#!/bin/bash
# Start one heavy job of lane 897 as its own transient unit on a booked CPU range.
# usage: unit.sh NAME CPU_RANGE MEMORY_MAX DIR -- CMD...   (rc in units/NAME.rc, output in units/NAME.log)
set -u
NAME=$1 RANGE=$2 MEM=$3 DIR=$4; shift 4
[ "$1" = "--" ] && shift
U=/data-2/milan/tmp/897-a776/units
rm -f $U/$NAME.rc
exec systemd-run --user --unit="milan-897-a776-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$RANGE" /bin/bash -c ". /data-2/milan/tmp/897-a776/scripts/env.sh; cd $DIR; $* > $U/$NAME.log 2>&1; echo \$? > $U/$NAME.rc"

#!/bin/bash
# Run a command as its own user unit, MemoryMax 10G, on the given CPUs, with the lane's tool environment; log and rc
# into the scratch dir. usage: unit.sh NAME CPUS DIR COMMAND...
set -eu
NAME=$1 CPUS=$2 DIR=$3; shift 3
T=/data-2/milan/tmp/894b-a781/units; mkdir -p $T
rm -f $T/$NAME.rc
printf '%q ' "$@" > $T/$NAME.cmd
systemd-run --user --unit=milan-894b-a781-$NAME --collect --property=MemoryMax=10G --setenv=HOME=$WORKSPACE_HOME \
  --working-directory=$DIR /usr/bin/taskset -c $CPUS /bin/bash -c ". /data-2/milan/tmp/894b-a781/scripts/env.sh; $(cat $T/$NAME.cmd) > $T/$NAME.log 2>&1; echo \$? > $T/$NAME.rc"

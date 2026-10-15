#!/bin/sh
# usage: suite.sh <name> <make args...>   (scratch; detached make -C tb/verilator/follow_ring, logs rc and wall seconds)
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
n=$1; shift
cd $LANES/645-bind-recentre || exit 1
s=$(date +%s)
env -u MAKEFLAGS make -C tb/verilator/follow_ring "$@" > /tmp/a620r2/$n.log 2>&1
rc=$?
echo $(( $(date +%s) - s )) > /tmp/a620r2/$n.secs
echo $rc > /tmp/a620r2/$n.rc

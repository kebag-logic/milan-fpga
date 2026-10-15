#!/bin/sh
# usage: launch.sh <name> <obj dir> <sweep args...>   (scratch; detached sweep, writes <name>.rc at the end)
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
n=$1; exe=$2; shift 2
cd $LANES/645-bind-recentre/tb/verilator/follow_ring || exit 1
python3 sweep.py bind --exe /tmp/a620r2/$exe/Vfollow_ring --out /tmp/a620r2/$n "$@" > /tmp/a620r2/$n.driver.log 2>&1
echo $? > /tmp/a620r2/$n.rc

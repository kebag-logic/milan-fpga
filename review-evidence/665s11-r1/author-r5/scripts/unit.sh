#!/bin/bash
# unit.sh NAME RANGE CMD...: CMD as the user unit milan-665s11-a761c-NAME on the CPUs RANGE (a cpu_ranges.py pick), at
# most 12 GB; its output in units/NAME.log and its exit status in units/NAME.rc
set -u
N=$1 R=$2; shift 2
U=<scratch>/r5/units
rm -f $U/$N.rc
systemd-run --user --unit=milan-665s11-a761c-$N --collect -p MemoryMax=12G -p MemorySwapMax=0 \
  /usr/bin/taskset -c $R /bin/bash -c "$* > $U/$N.log 2>&1; echo \$? > $U/$N.rc"

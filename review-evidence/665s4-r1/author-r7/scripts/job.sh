#!/bin/sh
# job.sh NAME CHECKOUT COMMAND...: one run in the gate environment, from a clean clone CHECKOUT. Writes
# $SCRATCH/NAME.log, $SCRATCH/NAME.rc (the command's exit status) and $SCRATCH/NAME.peak (the cgroup's memory peak).
. $MANAGEMENT/2026-09-23/665s4-a698h/scripts/env.sh
name=$1; dir=$2; shift 2
cd "$dir" || exit 2
rm -f "$SCRATCH/$name.rc"
( echo "# $(git rev-parse HEAD) in $(basename "$dir"): $*"; date -u +'# start %FT%TZ'; PATH="$GATE_PATH:$PATH" "$@"; rc=$?; date -u +'# end %FT%TZ'; exit $rc ) > "$SCRATCH/$name.log" 2>&1
rc=$?
cat "/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)/memory.peak" > "$SCRATCH/$name.peak" 2>/dev/null
echo $rc > "$SCRATCH/$name.rc"

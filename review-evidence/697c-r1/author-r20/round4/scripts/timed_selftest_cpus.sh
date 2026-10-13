#!/usr/bin/env bash
# Scratch: the boundary step's command on one tree, pinned to 4 CPUs (the hosted runner's count), each output
# line stamped with seconds since start.
# usage: timed_selftest.sh <tree> <log> [extra gate args]
set -u
tree=$1; log=$2; shift 2
. $VALIDATION_STORAGE/697c-a583/r4/scripts/env.sh
cd "$tree" || exit 2
taskset -c "${CPUS:-0-3}" python3 $VALIDATION_STORAGE/697c-a583/r4/scripts/stamp.py "$log" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest "$@"
echo "rc=$?" > "$log.rc"

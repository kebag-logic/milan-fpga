#!/bin/sh
# usage: run_leg.sh <milan_dp dir> <log dir> <name> <make target...>
# Runs one make target with the pinned Verilator; the log and rc land in <log dir>.
d=$1; l=$2; n=$3; shift 3
PATH=${VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH; export PATH
cd "$d" || exit 9
/usr/bin/time -v make -s VERILATOR_JOBS=4 "$@" > "$l/$n.log" 2>&1
echo $? > "$l/$n.rc"

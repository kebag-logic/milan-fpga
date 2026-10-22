#!/usr/bin/env bash
# Usage: launch.sh NAME LOGDIR WORKDIR CMD...  - detached run; writes LOGDIR/NAME.log and LOGDIR/NAME.rc
N=$1; L=$2; W=$3; shift 3; mkdir -p "$L"; rm -f "$L/$N.rc"
export VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator} VERILATOR_JOBS=${VERILATOR_JOBS:-2} PYTHON_CPU_COUNT=4 PYTHONHASHSEED=0
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
nohup setsid bash -c 'cd "$1"; shift; start=$(date +%s); "$@"; rc=$?; echo "wall_s=$(( $(date +%s)-start ))" ; echo $rc > "'"$L/$N"'.rc"' _ "$W" "$@" > "$L/$N.log" 2>&1 < /dev/null &
echo "launched $N pid $!"

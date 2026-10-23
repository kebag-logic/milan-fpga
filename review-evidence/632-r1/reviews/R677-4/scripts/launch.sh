#!/bin/sh
# launch.sh <name> <workdir> <command...>: run a probe detached with its own
# log, start/end stamps and exit status under receipts/probes/ of the packet
# this script sits in. VERILATOR names the pinned Verilator 5.050 wrapper.
P=$(cd "$(dirname "$0")/.." && pwd)
R=$P/receipts/probes
name=$1; dir=$2; shift 2
export TMPDIR=$P/scratch/tmp
export VERILATOR=${VERILATOR:?set VERILATOR to the pinned Verilator 5.050}
export VERILATOR_JOBS=${VERILATOR_JOBS:-6}
export PATH=$(dirname "$VERILATOR"):/usr/bin:/bin
mkdir -p "$R" "$TMPDIR"
rm -f "$R/$name.rc" "$R/$name.end"
date -Is > "$R/$name.start"
cd "$dir" || exit 1
setsid sh -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"; date -Is > "$0.end"' "$R/$name" "$@" < /dev/null > /dev/null 2>&1 &

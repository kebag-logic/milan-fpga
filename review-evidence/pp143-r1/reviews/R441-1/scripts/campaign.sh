#!/bin/bash
# usage: campaign.sh NAME CPULIST CMD...
# Runs one campaign from the review clone, pinned to CPULIST, with the pinned
# Verilator first on PATH and TMPDIR in a private scratch directory, so every
# unit copy the driver makes is visible under scratch/tmp-NAME. Writes
# receipts/NAME/{stdout.txt,rc,wall,cmd}.
set -u
P=${PACKET:-$REVIEWS/pp143-r441-1-packet}
CLONE=${CLONE:-$REVIEWS/r441-1-pp143}
VDIR=${VDIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}
name=$1; cpus=$2; shift 2
r=$P/receipts/$name; mkdir -p "$r" "$P/scratch/tmp-$name"
export TMPDIR=$P/scratch/tmp-$name PATH=$VDIR:$PATH
printf '%s\n' "cpus=$cpus" "$*" > "$r/cmd"
cd "$CLONE"
s=$(date +%s)
taskset -c "$cpus" "$@" > "$r/stdout.txt" 2>&1
rc=$?
e=$(date +%s)
echo $((e - s)) > "$r/wall"
echo $rc > "$r/rc"

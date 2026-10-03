#!/usr/bin/env bash
# Scratch launcher: run one Vivado batch script in its directory, recording rc,
# start/end time and the cgroup memory peak. Never committed.
#   run_vivado.sh <dir> <tcl> <log>
set -u
dir=$1; tcl=$2; log=$3
. $VALIDATION_STORAGE/234-a516/env.sh
cd "$dir" || { echo 2 > "$log.rc"; exit 2; }
date -Is > "$log.start"
rc=0
vivado -mode batch -source "$tcl" -nojournal -log "$log" > "$log.stdout" 2>&1 || rc=$?
date -Is > "$log.end"
echo "$rc" > "$log.rc"

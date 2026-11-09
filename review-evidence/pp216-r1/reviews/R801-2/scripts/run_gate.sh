#!/bin/bash
# run_gate.sh NAME WORKDIR CMD... : run CMD in WORKDIR with the pinned Verilator first on PATH,
# writing receipts/NAME.log, NAME.rc, NAME.cmd, NAME.start, NAME.end
set -u
PK=${PK:-$REVIEWS/pp216-r801-2-packet}
name=$1; dir=$2; shift 2
export PATH="$PK/scratch/bin:$PATH"
r="$PK/receipts/$name"
printf '%q ' "$@" > "$r.cmd"; echo "(cwd ${dir#$PK/})" >> "$r.cmd"
date -u +%FT%TZ > "$r.start"
( cd "$dir" && "$@" ) > "$r.log" 2>&1
echo $? > "$r.rc"
date -u +%FT%TZ > "$r.end"

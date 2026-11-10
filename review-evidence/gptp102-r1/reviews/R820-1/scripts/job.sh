#!/bin/bash
# One detached probe job: job.sh <name> <out> <cwd> <tmpdir> <cpus> cmd...
# Writes <out>/<name>.log (stdout), .time (stderr + /usr/bin/time -v) and,
# last, .rc with the command's exit status.
n=$1; out=$2; cwd=$3; tmp=$4; cpus=$5; shift 5
cd "$cwd" || { echo 127 > "$out/$n.rc"; exit; }
TMPDIR=$tmp /usr/bin/time -v taskset -c "$cpus" "$@" > "$out/$n.log" 2> "$out/$n.time"
echo $? > "$out/$n.rc"

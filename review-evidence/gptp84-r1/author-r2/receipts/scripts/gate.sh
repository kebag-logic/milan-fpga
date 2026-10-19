#!/bin/sh
# usage: gate.sh <tree> <label> <logdir> <cmd...>
# Runs one gate command in <tree>, writes <logdir>/<label>.log and appends
# "<label> rc=<n> secs=<s>" to <logdir>/rc.txt.
tree=$1; label=$2; logdir=$3; shift 3
mkdir -p "$logdir"
export PATH=<pinned-tools>:$PATH
export TMPDIR=<scratch>/tmpdir
start=$(date +%s)
( cd "$tree" && "$@" ) > "$logdir/$label.log" 2>&1
rc=$?
end=$(date +%s)
echo "$label rc=$rc secs=$((end - start)) cmd=$*" >> "$logdir/rc.txt"
echo "$label rc=$rc secs=$((end - start))"
tail -3 "$logdir/$label.log"

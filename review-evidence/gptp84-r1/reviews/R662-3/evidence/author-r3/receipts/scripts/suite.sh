#!/bin/sh
# usage: suite.sh <tree> <label> <logdir> <cmd...>
# Runs one parent suite command in <tree> with the consumer template's
# environment (the pinned Verilator first on PATH, the template's
# VERILATOR_ROOT, the lane's scratch as TMPDIR). Writes <logdir>/<label>.log
# and appends "<label> rc=<n> secs=<s> cmd=..." to <logdir>/rc.txt.
tree=$1; label=$2; logdir=$3; shift 3
mkdir -p "$logdir"
export PATH=<pinned-tools>:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR_ROOT=<pinned-tools>/usr/share/verilator
export TMPDIR=<scratch>/tmpdir
start=$(date +%s)
( cd "$tree" && "$@" ) > "$logdir/$label.log" 2>&1
rc=$?
echo "$label rc=$rc secs=$(( $(date +%s) - start )) cmd=$*" >> "$logdir/rc.txt"
echo "$label rc=$rc secs=$(( $(date +%s) - start ))"

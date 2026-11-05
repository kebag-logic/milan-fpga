#!/bin/sh
# Reviewer helper: run one gate command in a source tree, detached by the
# caller, recording its log, rc, start and end times under LOGDIR.
# Usage: run_gate.sh LOGDIR NAME SRCDIR CMD...
logdir=$1; name=$2; src=$3; shift 3
cd "$src" || exit 99
date +%s > "$logdir/$name.start"
"$@" > "$logdir/$name.log" 2>&1
echo $? > "$logdir/$name.rc"
date +%s > "$logdir/$name.end"

#!/usr/bin/env bash
# proc-b.sh <runs> <head>: the processor's docs, lint, yosys and elaboration-guard gates at the head, then the
# area of the head (main's area does not move with the branch); each step runs whatever the previous one's rc
R=$1; C=$2
T=$(cd "$(dirname "$0")" && pwd)
export PATH=$VALIDATION_TOOLS/sv2v-v0.0.12:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=$VALIDATION_STORAGE/scratch/pp214-a736b/tmp
mkdir -p $R
$T/fast-gates.sh $R/fast $C
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; "$@" > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
g area_head $T/area/area.sh $C $R/area/head

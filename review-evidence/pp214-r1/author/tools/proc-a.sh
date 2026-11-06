#!/usr/bin/env bash
# proc-a.sh <runs> <head> <main>: the processor's docs, lint, yosys and elaboration-guard gates at the head, the
# area of main and the head, then the full sweep with the executed traceability check; each step runs whatever
# the previous one's rc
R=$1; C=$2; M=$3
T=$(cd "$(dirname "$0")" && pwd)
export PATH=$VALIDATION_TOOLS/sv2v-v0.0.12:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=$VALIDATION_STORAGE/scratch/pp214-a736b/tmp
mkdir -p $R
$T/fast-gates.sh $R/fast $C
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; "$@" > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
g area_main $T/area/area.sh $M $R/area/main-92100657
g area_head $T/area/area.sh $C $R/area/head
$T/sweep.sh $R/sweep $C

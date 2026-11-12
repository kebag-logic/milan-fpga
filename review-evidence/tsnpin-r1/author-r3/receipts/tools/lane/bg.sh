#!/usr/bin/env bash
# bg.sh <name> <dir> <command...>: run detached, log to logs/<name>.log, rc to logs/<name>.rc
n=$1; d=$2; shift 2
L=<scratch>/logs
rm -f $L/$n.rc
. <scratch>/env.sh
cd "$d" || exit 3
{ echo "# $(date -Is) in $d: $*"; bash -c "$*"; } > $L/$n.log 2>&1
echo $? > $L/$n.rc

#!/bin/sh
# usage: bg.sh NAME DIR CMD...  - run CMD in DIR detached, writing $PACKET/receipts/NAME.log and NAME.rc
# PACKET defaults to this script's parent directory; scratch/bin (the capped
# Verilator wrapper) leads PATH and scratch/tmp holds every driver temp tree.
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
export PATH=$PACKET/scratch/bin:$PATH TMPDIR=$PACKET/scratch/tmp
cd "$dir" || exit 1
setsid nohup sh -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$PACKET/receipts/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo started $name

#!/usr/bin/env bash
# bg.sh NAME DIR CMD... : run CMD in DIR detached under env.sh, log to scratch/logs/NAME.log, rc to NAME.rc
P="${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}"; name=$1; dir=$2; shift 2
mkdir -p "$P/scratch/logs"; rm -f "$P/scratch/logs/$name.rc"
( source "$P/scripts/env.sh"; cd "$dir" && /usr/bin/time -v "$@" > "$P/scratch/logs/$name.log" 2>&1; echo $? > "$P/scratch/logs/$name.rc" ) </dev/null >/dev/null 2>&1 &
echo "started $name pid $!"

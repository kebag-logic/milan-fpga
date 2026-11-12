#!/bin/sh
# launch.sh NAME DIR CMD...: CMD in DIR in its own session; output NAME.log, exit status NAME.rc under the logs dir
L=<scratch>/logs; mkdir -p $L
name=$1; dir=$2; shift 2
rm -f "$L/$name.rc"
cd "$dir" || exit 2
setsid nohup bash -c 'source <scratch>/tools/env.sh; "$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$L/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "launched $name pid $!"

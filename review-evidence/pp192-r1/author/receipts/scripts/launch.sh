#!/usr/bin/env bash
# usage: launch.sh <name> <command...>   detached, its own log under <scratch>/jobs
J=<scratch>/jobs; mkdir -p "$J"; name="$1"; shift
setsid nohup "$@" > "$J/$name.out" 2>&1 < /dev/null &
echo "$!" > "$J/$name.pid"; echo "launched $name pid $!"

#!/bin/sh
# R490-1: launch one focused leg detached, with its own log and rc file.
# usage: r490_launch.sh <name> <logdir> <cmd...>
name=$1; dir=$2; shift 2
setsid sh -c 'd=$0; n=$1; shift; "$@" > "$d/$n.log" 2>&1; echo $? > "$d/$n.rc"' "$dir" "$name" "$@" < /dev/null > /dev/null 2>&1 &

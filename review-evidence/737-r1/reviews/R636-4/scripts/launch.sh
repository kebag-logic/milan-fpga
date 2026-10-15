#!/bin/sh
# Start one detached probe with its own HOME, log and rc file.
# Usage: launch.sh <name> <tree> <receipt-dir> <path-dir> <command...>
set -eu
name=$1; tree=$2; out=$3; pathdir=$4; shift 4
home=$(dirname "$tree")/home-$name
mkdir -p "$home" "$out"
rm -f "$out/$name.rc" "$out/$name.log"
cmd="$*"
setsid nohup sh -c "cd '$tree' && HOME='$home' PATH='$pathdir' /usr/bin/time -v $cmd > '$out/$name.log' 2>&1; echo \$? > '$out/$name.rc'" \
    >/dev/null 2>&1 &
echo "launched $name"
